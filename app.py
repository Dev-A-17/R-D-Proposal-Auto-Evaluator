import streamlit as st
import os
import re
import pandas as pd
import io
from dotenv import load_dotenv
from pdf_reader import read_pdf
from evaluator import get_gemini_response
from novelty_checker import check_novelty

# Helper function to parse scores from the AI's text output
def parse_scores_from_text(text):
    """
    Parses scores from the AI's text output using robust regular expressions.
    Handles variations like bolding and different whitespace.
    """
    scores = {}
    # More robust patterns to find scores regardless of minor formatting changes
    patterns = {
        'Clarity': r"\**Clarity Score\**.*?:\**?\s*(\d+)",
        'Novelty': r"\**Novelty Score\**.*?:\**?\s*(\d+)",
        'Feasibility': r"\**Feasibility Score\**.*?:\**?\s*(\d+)"
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            scores[key] = int(match.group(1))
    return scores

# --- Load environment variables from .env file ---
load_dotenv()

# --- App Layout ---
st.set_page_config(layout="wide", page_title="R&D Proposal Evaluator", page_icon="🤖")

st.title("🤖 R&D Proposal Auto-Evaluator")
st.write("Upload an R&D proposal for an AI-powered initial screening report.")

# --- Get API Key from environment variable ---
api_key = os.getenv("GOOGLE_API_KEY")

# --- Main Content Area ---
uploaded_file = st.file_uploader("Upload your R&D Proposal PDF", type="pdf")

if st.button("Analyze Proposal"):
    if not api_key:
        st.error("⚠️ GOOGLE_API_KEY not found. Please create a .env file with your key.")
    elif not uploaded_file:
        st.error("⚠️ Please upload a PDF file.")
    else:
        with st.spinner("AI is performing a deep analysis... This may take a moment."):
            # Read the file content into memory to use it multiple times
            file_bytes = uploaded_file.getvalue()
            file_stream = io.BytesIO(file_bytes)
            proposal_text = read_pdf(file_stream) 
            
            if "Error reading PDF file" in proposal_text:
                st.error(proposal_text)
            else:
                # Perform both checks
                max_similarity = check_novelty(proposal_text, 'database', api_key)
                evaluation_result = get_gemini_response(api_key, proposal_text)
                
                # Parse scores from the result
                scores = parse_scores_from_text(evaluation_result)
                
                # --- Display all results in the beautified layout ---
                st.header("Screening Report")

                col1, col2 = st.columns((1, 2))

                # --- Column 1: Metrics and Charts ---
                with col1:
                    with st.container(border=True):
                        if max_similarity != -1:
                            originality_score = (1 - max_similarity) * 100
                            st.metric(
                                label="🔬 Originality vs. Database",
                                value=f"{originality_score:.1f}%",
                                help=f"This proposal is {max_similarity*100:.1f}% similar to the most related project in the database."
                            )
                        else:
                            st.warning("Could not perform novelty check.")
                    
                    with st.container(border=True):
                        if scores:
                            st.subheader("📊 Evaluation Scores")
                            df_scores = pd.DataFrame(list(scores.items()), columns=['Criteria', 'Score'])
                            st.bar_chart(df_scores.set_index('Criteria'))
                        else:
                            st.warning("Could not parse scores for charting.")

                # --- Column 2: Detailed Text Analysis ---
                with col2:
                    with st.expander("✍️ View Detailed AI Analysis", expanded=True):
                        st.markdown(evaluation_result)