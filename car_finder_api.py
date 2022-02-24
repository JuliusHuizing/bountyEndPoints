

import pandas as pd
from fuzzywuzzy import fuzz
import numpy as np
import logging

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def pre_process(df):
    # Keep only columns of interest
    df = df[["id", "make", "fuelType", "year", "model", 'co2TailpipeGpm']]
    # Convert year attribute to string values
    df['year'] = df['year'].map(str)
    return df

def findTopNMatches(word, options, n=3, similarity_algorithm=fuzz):
    ratios = np.array([fuzz.ratio(word.lower(), op.lower()) for op in options])
    topn_indices = np.argsort(ratios)[::-1][:n]
    options=np.array(list(options))
    return options[topn_indices]

def querry_to_df_matches(df, querry, top):
    try: 
        maker, model, year = querry.split(" ")
    except:
        raise Exception("Please provide only three argumets (maker, model, year).")
    
    makers=df["make"]
    logging.debug(f"Finding maker, model, and year match for querry '{querry}'.")
    
    maker_match = findTopNMatches(maker, makers, n=top)[0]
    logging.debug(f"...found maker match '{maker_match}'.")
    
    # For successful querries, we should only find models that belong to the given maker.
    logging.debug("reducing dataframe to found maker...")
    df = df[df['make'] == maker_match]
    
    models = df['model']
    model_match = findTopNMatches(model, models, n=1)[0]
    logging.debug(f"...found model match {model_match}.")
    
    # For successful querries, we should only find models that belong to the given maker.
    logging.debug("reducing dataframe to found model...")
    df = df[df['model'] == model_match]
    
    years = df['year']
    logging.debug(f"looking among available years: \n {years}")
    year_match = findTopNMatches(year, years, n=1)[0]
    logging.debug(f"...found year match {year_match}.")

    return {"make": maker_match, "model": model_match, "year": year_match}

def get_car_info(df, make, model, year, top):
    return df.loc[(df['make'] == make) & (df['model'] == model) & (df['year'] == year)].iloc[:top]
    
def find_car(querry, df, top):
    df = pre_process(df)
    df['year'] = df['year'].map(str)
    match = querry_to_df_matches(df, querry=querry, top=top)
    return get_car_info(df=df, **match, top=top)


# TODO rm/comment this
# df_cars = pd.read_csv("vehicles.csv", low_memory=False)
# print("test")
# print(find_car(querry = "audi a4 2005", df=df_cars, top=3).to_dict(orient='records'))
