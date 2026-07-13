import streamlit as st

st.set_page_config(layout="wide")

if "role" not in st.session_state:
    st.session_state.role = None

ROLES = [None, "Researcher", "Admin"]

def login():
    st.header("Log In")
    role = st.selectbox("Select your role", ROLES)
    if st.button("Log In"):
        st.session_state.role = role
        st.rerun()

def logout():
    st.session_state.role = None
    st.rerun()

role = st.session_state.role

logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
mfd_home = st.Page("pages/mf_home.py", title="Home", icon="🏠")
settings_page = st.Page("pages/settings.py", title="Settings", icon=":material/settings:")
market_research_page = st.Page("pages/market_research.py", title="Research Tools", icon="🔍")
financial_knowledge_base_page = st.Page("pages/financial_knowledge_base.py", title="Financial Knowledge Base", icon="📚")
data_api_page = st.Page("pages/data_api.py", title="Data Api", icon="🌐")
mf_analysis_page = st.Page("pages/mf_analysis.py", title="Mutual Fund Analysis", icon="📊")
etf_analysis_page = st.Page("pages/etf_analysis.py", title="ETF Analysis", icon="📊")
pricing_page = st.Page("pages/pricing.py", title="Pricing", icon="💰")
documents_page = st.Page("pages/documents.py", title="Documents", icon="📄")
blogs_page = st.Page("pages/blogs.py", title="Blogs", icon="📝")
admin_page = st.Page("pages/admin.py", title="Admin Dashboard", icon="🦸‍♂️")

account_pages = [mfd_home, settings_page, logout_page]
product_pages = [market_research_page, data_api_page]
solution_pages = [financial_knowledge_base_page, mf_analysis_page, etf_analysis_page]
price_pages = [pricing_page]
resource_pages = [documents_page, blogs_page]
admin_pages = [admin_page]

# st.header("Quant Wealth Partner")
# st.divider(width="stretch")
# st.logo("static/images/logo.png", icon_image="static/images/icon.png", link="")

top_nav_pages = {}
if st.session_state.role in ["Researcher", "Admin"]:
    top_nav_pages["Products"] = product_pages
    top_nav_pages["Solutions"] = solution_pages
    top_nav_pages["Pricing"] = price_pages
    top_nav_pages["Resources"] = resource_pages
if st.session_state.role == "Admin":
    top_nav_pages["Admin"] = admin_pages

if len(top_nav_pages) > 0:
    top_nav_pg = st.navigation({"Account": account_pages} | top_nav_pages, position="top")
else:
    top_nav_pg = st.navigation([st.Page(login)])

top_nav_pg.run()