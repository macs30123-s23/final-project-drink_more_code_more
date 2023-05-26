import dataset
import praw
import boto3

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


def scrape_posts(subreddit_name):
    ''' input a string of the name of a subreddit  '''
    subreddit = reddit.subreddit(subreddit_name)
    posts = subreddit.hot(limit=10000)   # a praw generator
    scrape_post(posts)


def scrape_post(posts):
    ''' input a generator, store in posts RDS table '''
    for submission in posts:
        if submission.selftext:  # only obtain those have text comment
            post = {}
            post["subreddit"]= submission.subreddit.display_name
            post["id"]= submission.id
            post["title"] = submission.title
            post["score"] = submission.score
            post["url"] = submission.url
            post["comms_num"] = submission.num_comments
            post["body"] = submission.selftext
            post["ups"] = submission.ups
            
            db['posts'].upsert(post, ['id'])
            
    db.close()


def lambda_handler(event, context):
    scrape_posts(event['subreddit'])

    return {"statuscode": 200}