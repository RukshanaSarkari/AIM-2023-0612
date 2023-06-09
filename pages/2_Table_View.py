import streamlit as st
import pandas as pd
from kernel import app_utils
import numpy as np
import matplotlib.pyplot as plt
from kernel import data_utils as du
import plotly.express as px

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------
# ----------------------------------------------------------------
with st.sidebar:
    st.write("Table View Sidebar")

    if "csv_df" in st.session_state:

        csv_path = st.session_state["data_dir"]
        csv_files = st.session_state["csv_df"]["CSV collection"]
        selected_csv = st.selectbox("Select CSV:", csv_files)

        # Load the DataFrame
        loaded_df = du.load_csv(f"{csv_path}\\{selected_csv}")
        loaded_df.reset_index(inplace=True)

        st.session_state["df"] = loaded_df

# ----------------------------------------------------------------
# Main Page
# ----------------------------------------------------------------

if loaded_df is not None:

    tbl = loaded_df
    if not (tbl is None):
        df_head_tab, df_stats_tab, df_full_tab, var_tab = st.tabs(
            ["head", "statistics", "full table", "variables"]
        )

        with df_head_tab:
            st.dataframe(tbl.head())

        with df_stats_tab:
            st.dataframe(tbl.describe())

        with df_full_tab:
            st.dataframe(tbl)

        with var_tab:

            var_col, info_col = st.columns([1, 2])

            with var_col:
                var_sel = st.radio("Variables:", tbl.columns, label_visibility="hidden")

            with info_col:
                var_count_tbl = pd.DataFrame(tbl[var_sel].value_counts())
                var_count_tbl.reset_index(inplace=True)
                var_count_tbl.columns = [var_sel, "count"]
                var_count_tbl.sort_values(by=[var_sel], inplace=True)

                fig = px.pie(var_count_tbl,
                             values="count",
                             names=var_sel,
                             title=f'{var_sel}',
                             # height=300, width=200,
                             )
                # fig.update_layout(margin=dict(l=20, r=20, t=30, b=0), )
                st.plotly_chart(fig, use_container_width=True)

#
#
#
# if data_files:
#
#     data_file_df = pd.DataFrame(columns=["csv file collection", ""])
#     data_file_df.loc[:, "csv file collection"] = data_files
#     # Display CSVs in a data edit table
#     st.data_editor(data_file_df, hide_index=True)
#
#     st.button("Delete Selected")
#
# selected_file = st.selectbox("Select a .csv file:", data_files)
# else:
#     st.warning("Directory not found.")
#     selected_file = None
#
# if selected_file:
#     file_path = os.path.join(data_dir, selected_file)
#     st.session_state["file_name"] = selected_file
#
#     # Load the csv data
#     return load_csv(file_path)
#
#
#
#
# st.session_state["df"] = dm.process_data_folder()
# st.session_state["vars"] = list(st.session_state["df"].columns)
#
# tbl = st.session_state["df"]
# if not (tbl is None):
#     df_head_tab, df_stats_tab, df_full_tab, var_tab = st.tabs(
#         ["head", "statistics", "full table", "variables"]
#     )
#
#     with df_head_tab:
#         st.dataframe(tbl.head())
#
#     with df_stats_tab:
#         st.dataframe(tbl.describe())
#
#     with df_full_tab:
#         st.dataframe(tbl)
#
#     with var_tab:
#
#         var_col, info_col = st.columns([1, 2])
#
#         with var_col:
#             var_sel = st.radio("Variables:", tbl.columns, label_visibility="hidden")
#
#         with info_col:
#             var_count_tbl = pd.DataFrame(tbl[var_sel].value_counts())
#             var_count_tbl.reset_index(inplace=True)
#             var_count_tbl.columns = [var_sel, "count"]
#             var_count_tbl.sort_values(by=[var_sel], inplace=True)
#
#             fig = px.pie(var_count_tbl,
#                          values="count",
#                          names=var_sel,
#                          title=f'{var_sel}',
#                          # height=300, width=200,
#                          )
#             # fig.update_layout(margin=dict(l=20, r=20, t=30, b=0), )
#             st.plotly_chart(fig, use_container_width=True)


