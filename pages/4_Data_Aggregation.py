import pandas as pd
import streamlit as st
import altair as alt
from kernel import data_utils as du

# ----------------------------------------------------------------
# ----------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------
# ----------------------------------------------------------------
with st.sidebar:
    st.write("Aggregation Sidebar")

    if "csv_df" in st.session_state:

        csv_path = st.session_state["data_dir"]
        csv_files = st.session_state["csv_df"]["CSV collection"]
        selected_csv = st.selectbox("Select CSV:", csv_files)

        # Load the DataFrame
        loaded_df = du.load_csv(f"{csv_path}\\{selected_csv}")
        loaded_df.reset_index(inplace=True)

        st.session_state["df"] = loaded_df


# ----------------------------------------------------------------
# ----------------------------------------------------------------
# Main Page
# ----------------------------------------------------------------
# ----------------------------------------------------------------
st.title("Data Aggregation")
st.write("---")

if loaded_df is not None:

    df = loaded_df

    col1, col2, col3 = st.columns([2, 1, 2])

    with col1:
        col_sel = st.multiselect("For each value in ", df.columns)

    with col2:

        agg_type_sel = st.selectbox(
            "compute the ",
            ["count", "average", "sum", "min", "max"]
        )

    with col3:

        agg_target_sel = st.multiselect(
            "of ",
            df.columns
        )

    if col_sel and agg_type_sel and agg_target_sel:
        new_df = df.loc[:, col_sel + agg_target_sel]

        grouped_df = pd.DataFrame(columns=col_sel + agg_target_sel)

        if agg_type_sel == "count":
            grouped_df = new_df.groupby(col_sel).count()
        elif agg_type_sel == "average":
            grouped_df = new_df.groupby(col_sel).mean()
        elif agg_type_sel == "sum":
            grouped_df = new_df.groupby(col_sel).sum()
        elif agg_type_sel == "min":
            grouped_df = new_df.groupby(col_sel).min()
        elif agg_type_sel == "max":
            grouped_df = new_df.groupby(col_sel).max()

        grouped_df.reset_index(inplace=True)
        with st.expander("View Table"):
            st.dataframe(grouped_df)

        target_var = st.radio("select response", agg_target_sel, horizontal=True)

        # bar_chart1 = alt.Chart(grouped_df).mark_bar().encode(
        #     x="AircraftTypeName:O",
        #     y=f"{target_var}:Q",
        #     color="design_point",
        # )
        #
        # bar_chart2 = alt.Chart(grouped_df).mark_bar().encode(
        #     x=alt.X("design_point:O", axis=alt.Axis(labelAngle=0)),
        #     y=f"{target_var}:Q",
        #     color="AircraftTypeName",
        # )

        try:
            bar_chart = alt.Chart(grouped_df).mark_bar().encode(
                alt.Column(col_sel[0], header=alt.Header(titleColor="white", labelColor="white")),
                alt.X(col_sel[1], title=''),
                alt.Y(f"{target_var}", axis=alt.Axis(grid=True)),
                alt.Color(col_sel[1]),
            )

            st.altair_chart(bar_chart)
        except:
            st.warning("There was a problem generating this plot.")

else:
    st.warning("Empty data table.")