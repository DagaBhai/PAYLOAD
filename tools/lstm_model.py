import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras import layers
from keras.optimizers import Adam

def df_to_windowed_df(df, first_date, last_date, n):
    dates = []
    X = []
    y = []

    for i in range(n, len(df)):
        if df.index[i] < first_date or df.index[i] > last_date:
            continue

        dates.append(df.index[i])
        X.append(df.iloc[i-n:i].values)
        y.append(df.iloc[i].values)

    return pd.DataFrame({
        'Date': dates,
        'X': X,
        'y': y
    })


def windowed_df_to_date_X_y(windowed_df):
    dates = windowed_df['Date'].values
    X = np.array(windowed_df['X'].tolist())
    y = np.array(windowed_df['y'].tolist())
    return dates, X, y


def predict_next_n_days(model, last_window, ndays):
    preds = []
    current_window = last_window.copy()

    for _ in range(ndays):
        pred = model.predict(
            current_window.reshape(1, *current_window.shape),
            verbose=0
        )[0, 0]

        preds.append(pred)
    
        current_window = np.vstack(
            [current_window[1:], [[pred]]]
        )

    return np.array(preds)


def fullmodel(data, n_days=20, window_size=3):

    if len(data) <= window_size:
        raise ValueError(
            f"Not enough data points ({len(data)}) "
            f"for window size {window_size}"
        )

    df = pd.DataFrame(data)
    df.index = pd.to_datetime(df.index)

    original_close = df[['Close']].copy()

    scaler = MinMaxScaler()
    df['Close'] = scaler.fit_transform(df[['Close']])
    df = df[['Close']]

    start_date = df.index[window_size]
    end_date = df.index[-1]

    windowed_df = df_to_windowed_df(
        df,
        first_date=start_date,
        last_date=end_date,
        n=window_size
    )

    if windowed_df.empty:
        raise ValueError("Windowed dataframe is empty")

    dates, X, y = windowed_df_to_date_X_y(windowed_df)

    model = Sequential([
        layers.Input((window_size, 1)),
        layers.LSTM(64),
        layers.Dense(32, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])

    model.compile(
        loss='mse',
        optimizer=Adam(learning_rate=0.001),
        metrics=['mean_absolute_error']
    )

    model.fit(X, y, epochs=100, verbose=0)

    last_window = X[-1]

    future_preds_scaled = predict_next_n_days(
        model,
        last_window,
        ndays=n_days
    )

    if len(future_preds_scaled) == 0:
        raise ValueError("No future predictions generated")

    future_preds = scaler.inverse_transform(
        future_preds_scaled.reshape(-1, 1)
    ).flatten()

    future_dates = pd.date_range(
        start=df.index[-1] + pd.Timedelta(days=1),
        periods=n_days,
        freq='B'
    )

    future_df = pd.DataFrame(
        {'Close': future_preds},
        index=future_dates
    )

    full_df = pd.concat([original_close, future_df])

    return full_df

