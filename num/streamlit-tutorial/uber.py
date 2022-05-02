import streamlit as st
import pandas as pd
import numpy as np
import random

from datetime import datetime, timedelta

st.title("Uber pickups in Poznan")

@st.cache
def generate_data(n_rows: int = 100) -> pd.DataFrame:
    end = datetime.now()
    start = end - timedelta(days=100)

    dates = [
        random.random() * (end - start) + start
        for _ in range(n_rows)
    ]

    lat = np.random.uniform(52.36, 52.46, n_rows)
    lon = np.random.uniform(16.85, 17.00, n_rows)

    return pd.DataFrame({
        'date': dates,
        'lat': lat,
        'lon': lon
    })


n_rows = st.number_input(
    label='How many points to generate?',
    min_value=1,
    max_value=100000,
    value=1000,
    step=100
)

data = generate_data(n_rows=n_rows)

if st.checkbox("Show raw data?"):
    st.subheader("Raw data")
    st.dataframe(data)

hist_vals = np.histogram(data.date.dt.hour, bins=24)[0]
st.bar_chart(hist_vals)

# hour_filter = st.slider("hour", 0, 23, 17)
# df_filtered = data[data.date.dt.hour == hour_filter]

min_hour, max_hour = st.select_slider(
    label='hours',
    options=range(24),
    value=(7,16))

filter_idx = (data.date.dt.hour >= min_hour) & (data.date.dt.hour <= max_hour)
df_filtered = data[filter_idx]

st.map(df_filtered)
