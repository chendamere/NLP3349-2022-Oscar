import pandas as pd
import datetime as dt
import os 
import praw
from psaw import PushshiftAPI
import time

basecorpus = './my-dataset/'
dirpath = basecorpus

subreddit = "movies"
subredditdirpath = dirpath + '/' + subreddit


if not os.path.exists(dirpath):
    os.makedirs(dirpath)

submissions_csv_path = subreddit + 'submissions.csv'
submission_comments_csv_path = subreddit + 'submission' + '-comments.csv'
def log_action(action):
    print(action)
    return

api = PushshiftAPI()


reddit = praw.Reddit(
    client_id="7vOWhWf5NZ0ibOg9EYOUXQ",
    client_secret="z3lJZmNGzVMjecdraikZ0Bdgmx6SLw",
    user_agent=f"python_script:subreddit_downloader:(by /u/No-Resource2729)",
)

subreddits = ['movies']

### BLOCK 1 ###
start_year = 2019
end_year = 2020

ts_after = int(dt.datetime(2019, 1, 1).timestamp())
ts_before = int(dt.datetime(2020+1, 1, 1).timestamp())

#store all nominated movies to avoid
allNominated =[]

file = open("NominatedMovies.txt",'r')
for line in file:
    line = line.strip()
    allNominated.append(line)

for subreddit in subreddits:
    # start_time = time.time()
    
    # action = "\t[Subreddit] " + subreddit
    # log_action(action)
    # subredditdirpath = dirpath + '/' + subreddit
    # if os.path.exists(subredditdirpath):
    #     continue
    # else:
    #     os.makedirs(subredditdirpath)

    # submissions_csv_path = str(year) + '-' + subreddit + '-submissions.csv'

    submissions_dict = {
        "id" : [],
        "url" : [],
        "title" : [],
        "score" : [],
        "num_comments": [],
        "created_utc" : [],
        "selftext" : [],
    }

    # use PSAW only to get id of submissions in time interval
    gen = api.search_submissions(
        after=ts_after,
        before=ts_before,
        filter=['id'],
        subreddit=subreddit,
        limit=10
    )

    # use PRAW to get actual info and traverse comment tree
    for submission_psaw in gen:
        # use psaw here
        submission_id = submission_psaw.d_['id']
        
        print(submission_psaw)
        # use praw from now on
        submission_praw = reddit.submission(id=submission_id)

        if submission_praw.link_flair_text=="Official Discussion" and submission_praw.selftext != None:
            
            #skip nominated movies
            skip = False
            for name in allNominated:
                if name in submission_praw.title:
                    skip = True
                    continue

            print(submission_praw.title)
            submissions_dict["id"].append(submission_praw.id)
            submissions_dict["url"].append(submission_praw.url)
            submissions_dict["title"].append(submission_praw.title)
            submissions_dict["score"].append(submission_praw.score)
            submissions_dict["num_comments"].append(submission_praw.num_comments)
            submissions_dict["created_utc"].append(submission_praw.created_utc)
            submissions_dict["selftext"].append(submission_praw.selftext)

            submission_comments_dict = {
                "comment_id" : [],
                "comment_parent_id" : [],
                "comment_body" : [],
                "comment_link_id" : [],
            }
            
            submission_praw.comments.replace_more(limit=None)
            for comment in submission_praw.comments.list():
                submission_comments_dict["comment_id"].append(comment.id)
                submission_comments_dict["comment_parent_id"].append(comment.parent_id)
                submission_comments_dict["comment_body"].append(comment.body)
                submission_comments_dict["comment_link_id"].append(comment.link_id)
            print(submission_comments_dict["comment_body"][0:10])
            #pd.DataFrame(submission_comments_dict).to_csv(subredditdirpath + '/' + submission_comments_csv_path, index=False)