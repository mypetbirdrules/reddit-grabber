#!/usr/bin/env python3

import re
import requests

def galleryToImage(galleryURL):
    urlRegexMatch = False
    urlRegexMatchObject = re.match(".*imgur.com\/gallery\/[a-zA-Z0-9]+/?", galleryURL)

    if urlRegexMatchObject != None:
        if urlRegexMatchObject.span() == (0, len(urlRegexMatchObject.string)):
            urlRegexMatch = True

    if urlRegexMatch == True:
        return galleryURL.replace("/gallery/", "/")
    else:
        return galleryURL

def cleanURL(imgurURL):
    # removes unwanted trailing characters from the input URL
    while imgurURL[-1] == "/":
        imgurURL = imgurURL[0:-2]

    return imgurURL

def extractImageURL(imgurURL):

    imgurURL = galleryToImage(imgurURL)
    
    urlRegexMatch = False
    urlRegexMatchObject = re.match(".*imgur\.com\/[a-zA-Z0-9]+/?", imgurURL)

    if urlRegexMatchObject != None:
        if urlRegexMatchObject.span() == (0, len(urlRegexMatchObject.string)):
            urlRegexMatch = True

    if urlRegexMatch == True:
        # make a HEAD request at imgur.com/xxxx.jpg
        # read Content-Type from HTTP headers to determine file type
        HTTPHeadRequest = requests.head(cleanURL(imgurURL) + ".jpg")

        if HTTPHeadRequest.status_code == 200:
            # webpage exists
            # assigning file extension to URL
            responseHeader = HTTPHeadRequest.headers["Content-Type"]

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
            # return original for following reasons
            # horrible errors
            # unsupported features (Imgur albums/galleries)
            return imgurURL

        # close HTTP connection object
        HTTPHeadRequest.close()

    else:

        return imgurURL
