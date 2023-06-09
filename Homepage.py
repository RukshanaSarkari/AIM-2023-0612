import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="AD-ARM Visualization",
    page_icon=":globe_with_meridians:",
    layout="wide",
    # initial_sidebar_state="expanded",
    menu_items={
        'About': "# AD-ARM Visualization Tool."
    }
)

# Initialize session state variables
if "df" not in st.session_state:
    st.session_state["df"] = None

if "df_filtered" not in st.session_state:
    st.session_state["df_filtered"] = None

if "vars" not in st.session_state:
    st.session_state["vars"] = None

if "data_dir" not in st.session_state:
    st.session_state["data_dir"] = "data\\imported_csv_files"

# ----------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------
with st.sidebar:
    st.write("Add a homepage sidebar if desired")

# ----------------------------------------------------------------
# Main Page
# ----------------------------------------------------------------

st.title("AD-ARM Visualization Tool")
# st.write("---")

st.write("Add a description of the app and perhaps an image")

with st.expander("Start New Session"):
    new_session_cols = st.columns([4, 1], gap="small")

    with new_session_cols[0]:
        new_session_name = st.text_input("Session Name:")

    with new_session_cols[1]:
        st.write(" ")  # Added for vertical space
        st.write(" ")  #
        new_session_save_button = st.button("SAVE")

with st.expander("Load Saved Session"):
    st.write("Add this later")

st.write("---")

import_button = st.button("Data ➡")
if import_button:
    switch_page("Data")