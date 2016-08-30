#!/usr/bin/env python3

import re
import requests

def extractImageURL(imgurURL):
    if re.match(".*imgur\.com\/[a-zA-Z]+", imgurURL) != False:
        # make a get request at imgur.com/xxxx.jpg
        # read Content-Type from http headers to determine file type
        getRequest = requests.get(imgurURL + ".jpg")

        if getRequest.status_code == 200:
            # webpage exists
            # assigning file extension to URL
            responseHeader = getRequest.headers["Content-Type"]

            if responseHeader == "image/jpeg":
                return imgurURL + ".jpg"
            elif responseHeader == "image/png":
                return imgurURL + ".png"
            elif responseHeader == "image/gif":
                return imgurURL + ".gif"
	
        else:
            # return False for following reasons
            # horrible errors
            # unsupported features (Imgur albums/galleries)
            return False
