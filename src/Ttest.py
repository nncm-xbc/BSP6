import numpy as np
from bioinfokit.analys import stat
from pandas import *
import pandas as pd
import scipy.stats as stats
import os


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
    save_df = pd.DataFrame(columns=["Name" , "Time slot", "Period", "T value", "P value"])
    print(inp_path)
    for dirs in os.listdir(inp_path):
        print(dirs)
        path = inp_path + "/" + dirs + "/Abnormal_returns.csv"
        df = read_csv(path)

        filename = path.split('/')[-2]  # ex: AAL.L-Moody's-2018-08-03
        print(filename)

        before = df.columns.values.tolist()[0]
        print(before)
        after = df.columns.values.tolist()[-len(df.columns.values.tolist())]
        for col in df.columns.values.tolist():
            if "-01-01" in col:
                civ = col
        for col in df.columns.values.tolist():
            if col != civ and col != before and col != after:
                mid = col

        a = np.array(df[civ].tolist())
        b = np.array(df[mid].tolist())
        statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
        dfrow = {"Name": filename, "Time slot": "civ-mid", "Period": civ + "-" + mid, "T value": statistic, "P value": pvalue}
        save_df = save_df.append(dfrow, ignore_index=True)

        a = np.array(df[before].tolist())
        b = np.array(df[after].tolist())
        statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
        dfrow = {"Name": filename, "Time slot": "before-after", "Period": before + "-" + after, "T value": statistic, "P value": pvalue}
        save_df = save_df.append(dfrow, ignore_index=True)

    temp_list = inp_path.split('/')
    temp_list.remove('Prices')
    save_df.to_csv('/'.join(temp_list) + "/Two_sample_results.csv")
