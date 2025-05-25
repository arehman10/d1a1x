import csv
import io
import streamlit as st
from isic_classifier import load_isic, classify

st.title("ISIC Code Classifier")

isic_data = load_isic()

option = st.sidebar.radio("Select input method", ["Single description", "Upload CSV"])

if option == "Single description":
    text = st.text_area("Firm activity description")
    if st.button("Classify"):
        if text.strip():
            code, score = classify(text, isic_data)
            st.write(f"ISIC Code: {code}")
            st.write(f"Match Score: {score:.2f}")
        else:
            st.warning("Please enter a description.")
else:
    uploaded = st.file_uploader("Upload CSV file", type="csv")
    if uploaded:
        data = uploaded.read().decode("utf-8")
        reader = csv.DictReader(io.StringIO(data))
        rows = list(reader)
        if "d1a1x" not in reader.fieldnames:
            st.error("Column 'd1a1x' not found")
        else:
            for row in rows:
                code, score = classify(row["d1a1x"], isic_data)
                row["isic_code"] = code
                row["match_score"] = f"{score:.2f}"
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
            st.download_button("Download results", output.getvalue(), "classified.csv", "text/csv")
            st.write(rows)
