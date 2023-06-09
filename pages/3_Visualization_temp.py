import streamlit as st
import pandas as pd
from kernel import utils
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------
with st.sidebar:
    st.write("Visualization Sidebar")

# ----------------------------------------------------------------
# Main Page
# ----------------------------------------------------------------

st.title("Visualization")
st.write("---")

if "df_filtered" in st.session_state:

    # Chatgpt suggestion:

    # Load the DataFrame
    df = st.session_state["df_filtered"]

    st.dataframe(df)



    # Assuming the DataFrame is named 'df'
    # You should load your DataFrame here

    st.title('DataFrame GroupBy and Aggregation')

    # Select column to group by
    groupby_col = st.selectbox("GroupBy column", df.columns.tolist())

    # Select column to aggregate on
    aggregate_col = st.selectbox("Aggregate column", df.select_dtypes(include=['float64', 'int64']).columns.tolist())

    # Select aggregation operation
    aggregation = st.selectbox("Aggregation operation", ['sum', 'mean', 'count', 'min', 'max'])

    # Perform groupby and aggregation
    if st.button('Run Aggregation'):
        result_df = df.groupby(groupby_col)[aggregate_col].agg(aggregation)
        st.dataframe(result_df)


    #
    #
    # # Select visualization type
    # viz = st.selectbox("Visualization type", ['Histogram', 'Box plot', 'Bar chart', 'Heatmap'])
    #
    # if viz == 'Histogram':
    #     num_col = st.selectbox("Select column",
    #                            df.select_dtypes(include=['float64', 'int64', 'object']).columns.tolist())
    #     fig, ax = plt.subplots()
    #     # ax.hist(df[num_col], bins=20)
    #     st.bar_chart(df[num_col])
    #     # st.pyplot(fig)
    #
    # elif viz == 'Box plot':
    #     num_col = st.selectbox("Select column",
    #                            df.select_dtypes(include=['float64', 'int64']).columns.tolist())
    #     fig, ax = plt.subplots()
    #     ax.boxplot(df[num_col])
    #     st.pyplot(fig)
    #
    # elif viz == 'Bar chart':
    #     st.bar_chart(df)
    #     # cat_col = st.selectbox("Select column", df.select_dtypes(include=['object']).columns.tolist())
    #     # if cat_col is not None:
    #     #     fig, ax = plt.subplots()
    #     #     df[cat_col].value_counts().plot(kind='bar')
    #     #     st.pyplot(fig)
    #
    # elif viz == 'Heatmap':
    #     fig, ax = plt.subplots()
    #     sns.heatmap(df.corr(), annot=True, cmap='coolwarm', ax=ax)
    #     st.pyplot(fig)

    # df_analysis = st.session_state["df_filtered"]
    #
    # st.write(st.session_state['file_name'])
    #
    # if "Airbase" in st.session_state["file_name"]:
    #     df_analysis.columns = ["LAT", "LON"]
    #     st.map(df_analysis)
    #
    # # df_visual = pd.DataFrame(df_analysis)
    # df_visual = df_analysis.copy()
    # cols = pd.read_csv('data/metadata/column_type_desc.csv')
    # st.write(cols)
    # categorical, numerical, obj = utils.getColumnTypes(cols)
    # st.write("Here")
    # st.write(numerical)
    # cat_groups = {}
    # unique_category_val = {}
    #
    # for i in range(len(categorical)):
    #     if categorical[i] not in unique_category_val:
    #         unique_category_val[categorical[i]] = []
    #
    #     unique_category_val[categorical[i]] = utils.map_unique(df_analysis, categorical[i])
    #     # unique_category_val = {categorical[i]: utils.map_unique(df_analysis, categorical[i])}
    #
    #     if categorical[i] not in cat_groups:
    #         cat_groups[categorical[i]] = []
    #
    #     cat_groups[categorical[i]] = df_visual.groupby(categorical[i])
    #     # cat_groups = {categorical[i]: df_visual.groupby(categorical[i])}
    #
    # category = st.selectbox("Select Category ", categorical + obj)
    #
    # sizes = (df_visual[category].value_counts() / df_visual[category].count())
    #
    # labels = sizes.keys()
    #
    # max_index = np.argmax(np.array(sizes))
    # explode = [0] * len(labels)
    # explode[int(max_index)] = 0.1
    # explode = tuple(explode)
    #
    # fig1, ax1 = plt.subplots()
    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=0)
    # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # ax1.set_title('Distribution for categorical Column - ' + str(category))
    # st.pyplot(fig1)
    #
    # corr = df_analysis.corr(method='pearson')
    #
    # fig2, ax2 = plt.subplots()
    # # mask = np.zeros_like(corr, dtype=np.bool)
    # mask = np.full(corr.shape, True, dtype=bool)
    #
    # mask[np.triu_indices_from(mask)] = True
    # # Colors
    # cmap = sns.diverging_palette(240, 10, as_cmap=True)
    # sns.heatmap(corr, mask=mask, linewidths=.5, cmap=cmap, center=0, ax=ax2)
    # ax2.set_title("Correlation Matrix")
    # st.pyplot(fig2)
    #
    # category_object = st.selectbox("Select " + str(category), unique_category_val[category])
    # st.write(cat_groups[category].get_group(category_object).describe())
    # col_name = st.selectbox("Select Column ", numerical)
    #
    # try:
    #     st.bar_chart(cat_groups[category].get_group(category_object)[col_name])
    # except KeyError:
    #     st.warning("Something went wrong")

else:
    st.warning("Empty data table.")
