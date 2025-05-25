import io
import pandas as pd
import streamlit as st

from isic_classifier import load_isic, classify

st.title("ISIC Rev.4 Classifier")

isic_data = load_isic()

st.header("Classify a single activity")
text = st.text_input("Activity description")
if st.button("Classify"):
    if text:
        code, score = classify(text, isic_data)
        st.write(f"**ISIC code:** {code}")
        st.write(f"**Match score:** {score:.2f}")
    else:
        st.warning("Please enter a description")

st.header("Classify activities from a CSV file")
file = st.file_uploader("Upload CSV with a 'd1a1x' column", type=["csv"])
if file is not None:
    df = pd.read_csv(file)
    if "d1a1x" not in df.columns:
        st.error("Column 'd1a1x' not found in uploaded file")
    else:
        codes = []
        scores = []
        for desc in df["d1a1x"].astype(str):
            code, score = classify(desc, isic_data)
            codes.append(code)
            scores.append(round(score, 2))
        df["isic_code"] = codes
        df["match_score"] = scores
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download results", csv, "isic_results.csv", "text/csv")

