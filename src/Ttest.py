import numpy as np
from bioinfokit.analys import stat
from pandas import *
import pandas as pd
import scipy.stats as stats
import os
from datetime import datetime


def one_sample_t_test(path):
    path = path + "/Abnormal_returns.csv"
    df = read_csv(path)
    cols = df.columns

    for i in range(1, 4):
        res = stat()
        res_str = cols[i]
        print("One sample T test for " + res_str)
        res.ttest(df=df, test_type=1, res=res_str, mu=5)
        print(res.summary)


def two_sample_t_test(inp_path):
    save_df = pd.DataFrame(columns=["Name","Time Slot", "Period", "T value", "P value"])
    for dirs in os.listdir(inp_path):
        path = inp_path + "/" + dirs + "/Abnormal_returns.csv"
        df = read_csv(path)
        filename = path.split('/')[-2]  # ex: AAL.L-Moody's-2018-08-03
        print(filename)

        before = df.columns.values.tolist()[1]
        after = df.columns.values.tolist()[4]
        for col in df.columns.values.tolist():
            if "-01-01" in col:
                civ = col
        for col in df.columns.values.tolist():
            if col != civ and col != before and col != after:
                mid = col

        # ---------------------For CIVIL YEAR ---------------------
        # Compure all 4 time windows
        str_d1 = before
        str_d2 = civ

        # convert string to date object
        d1 = datetime.strptime(str_d1, "%Y-%m-%d")
        d2 = datetime.strptime(str_d2, "%Y-%m-%d")

        # difference between dates in timedelta
        delta = d2 - d1
        nb_days = delta.days

        row_of_change = len(df) - nb_days - 1

        # [-20;-11] and [+11; +20]
        start_1 = row_of_change - 20
        end_1 = row_of_change - 11

        start_5 = row_of_change + 11
        end_5 = row_of_change + 20

        # [-10; -2] and [+2; +10]
        start_2 = row_of_change - 10
        end_2 = row_of_change - 2

        start_4 = row_of_change + 2
        end_4 = row_of_change + 10

        df1 = df[start_1:end_1]
        df5 = df[start_5:end_5]

        df2 = df[start_2:end_2]
        df4 = df[start_4:end_4]

        a = np.array(df1[civ].tolist())
        b = np.array(df5[civ].tolist())
        statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
        dfrow = {"Name": filename, "Time Slot": "Civ", "Period":  "[-20;-11] and [+11; +20]", "T value": statistic, "P value": pvalue}
        save_df = save_df.append(dfrow, ignore_index=True)

        a = np.array(df2[civ].tolist())
        b = np.array(df4[civ].tolist())
        statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
        dfrow = {"Name": filename, "Time Slot": "Civ", "Period": "[-10; -2] and [+2; +10]", "T value": statistic, "P value": pvalue}
        save_df = save_df.append(dfrow, ignore_index=True)

        # ---------------------For MIDDLE YEAR ---------------------
        # Compure all 4 time windows
        str_d1 = before
        str_d2 = mid

        # convert string to date object
        d1 = datetime.strptime(str_d1, "%Y-%m-%d")
        d2 = datetime.strptime(str_d2, "%Y-%m-%d")

        # difference between dates in timedelta
        delta = d2 - d1
        nb_days = delta.days

        row_of_change = len(df) - nb_days - 1

        # [-20;-11] and [+11; +20]
        start_1 = row_of_change - 20
        end_1 = row_of_change - 11

        start_5 = row_of_change + 11
        end_5 = row_of_change + 20

        # [-10; -2] and [+2; +10]
        start_2 = row_of_change - 10
        end_2 = row_of_change - 2

        start_4 = row_of_change + 2
        end_4 = row_of_change + 10

        df1 = df[start_1:end_1]
        df5 = df[start_5:end_5]

        df2 = df[start_2:end_2]
        df4 = df[start_4:end_4]

        a = np.array(df1[mid].tolist())
        b = np.array(df5[mid].tolist())
        statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
        dfrow = {"Name": filename, "Time Slot": "Mid", "Period": "[-20;-11] and [+11; +20]", "T value": statistic, "P value": pvalue}
        save_df = save_df.append(dfrow, ignore_index=True)

        a = np.array(df2[mid].tolist())
        b = np.array(df4[mid].tolist())
        statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
        dfrow = {"Name": filename, "Time Slot": "Mid", "Period": "[-10; -2] and [+2; +10]", "T value": statistic, "P value": pvalue}
        save_df = save_df.append(dfrow, ignore_index=True)

    temp_list = inp_path.split('/')
    temp_list.remove('Prices')
    save_df.to_csv('/'.join(temp_list) + "/Two_sample_results.csv")
