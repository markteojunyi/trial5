import streamlit as st  
import hmac  
from helper_function.stpassword import check_password  

if not check_password():  
    st.stop()

# Set the title of the Streamlit app
st.title("About Us")

# A detailed page outlining the project scope, objectives, data sources, and features.


# Create a disclaimer
# with st.expander("IMPORTANT NOTICE: Click to expand/disclose", expanded=True):
st.write("""
This streamlit application is for a personal GenAI project and not meant for educational purposes.
Please consult your property agent or HDB officer if you require any advice on property related issues.
The website developer takes no responsibility for the information you take from this website.
""")

# Project Scope with Icon
st.markdown("#### **Project Scope**")
st.markdown("""
There are 2 main modules for this project:
            
1. **BuyHDBApp**:  
- A GenAI application that allows users to ask any question related to buying of HDB or Executive Condos.  
- In order to do this, a scrapeHDB.py file was created to help to scrape all the relevent data, then save it in a .json file first. If this isn't done, then the BuyHDBApp would have to scrape the data everytime upon starting, which would make the entire app very slow  
- The impact of saving the .json file is not that big, because HDB policies do not change very often. Therefore, should be quite accurate.  

2. **Resaleprice**:  
- A tool that allows users to find out the recent sale prices of flats. Users can apply different filters to narrow down their results. This will complement the buyer's decision on what type of flat to buy, because usually, people will want to sell a house, before they buy a new place.  
- Likewise, for Resaleprice, the .csv file was saved first, so that the application wouldnt have to fetch the .csv file from data.gov everytime it loads.  
- The impact a bit more than the BuyHDBApp, because it isn't table to take the latest data.  
""")

# Objectives with Icon
st.markdown("#### **Objectives**")
st.markdown("""
1. The purpose of the first application, BuyHDBFlat, is to build an application to allow interested buyers of HDB properties to ask any questions related to it. The problem is that this information is all over HDB's website and there isn't an easy way to find out the necessary information.
2. The second application, ResalePrice, is for prospective buyers/sellers to know what are the recently transacted price around the area that they are interested in. A filter was added, so that people can easily filter down to the region/type of housing etc. that they are interested in.
            """)

# Data Sources with Icon
st.markdown("#### **Data Sources**")
st.markdown("""
My application takes data from the following sources:

1. **HDB's Official Website**: I scraped the information from the website, then store it in a .json file.
- **URLs Scraped Regarding:**
    - Executive Condos  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/eligibility",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/cpf-housing-grants",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/buying-procedures",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/application",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/executive-condominium/conditions-after-buying-for-ec",  
    - Resale Flats  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/overview",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/plan-source-and-contract",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-application",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-resale-flats/resale-completion",  
    - New Flats  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/timeline",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/modes-of-sale",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/application",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/booking-of-flat",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/sign-agreement-for-lease",  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/buying-procedure-for-new-flats/key-collection",  
    "https://www.hdb.gov.sg/residential/buying-a-flat/conditions-after-buying",  
    - Housing Loan Options  
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options",  
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/flat-and-grant-eligibility",  
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/housing-loan-options/housing-loan-from-hdb",  
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/housing-loan-options/housing-loan-from-financial-institutions",  
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/application-for-an-hdb-flat-eligibility-hfe-letter",  
    "https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/application-for-an-hdb-flat-eligibility-hfe-letter/income-guidelines",  
    - Finding a flat  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/finding-a-flat",  
    - Conditions after buying  
    "https://www.hdb.gov.sg/cs/infoweb/residential/buying-a-flat/conditions-after-buying",  

2. **Resale Prices Data**:   
- I took the data from "https://data.gov.sg/datasets?topics=housing&page=1&resultId=d_8b84c4ee58e3cfc0ece0d773c8ca6abc", which contains the data of all resale HDB flats from 2017 onwards. I didn't take earlier information as it might not be relevant in today's property market
""")

# Features Section with Icon
st.markdown("#### **Features**")

# 1. Buy HDB Flat app
st.markdown("1. **BuyHDBFlat app**")
st.markdown("""
- **RAG question and answer section**: At the backend, I have scraped the necessary data from HDB's website, put it in a .json file, split the information, vectorise it, put it into a vector database, then built a frontend chat box to allow users to ask any questions related to it. If it is outside of the scope, then the answer will be "I don't know"
""")

# 2. Resaleprice
st.markdown("2. **Resaleprice**")
st.markdown("""
- **Filter Selection**: A filter that allows users to select any number of filters. This will help users scope down to the region or flat type etc. that they are interested in.
- **Display results**: Displays the results for all the relevant filters that was added above
""")

if __name__ == "__main__":
    # Removed the unwanted section
    pass
