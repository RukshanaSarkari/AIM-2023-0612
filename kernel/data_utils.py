import os
import sqlite3
import streamlit as st
import pandas as pd


def rename_csv_files(old_files, new_files):
    for old, new in zip(old_files, new_files):
        os.rename(old, new)


def delete_csv_files(files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)


# Returns all files in "path" with the specified file extension "ext"
def get_files_in_folder(path=None, ext="csv"):
    if not os.path.exists(path):
        return None

    files = []
    for file in os.listdir(path):
        if file.endswith("." + ext):
            files.append(file)
    return files


# Returns all tables in a SQLite database specified by "db_path"
def get_tables_in_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    conn.close()
    return tables


@st.cache_data
def load_csv(file_path):
    return pd.read_csv(file_path)


def filter_table_columns():
    tbl = st.session_state["df"]
    cols = st.session_state["vars"]
    st.session_state["df"] = tbl.loc[:, cols]


def process_drag_drop(files):
    st.write(files)


def get_dataframe_info(df):
    df_types = pd.DataFrame(df.dtypes)
    df_nulls = df.count()

    df_null_count = pd.concat([df_types, df_nulls], axis=1)
    df_null_count = df_null_count.reset_index()

    # Reassign column names
    col_names = ["features", "types"]
    df_null_count.columns = col_names

    return df_null_count
