# Simon Hugot
import os
import pandas as pd
from pandas import *
from pathlib import Path


def detect_event(raw_data, market):
    """
    Function that takes as input a raw csv file containing the event-log of security ratings
    for both the S&P and Moody's rating agencies.
    This function can only handle S&P and Moody's ratings as the grading scales are hardcoded.
    :param raw_data: name of the csv file containing the event-log of the security ratings for S&P and Moody's on a specified market
    :param market: name of the market for which the security ratings are defined.
    :return: returns a csv that only contains the stocks for which the security ratings has been updated.
    The date of the change is specified, as well as whether it has been upgraded of downgraded.
    """

    doc = read_csv(raw_data)
    r, c = doc.shape

    # first S&P second Moody's
    rating_scales = [["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC", "CCC-", "CC", "C", "D"],
                     ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2", "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa1", "Caa2", "Caa3", "Caa"]]

    names_agencies = ["S&P", "Moody's"]
    names_dates = ["DateS", "DateM"]

    # perform the actions for both security agencies
    for index_agency in range(len(names_agencies)):
        variation_list = []
        for col in range(1, c):
            ratings_list = []
            dates_list = []
            prices_list = []

            # create 3 lists for each comopany: ratings, dates, prices (makes it easier to compare the indexes)
            for row in range(1, r):
                if names_agencies[index_agency] in doc.iloc[row, 0]:
                    ratings_list.append(doc.iloc[row, col])
                elif names_dates[index_agency] in doc.iloc[row, 0]:
                    dates_list.append(doc.iloc[row, col])
                else:
                    prices_list.append(doc.iloc[row, col])

            # check that the rating for that year (row) is different from ***(null)
            for i in ratings_list:
                if i != "***":
                    temp_index = ratings_list.index(i)
                    variation_list.append((doc.iloc[r - 1, col], dates_list[temp_index], i))

        final_list = []

        for tupl in variation_list:
            for tups in variation_list:
                if tupl[0] == tups[0] and tupl[1] != tups[1] and variation_list.index(tupl) < variation_list.index(tups):
                    # some ratings have a 'range' with either '/' or '-' as a seperator
                    # we will only take into account the lowest rating of the range
                    if ' / ' in tupl[2] or ' / ' in tups[2]:
                        st1 = tupl[2].split(' / ')[0]
                        st2 = tups[2].split(' / ')[0]
                        val_recent = rating_scales[index_agency].index(st1)
                        val_old = rating_scales[index_agency].index(st2)
                    elif ' - ' in tupl[2] or ' - ' in tups[2]:
                        st1 = tupl[2].split(' - ')[0]
                        st2 = tups[2].split(' - ')[0]
                        val_recent = rating_scales[index_agency].index(st1)
                        val_old = rating_scales[index_agency].index(st2)
                    else:
                        val_recent = rating_scales[index_agency].index(tupl[2])
                        val_old = rating_scales[index_agency].index(tups[2])

                    # check indexes and attribute the correct change to the corresponding difference
                    if val_recent < val_old:
                        final_list.append((tupl[0], tupl[1], "Increased"))
                    elif val_recent > val_old:
                        final_list.append((tupl[0], tupl[1], "Decreased"))
                    else:
                        # if the comparison cannot be made the change is simply non-available
                        # ie: first rating change of the dataset
                        final_list.append((tupl[0], tupl[1], "N/A"))
                elif tupl[0] == tups[0] and tupl[1] != tups[1] and variation_list.index(tupl) > variation_list.index(tups):
                    final_list.append((tupl[0], tupl[1], "N/A"))
                else:
                    continue

        # create corresponding dataframe and save it as csv file in the folde corresponding to the correct market.
        df = pd.DataFrame(final_list, columns=["Stock", "Date", "Variation"])
        df.insert(0, "Rating Agency", names_agencies[index_agency])
        df.insert(0, "Market", market)
        df.drop_duplicates(subset=None, keep="first", inplace=True)

        # save the dataframe as a csv in the correct folder
        filepath = Path('Data/'+market+'/StockChanges-'+market+'-'+names_agencies[index_agency]+'.csv')
        df.to_csv(filepath)
