import streamlit as st
import os
from scanner import scan_sql_injection, scan_xss, scan_path_traversal, scan_directory_listing
from report import generate_pdf

st.set_page_config(page_title="🛡️ VulnScan Web", layout="centered")

st.markdown("""
    <style>
        .reportview-container { background-color: #f7f9fc; }
        .stButton button { background-color: #1f1f2e; color: white; }
        h1 { color: #1f1f2e; font-size: 2.5em; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ VulnScan Web")
st.subheader("Scan your website for common vulnerabilities")
st.caption("Built with Python & Streamlit · Generates a downloadable PDF report")

url = st.text_input("🔗 Enter target URL", placeholder="http://example.com")
results = {}

if st.button("🚀 Run Vulnerability Scan"):
    if not url.strip():
        st.error("Please enter a valid URL.")
    else:
        st.info("Running scans... please wait.")
        results['SQL Injection'] = scan_sql_injection(url)
        results['XSS'] = scan_xss(url)
        results['Path Traversal'] = scan_path_traversal(url)
        results['Directory Listing'] = scan_directory_listing(url)

        st.success("✅ Scan complete")
        for sec, msgs in results.items():
            st.markdown(f"### 🔍 {sec}")
            for level, msg in msgs:
                if level == 'error':
                    st.error(msg)
                elif level == 'warning':
                    st.warning(msg)
                else:
                    st.info(msg)

        pdf_path = "scan_results.pdf"
        from report import generate_pdf
        generate_pdf(results, pdf_path, logo_path="vulnscan_logo.png")
        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download Full PDF Report", f, file_name="vuln_report.pdf")


