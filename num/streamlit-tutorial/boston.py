import streamlit as st
import pandas as pd
import numpy as np
from sklearn.datasets import load_boston
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt


st.title("Boston housing stuff")

boston = load_boston()
data = pd.DataFrame(data=boston.data, columns=boston.feature_names)
data['MEDV'] = boston.target

boston_expander = st.expander("Dataset description")
boston_expander.write(boston.DESCR)

st.sidebar.write("Filters")
display_rivers = st.sidebar.checkbox('House should be near river')

min_tax, max_tax = st.sidebar.select_slider(
    label='Taxes range',
    options=range(int(np.min(data.TAX)), int(np.max(data.TAX)+1)),
    value=(int(np.min(data.TAX)), int(np.max(data.TAX))))

columns_expander = st.sidebar.expander("Choose columns")
column_names = np.hstack([boston.feature_names[boston.feature_names != 'CHAS'], 'MEDV'])
data_multi = columns_expander.multiselect("Columns", data.columns.tolist(), default=column_names)

filter_idx = (data.TAX >= min_tax) & (data.TAX <= max_tax)
filtered = data[filter_idx]
river_data = filtered[filtered.CHAS == display_rivers]
st.dataframe(river_data[data_multi])

if st.checkbox("Pokaż rozkład średnich cen domów"):
    st.write("Rozkład średnich cen domów")

    fig, ax = plt.subplots()
    ax.hist(river_data.MEDV, bins=np.unique(river_data.MEDV//1), rwidth=0.8)
    plt.xlabel("Median value of house prices in thousands of dollars")
    st.pyplot(fig)
    # hist_costs = np.histogram(river_data.MEDV, bins='auto')[0]
    # st.bar_chart(hist_costs)

_str = 'Predict house price:'
st.write(_str)

decision_tree = DecisionTreeRegressor(splitter="best", max_depth=5)
decision_data = pd.DataFrame(data=boston.data, columns=boston.feature_names)
decision_data = decision_data[['AGE', 'CRIM', 'RM', 'TAX']]
decision_tree.fit(X=decision_data.values, y=boston.target)

with st.form(key='Price prediction'):
    age_input = st.number_input('Age:')
    crim_input = st.number_input('Crime rate:')
    rm_input = st.number_input('Number of rooms:')
    tax_input = st.number_input('Taxes:')

    submit_btn = st.form_submit_button('Predict price')

if submit_btn:
    inputs = np.array([age_input, crim_input, rm_input, tax_input]).reshape(1, -1)
    prediction = decision_tree.predict(inputs)
    st.write(f'Based on provided data, predicted house price (MEDV) is: {prediction}')
