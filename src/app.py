# src/app.py
import json
import streamlit as st
import pandas as pd
from pathlib import Path
from parsing import parse_file
from cleaning import normalize_text
from skills_extraction import load_taxonomy, build_skill_dict, extract_skills
from recommend import recommend

# Load taxonomy
taxonomy = load_taxonomy("data/job_role_taxonomy.json")

st.set_page_config(page_title="Resume Role Recommender", layout="centered")
st.title("📄 Resume → Role Recommender")
st.write("Upload a resume and get recommended job roles based on extracted skills.")

# File uploader
uploaded = st.file_uploader(
    "📤 Upload resume (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"]
)

if uploaded:
    import tempfile, os

    # Preserve original file extension
    suffix = Path(uploaded.name).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.read())
        path = tmp.name

    # Parse and clean
    raw_text = parse_file(path)
    os.unlink(path)
    clean_text = normalize_text(raw_text)

    # Extract skills
    skill_list = build_skill_dict(taxonomy)
    skills = extract_skills(clean_text, skill_list, score_cutoff=75)

    # Display extracted skills
    st.subheader("✅ Extracted Skills")
    if skills:
        for i, skill in enumerate(skills, start=1):
            st.markdown(f"{i}. **{skill}**")
    else:
        st.warning(
            "⚠️ No matching skills found. Try expanding your taxonomy or lowering the match threshold."
        )

    # Recommend roles
    roles = recommend(skills, taxonomy)

    # Display top roles with percentage match
    st.subheader("🎯 Top Recommended Roles")
    if roles:
        for r in roles[:3]:
            percent = round((r["score"] / 3.0) * 100)
            st.write(f"**{r['role']}** — {percent}% match")

        # Bar chart of all role scores
        st.subheader("📊 Role Match Scores")
        df = pd.DataFrame(roles)
        df["percent"] = (df["score"] / 3.0) * 100
        st.bar_chart(df.set_index("role")["percent"])
    else:
        st.warning("⚠️ No roles matched. Check your taxonomy or resume content.")