st.write("---")

if not ("df" in st.session_state):
    st.warning("No data found. Please import data.")

elif st.session_state["df"] is None:
    st.warning("Empty data table.")

else:

    tbl = st.session_state["df"]

    selected = [False] * len(tbl.columns)
    var2 = list(tbl.columns)
    var_df = pd.DataFrame(data=zip(selected, var2), columns=["Selection", "Variables"])

    st.data_editor(
        var_df,
        column_config={
            "Selection": st.column_config.CheckboxColumn(
                "",
                help="Select your",
                default=False,
            )
        },
        key="var_picker",
        disabled=["Variables"],
        hide_index=True,
        height=37 + 35 * len(tbl.columns),
    )

    if "var_picker" in st.session_state:
        edited_rows = st.session_state["var_picker"]["edited_rows"]
        for k, v in edited_rows.items():
            selected[k] = v["Selection"]

    selected_vars = var_df.loc[selected, "Variables"]

    if len(selected_vars) > 0:
        st.header("Selected Variable Metadata")

        filtered_tbl = st.session_state["df"].loc[:, selected]

        val_cts = filtered_tbl.value_counts()

        # val_cts["count"] = filtered_tbl.value_counts()
        # val_cts = val_cts.reset_index()
        # val_cts = val_cts.rename(columns={0: "count"})
        st.write(val_cts)

        # fig, ax = plt.subplots()
        # ax.hist(filtered_tbl.value_counts(), bins=20)
        # st.pyplot(fig)
        # st.bar_chart(val_cts)

        # initialize the variable info dataframe
        var_info_df = pd.DataFrame(columns=["name", "count", "type"])

        # initialize the metadata array
        columns = []

        if not filtered_tbl.empty:

            # Detect the categorical and numerical columns
            numeric_cols = filtered_tbl.select_dtypes(include=np.number).columns.tolist()
            categorical_cols = list(set(list(filtered_tbl.columns)) - set(numeric_cols))

            # get the numerical and categorical columns
            columns = du.generate_meta_data(filtered_tbl)

            # convert the column information into a dataframe
            columns_df = pd.DataFrame(columns, columns=['column_name', 'type'])

            # save the metadata as a csv
            columns_df.to_csv('data/metadata/column_type_desc.csv', index=False)

            # update the variable information table
            for i in range(columns_df.shape[0]):
                col_name = columns_df.iloc[i]['column_name']
                var_info_df.loc[i, "name"] = col_name
                var_info_df.loc[i, "count"] = len(filtered_tbl.loc[:, col_name].unique())
                var_info_df.loc[i, "type"] = columns_df.iloc[i]['type']
                # var_info_df.loc[i, "unique values"] = set(filtered_tbl.loc[:, col_name])

            # display the variable information
            st.dataframe(var_info_df, hide_index=True)

            st.write(du.compute_metadata(filtered_tbl))

            # st.write(du.compute_variable_importance(filtered_tbl, col_name))

            st.header("Show redundant variables?")

            red_cols = du.get_redundant_columns
            corr = filtered_tbl.corr(method='pearson')
            y_var = st.radio("Select the variable to be predicted (y)", options=corr.columns)
            th = st.slider("Correlation Threshold", min_value=0.05, max_value=0.95, value=0.25, step=0.01,
                           format='%f')  # , key=None, help=None)

            redundant_cols = pd.Series(du.get_redundant_columns(corr, y_var, th), name="Redundant Variables")
            new_df = du.new_df(filtered_tbl, redundant_cols)
            st.write("Redundant Variables:", redundant_cols)
            st.write("Number of Columns Dropped: ", len(redundant_cols))
            st.write("New Data: \n", new_df.head())

            st.session_state["df_filtered"] = filtered_tbl

# ----------------------------------------------------------------
# Navigation Button Section

# data_sel_button = st.button("Data Selection ➡")
# if data_sel_button:
#     switch_page("Data_Selection")