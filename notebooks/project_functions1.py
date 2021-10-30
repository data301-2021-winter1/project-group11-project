import numpy as np
import pandas as pd

def unprocessed(csv_file):
    df = pd.read_csv(csv_file)
    return df

def load(csv_file):
    df = pd.read_csv(csv_file)
    df1=(df[["id", 'name', 'host_id', 'host_name', 'host_is_superhost','price','review_scores_cleanliness','accommodates'  ]]
         .sort_values("review_scores_cleanliness",ascending=False, ignore_index=True)
        )
    clean =  df1[['host_is_superhost','review_scores_cleanliness']]
    temp =     clean[clean['review_scores_cleanliness'].notna()] 
    price = df1[['host_is_superhost', 'accommodates', 'price']]
    
    return (df1,temp,price)

def process_clean(df):
    clean = df
    cleanmean = (clean.groupby("host_is_superhost", as_index=False)
                 .mean()
                 )  
    return cleanmean

def process_price(df):
    pr = df
    pr['price'] = ( pr['price']
                    .str.replace('$','')
                    .str.replace(',','')
                    .astype(float) )
    price_processed = (pr
                         .groupby(["host_is_superhost","accommodates"],as_index=False)
                         .mean()
                         .drop(price_processed[price_processed['price']==0].index, inplace=True) )
    return price_processed

def wrang_clean(df):
    remaned = df.rename(columns = {"host_is_superhost":"Host is Super Host?","review_scores_cleanliness":"mean of cleanliness score" })
    return remaned
    
def wrang_price(df):
    remaned = df.rename(columns = {'price' :"mean of the prices"})
    return remaned
    