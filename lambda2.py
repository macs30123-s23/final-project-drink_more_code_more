import dataset
import praw
import boto3
import time

reddit = praw.Reddit(client_id="_LfZX0gAkzmoyrMnVVv2lQ",         # your client id
                                client_secret="I4nebJfWx9-CD7c2XlAwyuozluh6_Q",      # your client secret
                                user_agent="large_scale",        # your user agent
                                username="Far-Factor-103",        # your reddit username
                                password="03011001@Yw")        # your reddit password

rds = boto3.client('rds')
db = rds.describe_db_instances()['DBInstances'][0]
ENDPOINT = db['Endpoint']['Address']
PORT = db['Endpoint']['Port']
# connect to db
db_url = 'mysql+mysqlconnector://{}:{}@{}:{}/reddit_scrapes'.format('username',
                                                                   'password',
                                                                ENDPOINT, PORT)
db = dataset.connect(db_url)

def scrape_comments(post_urls):
    for url in post_urls:
        try:
            submission = reddit.submission(url=url)
            for comm in submission.comments:
                if comm.body:
                    comment = {}
                    comment['subreddit'] = comm.subreddit.display_name
                    comment['post_url'] = url
                    comment['comment_id'] = comm.id
                    comment['comment_body'] = comm.body
                    comment['comment_score'] = comm.score

                    db['comments'].upsert(comment, ['comment_id'])
        except:
            continue
    
    db.close()


def lambda_handler(event, context):
    scrape_comments(event['post_url'])

    return {"statuscode": 200}