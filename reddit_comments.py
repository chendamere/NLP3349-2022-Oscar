import pandas as pd
import praw 
from praw.models import MoreComments
from sklearn.model_selection import train_test_split

reddit = praw.Reddit(
    client_id = "huuaTkdCFRpGi7m6XEslnA",
    client_secret = "gzYzY1oyX1rqfXTLACVgtSVuvz_33g",
    user_agent = "vscodepython:oscar.sentiment:v1.0.0"
)

submissions = pd.read_csv("movie_submissions.csv")
comment_data = []

for i in range(0, submissions.shape[0]):
    submission = reddit.submission(submissions.loc[i][3])
    all_comments = submission.comments.list()
    commentstring = ""
    for comment in all_comments:
        if isinstance(comment, MoreComments):
            continue
        commentstring = commentstring + comment.body + " "
    comment_data.append((commentstring, submissions.loc[i][4]))
comment_sents = pd.DataFrame.from_records(comment_data, columns = ["comments", "nominated"])

train, test = train_test_split(comment_sents, test_size=0.2)
train.to_csv("reddit_train.csv")
test.to_csv("reddit_test.csv")