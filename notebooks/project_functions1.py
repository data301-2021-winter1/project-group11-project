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
    clean =  clean[clean['review_scores_cleanliness'].notna()]
    clean = clean[clean['host_is_superhost'].notna()]
    
    pr = df1[['host_is_superhost', 'accommodates', 'price']]
    pr = pr[pr['host_is_superhost'].notna()]
    
    return (df1,clean,pr)

def process_clean(df):
    clean = df
    
    cleanmean = (clean
                  .groupby("host_is_superhost", as_index=False)
                  .mean()
                 )  
    return cleanmean

def process_price(df):
    pr = df
   
    pr['price'] =  (  pr['price']
                      .str.replace('$','')
                     .str.replace(',','') 
                     .astype(float) )
    price_processed = (  pr
                         .groupby(["host_is_superhost","accommodates"],as_index=False)
                        .mean() )
    price_processed.drop(price_processed[price_processed['price']==0].index, inplace=True)
    return price_processed

def wrang_clean(df):
    remaned = df.rename(columns = {"host_is_superhost":"Is_Super_Host","review_scores_cleanliness":"mean of cleanliness score" })
    remaned['Is_Super_Host'] = remaned.Is_Super_Host.replace({'t':'Super host', 'f':'normal host'})
    # The above line of code is extracted from https://www.kite.com/python/answers/how-to-replace-column-values-in-a-pandas-dataframe-in-python#:~:text=Access%20a%20specific%20pandas.,old%20values%20to%20new%20values.
    return remaned
    
def wrang_price(df):
    remaned = df.rename(columns = {'price' :"mean of the prices"})
    remaned['host_is_superhost'] = remaned.host_is_superhost.replace({'t':'Super host', 'f':'normal host'})
    # The above line of code is extracted from https://www.kite.com/python/answers/how-to-replace-column-values-in-a-pandas-dataframe-in-python#:~:text=Access%20a%20specific%20pandas.,old%20values%20to%20new%20values.
    return remaned
    