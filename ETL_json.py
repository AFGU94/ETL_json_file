import pandas as pd
import json
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

def extract(file_path):
    # Open the JSON file in read mode
    try:
        with open(file_path, 'r') as file:
            # Load the JSON data
            data = json.load(file)
            return data
    except Exception as e:
        logging.error("Error en la extracción: %s", e)
        return None

def transform(data):  
    # Create a DataFrame with the data
    print(data)
    df = pd.DataFrame(data)
    print(df.head())
    print(f"The columns of the json data are: {df.columns}")
    # Select the nested JSON data based on the debug column messages
    df_filt = df['movies']
    # Normalize the nested JSON data
    df_filt = pd.json_normalize(df_filt)
    pd.set_option('display.max_columns', None) # Display all columns
    print(f"The columns of the normalized dataframe are: {df_filt.columns}")
    
    # display the null data in the dataframe
    msno.matrix(df_filt, figsize=(8, 6), fontsize=6)
    plt.show()
    print(df_filt[['releaseDate.day','releaseDate.month']])
    # Replace the missing values with 1
    df_filt[['releaseDate.day','releaseDate.month']]= df_filt[['releaseDate.day','releaseDate.month']].fillna(1) # fillna(1) ya que es una fecha no hay un dia 0
    # Convert the releaseDate columns to datetime
    df_filt[['releaseDate.day','releaseDate.month','releaseDate.year']] = df_filt[['releaseDate.day','releaseDate.month','releaseDate.year']].astype(int)
    # Create a new column with the combined date
    df_filt['releaseDate'] = pd.to_datetime(df_filt[['releaseDate.year','releaseDate.month','releaseDate.day']].rename(columns={'releaseDate.day':'day','releaseDate.month':'month','releaseDate.year':'year'}))
    # Drop the columns that are no longer needed
    df_clean = df_filt.drop(columns=['releaseDate.day','releaseDate.month','releaseDate.year'])
    print((f"The columns of the cleaned dataframe are: {df_clean.columns}"))
    
    # Find duplicates based on the id column
    column_names = ['id']
    duplicates = df_clean.duplicated(subset=column_names, keep=False)
    data_duplicates = df_clean[duplicates].sort_values(by='id')
    print(data_duplicates)
    # Drop duplicates based on the id column
    df_clean = df_clean.drop_duplicates(subset='id')

    # shapes of the dataframe
    print(f"The shape of the json data is: {df.shape}")
    print(f"The shape of the normalized dataframe is: {df_filt.shape}") 
    print(f"The shape of the cleaned dataframe is: {df_clean.shape}")
    return df_clean 

def load(df, path_to_save):
    # Save the data to a CSV file
    try:
        df.to_csv(path_to_save, index=False)
        logging.info("Data saved successfully")
    except Exception as e:
        logging.error("Error en la carga: %s", e)
    
def plot(df):
    # Plot the releaseDate column
    try:
        sns.histplot(df['releaseDate'], bins=20, kde=True)
        plt.title('Distribution of Release Dates of the movies')
        plt.xlabel('Release Dates')
        plt.ylabel('Count')
        plt.show()

    except Exception as e:
        logging.error("Error en la visualización: %s", e)


# prompt the user to enter the path to the JSON file
#url = input("Enter the path to the JSON file: ")
url = "palestinian_movies.json"
data = extract(url)
df = transform(data)
plot(df)

