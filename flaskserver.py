from flask import Flask, request, jsonify, abort
# import json, urllib, sys, cv2, shutil, time
import json, urllib, sys, shutil, time
from io import BytesIO
from PIL import Image
import numpy as np
import pyyolo
import IOfuncs as iof

darknet_path = '../pyyolo/darknet'
datacfg = 'cfg/coco.data'
cfgfile = 'cfg/yolo.cfg'
weightfile = '../weights/yolo.weights'
thresh = 0.24
hier_thresh = 0.5
pyyolo.init(darknet_path, datacfg, cfgfile, weightfile)

application = Flask(__name__)


# # WHITELIST
# # Limit use of API to IPs in whitelist.txt
# @application.before_request
# def limit_remote_addr():
    # whitelist = list()
    # for line in open('whitelist.txt'):
        # line = line.strip()
        # whitelist.append(line)
    # if request.remote_addr not in whitelist:
        # print "[ABORT] IP not on whitelist:", request.remote_addr
        # abort(403)

@application.route("/", methods=['GET', 'POST'])
def serve():
    data = json.loads(request.data.decode('utf-8'))
    print "\n"
    print "[TIME] " + time.strftime("%d/%m/%Y") + "  " + time.strftime("%H:%M:%S")
    path_to_client_data = iof.assert_client_data_path(request)

    image_data, num_valid_images = iof.download_images(data, path_to_client_data)
    
    out = list()
    # print "[Classifying]...", num_valid_images, "images"
    err_count = 0
    for idx in image_data:
        img_data = image_data[idx]
        out.append(dict())
        o = out[-1] 
        o["url"] = img_data["url"]
        o["img_resize"] = img_data["img_resize"]
        if img_data["path"] == None:
           o["pred"] = None
           continue
        try:
            o["pred"] = pyyolo.test(img_data["path"], thresh, hier_thresh, 0)
            if len(o["pred"]) == 0:
                o["pred"] = None
        except Exception as e:
            o["pred"] = None
            err_count += 1
            print "[ERROR] while classifiying image\n\tsrc:", o["url"], "\n\tError:", e
    print "[+] Classified", num_valid_images - err_count, "/", num_valid_images, "images"
    shutil.rmtree(path_to_client_data) 
    print "[+] Deleted downloaded images."
    print "[+] Returning predictions..."
    return jsonify(out)


if __name__ == "__main__":
   
    application.run(host='0.0.0.0', port=8888)
