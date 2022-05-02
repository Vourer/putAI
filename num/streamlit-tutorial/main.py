import streamlit as st
import pandas as pd
import lorem
import time


st.title('Hello world app')
st.header('This is my first Streamlit app')

_str = 'Hello, universe!'
st.write(_str)

url = 'https://gist.githubusercontent.com/balmasi/0e65f72c48f2a3498ceb36ffc216f5eb/raw/fa71405126017e6a37bea592440b4bee94bf7b9e/titanic.csv'
df = pd.read_csv(url)

display_sex = st.sidebar.selectbox('Select sex to display', df.Sex.unique())
st.dataframe(df[df.Sex == display_sex])

cols = ["Name", "Sex", "Age"]
df_multi = st.multiselect("Columns", df.columns.tolist(), default=cols)
st.dataframe(df[df_multi])

if st.sidebar.checkbox("Show age distribution?"):
    age_distribution = df.Age.dropna().value_counts()
    st.bar_chart(age_distribution)

left, right = st.columns(2)
btn_clicked = left.button("Click me!")

if btn_clicked:
    right.write("Thank you!")

expander = st.expander("Lorem ipsum")
expander.write(lorem.paragraph())

# current_iter = st.empty()
# progress_bar = st.progress(0)
#
# for i, _ in enumerate(range(100)):
#     current_iter.text(f'Iteration {i+1}')
#     progress_bar.progress(i+1)
#     time.sleep(0.1)
