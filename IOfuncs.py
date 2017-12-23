import os, shutil, time
from random import random
from io import BytesIO
import urllib
from PIL import Image

def assert_client_data_path(request):
    client_name = request.remote_addr.replace(".", "-");
    add_on = str(int(time.time())) + "-" + str(int(random()*10000))
    path_to_client_data = os.path.join("temp-client-data", client_name+add_on)
    if os.path.isdir(path_to_client_data):
        shutil.rmtree(path_to_client_data) 
    os.makedirs(path_to_client_data)
    return path_to_client_data

def download_file(url, path_to_data, i, w, h, resize):
    local_filename = os.path.join(path_to_data, "temp"+str(i)+".jpg")
    try:
        f = BytesIO(urllib.urlopen(url).read())
        im = Image.open(f)
        size = w,h
        if resize == True:
            im.thumbnail(size, Image.ANTIALIAS)
        im.save(local_filename)
    except Exception as e:
        # print "[Error] while downloading image\n\tsrc:",url,"\n\tError:", e
        return None, (0,0)
    return local_filename, im.size

def download_images(data, path_to_client_data, w=640, h=640):
    image_data_object = dict()
    resize = True
    try:
        if data["resize"] == 0: resize = False
    except:
        pass
    urls = data["urls"]
    # print "[Downloading]...", len(urls), "urls"
    err_count = 0
    for i, url in enumerate(urls, 0):
        image_data_object[i] = dict()
        local_path, size = download_file(url, path_to_client_data, i, w, h, resize)
        if local_path == None: err_count += 1
        image_data_object[i]["url"] = url
        image_data_object[i]["path"] = local_path
        image_data_object[i]["img_resize"] = {"w": size[0], "h":size[1]}
    print "[+] Downloaded", len(urls) - err_count, "/", len(urls), "images"
    return image_data_object, len(urls) - err_count

