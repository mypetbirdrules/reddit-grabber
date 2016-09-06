#!/usr/bin/env python3

# This software is licensed under the GNU General Public License

import argparse
import sys
import os
import time
import imgur
import praw
import re

if __name__ == "__main__":

    # Creating argument parser
    parserObj = argparse.ArgumentParser(description="A simple Python Reddit scraper")

    # Configuring argument parser
    parserObj.add_argument("-r", action="store", required=True, dest="subredditName", type=str, help="the name of the subreddit to scrape (default=all)")
    parserObj.add_argument("--resolve-imgur-links", action="store_true", dest="imgurResolve", help="extract direct links from Imgur")
    parserObj.add_argument("-o", action="store", default="redditurls.txt", dest="outputFilename", type=str, help="output file for scraped URLs")
    parserObj.add_argument("--filter", action="store", default="hot", dest="filter", type=str, help="subreddit content sort method (default=hot)")
    parserObj.add_argument("-n", action="store", default=100, dest="limit", type=int, help="number of posts to scrape")
    parserObj.add_argument("--title-regex", action="store", default=".*", dest="titleRegex", type=str, help="filter posts by title with a regexp (default=.*)")
    parserObj.add_argument("-v", action="store_true", default=False, dest="verboseFlag", help="toggle verbose script output")

    arguments = parserObj.parse_args(sys.argv[1:])

    # setting up PRAW API
    redditAPIAgent = praw.Reddit(user_agent="Simple Reddit Scraper v1.0")
    subredditObject = redditAPIAgent.get_subreddit(arguments.subredditName)

    if arguments.limit > 0:
        outputFile = open(arguments.outputFilename, 'w')
        
        if arguments.filter == "hot":
            submissions = subredditObject.get_hot(limit=arguments.limit)
        elif arguments.filter == "top":
            submissions = subredditObject.get_top(limit=arguments.limit)
        elif arguments.filter == "controversial":
            submissions = subredditObject.get_controversial(limit=arguments.limit)
        elif arguments.filter == "rising":
            submissions = subredditObject.get_rising(limit=arguments.limit)
        else:
            print("Runtime Error: Invalid subreddit sort filter")
            sys.exit(1)
        
        # count number of grabbed get_content objects
        grabCount = 0

        for post in submissions:
            
            # wait between requests
            time.sleep(0.1)

            # pre-fetching submission attributes
            postTitle = post.title
            postURL = post.url

            titleRegexMatchObject = re.match(arguments.titleRegex, postTitle)

            # setting defaults for match flag
            titleRegexMatch = False

            if titleRegexMatchObject != None:
                if titleRegexMatchObject.span() == (0, len(titleRegexMatchObject.string)):
                    titleRegexMatch = True

            if titleRegexMatch == True:
                # increment grabCount for every correct regex title match
                grabCount += 1

                if arguments.verboseFlag == True:
                    print("match #"+str(grabCount)+": "+post.title)

                if arguments.imgurResolve == True:
                    outputFile.write(imgur.extractImageURL(post.url)+"\n")
                else:
                    outputFile.write(post.url+"\n")

        if grabCount > 0:
            print("Success - reddit-grabber scraped "+str(grabCount)+(" post"," posts")[grabCount>1])
            outputFile.close()
        else:
            print("reddit-grabber grabbed 0 posts - deleting output file...")
            outputFile.close()
            os.remove(arguments.outputFilename)
            print(arguments.outputFilename+" deleted")
            
    else:
        print("Runtime Error: Scrape limit must be over 0")
        sys.exit(1)
