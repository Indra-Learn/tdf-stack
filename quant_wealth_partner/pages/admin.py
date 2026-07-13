import streamlit as st
import pandas as pd
# from streamlit_gsheets import GSheetsConnection
from utilities.mutualfund import mf_data
from utilities.read_write_google_sheet import read_sheet_data, write_sheet_data


# gs_conn = st.connection("gsheets", type=GSheetsConnection)

st.subheader("⚙️ Source Data Refresh")

with st.sidebar:
    data_status = st.selectbox("See Status or Load Data", ("See Status", "Load Data"))

    if data_status == "Load Data":
        load_data_option = st.selectbox(
            "Load data for -",
            tuple(mf_data.get_mf_info().get("admin_page", {}).get("sidebar", {}).keys()),
        )

        load_type = st.radio(
            "Select options -",
            tuple(mf_data.get_mf_info().get("admin_page", {}).get("sidebar", {}).get(load_data_option, {}).keys()),
            horizontal=True
        )

if data_status == "See Status":
    st.info("Select 'Load Data' from the sidebar to load data.")

    # debug sidebar options
    # st.write(mf_data.get_mf_info().get("admin_page", {}).get("sidebar", {}))

    sheet_status_df = read_sheet_data("Sheets_Status")
    sheet_status_df["Select_to_Refresh"] = False  # Append the interaction column at the end (Default to False/Unchecked)
    edited_sheet_status_df = st.data_editor(sheet_status_df,
                                            column_config={
                                                "Select_to_Refresh": st.column_config.CheckboxColumn(
                                                    "🔄 Refresh?", 
                                                    help="Select the specific sheet to refresh from the API",
                                                    default=False
                                                )
                                            },
                                            disabled=["Sheet_Name", "Rows", "Columns", "Is_Automated"], # Lock the data columns
                                            hide_index=True,
                                            width='stretch'
                                        )
    
    st.divider()
    if st.button("🚀 Execute Selected Refreshes", type="primary"):
        # Extract only the rows where the user clicked the checkbox
        selected_rows = edited_sheet_status_df[edited_sheet_status_df["Select_to_Refresh"] == True]
        print(selected_rows)
        if selected_rows.empty:
            st.warning("⚠️ Please select at least one row to refresh.")
        else:
            st.info(f"Initiating parallel API calls for {len(selected_rows)} sheets...")
            target_sheets = selected_rows["Sheet_Name"].tolist()

            # function api call
            for sheet in target_sheets:
                with st.spinner("Writing to Google Sheets ({sheet})..."):
                    # Create a sample dataframe
                    new_data = pd.DataFrame({
                        "Asset_Class": ["Equity", "Debt", "Hybrid"],
                        "AUM_Cr": [5000, 3000, 1500]
                    })
                    success = write_sheet_data(sheet, new_data)
                    if success:
                        st.success(f"Successfully triggered refresh for: {sheet}")
            st.rerun()

            

    