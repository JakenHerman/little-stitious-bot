import os
import praw
import time

def login():
  return praw.Reddit(
    username = os.getenv('REDDIT_USERNAME'),
		password = os.getenv('REDDIT_PASSWORD'),
		client_id = os.getenv('API_CLIENT'),
		client_secret = os.getenv('API_SECRET'),
		user_agent = "Little Stitious Bot"
  )

def read_comments(reddit, comments_already_responded_to):
  for comment in reddit.subreddit('dundermifflin').comments(limit=1000):
    if "superstitious" in comment.body.lower() and comment.id not in comments_already_responded_to and comment.author != reddit.user.me():
      comment.reply("I'm not superstitious, but I am a little stitious.")
      comments_already_responded_to.append(comment.id)
      with open("comment_ids.txt", "a") as ids:
        ids.write(comment.id + "\n")
  time.sleep(120)

def get_saved_comments():
	if os.path.isfile("comment_ids.txt"):
		with open("comment_ids.txt", "r") as f:
			return f.read().split("\n")
	return []

        
reddit = login()

while True:
  read_comments(reddit, get_saved_comments())