import pandas as pd
import numpy as np

def unprocessed(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Drop columns with missing values
def drop_empty(df):
    df = df.drop(['neighbourhood_group_cleansed', 'license', 'calendar_updated', 'bathrooms'], axis=1, inplace=True)    
             
    return df

# Rename columns we will be working with
def rename_columns(df):
    df1 = df.rename(columns={"review_scores_communication":"Reviews Scores Communication",
                  "reviews_per_month": "Reviews per Month",
                   "host_response_rate": "Host Response Rate",
                   "host_acceptance_rate": "Host Acceptance Rate",
                   'review_scores_accuracy': "Review Scores Accuracy",
                   "review_scores_checkin": "Review Scores Checkin",
                   "review_scores_location": "Review Scores Location",
                    "review_scores_value": "Review Scores Value"})
    return df1


#adapted from https://github.com/jsprovost1/Airbnb_EDA/blob/master/Airbnb_Seattle.ipynb
def replace_characters(main_string, chars, new_string):
    """
    Parameters:
    main_string (str): The string for which you want to make the replacement
    chars (str): The character that you want to replace
    new_string (str): The new string that will replace the previous string (chars)
    
    Return:
    The original string, but with the new characters now incorporated.
    """
    
    for char in chars:
        try :
            if char in main_string:
                main_string = main_string.replace(char, new_string)
        except:
            continue       
    return main_string



def get_num_mean_hosts(superhosts_num, regularhosts_num):
    """
        get mean values of numeric column by host
        mean() function skip NaN values
        NaN is difficult to measure, so exclude it
    """
    
    # drop useless columns and get only numeric data
    mean_compare = pd.concat(
        [
            superhosts_num.mean(), 
            regularhosts_num.mean()
        ], 
        axis=1)
    
    mean_compare.columns = ["superhost", "regular"]
    
    # add dataframe length on the first row
    return pd.concat([
        pd.DataFrame(
            [[len(superhosts), len(regularhosts)]], 
            index = ['count'],
            columns=mean_compare.columns), mean_compare])


def numeric_set(df):

    drop_columns = """
    calculated_host_listings_count
    neighbourhood_group_cleansed
    calendar_updated
    latitude
    license
    longitude
    bathrooms
    maximum_nights_avg_ntm
    maximum_maximum_nights
    minimum_maximum_nights
    maximum_nights
    id
    scrape_id
    host_id
    """.split()


    """
        drop columns that do no have numeric data (ex: id, location) and that are missing data
    """
    return df.drop(columns=drop_columns)._get_numeric_data()



def split_host(df=pd.read_csv ("../data/raw/listings.csv")): 
    """
        split listings into two categories : whether host is superhost or not(regular host)
    """
    superhosts = df[df.host_is_superhost == 't']
    regularhosts = df[df.host_is_superhost == 'f']
    
    return superhosts, regularhosts

superhosts, regularhosts = split_host()



def get_num_mean_hosts(superhosts_num, regularhosts_num):
    """
        get mean values of numeric column by host
        mean() function skip NaN values
        NaN is difficult to measure, so exclude it
    """
    
    # drop useless columns and get only numeric data
    mean_compare = pd.concat(
        [
            superhosts_num.mean(), 
            regularhosts_num.mean()
        ], 
        axis=1)
    
    mean_compare.columns = ["superhost", "regular"]
    
    # add dataframe length on the first row
    return pd.concat([
        pd.DataFrame(
            [[len(superhosts), len(regularhosts)]], 
            index = ['count'],
            columns=mean_compare.columns), mean_compare])



def plot_numeric_mean_by_host(numeric_mean_by_hosts):
    """
        Convert average values for each category into ratio (for superhost and normal hosts). 
        Display a bar histogram.
    """
    proportions = numeric_mean_by_hosts.div(numeric_mean_by_hosts.sum(axis=1), axis=0)
    proportions.plot(kind='barh', stacked='true', figsize=(10, 10), title = 'Comparison Metrics for Regular host vs Superhost')
    
    

