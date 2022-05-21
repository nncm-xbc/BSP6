from bioinfokit.analys import stat
from pandas import *


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
    res = stat()
    res.ttest(df=df, xfac= "", res='2018-07-30', test_type=2)
    print(res.summary)
