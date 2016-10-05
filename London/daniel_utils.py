from pandas import *
import numpy as np
from pandas import read_csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
def get_cycle_with_bbt(df, cycle_index):
	d = {}
	for i in range(1, df['L_CYCLE'][cycle_index]+1):
		d[i]=df['TEMP'+str(i)][cycle_index]
	dfcycle = DataFrame(list(d.items()), columns=['day', 'BBT'])
	return dfcycle
def zero_to_nan(df):
	df = df.replace(0, np.nan)
	return df
def rename_it_en(df):
    df = df.rename(columns = {'DONNA': 'ID',
                            'P_SPEZZ' : 'GROUP_ID',
                            'P_CICLO' : 'CYCLE_ID',
                            'ANNO_NAS' : 'BIRTH_YR',
                            'DATA' : 'BEGIN_DATE',
                            'T_SPEZZ' : 'N_GROUPS',
                            'T_CICLI' : 'N_CYCLES',
                            'QUALIFI' : 'DESC',
                            'TIPOTEMP' : 'TEMP_SCALE',
                            'L_CICLO' : 'L_CYCLE',
                            'L_PREOV' : 'L_PREOVULATION',
                            'L_PERIOD' : 'L_PERIOD',
                            'FIGLI' : 'CHILDREN'
                           })
    if 'ETA' in df.columns: # Alletaev
        df = df.rename(columns = {
                'ETA' : 'AGE',
                'GG_MATR' : 'DD_MARRIAGE',
                'MM_MATR' : 'MM_MARRIAGE',
                'YY_MATR' : 'YY_MARRIAGE',
                'GG_UL_EV' : 'DD_PREV_EV',
                'MM_UL_EV' : 'MM_PREV_EV',
                'AA_UL_EV' : 'YY_PREV_EV',
                'GG_1_EV' : 'DD_1_EV',
                'MM_1_EV' : 'MM_1_EV',
                'AA_1_EV' : 'YY_1_EV',
                'GG_2_EV' : 'DD_2_EV',
                'MM_2_EV' : 'MM_2_EV',
                'AA_2_EV' : 'YY_2_EV',
                'GG_3_EV' : 'DD_3_EV',
                'MM_3_EV' : 'MM_3_EV',
                'AA_3_EV' : 'YY_3_EV',
                'GG_4_EV' : 'DD_4_EV',
                'MM_4_EV' : 'MM_4_EV',
                'AA_4_EV' : 'YY_4_EV'
                })
    return df
def process_df(df):
    df = zero_to_nan(df)
    df = df.dropna(subset={'L_PREOV', 'L_PERIOD'})
    df = df.reset_index(drop=True)
    df = rename_it_en(df)
    return df;
"""
def drop_row_if(df, col, val): #drops row if the column (col) value is val
	df = df[df[col]!=val]
	df = df.reset_index(drop=True)
	return df
def drop_row_if_nan(df, col):
    df = df.dropna(subset={col})
    df = df.reset_index(drop=True)
    return df
"""
def plot_cycle(df_cycle, cycle_index, l_period, l_preov):
    df_cycle.plot(kind='line', x='day', y='BBT')
    
    plt.axvline(l_period, color='red')
    plt.axvline(l_preov, color='green')
    plt.savefig('figs/' + str(cycle_index) + '.png')  # write image to file.. filename+2=row in csv file
    
def subject_cycles(df, subject_id):
    df = df[df['ID'] == subject_id]
    df.reset_index(drop=True)
    return df

def begin_date_to_datetime(df):
    for i in range(0, len(df)):
        df['BEGIN_DATE'][i] = str(df['BEGIN_DATE'][i])[:-2] + "19" + str(df['BEGIN_DATE'][i])[-2:]
    df['BEGIN_DATE'] = pd.to_datetime(df['BEGIN_DATE'], format='%d-%m-%Y')
    return df