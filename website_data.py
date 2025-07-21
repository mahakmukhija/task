import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="🌐 Website Scraper", layout="centered")
st.title("🌐 Download Entire Website HTML")

# Input field for the website URL
url = st.text_input("Enter Website URL", placeholder="https://example.com")

# Scrape and download
if st.button("Scrape Website"):
    try:
        # Request page content
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        cleaned_html = soup.prettify()

        # File download
        st.download_button(
            label="📥 Download HTML File",
            data=cleaned_html,
            file_name="website_data.html",
            mime="text/html"
        )

        st.success("✅ Website data scraped successfully!")

        # Optional preview
        with st.expander("🔍 Preview HTML"):
            st.code(cleaned_html[:2000])  # Show only first 2000 chars

    except Exception as e:
        st.error(f"❌ Failed to scrape the site: {e}")
