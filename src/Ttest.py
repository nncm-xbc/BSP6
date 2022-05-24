import numpy as np
from bioinfokit.analys import stat
from pandas import *
import scipy.stats as stats


def one_sample_t_test(path):
    df = read_csv(path)
    cols = df.columns

    for i in range(1, 4):
        res = stat()
        res_str = cols[i]
        print("One sample T test for " + res_str)
        res.ttest(df=df, test_type=1, res=res_str, mu=5)
        print(res.summary)


def two_sample_t_test(path):
    df = read_csv(path)

    filename = path.split('/')[3]  # ex: AAL.L-Moody's-2018-08-03
    path_to_save = path.remove[path[:20]]  # path - Abnormal_returns.csv

    civ = ""  # ex: "2019-01-01"
    mid = ""
    before = ""
    after = ""

    # print also the name of company and save data in CSVs.
    print("Civ - Mid")
    a = np.array(df["2019-01-01"].tolist())
    b = np.array(df['2019-01-30'].tolist())
    statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
    print("T value = ", statistic, "\n P value = ", pvalue)

    print("Before - Mid")
    a = np.array(df["2018-07-30"].tolist())
    b = np.array(df['2019-01-30'].tolist())
    statistic, pvalue = stats.ttest_ind(a=a, b=b, equal_var=True)
    print("T value = ", statistic, "\n P value = ", pvalue)
