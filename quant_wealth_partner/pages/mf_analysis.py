import streamlit as st
from utilities.mutualfund import mf_data


st.subheader("Mutual Fund Analysis")
st.divider()

mf_info = mf_data.get_mf_info()
mf_info_len = len(mf_info.get("mf_selection_parameters", []))

if st.session_state.get("mf_category_subcategory_df") is None:
    st.session_state["mf_category_subcategory_df"] = mf_data.get_amfi_category_subcategory()
amfi_category_subcategory_df = st.session_state["mf_category_subcategory_df"]

if st.session_state.get("amfi_mutual_fund_id") is None:
    st.session_state["amfi_mutual_fund_id"] = mf_data.get_amfi_mutual_fund_id()
amfi_mutual_fund_id = st.session_state["amfi_mutual_fund_id"]

if st.session_state.get("amfi_fund_performance_df") is None:
    st.session_state["amfi_fund_performance_df"] = mf_data.get_amfi_fund_performance()
amfi_fund_performance_df = st.session_state["amfi_fund_performance_df"]

if st.session_state.get("amfi_all_mutual_fund_schemes_df") is None:
    st.session_state["amfi_all_mutual_fund_schemes_df"] = mf_data.get_amfi_all_mutual_fund_schemes()
    st.toast("Data fetched successfully!", icon="✅")
amfi_all_mutual_fund_schemes_df = st.session_state["amfi_all_mutual_fund_schemes_df"]

# st.dataframe(amfi_category_subcategory_df)
# st.dataframe(amfi_mutual_fund_id)
# st.dataframe(amfi_fund_performance_df)
# st.dataframe(amfi_all_mutual_fund_schemes_df)

tab1, tab2, tab3 = st.tabs(["Basic Info", "MF Categories", "MF Performance"]) 
with tab1:
    # rows = [st.columns(3) for _ in range(int(mf_info_len / 3) + 1)]
    # all_columns = [col for row in rows for col in row]
    # for col, (key, val) in zip(all_columns, mf_info.get("mf_selection_parameters", {}).items()):
    

    # cols = st.columns(3)
    # for i, item in enumerate(mf_info.get("mf_selection_parameters", [])):
    #     # Select the column based on index (loops back if more than 3 items)
    #     with cols[i % 3].container(height=350):
    #         st.markdown(f"### 📘 {item['parameter']}")
            
    #         # Display description if it exists
    #         if item['description']:
    #             st.caption(item['description'][:200] + "...") # Truncated for UI consistency
                
    #         # Display first importance point as a highlight
    #         if item['importances']:
    #             st.info(item['importances'][0])
                
    #         # Link to source
    #         if item['source_urls']:
    #             st.link_button("View Source", item['source_urls'][0])

    st.subheader("Basic Information")
    cols = st.columns(2, border=True)
    for i, item in enumerate(mf_info.get("mf_selection_parameters", [])):
        with cols[i % 2].container():
            st.markdown(f"### 📘 {item['parameter']}")
            st.markdown("**Description:**")
            st.markdown(item["description"])
            st.markdown("**Key Importance:**")
            if item["importances"]:
                st.markdown(f"- {item['importances'][0]}")  # Highlight the first importance point
            st.markdown(f"**Source:** {item['source_urls'][0] if item['source_urls'] else 'N/A'}")

    # for item in mf_info.get("mf_selection_parameters"):
    #     # Create a clickable card for each concept
    #     with st.expander(f"📘 {item['parameter']}"):
    #         st.markdown("**Description:**")
    #         st.markdown(item["description"])
    #         # Render the list as clean bullet points
    #         for importance in item["importances"]:
    #             st.markdown(f"- {importance}")
    #         st.markdown(f"**Source:** {item["source_urls"]}")

with tab2:
    st.subheader("Mutual Fund Categories and Subcategories")
    st.link_button(label="View AMFI Website", 
                   url="https://www.amfiindia.com/investor/knowledge-center-info?zoneName=CategorizationOfMutualFundSchemes",
                   icon="🔗",
                   type="secondary",
                   help="Click to visit the AMFI website for more details on mutual fund categories and subcategories.")
    st.dataframe(amfi_category_subcategory_df.loc[:, ["category_name", "sub_category_name"]]
                 .rename(columns={"category_name": "Category", "sub_category_name": "Sub-Category"}))
    
with tab3:
    st.subheader("Mutual Fund Performance Analysis")
    st.markdown("This section will provide insights into the performance of various mutual funds based on historical data, risk metrics, and other relevant factors. Stay tuned for detailed analysis and visualizations to help you make informed investment decisions.")
    # st.dataframe(amfi_fund_performance_df)
    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        mf_category = st.selectbox("Select Mutual Fund Category", options=amfi_category_subcategory_df["category_name"].unique())
        mf_category_int = int(amfi_category_subcategory_df[amfi_category_subcategory_df["category_name"] == mf_category]["category_id"].iloc[0])
    with col2:
        mf_sub_category = st.selectbox("Select Mutual Fund Sub-Category", options=amfi_category_subcategory_df[amfi_category_subcategory_df["category_name"] == mf_category]["sub_category_name"].unique())
        mf_sub_category_int = int(amfi_category_subcategory_df[(amfi_category_subcategory_df["category_name"] == mf_category) & (amfi_category_subcategory_df["sub_category_name"] == mf_sub_category)]["sub_category_id"].iloc[0])
    st.write(f"You selected: **{mf_category}({mf_category_int})** > **{mf_sub_category}({mf_sub_category_int})**")
    filtered_amfi_fund_performance_df = mf_data.get_amfi_fund_performance(maturityType=1, # Open ended funds
                                                category=mf_category_int, # pass int instead of name
                                                subCategory=mf_sub_category_int, 
                                                mfid=0, 
                                                reportDate="27-Mar-2026")
    # st.write("sample_df:")
    # st.dataframe(sample_df)
    
    st.dataframe(filtered_amfi_fund_performance_df.loc[:, ['schemeName', 'preNavDate', 'preNavRegular', 'preNavDirect', 'benchmark', 'navDate', 'navRegular', 'navDirect', 'dailyAUM', 'return1YearRegular', 'return1YearDirect', 'return3YearRegular', 'return3YearDirect', 'return5YearRegular', 'return5YearDirect']])


st.caption("Note: The above information is sourced from the AMFI website and may be subject to change. Please refer to the official AMFI website for the most up-to-date information.")


