import numpy as np
import pandas as pd

def unprocessed(csv_file):
    df = pd.read_csv(csv_file)
    return df

def replace_characters(main_string, chars, new_string):
    for char in chars:
        try :
            if char in main_string:
                main_string = main_string.replace(char, new_string)
        except:
            continue       
    return main_string

def loadfinal(csv_file):
    df = pd.read_csv(csv_file)
    df1=(df[["id", 'name', 'host_name','price','accommodates', 'review_scores_rating','review_scores_value']]
         .sort_values("accommodates",ascending=False, ignore_index=True)
        )
    df1['price'] = df1['price'].apply(lambda x : replace_characters(x, ['$', ','], '')).astype(float)
    return df1

def loadall(csv_file):
    df = pd.read_csv(csv_file)
    df1=(df[["id", 'name', 'host_name','price','accommodates', 'review_scores_rating','review_scores_value','review_scores_accuracy',
       'review_scores_cleanliness', 'review_scores_checkin',
       'review_scores_communication', 'review_scores_location']]
         .sort_values("accommodates",ascending=False, ignore_index=True)
        )
    df1['price'] = df1['price'].apply(lambda x : replace_characters(x, ['$', ','], '')).astype(float)
    return df1

def cleanfinal(df):
    df1 = df
    clean =  df1[['price','accommodates','review_scores_rating']]
    clean['price'] = clean['price'].apply(lambda x : replace_characters(x, ['$', ','], '')).astype(float)
    temp_clean = clean[clean['review_scores_rating'].notna()]
    temp_clean= temp_clean[temp_clean['accommodates'].notna()]
    temp_clean= temp_clean[temp_clean['price'].notna()] 
    return temp_clean

def cleanall(df):
    df1 = df
    clean =  df1[["id", 'name', 'host_name','price','accommodates', 'review_scores_rating','review_scores_value','review_scores_accuracy',
       'review_scores_cleanliness', 'review_scores_checkin',
       'review_scores_communication', 'review_scores_location']]
    clean['price'] = clean['price'].apply(lambda x : replace_characters(x, ['$', ','], '')).astype(float)
    temp_clean = clean[clean['review_scores_rating'].notna()]
    temp_clean= temp_clean[temp_clean['accommodates'].notna()]
    temp_clean= temp_clean[temp_clean['id'].notna()] 
    temp_clean= temp_clean[temp_clean['name'].notna()] 
    temp_clean= temp_clean[temp_clean['price'].notna()] 
    temp_clean= temp_clean[temp_clean['review_scores_value'].notna()] 
    temp_clean= temp_clean[temp_clean['review_scores_accuracy'].notna()] 
    temp_clean= temp_clean[temp_clean['review_scores_communication'].notna()] 
    temp_clean= temp_clean[temp_clean['review_scores_location'].notna()] 
    temp_clean= temp_clean[temp_clean['host_name'].notna()] 
    return temp_clean

#Function to accepts threshold of missing values and removes it from the list
def rmissingvaluecol(df, threshold):
    l = []
    l = list(df.drop(df.loc[:,list((100*(df.isnull().sum()/len(df.index)) >= threshold))].columns, 1).columns.values)
    print("Number of columns having more than %s percent missing values: "%threshold, (df.shape[1] - len(l)))
    print("Columns:\n", list(set(list((df.columns.values))) - set(l)))
    return l

def price_per_person_all(df):
    df = cleanall(df)
    df['price_per_person'] = df['price']/df['accommodates']
    return df

def price_per_person_final(df):
    df = cleanfinal(df)
    df['price_per_person'] = df['price']/df['accommodates']
    return df

def ppp_rs_all(df):
    answers = []
    for i in range(20):
        a = i*5
        b = a+5
        r = df[(df["price_per_person"]>a) ]
        r = r[(r["price_per_person"]<b) ]
        m1 = r["review_scores_rating"].mean()
        m2 = r["review_scores_value"].mean()
        m3 = r["review_scores_accuracy"].mean()
        m4 = r["review_scores_cleanliness"].mean()
        m5 = r["review_scores_checkin"].mean()
        m6 = r["review_scores_communication"].mean()
        m7 = r["review_scores_location"].mean()
        answers.append([m1, m2, m3, m4, m5, m6, m7])
    df = pd.DataFrame(answers, columns=["mean_review_scores_rating","mean_review_scores_value","mean_review_scores_accuracy","mean_review_scores_cleanliness","mean_review_scores_checkin","mean_review_scores_communication", "mean_review_scores_location"])
    for i in range(20):
        a = i*5
        b = a+5
        df = df.rename(index={i:str(a)+'-'+str(b)})
    return df

def ppp_rs(df):
    answers = []
    for i in range(20):
        a = i*5
        b = a+5
        r = df[(df["price_per_person"]>a) ]
        r = r[(r["price_per_person"]<b) ]
        m = r["review_scores_rating"].mean()
        answers.append(m)
    df = pd.DataFrame(answers, columns=["mean_review_scores_rating"])
    for i in range(20):
        a = i*5
        b = a+5
        df = df.rename(index={i:str(a)+'-'+str(b)})
    return df

def rename(df):
    mr = df.rename(index={0:'0-5',1:'10-15',2:'15-20',3:'20-25',4:'25-30',5:'30-35',6:'35-40',
                         7:'40-45',8:'45-50',9:'50-55',10:'55-60',11:'60-65',12:'65-70',13:'70-75',
                         14:'75-80',15:'80-85',16:'85-90',17:'90-95',18:'95-100',19:'100-105'})
    return mr
    
def p_rs(df):
    answers = []
    for i in range(20):
        a = i*50
        b = a+50
        r = df[(df["price"]>a) ]
        r = r[(r["price"]<b) ]
        m = r["review_scores_rating"].mean()
        answers.append(m)
    df = pd.DataFrame(answers, columns=["mean_review_scores_rating"])
    for i in range(20):
        a = i*5
        b = a+5
        df = df.rename(index={i:str(a)+'-'+str(b)})
    return df       

def a_rs(df):
    answers = []
    for i in range(17):
        a = i*1
        b = a+1
        r = df[(df["accommodates"]==a) ]
        m = r["review_scores_rating"].mean()
        answers.append(m)
    df = pd.DataFrame(answers, columns=["mean_review_scores_rating"])
    temp_clean = df[df['mean_review_scores_rating'].notna()]
    return temp_clean      
                   
                   
#https://thispointer.com/python-find-indexes-of-an-element-in-pandas-dataframe/
def getIndexes(dfObj, value):
    ''' Get index positions of value in dataframe i.e. dfObj.'''
    listOfPos = list()
    # Get bool dataframe with True at positions where the given value exists
    result = dfObj.isin([value])
    # Get list of columns that contains the value
    seriesObj = result.any()
    columnNames = list(seriesObj[seriesObj == True].index)
    # Iterate over list of columns and fetch the rows indexes where value exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append((row, col))
    # Return a list of tuples indicating the positions of value in the dataframe
    return listOfPos

