import numpy as np
import pandas as pd

def unprocessed(csv_file):
    df = pd.read_csv(csv_file)
    return df

def load(csv_file):
    df = pd.read_csv(csv_file)
    df1=(df[['id', 'host_id', 'host_is_superhost', 'accommodates', 'review_scores_cleanliness', 'price'   ]]
         .sort_values("review_scores_cleanliness",ascending=False, ignore_index=True)
        )
    clean = df1[['host_is_superhost','review_scores_cleanliness']]
    clean =  clean[clean['review_scores_cleanliness'].notna()]
    price = df1[['host_is_superhost', 'accommodates', 'price']]
    
    return (clean,price)

def process_clean(df):
    clean = df
    cleanmean = (clean.groupby("host_is_superhost", as_index=False)
                 .mean()
                 )  
    return cleanmean

def process_price(df):
    price = df
    return price

def wrang_clean(df):
    remaned = df.rename(columns = {"host_is_superhost":"Host is Super Host?","review_scores_cleanliness":"mean of cleanliness score" })
    return remaned
    