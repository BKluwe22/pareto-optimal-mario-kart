import pandas as pd
import numpy as np 
import os 
import itertools 

DATA_DIR = os.path.join(os.getcwd(), "data")

datasets = [ ("drivers", "Driver"), ("karts", "Body"), ("tires", "Tire"), ("gliders", "Glider") ]

combination_elements = []

for dataset in datasets:
    file_name, dataset_colname = dataset
    df = pd.read_csv(os.path.join(DATA_DIR, f"{file_name}.csv"))
    name_list = df[dataset_colname].tolist()    
    combination_elements.append(name_list)
    
    
all_combinations = list( itertools.product(*combination_elements) )
all_combinations = pd.DataFrame(all_combinations, columns=["Driver", "Body", "Tire", "Glider"])
all_combinations.to_csv("all-combinations.csv", index=False)