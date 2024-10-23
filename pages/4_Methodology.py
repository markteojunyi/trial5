import streamlit as st  
import hmac  
from helper_function.stpassword import check_password  

if not check_password():  
    st.stop()

# Set the title of the Streamlit app
st.title("Methodology")

# Section for Buy HDB Flat App
st.markdown("**Buy HDB Flat**")

# Add space using HTML line break
st.markdown("<br>", unsafe_allow_html=True)

# Insert Image 1
st.image("Images/Methodology_BuyHDBFlat.png", caption="Buy HDB Flat app flowchart", use_column_width=True)

# Section for Resale Price App
st.markdown("**Resale Price App**")

# Add space using HTML line break
st.markdown("<br>", unsafe_allow_html=True)

# Insert Image 2
st.image("Images/Methodology_Resaleprice.png", caption="Resale Price App flowchart", use_column_width=True)
