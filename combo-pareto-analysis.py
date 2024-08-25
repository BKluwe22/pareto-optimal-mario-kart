import pandas as pd
import os 
from tqdm import tqdm
import torch


DATA_DIR = os.path.join(os.getcwd(), "data")
RESULTS_DIR = os.path.join(os.getcwd(), "results")

# GPU isn't strictly required for this but in case where the pareto set
# is very large, it will significant advantages - if applying to other
# use cases
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


df = pd.read_csv("all-combination-stats.csv")
parameter_cols = [x for x in df.columns if x not in ["driver", "body", "tire", "glider"]]


# before we start, we want to sort the dataframe from highest total to lowest
# total - this is because we are more likely to encounter pareto efficient 
# configs early which would probably decrease the number of times we encounter
# a point that dominates others in the set which would result in need to 
# remove elements in the set - once sorted, drop the column as its not a value
# we care about in the pareto calculation
df['total'] = df['WG'] + df['AC'] + df["ON"] + df["OF"] + df["MT"] + df["SL"] + df["SA"] + df["SG"] + df["TL"] + df["TW"] + df["TA"] + df["TG"] + df["IV"]
df = df.sort_values("total", ascending=False).reset_index(drop=True)
df = df.drop(["total"], axis=1)


# Algorithm = maxima of a point set 
# runs well on GPU 


# We want to minimize data transfer from host to GPU 
# 1. filter df to only include parameters we are trying to optimize - no driver, body, tire, glider as these are text values
# 2. convert df to torch tensors - since all numbers are between 0 and 255, we can represent them using int8
# 3. initialize the pareto set on the GPU as well

# now all data movement will be on GPU
df_arr = torch.from_numpy(df[parameter_cols].to_numpy()).to(dtype=torch.int8).to(DEVICE)
pareto_set = torch.zeros((0, 14), dtype=torch.int8, device=DEVICE)

for build_stats in tqdm(df_arr):
    
    if pareto_set.size(0) > 0:
        
        # subtact config_stats vector (1, 14) or (14,) from pareto set matrix (n, 14)
        diffs = pareto_set - build_stats
        
        # if there is a row where all elements are zero - then skip further 
        # calculations because the build has stats that are already in the 
        # pareto set
        if torch.any(torch.all(diffs == 0, dim=1)):
            continue
        
        # Determine if the build is dominated - i.e.: if there is a row where 
        # all values are less than or equal to zero - if additionally at least one is less
        # than zero, then the build is pareto dominated
        is_build_dominated_vector = torch.all(diffs <= 0, dim=1) & torch.any(diffs < 0, dim=1)
        
        # if build is pareto dominated, then we just jump to the next build
        if torch.any(is_build_dominated_vector):
            continue
        
        
        # Determine if the build dominates existing points - this creates a mask
        # vector where True indicates that the build dominates the build at 
        # index in the pareto set and False indicates that the build doesn't 
        # dominate
        does_build_dominate_existing_points_vector = torch.all(diffs >= 0, dim=1) & torch.any(diffs > 0, dim=1)
        
        # Use above vector as filter - invert and use ask mask filter to remove
        # points that were dominated by our current build
        pareto_set = pareto_set[~does_build_dominate_existing_points_vector]
    
    # if we have reached this point, then the build is pareto efficient, so 
    # we add to the pareto set
    pareto_set = torch.cat((pareto_set, build_stats.unsqueeze(0)), dim=0)
    
    



# safe to df
pareto_set = pd.DataFrame(pareto_set.cpu().numpy(), columns=parameter_cols)

# do right merge on main dataframe - result is df that contains all pareto 
# optimal kart configurations
pareto_combos = pd.merge(
    df,
    pareto_set,
    how="right",
    left_on=parameter_cols,
    right_on=parameter_cols
)

# save for further analysis 
pareto_set.to_csv("pareto-values-matrix.csv", index=False)
pareto_combos.to_csv("pareto-combos.csv", index=False)
    
    


