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
    username = os.environ.get('REDDIT_USERNAME'),
		password = os.environ.get('REDDIT_PASSWORD'),
		client_id = os.environ.get('API_CLIENT'),
		client_secret = os.environ.get('API_SECRET'),
		user_agent = "Little Stitious Bot"
  )

# Use the application default credentials
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "lilstitiousbot",
  "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
  "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n') if os.environ.get('FIREBASE_PRIVATE_KEY') is not None else os.error('Actions does not have key access'),
  "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
  "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-33av6%40lilstitiousbot.iam.gserviceaccount.com"
})

firebase_admin.initialize_app(cred, {
  'projectId': 'lilstitiousbot',
})

db = firestore.client()

saved_comments = db.collection(u'comment_ids')
docs = saved_comments.stream()

read_comments(reddit, [doc.id for doc in docs], db)
