import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def remove_duplicates(column):
    unique_values = column.unique()
    st.write("Original values:", column.tolist())
    st.write("Unique values:", unique_values.tolist())


def plot_histogram(column, selected_elements):
    filtered_column = column[column.isin(selected_elements)]
    plt.hist(filtered_column, bins='auto', alpha=0.7)
    plt.xlabel('Values')
    plt.ylabel('Frequency')
    plt.title('Histogram Analysis')
    st.pyplot(plt)

df_csv = st.session_state["csv_df"]
dir = st.session_state['data_dir']

# File upload
selected_file = st.selectbox(
    'Select a Data Set',
    df_csv.loc[:, 'CSV collection']
)

def main():
    st.title("Histogram Analysis")

    if selected_file is not None:
        df = pd.read_csv(selected_file)

        # Show the uploaded dataframe
        st.subheader("Uploaded DataFrame")
        st.write(df)

        # Column selection for duplicate removal
        duplicate_column = st.selectbox("Select a column to remove duplicates", options=["None"] + df.columns.tolist())


        if st.button("Remove Duplicates"):
            if duplicate_column != "None":
                column = df[duplicate_column]
                remove_duplicates(column)
            else:
                st.write("No column selected for duplicate removal.")

        # Column selection for histogram analysis
        selected_columns = st.multiselect("Select columns for histogram analysis", options=df.columns)

        if selected_columns:
            selected_elements = []
            for column in selected_columns:
                st.write(f"Selected elements for {column}:")
                elements = st.multiselect(f"Select elements from {column}", options=df[column].unique())
                selected_elements.extend(elements)
                st.write(f"Selected elements for {column}:", selected_elements)
                plot_histogram(df[column], selected_elements)


if __name__ == "__main__":
    main()