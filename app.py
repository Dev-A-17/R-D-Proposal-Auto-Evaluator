import streamlit as st
import os
import json
import pandas as pd
import io
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv
from fpdf import FPDF
from pdf_reader import read_pdf
from evaluator import get_gemini_response
from novelty_checker import check_novelty
from datetime import datetime

# Custom CSS for beautiful styling
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main title styling */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        animation: fadeIn 1s ease-in;
    }
    
    /* Headers with gradient underline */
    h2 {
        color: #2D3748;
        position: relative;
        padding-bottom: 10px;
        margin-bottom: 20px !important;
        font-weight: 600;
    }
    
    h2:after {
        content: "";
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    /* Card-like containers */
    .stContainer > div {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stContainer > div:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Metrics styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="metric-container"] label {
        color: #4A5568;
        font-weight: 500;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-size: 2.5rem !important;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Download button special styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 0.95rem;
        font-weight: 600;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(86, 171, 47, 0.3);
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(86, 171, 47, 0.4);
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px dashed #CBD5E0;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #f0f4ff 0%, #e0e7ff 100%);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 12px !important;
        padding: 1rem !important;
        font-weight: 600;
        color: #2D3748;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, #e0e7ff 0%, #cfd8ef 100%);
    }
    
    /* Success/Error/Warning messages */
    .stAlert {
        border-radius: 12px;
        padding: 1rem 1.5rem;
        border-left: 4px solid;
        animation: slideIn 0.5s ease;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        color: #667eea !important;
    }
    
    /* Animation keyframes */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46a0 100%);
    }
    
    /* Score cards */
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .score-card:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        background: white;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper class for PDF generation with enhanced styling
class PDF(FPDF):
    def header(self):
        self.set_fill_color(102, 126, 234)
        self.rect(0, 0, 210, 30, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 16)
        self.set_y(10)
        self.cell(0, 10, 'R&D Proposal Screening Report', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, f'Generated: {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()} | Powered by AI Analysis', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(102, 126, 234)
        self.cell(0, 10, title, 0, 1, 'L')
        self.set_text_color(0, 0, 0)
        self.ln(3)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(5)

def create_pdf_report(report_text):
    pdf = PDF()
    pdf.add_page()
    
    # Split report into sections and format nicely
    sections = report_text.split('--------------------------------------------------')
    for section in sections:
        if section.strip():
            lines = section.strip().split('\n')
            if lines:
                if any(keyword in lines[0].upper() for keyword in ['EVALUATION', 'DETAILED', 'ORIGINALITY']):
                    pdf.chapter_title(lines[0])
                    pdf.chapter_body('\n'.join(lines[1:]))
                else:
                    pdf.chapter_body(section.strip())
    
    return bytes(pdf.output())

def create_gauge_chart(value, title, color):
    """Create a beautiful gauge chart for scores"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 24, 'family': 'Inter'}},
        delta = {'reference': 5, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [None, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 2.5], 'color': '#FFE5E5'},
                {'range': [2.5, 5], 'color': '#FFF4E5'},
                {'range': [5, 7.5], 'color': '#E5F4FF'},
                {'range': [7.5, 10], 'color': '#E5FFE5'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 9
            }
        }
    ))
    
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': 'Inter', 'color': '#2D3748'}
    )
    
    return fig

def create_radar_chart(scores):
    """Create a radar chart for evaluation scores"""
    categories = list(scores.keys())
    values = list(scores.values())
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='rgb(102, 126, 234)', width=2),
        marker=dict(size=8, color='rgb(102, 126, 234)')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=12, family='Inter', weight=600)
            )
        ),
        showlegend=False,
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        font={'family': 'Inter', 'color': '#2D3748'}
    )
    
    return fig

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="R&D Proposal Evaluator",
    page_icon="🚀",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
load_css()

# Header section with animation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h1>🚀 R&D Proposal Auto-Evaluator</h1>
            <p style="font-size: 1.2rem; color: #718096; margin-top: 1rem;">
                Leverage AI-powered intelligence for comprehensive proposal screening
            </p>
        </div>
    """, unsafe_allow_html=True)

# Get API Key
api_key = os.getenv("GOOGLE_API_KEY")

# Create beautiful sidebar
with st.sidebar:
    st.markdown("### 📊 Dashboard Settings")
    st.markdown("---")
    
    show_advanced = st.checkbox("Show Advanced Metrics", value=True)
    enable_animations = st.checkbox("Enable Animations", value=True)
    
    st.markdown("---")
    st.markdown("### 📈 Analysis Parameters")
    similarity_threshold = st.slider("Similarity Threshold", 0.0, 1.0, 0.7, 0.05)
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("""
    This AI-powered tool provides:
    - 🔬 Novelty checking
    - 📊 Multi-criteria evaluation
    - 📑 Detailed PDF reports
    - 🎯 Actionable insights
    """)

