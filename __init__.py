import os
import praw
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def read_comments(reddit, comments_already_responded_to, db):
  for comment in reddit.subreddit('dundermifflin').comments(limit=1000):
    if "superstitious" in comment.body.lower() and comment.id not in comments_already_responded_to and comment.author != reddit.user.me():
      comment.reply("I'm not superstitious, but I am a little stitious.")
      doc_ref = db.collection(u'comment_ids').document(comment.id)
      doc_ref.set({
          u'body': comment.body
      })
  
reddit = praw.Reddit(
    username = os.getenv('REDDIT_USERNAME'),
		password = os.getenv('REDDIT_PASSWORD'),
		client_id = os.getenv('API_CLIENT'),
		client_secret = os.getenv('API_SECRET'),
		user_agent = "Little Stitious Bot"
  )

# Use the application default credentials
cred = credentials.Certificate("adminsdk.json")
firebase_admin.initialize_app(cred, {
  'projectId': 'lilstitiousbot',
})

db = firestore.client()

saved_comments = db.collection(u'comment_ids')
docs = saved_comments.stream()

read_comments(reddit, [doc.id for doc in docs], db)