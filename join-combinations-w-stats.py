import pandas as pd
import numpy as np 
import os 
import itertools 

DATA_DIR = os.path.join(os.getcwd(), "data")

combinations = pd.read_csv("all-combinations.csv")


drivers = pd.read_csv(os.path.join(DATA_DIR, "drivers.csv")).set_index("Driver")
bodies = pd.read_csv(os.path.join(DATA_DIR, "karts.csv")).set_index("Body")
tires = pd.read_csv(os.path.join(DATA_DIR, "tires.csv")).set_index("Tire")
gliders = pd.read_csv(os.path.join(DATA_DIR, "gliders.csv")).set_index("Glider")

combo_df_cols = [ *["driver", "body", "tire", "glider"], *drivers.columns ]

rows = []
for idx, combo in enumerate(combinations.itertuples()):
    
    d_values = drivers.loc[combo.Driver].to_numpy()
    b_values = bodies.loc[combo.Body].to_numpy()
    t_values = tires.loc[combo.Tire].to_numpy()
    g_values = gliders.loc[combo.Glider].to_numpy()
    
    combined_values = d_values + b_values + t_values + g_values
    
    data = [combo.Driver, combo.Body, combo.Tire, combo.Glider, *combined_values]
    
    rows.append(data)
    
    if idx % 1000 == 0:
        print(f"{idx}/{len(combinations)}")
    
# Create the DataFrame once
combo_df = pd.DataFrame(rows, columns=combo_df_cols)

combo_df.to_csv("all-combination-stats.csv", index=False)