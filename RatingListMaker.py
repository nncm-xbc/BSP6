# Simon Hugot
from pandas import *
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

doc = read_csv('/content/drive/MyDrive/Class/BSPs/BSP06/Abnormal_results/Dax/rating_dax.csv')
doc = doc.iloc[:, 1:]
r, c = doc.shape
changesList = []
final_list = []
rating_SP = ["AAA", "AA+", "AA", "AA-", "A+", "A", "A-", "BBB+", "BBB", "BBB-", "BB+", "BB", "BB-", "B+", "B", "B-", "CCC+", "CCC", "CCC-", "CC", "C", "D"]
rating_moodys = ["Aaa", "Aa1", "Aa2", "Aa3", "A1", "A2", "A3", "Baa1", "Baa2", "Baa3", "Ba1", "Ba2", "Ba3", "B1", "B2", "B3", "Caa1", "Caa2", "Caa3", "Caa"]

print("---------List of rating variations for S&P rating---------")
# process for S&P
variation_list = []
for col in range(1, c):
    ratings_list = []
    dates_list = []
    prices_list = []

    # create 3 lists for each comopany: ratings, dates, prices (makes it easier to compare the indexes)
    for row in range(1, r):
        if "S&P" in doc.iloc[row, 0]:
            ratings_list.append(doc.iloc[row, col])
        elif "DateS" in doc.iloc[row, 0]:
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
                val_recent = rating_SP.index(st1)
                val_old = rating_SP.index(st2)
            elif ' - ' in tupl[2] or ' - ' in tups[2]:
                st1 = tupl[2].split(' - ')[0]
                st2 = tups[2].split(' - ')[0]
                val_recent = rating_SP.index(st1)
                val_old = rating_SP.index(st2)
            else:
                val_recent = rating_SP.index(tupl[2])
                val_old = rating_SP.index(tups[2])

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
'''
for i in list(dict.fromkeys(final_list)):
    print(i)
'''
# daily index of the company and the
for tuples in final_list:
    # Company growth index
    name = tuples[0]
    start_date = tuples[1].split("-")[0] + "-01-01"
    end_date = tuples[1].split("-")[0] + "-12-31"
    yearly_company_return = 0
    daily_returns = []

    prices_data = yf.download(name, start=start_date, end=end_date, interval="1d")
    prices_data = prices_data.drop(['High', 'Low', 'Adj Close', 'Volume', 'Open'], axis=1)

    r, c = prices_data.shape
    for row in range(r):
        prev_daily_return = prices_data.iloc[row - 1, 0]
        if prev_daily_return != 0:
            temp_daily_return = ((prices_data.iloc[row, 0] - prev_daily_return) / prev_daily_return) * 100
        else:
            temp_daily_return = 0
        daily_returns.append(temp_daily_return)
        yearly_company_return += temp_daily_return

    prices_data.insert(1, 'Daily return', daily_returns)

    # Market growth index
    market_data = yf.download('dax', start=start_date, end=end_date, interval="1d")
    market_data = market_data.drop(['High', 'Low', 'Adj Close', 'Volume', 'Open'], axis=1)
    yearly_market_return = 0
    daily_market_returns = []

    r, c = market_data.shape
    for row in range(r):
        prev_daily_market_return = market_data.iloc[row - 1, 0]
        if prev_daily_market_return != 0:
            temp_daily_return = ((market_data.iloc[row, 0] - prev_daily_market_return) / prev_daily_market_return) * 100
        else:
            temp_daily_return = 0
        daily_market_returns.append(temp_daily_return)
        yearly_market_return += temp_daily_return

    diff_sizes = prices_data.shape[0] - len(daily_market_returns)
    prices_data.drop(index=prices_data.index[:diff_sizes], axis=0, inplace=True)
    prices_data.insert(2, 'Daily Market return', daily_market_returns)
    prices_data = prices_data.drop(['Close'], axis=1)

    # print(prices_data)

# Linear regression between market index and company index for a range of years
'''
prices_data.plot(x='Daily return', y='Daily Market return', style='o')
plt.title('Market growth vs Company growth')
plt.xlabel('Company growth')
plt.ylabel('Market growth')
plt.show()
'''
X = prices_data.iloc[:, :-1].values
y = prices_data.iloc[:, 1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# prediction
y_pred = regressor.predict(X_test)
df_prediction = DataFrame({'Actual': y_test, 'Predicted': y_pred})

alpha = regressor.intercept_
beta = regressor.coef_[0]
print(alpha, beta)

fig, ax = plt.subplots()
ax.set_title("Intercept: " + str(round(alpha, 5)) + ", Coefficient: " + str(round(beta, 3)))
ax.scatter(X, y)
ax.plot(X, y_pred, c='r')

# Evaluate the model
print("Evaluation Metrics")
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))