# Main content area
st.markdown("---")

# File upload section with enhanced styling
upload_col1, upload_col2, upload_col3 = st.columns([1, 2, 1])
with upload_col2:
    uploaded_file = st.file_uploader(
        "📄 Upload your R&D Proposal PDF",
        type="pdf",
        help="Select a PDF file containing your R&D proposal for analysis"
    )

# Analysis button and process
if uploaded_file:
    st.markdown("---")
    
    # Show file info
    file_details = {
        "Filename": uploaded_file.name,
        "File Size": f"{uploaded_file.size / 1024:.2f} KB",
        "File Type": uploaded_file.type
    }
    
    col1, col2, col3 = st.columns(3)
    for i, (key, value) in enumerate(file_details.items()):
        with [col1, col2, col3][i]:
            st.metric(key, value)
    
    st.markdown("---")
    
    # Center the analyze button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_button = st.button("🔍 ANALYZE PROPOSAL", use_container_width=True)
    
    if analyze_button:
        if not api_key:
            st.error("⚠️ GOOGLE_API_KEY not found. Please create a .env file with your key.")
        else:
            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner():
                # Stage 1: Reading PDF
                status_text.text("📖 Reading PDF document...")
                progress_bar.progress(20)
                
                file_bytes = uploaded_file.getvalue()
                file_stream = io.BytesIO(file_bytes)
                proposal_text = read_pdf(file_stream)
                
                if "Error reading PDF file" in proposal_text:
                    st.error(proposal_text)
                    progress_bar.empty()
                    status_text.empty()
                else:
                    # Stage 2: Novelty Check
                    status_text.text("🔬 Checking novelty against database...")
                    progress_bar.progress(50)
                    top_matches = check_novelty(proposal_text, 'database', api_key)
                    
                    # Stage 3: AI Evaluation
                    status_text.text("🤖 Performing deep AI analysis...")
                    progress_bar.progress(80)
                    evaluation_result_text = get_gemini_response(api_key, proposal_text)
                    
                    # Complete
                    progress_bar.progress(100)
                    status_text.text("✅ Analysis complete!")
                    
                    # Clear progress indicators
                    progress_bar.empty()
                    status_text.empty()
                    
                    # Display results in tabs
                    st.markdown("---")
                    st.markdown("## 📊 Analysis Results")
                    
                    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "🎯 Scores", "📝 Detailed Analysis", "📥 Export"])
                    
                    # Parse JSON response
                    json_string = evaluation_result_text
                    if '```json' in evaluation_result_text:
                        start_index = evaluation_result_text.find('{')
                        end_index = evaluation_result_text.rfind('}') + 1
                        json_string = evaluation_result_text[start_index:end_index]
                    
                    try:
                        data = json.loads(json_string)
                        
                        with tab1:
                            # Overview metrics
                            st.markdown("### 🎯 Key Metrics")
                            
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                originality_score = (1 - top_matches[0][0]) * 100 if top_matches else 0
                                st.metric(
                                    "Originality",
                                    f"{originality_score:.1f}%",
                                    f"vs {top_matches[0][1][:20]}..." if top_matches else "N/A"
                                )
                            
                            with col2:
                                avg_score = (data['clarity_score']['score'] + 
                                           data['novelty_score']['score'] + 
                                           data['feasibility_score']['score']) / 3
                                st.metric(
                                    "Average Score",
                                    f"{avg_score:.1f}/10",
                                    f"{(avg_score - 5):.1f}" if avg_score != 5 else "0"
                                )
                            
                            with col3:
                                st.metric(
                                    "Highest Score",
                                    f"{max(data['clarity_score']['score'], data['novelty_score']['score'], data['feasibility_score']['score'])}/10",
                                    "✨ Excellent" if max(data['clarity_score']['score'], data['novelty_score']['score'], data['feasibility_score']['score']) >= 8 else "Good"
                                )
                            
                            with col4:
                                st.metric(
                                    "Areas to Improve",
                                    f"{sum(1 for s in [data['clarity_score']['score'], data['novelty_score']['score'], data['feasibility_score']['score']] if s < 7)}",
                                    "aspects" if sum(1 for s in [data['clarity_score']['score'], data['novelty_score']['score'], data['feasibility_score']['score']] if s < 7) > 0 else "None"
                                )
                            
                            # Similarity matches
                            if top_matches:
                                st.markdown("### 🔍 Similarity Analysis")
                                similarity_data = pd.DataFrame(
                                    [(f"{(1-score)*100:.1f}%", name[:50]) for score, name in top_matches[:5]],
                                    columns=["Uniqueness", "Similar Project"]
                                )
                                st.dataframe(similarity_data, use_container_width=True, hide_index=True)
                        
                        with tab2:
                            st.markdown("### 📊 Evaluation Scores")
                            
                            scores = {
                                'Clarity': data['clarity_score']['score'],
                                'Novelty': data['novelty_score']['score'],
                                'Feasibility': data['feasibility_score']['score']
                            }
                            
                            # Radar chart
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                st.plotly_chart(create_radar_chart(scores), use_container_width=True)
                            
                            with col2:
                                st.markdown("#### Score Breakdown")
                                for criterion, score in scores.items():
                                    color = "#10B981" if score >= 7 else "#F59E0B" if score >= 5 else "#EF4444"
                                    st.markdown(f"""
                                        <div style="background: linear-gradient(90deg, {color}22 0%, {color}11 100%); 
                                                    padding: 1rem; border-radius: 8px; margin: 0.5rem 0;
                                                    border-left: 4px solid {color};">
                                            <strong style="color: #2D3748;">{criterion}</strong><br>
                                            <span style="font-size: 2rem; font-weight: bold; color: {color};">{score}</span>
                                            <span style="color: #718096;">/10</span>
                                        </div>
                                    """, unsafe_allow_html=True)
                            
                            # Individual gauge charts
                            if show_advanced:
                                st.markdown("---")
                                st.markdown("### 🎯 Detailed Score Visualization")
                                cols = st.columns(3)
                                colors = ["#667EEA", "#F56565", "#48BB78"]
                                for i, (criterion, score) in enumerate(scores.items()):
                                    with cols[i]:
                                        st.plotly_chart(
                                            create_gauge_chart(score, criterion, colors[i]),
                                            use_container_width=True
                                        )
                        
                        with tab3:
                            st.markdown("### 📝 Detailed Analysis")
                            
                            # Justifications in expandable sections
                            with st.expander("🎯 Score Justifications", expanded=True):
                                for criterion in ['clarity_score', 'novelty_score', 'feasibility_score']:
                                    st.markdown(f"""
                                        <div style="background: #F7FAFC; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                                            <h4 style="color: #2D3748; margin-bottom: 0.5rem;">
                                                {criterion.replace('_score', '').title()}
                                            </h4>
                                            <p style="color: #4A5568; line-height: 1.6;">
                                                {data[criterion]['justification']}
                                            </p>
                                        </div>
                                    """, unsafe_allow_html=True)
                            
                            # Strengths and Weaknesses
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("""
                                    <div style="background: linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%); 
                                                padding: 1.5rem; border-radius: 12px;">
                                        <h3 style="color: #155724;">💪 Strengths</h3>
                                    </div>
                                """, unsafe_allow_html=True)
                                st.markdown(data['strengths'])
                            
                            with col2:
                                st.markdown("""
                                    <div style="background: linear-gradient(135deg, #F8D7DA 0%, #F5C6CB 100%); 
                                                padding: 1.5rem; border-radius: 12px;">
                                        <h3 style="color: #721C24;">⚠️ Weaknesses</h3>
                                    </div>
                                """, unsafe_allow_html=True)
                                st.markdown(data['weaknesses'])
                        
                        with tab4:
                            st.markdown("### 📥 Export Options")
                            
                            # Prepare report
                            report_text = f"""
R&D PROPOSAL SCREENING REPORT
============================================

ORIGINALITY ASSESSMENT
--------------------------------------------
Originality vs. Database: {(1 - top_matches[0][0]) * 100:.1f}% Original
Most similar file: {top_matches[0][1]} ({top_matches[0][0]*100:.1f}% similar)

EVALUATION SCORES
--------------------------------------------
- Clarity: {scores.get('Clarity', 'N/A')} / 10
- Novelty: {scores.get('Novelty', 'N/A')} / 10
- Feasibility: {scores.get('Feasibility', 'N/A')} / 10
- Average Score: {avg_score:.1f} / 10

DETAILED ANALYSIS
--------------------------------------------
Score Justifications:

Clarity: {data['clarity_score']['justification']}

Novelty: {data['novelty_score']['justification']}

Feasibility: {data['feasibility_score']['justification']}

Strengths:
{data['strengths']}

Weaknesses:
{data['weaknesses']}

RECOMMENDATIONS
--------------------------------------------
Based on the analysis, this proposal shows {
    'excellent potential' if avg_score >= 8 else 
    'good potential' if avg_score >= 6 else 
    'moderate potential' if avg_score >= 4 else 
    'limited potential'
} for R&D funding consideration.
"""
                            
                            # Export buttons
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # PDF export
                                sanitized_report_text = report_text.replace("—", "-").replace("'", "'").replace("'", "'")
                                pdf_data = create_pdf_report(sanitized_report_text)
                                
                                st.download_button(
                                    label="📄 Download PDF Report",
                                    data=pdf_data,
                                    file_name=f"RD_Screening_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            
                            with col2:
                                # JSON export
                                st.download_button(
                                    label="📊 Download JSON Data",
                                    data=json.dumps(data, indent=2),
                                    file_name=f"RD_Analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                    mime="application/json",
                                    use_container_width=True
                                )
                            
                            # Preview area
                            st.markdown("---")
                            with st.expander("📋 Preview Report"):
                                st.text(report_text)
                    
                    except (json.JSONDecodeError, KeyError) as e:
                        st.error(f"Could not parse AI response. Error: {str(e)}")
                        st.code(json_string)
else:
    # Landing page when no file is uploaded
    st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    border-radius: 20px; margin: 2rem 0;">
            <h2 style="color: #2D3748;">Welcome to the AI-Powered R&D Evaluator</h2>
            <p style="color: #4A5568; font-size: 1.1rem; margin: 1rem 0;">
                Transform your R&D proposal evaluation process with cutting-edge AI technology
            </p>
            <div style="display: flex; justify-content: center; gap: 3rem; margin-top: 2rem;">
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem;">🚀</div>
                    <strong>Fast Analysis</strong>
                    <p style="color: #718096; font-size: 0.9rem;">Results in seconds</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem;">🎯</div>
                    <strong>Accurate Scoring</strong>
                    <p style="color: #718096; font-size: 0.9rem;">Multi-criteria evaluation</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem;">📊</div>
                    <strong>Detailed Reports</strong>
                    <p style="color: #718096; font-size: 0.9rem;">Comprehensive insights</p>
                </div>
            </div>
            <p style="color: #667eea; font-weight: 600; margin-top: 2rem; font-size: 1.1rem;">
                👆 Upload your PDF above to get started
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    st.markdown("---")
    st.markdown("## ✨ Features")
    
    feature_cols = st.columns(3)
    
    features = [
        {
            "icon": "🔬",
            "title": "Novelty Detection",
            "description": "Compare your proposal against existing database to ensure uniqueness and innovation"
        },
        {
            "icon": "🤖",
            "title": "AI-Powered Analysis",
            "description": "Leverage Google's Gemini AI for deep content understanding and evaluation"
        },
        {
            "icon": "📈",
            "title": "Visual Analytics",
            "description": "Interactive charts and visualizations for better insight comprehension"
        }
    ]
    
    for col, feature in zip(feature_cols, features):
        with col:
            st.markdown(f"""
                <div style="background: white; padding: 2rem; border-radius: 16px; 
                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07); height: 200px;
                            transition: transform 0.3s ease;">
                    <div style="font-size: 3rem; text-align: center; margin-bottom: 1rem;">
                        {feature["icon"]}
                    </div>
                    <h3 style="color: #2D3748; text-align: center; margin-bottom: 0.5rem;">
                        {feature["title"]}
                    </h3>
                    <p style="color: #718096; text-align: center; font-size: 0.95rem;">
                        {feature["description"]}
                    </p>
                </div>
            """, unsafe_allow_html=True)
    
    # How it works section
    st.markdown("---")
    st.markdown("## 🔄 How It Works")
    
    process_cols = st.columns(4)
    
    processes = [
        {"step": "1", "title": "Upload", "desc": "Submit your R&D proposal in PDF format"},
        {"step": "2", "title": "Process", "desc": "AI analyzes content and checks novelty"},
        {"step": "3", "title": "Evaluate", "desc": "Multi-criteria scoring and assessment"},
        {"step": "4", "title": "Report", "desc": "Get detailed insights and recommendations"}
    ]
    
    for col, process in zip(process_cols, processes):
        with col:
            st.markdown(f"""
                <div style="text-align: center;">
                    <div style="width: 60px; height: 60px; margin: 0 auto 1rem; 
                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                border-radius: 50%; display: flex; align-items: center; 
                                justify-content: center; color: white; font-size: 1.5rem; 
                                font-weight: bold; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                        {process["step"]}
                    </div>
                    <h4 style="color: #2D3748; margin-bottom: 0.5rem;">{process["title"]}</h4>
                    <p style="color: #718096; font-size: 0.9rem;">{process["desc"]}</p>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #718096;">
        <p style="margin-bottom: 0.5rem;">
            🚀 Powered by Advanced AI Technology | 
            Built with ❤️ for R&D Excellence
        </p>
        <p style="font-size: 0.9rem;">
            © 2024 R&D Proposal Auto-Evaluator | All Rights Reserved
        </p>
    </div>
""", unsafe_allow_html=True)