#!/usr/bin/python

import praw
import re

subreddit = ""
titleRegex = ""
urlRegex = ""
outputFilename = ""

subreddit = input("Subreddit Name: ")
titleRegex = input("Title Regex: ")
urlRegex = input("URL Regex: ")
outputFilename = input("Output Filename: ")

if subreddit == "" or titleRegex == "" or outputFilename == "" or urlRegex == "":
	print("One or more options were empty")
else:
	titlePatternObj = re.compile(titleRegex)
	urlPatternObj = re.compile(urlRegex)
	
	redditAgent = praw.Reddit(user_agent="RegexGrabber v1.0")
	subreddit = redditAgent.get_subreddit(subreddit)
	submissions = subreddit.get_top_from_all(limit=1000)
	
	outputFile = open(outputFilename, "w")
	
	try:
		for submission in submissions:
			if titlePatternObj.match(submission.title) and urlPatternObj.match(submission.url):
				print("Writing: " + submission.title)
				outputFile.write(submission.url + "\n")
	except:
		print("An error occured: Unable to continue")
	print("Done writing - Closing output file...")
	outputFile.close()
	
