# Image Classification API for Data Selfie

This is the code for the image classification API that is used by [Data Selfie](https://github.com/d4t4x/data-selfie).
Its main components are [Yolo and Darknet](https://pjreddie.com/darknet/yolo/), used via the [pyyolo-wrapper](https://github.com/digitalbrain79/pyyolo) for image classification and [Gunicorn](http://gunicorn.org) for reliable server functionality. 

## Build it yourself

### Install pyyolo

Follow the installation instructions of [pyyolo](https://github.com/digitalbrain79/pyyolo). To avoid unexcessary logging of the prediction times for each image, I got rid of [this line](https://github.com/digitalbrain79/pyyolo/blob/master/libyolo.c#L140) before the install.

### Download weight file

For Data Selfie, we are using weights from the makers of Darknet as described on [this](https://pjreddie.com/darknet/yolo/) page. 

```
wget https://pjreddie.com/media/files/yolo.weights
```

### Download this repo

Finally, clone this repo with

```
git clone git@github.com:d4t4x/data-selfie-image-classification.git
```

The folder structure should look like this:

```
.
├── data-selfie-image-classification
│   ├── ...
├── pyyolo
│   ├── ...
└── weights
    └── yolo.weights
```

### A few more dependencies

Before running the server, we need to install pillow, flask, request, numpy
```
pip install pillow flask request numpy
```
and gunicorn, greenlet and gevent
```
pip install gunicorn greenlet gevent
```

### Run the API

For Data Selfie we run the API like this, from the directory of this repo:

```
gunicorn --workers=2 --bind=0.0.0.0:8888 -t 100 -k gevent wsgi
```


Good luck! File a issue in this repo, contact us or [Leon Eckert](http://leoneckert.com) if you have any questions.


