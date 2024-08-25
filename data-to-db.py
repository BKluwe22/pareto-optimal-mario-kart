import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///mario.db', echo=False)

cols = [ 
    'driver', 'body', 'tire', 'glider', 'weight',
    'acceleration', 'onRoadTraction', 'offRoadTraction', 
    'miniTurbo', 'groundSpeed', 'waterSpeed', 'antiGravitySpeed',
    'airSpeed', 'groundHandling', 'waterHandling', 'antiGravityHandling', 
    'airHandling', 'invincibility'
]

pareto_combos = pd.read_csv("pareto-combos.csv")
all_combos = pd.read_csv("all-combination-stats.csv")

pareto_combos.columns = cols
all_combos.columns = cols

pareto_combos.to_sql(name='pareto_combos', con=engine, if_exists='replace')
all_combos.to_sql(name='all_combos', con=engine, if_exists='replace')
