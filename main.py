#!/usr/bin/env python3

import argparse
import sys
import os
import imgur
import praw

if __name__ == "__main__":

    # Creating argument parser
    parserObj = argparse.ArgumentParser(description="A simple Python Reddit scraper")

    # Configuring argument parser
    parserObj.add_argument("-r", action="store", required=True, dest="subredditName", type=str, help="the name of the subreddit to scrape (default=all)")
    parserObj.add_argument("--resolve-imgur-links", action="store_true", dest="imgurResolve", help="extract direct links from Imgur")
    parserObj.add_argument("-o", action="store", default="redditurls.txt", dest="outputFilename", type=str, help="output file for scraped URLs")
    parserObj.add_argument("--filter", action="store", default="hot", dest="filter", type=str, help="subreddit content sort method (default=hot)")
    parserObj.add_argument("-n", action="store", default=100, dest="limit", type=int, help="number of posts to scrape")

    arguments = parserObj.parse_args(sys.argv[1:])

    # setting up PRAW API
    redditAPIAgent = praw.Reddit(user_agent="Simple Reddit Scraper v1.0")
    subredditObject = redditAPIAgent.get_subreddit(arguments.subredditName)

    if arguments.limit > 0:
        outputFile = open(arguments.outputFilename, 'w')
        
        if arguments.filter == "hot":
            submissions = subredditObject.get_hot(limit=arguments.limit)
        elif arguments.filter == "top":
            submissions = subredditObject.get_top_from_all(limit=arguments.limit)
        elif arguments.filter == "controversial":
            submissions = subredditObject.get_controversial(limit=arguments.limit)
        elif arguments.filter == "rising":
            submissions = subredditObject.get_rising(limit=arguments.limit)
        else:
            print("Invalid subreddit sort filter")
            os.exit()
        
        for post in submissions:
            if arguments.imgurResolve == True:
                outputFile.write(imgur.extractImageURL(post.url)+"\n")
            else:
                outputFile.write(post.url+"\n")

        print("Success")
        outputFile.close()
    else:
        print("Limit must be over 0")
        os.exit()
