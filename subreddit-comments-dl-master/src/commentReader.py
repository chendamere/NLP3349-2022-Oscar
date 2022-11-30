import pandas as pd
from tika import parser
import re

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)

def NotRemoved(comment):
    return ("[deleted]" not in comment) and ("[removed]" not in comment)

def main():
    
    df = pd.read_csv("src\dataset\greenbook\comments.csv")
    allcomments = list(df["body"])
    sentences = []

    for comment in allcomments:
        #remove \n
        comment = re.sub(r"\\n","", comment)
        
        #remove hyper links
        comment = re.sub(r"http(\S)*", "", comment)
        
        comment = remove_emojis(comment)

        if(NotRemoved(comment)):
            sentences.append(comment)

    print(sentences[0:10])

main()