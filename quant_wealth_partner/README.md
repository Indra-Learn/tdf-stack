# Quant Wealth Partner

This site is dedicated to MFD professionals and Individual Investors, who can do their own market-research and start/continue their wealth creation journey smartly.

# How To Use This Repo:

## Setup the workspace:
1. Create a folder and open it in VS code.
    ```sh
    mkdir quant_wealth_partner
    cd quant_wealth_partner
    ```
2. Create & activate python virtual environment and install Python dependencies (One-Time Activity):
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate

    pip install --upgrade pip
    pip install -r requirements.txt
    ```
3. Run the app:
    ```sh
    <!-- streamlit run quant_wealth_partner/streamlit_app.py -->
    streamlit run streamlit_app.py 
    ```