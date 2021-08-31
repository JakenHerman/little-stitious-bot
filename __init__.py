import os
import praw
from supabase_py import create_client, Client

def read_comments():
  reddit = praw.Reddit(
    username = os.environ.get('REDDIT_USERNAME'),
		password = os.environ.get('REDDIT_PASSWORD'),
		client_id = os.environ.get('API_CLIENT'),
		client_secret = os.environ.get('API_SECRET'),
		user_agent = "Little Stitious Bot"
  )

  url: str = os.environ.get("SUPABASE_URL")
  key: str = os.environ.get("SUPABASE_KEY")
  supabase: Client = create_client(url, key)
  comments = supabase.table("comment_ids").select("*").execute()
  comments_already_responded_to = [comment.id for comment in comments.get("data", [])]

  for comment in reddit.subreddit('dundermifflin').comments(limit=100000):
    if "superstitious" in comment.body.lower() and comment.id not in comments_already_responded_to and comment.author != reddit.user.me():
      comment.reply("I'm not superstitious, but I am a little stitious.")
      data = supabase.table("comment_ids").insert({"id":comment.id,"comment_body":comment.body}).execute()

read_comments()