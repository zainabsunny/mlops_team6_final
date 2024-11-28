import pandas as pd
from ucimlrepo import fetch_ucirepo 



def get_bike_data():
    # fetch dataset 
    bike_sharing = fetch_ucirepo(id=275) 
    
    # data (as pandas dataframes) 
    X = bike_sharing.data.features 
    y = bike_sharing.data.targets 
    
    # metadata 
    print(bike_sharing.metadata) 
    
    # variable information 
    print(bike_sharing.variables) 

    bike_df = bike_sharing.data.original
    bike_df.drop(columns=['casual', 'registered'], inplace=True)
    bike_df.set_index('dteday', inplace=True)

    return bike_df



def get_train_test_split(bike_df):

    train_df = pd.DataFrame(bike_df[:'2012-06-30'])
    test_df = pd.DataFrame(bike_df['2012-06-30':])


    return train_df, test_df


def get_x_y_split(bike_df):
    x = bike_df.drop(columns='cnt')
    y = bike_df['cnt']

    return x, y


def update_feature_data(bike_df):
    altered_bike_df = bike_df.copy()
    altered_bike_df["temp"] *= 1.2  # Increase temperature by 20%
    altered_bike_df["windspeed"] *= 0.8  # Decrease windspeed by 20%
    
    return altered_bike_df


def change_test_features(bike_test):
    pass