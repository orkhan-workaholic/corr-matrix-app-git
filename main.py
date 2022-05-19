import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


st.write("""
# Correlation Matrix Builder

This app provides correlation matrix as dataframe, its heatmap and the most important correlations!
""")
st.sidebar.header('1. Upload File')



uploaded_file = st.sidebar.file_uploader(label='Upload your CSV or Excel file.',
                         type=['csv', 'xlsx'])


if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        print('CSV file is uploaded')
    except Exception as e:
        df = pd.read_excel(uploaded_file)
        print('Excel file is uploaded')

    except Exception as e:
        st.write('Please upload file to the application.')


#Title of dashboard
# st.title("Corr")

###############################################################################
# @st.cache
def load_data():
    # taking numerical columns and averaging their missing values
    df_raw = df.copy()
    all_cols = df.columns

    numerical_columns = []
    for column in df.columns:
      if column in df.columns[df.dtypes == "float"] | df.columns[df.dtypes == "int"]:
        numerical_columns.append(column)

    for i in numerical_columns:
      df[i] = df[i].fillna(df[i].mean())

    # taking columns with string values and lowercasing them and their values
    # df.columns = df.columns.str.lower()

    string_columns = []
    for column in df.columns:
      if column in df.columns[df.dtypes == "object"]:
        string_columns.append(column)

#    for i in string_columns:
#      df[i] = df[i].str.lower()

    df_clean = df.copy()

    return df, df_raw, all_cols, df_clean


# def feat_selection_function(df, all_cols):
#     feature_selection = st.sidebar.multiselect(label="Attributes to include to correlation matrix",
#                                            options=all_cols)
#     selected_cols = []
#     for i in df.columns:
#         if i in feature_selection:
#             selected_cols.append(i)
#     return selected_cols





if uploaded_file:
    df, df_raw, all_cols, df_clean = load_data()

    ######################################################
    st.sidebar.header('2. Display datasets')

    check_box = st.sidebar.checkbox(label="Display loaded dataset", value=True)
    #
    if check_box:
        st.write('### Loaded dataset:')
        st.write(df_raw)

    check_box2 = st.sidebar.checkbox(label="Display clean dataset")
    #
    if check_box2:
        st.write("""
        ### Dataset after cleaning
        Dataset cleaning includes:
        - detecting categorical columns lowercasing all the values of the columns as the correlation matrix is case sensitive;
        - detecting numerical columns and filling their missing values by their averages.
        """)
        st.write(df_clean)

    #give sidebar a title
    st.sidebar.header("3. Adjustment")





    feature_selection = st.sidebar.multiselect(label="Attributes to include to correlation matrix",
                                           options=all_cols)
    if feature_selection:
        selected_cols = []
        for i in df.columns:
            if i in feature_selection:
                selected_cols.append(i)
    #
    # except Exception:
    #     st.error('Please select attributes to see correlation')

        selected_df = df.loc[:, selected_cols]
        selected_df_with_dummmies = pd.get_dummies(selected_df)
        corr_matrix = selected_df_with_dummmies.corr()

        st.write("""
        ## Correlation Matrix
        \n The lighter the color is, the stronger the correlation is. Darker colors mean little to zero correlation!
        Blue colors depict negative, orange colors depict positive correlation.
        \n Include more attribute to the correlation matrix from the sidebar on the left handside.
        """)
        check_box_corr_plot = st.sidebar.checkbox(label="Display plot of correlation matrix")
        #
        if check_box_corr_plot:
        # if len(corr_matrix.columns) < 50:
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
#             else:
#                 st.error("Your corr_matrix includes " + str(len(corr_matrix.columns)) + "criteria which is more than the accepted level: 50")


        ###############################################################################


        st.sidebar.header("4. Top correlations with sentences")
        check_box3 = st.sidebar.checkbox(label="Show highly correlated attributes")
        #
        if check_box3:
          treshold = st.sidebar.slider('Change correlation range to show highly correlated attributes.', 0.0, 1.0, 0.3)
          list_of_corr = []

          for colname in corr_matrix.columns:
              for num, value in enumerate(corr_matrix[colname]):
                  if abs(value) > treshold and value < 1:
                      if value > 0:
                          list_of_corr.append(str(abs(
                              round(value, 2))) + ' of positive (+) correlation detected between ' + colname + ' and ' +
                                              corr_matrix.columns[num])
                      elif value < 0:
                          list_of_corr.append(str(abs(
                              round(value, 2))) + ' of negative (-) correlation detected between ' + colname + ' and ' +
                                              corr_matrix.columns[num])

          top_corr_sentence = sorted(list_of_corr, reverse=True)
          top_corr_sentence = pd.DataFrame(top_corr_sentence)
          st.write('### Top correlated attributes:')
          st.table(top_corr_sentence)
        else:
            st.error('Show highly correlated sentences by ticking from the left handside')
    else:
        st.error('Select attributes to create correlation matrix')
else:
    st.error('Upload a file from left handside')
