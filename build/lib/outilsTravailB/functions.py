import pandas as pd
import plotly as pl
import numpy as np
from datetime import date
import subprocess


def cleanData(data):
    cleanData = {}
    for i in data:
        df = data[i].copy()  # Create a copy with only the necessary columns
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)  # Set the index directly
        df["dailyDate"] = df.index.strftime("%Y-%m-%d")  # Create a new column with formatted date strings
        cleanData[i] = df
    
    return cleanData


def createFramework(df, k, annualize, type):
    
    def applyRollingWindow(group, k, annualize, type, date):
        n = len(group)
        knew = int(min(k, 391 - k))
        res = np.zeros((1, knew))
        rendementSomme = group['LogReturn'].rolling(window=k, min_periods=k).sum()
        multiplier = 252 if annualize else 1

        for decalage in range(knew):
            idx = list(range(decalage + k - 1, n, k))
            vector = rendementSomme.iloc[idx]

            if type == "vq":  # Quadratic Variation
                res[0, decalage] = (np.square(vector) * multiplier).sum()
                
            elif type == "iv":  # Integrated Variance (Bipower Variation)
                
                if len(idx) > 1 :
                    bipower_factor = (np.pi / 2)
                    bipower_sum = 0
                    for i in range(1, len(idx)):
                        bipower_sum +=  abs(vector.iloc[i] * vector.iloc[i - 1])
                        
                    res[0, decalage] = bipower_sum * bipower_factor* multiplier
                    
                else : res[0, decalage] = 0
                    
        return pd.DataFrame(res, index=[date])
                    

    # Prepare a list to collect the results of each group
    results = []
    # Group by day and apply the rolling window function
    for date, group in df.groupby(df["dailyDate"]):
        results.append(applyRollingWindow(group, k=k, annualize=annualize, date=date, type = type))

    # Concatenate all the results into a single DataFrame
    final_df = pd.concat(results)
    
    return final_df


def groupByDay(tmp : pd.DataFrame, type) :
    
    if type == "Naive":
        res = tmp[0]
    elif type == "Mean":
        res = tmp.mean(axis=1)  
    
    return res




def runApp():
    subprocess.run(["streamlit", "run", "app.py"])