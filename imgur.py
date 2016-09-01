#!/usr/bin/env python3

import re
import requests

def cleanURL(imgurURL):
    # removes unwanted trailing characters from the input URL
    while imgurURL[-1] == "/":
        imgurURL = imgurURL[0:-2]

    return imgurURL

def extractImageURL(imgurURL):
    if re.match(".*imgur\.com\/[a-zA-Z]+/?", imgurURL) != False:
        # make a get request at imgur.com/xxxx.jpg
        # read Content-Type from http headers to determine file type
        getRequest = requests.get(cleanURL(imgurURL) + ".jpg")

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
                # in case of unknown format
                return imgurURL

        else:
            # return False for following reasons
            # horrible errors
            # unsupported features (Imgur albums/galleries)
            return imgurURL
