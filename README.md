# Pareto Optimal Mario Kart Configurations

## Mario Kart Configurations Optimization

This repository contains scripts to generate and analyze optimal Mario Kart 8 Deluxe configurations based on various character, kart, tire, and glider combinations. It uses
a modified form of the "maxima of a point set algorithm". Instead of using a set to
keep track of efficient points, it uses a 2D array/matrix. It takes advantage of 
vectorized methods to add and remove elements from the matrix. It uses PyTorch tensors
so one can take advantage of GPU acceleration. It should quite scale well to problems where one needs to find pareto optimal configurations with far more than 703,560 candidates and with 
more than 14 parameters compared to the standard implementation for the maxima of a point set algorithm.


It takes an average of 35 seconds to calculate the pareto efficient configurations for all 703,560 builds for all 14 in-game attributes on a NVIDIA GeForce GTX 1650.


## Files

- data/: Directory containing CSV files for drivers, karts, tires, and gliders.

- combination-generator.py: Script to generate all possible combinations of drivers, karts, tires, and gliders.

- join-combinations-w-stats.py: Script to compute the combined stats for each combination.

- combo-pareto-analysis.py: Script to calculate Pareto optimal configurations

- data-to-db.py: Script to save relevant dataframes to sqllite database for easy exploration with SQL.

## Data Source
- [Mario Kart Wiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics)


