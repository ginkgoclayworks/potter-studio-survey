# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# results.py
# Results Dashboard Orchestrator
# Manages data loading and coordinates free/premium views
# """

# import streamlit as st
# import pandas as pd
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# from results_free import show_free_charts, derive_kpis
# # from results_premium import show_premium_charts

# # Initialize premium state
# # if 'premium' not in st.session_state:
# #     st.session_state.premium = False

# @st.cache_data(ttl=900)  # Cache for 15 minutes

# def load_responses():
#     """Load survey responses from Google Sheets and normalize row widths."""
#     try:
#         credentials = service_account.Credentials.from_service_account_info(
#             st.secrets["gcp_service_account"],
#             scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
#         )
#         service = build('sheets', 'v4', credentials=credentials)
#         sheet_id = st.secrets["sheet_id"]

#         result = service.spreadsheets().values().get(
#             spreadsheetId=sheet_id,
#             range="Sheet1"
#         ).execute()

#         values = result.get("values", [])
#         if not values or len(values) < 2:
#             return pd.DataFrame()

#         header = values[0]
#         width = len(header)

#         # Google Sheets omits trailing blanks per row; pad/trim to header width
#         normalized = []
#         for row in values[1:]:
#             row = list(row)
#             if len(row) < width:
#                 row += [""] * (width - len(row))
#             elif len(row) > width:
#                 row = row[:width]
#             normalized.append(row)

#         df = pd.DataFrame(normalized, columns=header)
#         return df

#     except Exception as e:
#         st.error(f"Failed to load survey data: {e}")
#         return pd.DataFrame()

# def render_results():
#     """Main results dashboard rendering function"""
    
#     st.title("Pottery Studio Survey Results")
    
#     # Load data
#     with st.spinner("Loading survey responses..."):
#         df = load_responses()
    
#     if df.empty:
#         st.warning("No survey responses available yet. Be the first to submit!")
#         if st.button("Take the Survey"):
#             st.session_state.page = 'survey'
#             st.rerun()
#         return
    
#     # Derive KPIs
#     df = derive_kpis(df)
    
#     st.success(f"Loaded {len(df)} survey responses")
    
#     # Show refresh button
#     col1, col2 = st.columns([3, 1])
#     with col2:
#         if st.button("Refresh Data"):
#             st.cache_data.clear()
#             st.rerun()
    
#     st.markdown("---")
    
#     # Free tier visualizations
#     show_free_charts(df)
    
#     st.markdown("---")
  
#     # # --- Support / Donate (Premium disabled) ---
#     # st.subheader("Support this project")
#     # st.caption("If you’ve found these insights useful, you can chip in to help cover hosting and development.")
#     # donate_url = st.secrets.get("donate_url", "")
#     # col1, col2, col3 = st.columns([1, 1, 1])
#     # with col2:
#     #     if donate_url:
#     #         # Streamlit >=1.31 supports link_button; falls back to markdown link if not available
#     #         try:
#     #             st.link_button("Buy me a chai ☕ ($3)", donate_url, use_container_width=True)
#     #         except Exception:
#     #             st.markdown(
#     #                 f'<a target="_blank" href="{donate_url}" class="stButton"><button>Buy me a chai ☕ ($3)</button></a>',
#     #                 unsafe_allow_html=True
#     #             )
#     #     else:
#     #         if st.button("Buy me a chai ☕ ($3)", type="primary", use_container_width=True):
#     #             st.info(
#     #                 "Add `donate_url` to your Streamlit secrets to redirect this button to Stripe/PayPal/etc.\n\n"
#     #                 "Example in `.streamlit/secrets.toml`:\n\n"
#     #                 'donate_url = "https://your-payment-link.example"'
#     #             )
                
# if __name__ == "__main__":
#     render_results()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
results.py
Results Dashboard Orchestrator
Manages data loading and coordinates free/premium views
"""

import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build

from results_free import show_free_charts, derive_kpis

@st.cache_data(ttl=900)  # Cache for 15 minutes
def load_responses():
    """Load survey responses from Google Sheets and normalize row widths."""
    try:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
        )
        service = build('sheets', 'v4', credentials=credentials)
        sheet_id = st.secrets["sheet_id"]

        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range="Sheet1"
        ).execute()

        values = result.get("values", [])
        if not values or len(values) < 2:
            return pd.DataFrame()

        header = values[0]
        width = len(header)

        # Google Sheets omits trailing blanks per row; pad/trim to header width
        normalized = []
        for row in values[1:]:
            row = list(row)
            if len(row) < width:
                row += [""] * (width - len(row))
            elif len(row) > width:
                row = row[:width]
            normalized.append(row)

        df = pd.DataFrame(normalized, columns=header)
        return df

    except Exception as e:
        st.error(f"Failed to load survey data: {e}")
        return pd.DataFrame()

def render_results():
    """Main results dashboard rendering function"""
    
    st.title("Pottery Studio Survey Results")
    
    # Load data
    with st.spinner("Loading survey responses..."):
        df = load_responses()
    
    if df.empty:
        st.warning("No survey responses available yet. Be the first to submit!")
        if st.button("Take the Survey"):
            st.session_state.page = 'survey'
            st.rerun()
        return
    
    # Derive KPIs
    df = derive_kpis(df)
    
    st.success(f"Loaded {len(df)} survey responses")
    
    # Show refresh button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    
    # Free tier visualizations
    show_free_charts(df)
    
    st.markdown("---")
                
if __name__ == "__main__":
    render_results()