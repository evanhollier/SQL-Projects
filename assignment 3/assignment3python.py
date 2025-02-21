import mysql.connector
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import statsmodels.api as sm

def main():
  db = mysql.connector.connect(
    host='localhost',
    database='mlb',
    user='root',
    password='mysql'
  )
  cur = db.cursor()

# 2) Do a regression on players heights and weights to get the mathematical relationship between
#    the two. (get the slope and intercept of the regression).
  sql = """SELECT height, weight FROM mlb_master \
            WHERE player_id NOT IN \
            (SELECT player_id FROM mlb_manager)"""
  cur.execute(sql)
  heights = np.array([])
  weights = np.array([])
  for q in cur:
    heights = np.append(heights, q[0])
    weights = np.append(weights, q[1])
  reg = LinearRegression()
  reg.fit(heights.reshape(-1, 1), weights.reshape(-1, 1))
  print("The linear model is: Y = {:.5} + {:.5}X".format(reg.intercept_[0], reg.coef_[0][0]))
  
  db.commit()
  db.close()

if __name__ == "__main__":
  main()