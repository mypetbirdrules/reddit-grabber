#!/usr/bin/env python3

import argparse
import sys
import imgur
import praw

if __name__ == "__main__":

    # Creating argument parser
    parserObj = argparse.ArgumentParser(description="A simple Python Reddit scraper")

    # Configuring argument parser
    parser.add_argument("--subreddit", action="store", required=True, dest="subredditName", type=str, help="The name of the subreddit to scrape (default=all)")
    parser.add_argument("--resolve-imgur-links", action="store_true", dest="imgurResolve", help="Choose whether to grab direct images from Imgur")
    parser.add_argument("--output-file", action="store", default="redditurls.txt", dest="outputFilename", type=str, help="Configure the file path of the program output")
    parser.add_argument("--filter-by", action="store", default="hot", dest="filter", type=str, help="Configure subreddit sort type (default=hot)")
    parser.add_argument("--limit", action="store", default=100, dest="limit", type=int, help="Number of posts to scrape")

    arguments = parser.parse_args(sys.argv[1:])

    # setting up PRAW API
    redditAPIAgent = praw.Reddit(user_agent="Simple Reddit Scraper v1.0")
    subredditObject = redditAPIAgent.get_subreddit(arguments.subredditName)

    if arguments.limit > 0:
        outputFile = open(arguments.outputFilename, 'w')
        if arguments.filter == "hot":
            submissions = subredditObject.get_hot(limit=arguments.limit)
            
        else:
            print("Invalid subreddit sort filter")
    else:
        print("Limit must be over 0")
