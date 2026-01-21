import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.optimizers import Adam
from keras import layers
from market import options_map, get_market_data, period_options

def df_to_windowed_df(dataframe, first_date, last_date, n=3):
    
    first_date = pd.to_datetime(first_date)
    last_date = pd.to_datetime(last_date)

    dates = []
    X, Y = [], []

    target_date = first_date

    while target_date <= last_date:
        # Take last (n + 1) values up to target_date
        df_subset = dataframe.loc[:target_date].tail(n + 1)

        if len(df_subset) != n + 1:
            raise ValueError(
                f"Window of size {n} is too large for date {target_date}"
            )

        values = df_subset['Close'].to_numpy()
        x, y = values[:-1], values[-1]

        dates.append(target_date)
        X.append(x)
        Y.append(y)

        # Move to next available trading day
        next_idx = dataframe.index.get_loc(target_date) + 1

        if next_idx >= len(dataframe):
            break

        target_date = dataframe.index[next_idx]

    # Build output DataFrame
    ret_df = pd.DataFrame({'Target Date': dates})

    X = np.array(X)
    for i in range(n):
        ret_df[f'Target-{n-i}'] = X[:, i]

    ret_df['Target'] = Y

    return ret_df

import numpy as np

def windowed_df_to_date_X_y(windowed_dataframe):

    dates = windowed_dataframe['Target Date'].values

    feature_cols = windowed_dataframe.columns[1:-1]

    X = windowed_dataframe[feature_cols].values.astype(np.float32)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    Y = windowed_dataframe['Target'].values.astype(np.float32)

    return dates, X, Y

def predict_next_n_days(model, last_window, ndays=20):

    predictions = []
    current_window = last_window.copy()

    for _ in range(ndays):
        pred = model.predict(
            current_window.reshape(1, -1, 1),
            verbose=0
        )[0, 0]

        predictions.append(pred)
        current_window = np.roll(current_window, -1)
        current_window[-1] = pred

    return np.array(predictions)



data = get_market_data("^GSPC", period='1mo')
df = pd.DataFrame(data)
scaler = MinMaxScaler()
df['Close'] = scaler.fit_transform(df[['Close']])
df = df[['Close']]

n = 3
start_date = df.index[n]
end_date = df.index.max()

windowed_df = df_to_windowed_df(
    df,
    first_date=start_date,
    last_date=end_date,
    n=n
)

dates, X, y = windowed_df_to_date_X_y(windowed_df)

q_80 = int(len(dates) * .8)
q_90 = int(len(dates) * .9)

dates_train, X_train, y_train = dates[:q_80], X[:q_80], y[:q_80]

dates_val, X_val, y_val = dates[q_80:q_90], X[q_80:q_90], y[q_80:q_90]
dates_test, X_test, y_test = dates[q_90:], X[q_90:], y[q_90:]

model = Sequential([layers.Input((3, 1)),
                    layers.LSTM(64),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(32, activation='relu'),
                    layers.Dense(1)])

model.compile(loss='mse', 
              optimizer=Adam(learning_rate=0.001),
              metrics=['mean_absolute_error'])

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=100)

window_size = X.shape[1]
last_window = X[-1]

future_preds = predict_next_n_days(
    model,
    last_window,
    ndays=20
)

future_preds = scaler.inverse_transform(
    future_preds.reshape(-1, 1)
).flatten()


print(future_preds)


'''
train_predictions = model.predict(X_train).flatten()

val_predictions = model.predict(X_val).flatten()

test_predictions = model.predict(X_test).flatten()
print(train_predictions)
print(test_predictions)
print(val_predictions)
'''