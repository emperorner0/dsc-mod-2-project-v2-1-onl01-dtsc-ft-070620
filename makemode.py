import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import plotly.express as px
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib as mpl
import warnings
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from IPython.display import display

def make_model(df, target='price', drop_cols=[], show_sum = True):
    
    """
    Returns model, shows QQplot, shows homoescedascity test
    df - dataframe
    target - Target for estimation
    drop_cols - list of columns to drop, if any
    
    return: Model from statsmodels"""
    
    
    df_ohe = df.copy()

    ## Dropping columns not needed
    for col in drop_cols:
        if col in df_ohe.columns:
            df_ohe.drop(columns=col,inplace=True)
    
    ## Formula and Model
    features = '+'.join(df_ohe.drop(columns=target).columns)
    f = target + '~' + features
    m = smf.ols(f, df_ohe).fit()
    resids = m.resid
    if show_sum:
        display(m.summary())

        ## Plotting
        fig,ax = plt.subplots(ncols=2,figsize=(10,5))
        sm.graphics.qqplot(m.resid,fit=True, line='45', ax=ax[0])
        ax[0].set_title('QQ Plot')
        ax[1].scatter(x=df_ohe[target],y=resids)
        ax[1].axhline(0,color='k')
        ax[1].set(ylabel='Resids',title='Homoscedasticity Check',
                      xlabel='Target Values')
        plt.tight_layout()
        plt.show()

    return m