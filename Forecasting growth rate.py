
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tsa.api import VAR # vector autoregression
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tsa.base.datetools import dates_from_str
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

sns.set(rc={'figure.figsize':(20, 4)})

get_ipython().run_line_magic('matplotlib', 'inline')


data = pd.read_csv("ModifiedChange-ETH.csv")
data = data.set_index("Time")
data.head()




def grangers_causality_matrix(data, variables, test='ssr_chi2test', maxlag=2, verbose=True):

    dataset = pd.DataFrame(np.zeros((len(variables), len(variables))), columns=variables, index=variables)

    for c in dataset.columns:
        for r in dataset.index:
            test_result = grangercausalitytests(data[[r,c]], maxlag=maxlag, verbose=False)
            p_values = [round(test_result[i+1][0][test][1], 5) for i in range(maxlag)]
            if verbose:
                print(f'Y = {r}, X = {c}, P Values = {p_values}')

            min_p_value = np.min(p_values)
            dataset.loc[r,c] = min_p_value

    dataset.columns = [var + '_x' for var in variables]

    dataset.index = [var + '_y' for var in variables]

    return dataset

grangers_causality_matrix(data, variables=data.columns)



BTC = data["BTC_Growth"].values
ETH = data["ETH_Growth"].values

BTC_result = adfuller(BTC)
print('BTC - ADF Statistic: %f' % BTC_result[0])
print('BTC - p-value: %f' %  BTC_result[1])

ETH_result = adfuller(ETH)
print('\nETH - ADF Statistic: %f' % ETH_result[0])
print('ETH - p-value: %f' %  ETH_result[1])



model = VAR(data)
lag_orders = model.select_order(25)
lag_orders.summary()



lag_order = 1
results = model.fit(lag_order, ic="aic")
results.summary()



dw_r = durbin_watson(results.resid)

for col, val in zip(data.columns, dw_r):
    print(col, ':', round(val, 2))


fc = results.forecast(data.values[-lag_order:], steps=20
                     )
fc = pd.DataFrame(fc, columns=["BTC_forecast", "ETH_forecast"])
fc



results.plot_forecast(20);





