import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import openpyxl

st.write("""
# Correlation Matrix Builder

This app provides correlation matrix as dataframe, its heatmap and the most important correlations!
""")
st.sidebar.header('1. Upload File')

uploaded_file = st.sidebar.file_uploader(label='Upload your CSV or Excel file.',
                         type=['csv', 'xlsx'])

df = pd.read_csv(uploaded_file)
df_raw = df.copy()



##############################
df.columns = df.columns.str.lower()
all_cols = df.columns

string_columns = []
for column in df.columns:
  if column in df.columns[df.dtypes == "object"]:
    string_columns.append(column)

for i in string_columns:
    df[i] = df[i].str.lower()

##############################
numerical_columns = []
for column in df.columns:
    if column in df.columns[df.dtypes == "float"] | df.columns[df.dtypes == "int"]:
        numerical_columns.append(column)

for i in numerical_columns:
  df[i] = df[i].fillna(df[i].mean())
############################################
df_clean = df.copy()


if uploaded_file:
    st.write(df_raw)
    st.write(df_clean)

    feature_selection = st.sidebar.multiselect(label="Attributes to include to correlation matrix",
                                           options=all_cols)

    if feature_selection:
        selected_cols = []
        for i in df.columns:
            if i in feature_selection:
                selected_cols.append(i)

        selected_df = df.loc[:, selected_cols]
        selected_df_with_dummmies = pd.get_dummies(selected_df)
        corr_matrix = selected_df_with_dummmies.corr()

        fig, ax = plt.subplots(figsize=(25, 20))

        # create seaborn heatmap
        g = sns.heatmap(corr_matrix, annot=True, linewidths=.5, center=0)

        g.set_yticklabels(g.get_yticklabels(), rotation = 0, fontsize = 25)
        g.set_xticklabels(g.get_xticklabels(), rotation = 90, fontsize = 25)


        try:
            g;
            st.write(fig)

        except Exception as e:
            print(e)
            st.write('Please select attributes to see correlation.')
