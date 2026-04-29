import streamlit as st
import requests
import json
import re
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="FinDash Pro", layout="wide", initial_sidebar_state="expanded")

# ---------------- STYLING ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 15% 50%, rgba(37, 99, 235, 0.08), transparent 25%),
                radial-gradient(circle at 85% 30%, rgba(16, 185, 129, 0.08), transparent 25%),
                #0B1120;
    background-size: 200% 200%;
    animation: gradientMove 15s ease infinite;
    color: #e2e8f0;
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

[data-testid="stHeader"] {
    background-color: transparent;
}

/* Premium Animated Glass Card */
.glass {
    background: rgba(17, 24, 39, 0.45);
    backdrop-filter: blur(20px) saturate(150%);
    -webkit-backdrop-filter: blur(20px) saturate(150%);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.glass::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    border-radius: 16px;
    padding: 1px;
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0) 50%, rgba(255,255,255,0.05));
    -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
    pointer-events: none;
    transition: all 0.4s ease;
}

.glass:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 15px 40px -5px rgba(59, 130, 246, 0.15), 0 8px 32px 0 rgba(0, 0, 0, 0.4);
}

.glass:hover::before {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.5), rgba(16, 185, 129, 0.2));
}

h1 {
    color: #F8FAFC !important;
    font-weight: 700 !important;
    letter-spacing: -0.025em;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 16px;
    color: #F8FAFC;
    letter-spacing: 0.5px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding-bottom: 8px;
}

/* Premium Animated Buttons */
.stButton button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative;
    overflow: hidden;
}

.stButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.5) !important;
    background: linear-gradient(135deg, #3B82F6, #2563EB) !important;
    border-color: rgba(255,255,255,0.2) !important;
}

.stButton button:active {
    transform: translateY(1px);
}

/* Glass Inputs & File Uploader */
[data-testid="stFileUploadDropzone"] {
    background: rgba(17, 24, 39, 0.4) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px dashed rgba(255, 255, 255, 0.15) !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
}

[data-testid="stFileUploadDropzone"]:hover {
    border-color: #3B82F6 !important;
    background: rgba(37, 99, 235, 0.05) !important;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.1) !important;
}

.stTextInput input, .stTextArea textarea {
    background: rgba(17, 24, 39, 0.6) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: white !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25) !important;
    background: rgba(17, 24, 39, 0.8) !important;
}

/* Tabs Styling - Enterprise look */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: transparent;
    padding: 0px 20px 0px 0px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.stTabs [data-baseweb="tab"] {
    height: 48px;
    background-color: transparent;
    border-radius: 0;
    padding: 12px 4px;
    margin-right: 16px;
    transition: all 0.3s ease;
}

.stTabs [aria-selected="true"] {
    color: #3B82F6 !important;
    border-bottom: 2px solid #3B82F6 !important;
    font-weight: 500 !important;
}

.stTabs [aria-selected="false"] {
    color: #9CA3AF !important;
}

.stTabs [aria-selected="false"]:hover {
    color: #E2E8F0 !important;
}

/* KPI Numbers with Shimmer */
.kpi-value {
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(to right, #F8FAFC, #94A3B8, #F8FAFC);
    background-size: 200% auto;
    color: transparent;
    -webkit-background-clip: text;
    background-clip: text;
    animation: shine 4s linear infinite;
}

@keyframes shine {
    to { background-position: 200% center; }
}

.kpi-label {
    font-size: 13px;
    color: #9CA3AF;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
    font-weight: 600;
}

.trend-up {
    color: #10B981;
    font-size: 13px;
    font-weight: 600;
    margin-left: 10px;
    padding: 2px 6px;
    background: rgba(16, 185, 129, 0.1);
    border-radius: 4px;
}

/* Chat Overrides - Animated Glass */
[data-testid="stChatMessage"] {
    background: rgba(17, 24, 39, 0.5) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    margin-bottom: 16px !important;
    transition: transform 0.3s ease, border-color 0.3s ease !important;
}

[data-testid="stChatMessage"]:hover {
    border-color: rgba(255, 255, 255, 0.15) !important;
    transform: translateX(4px);
}

[data-testid="stChatMessage"][data-baseweb="card"]:nth-child(even) {
    background: rgba(15, 23, 42, 0.6) !important;
}

[data-testid="stChatMessageContent"] {
    color: #e2e8f0 !important;
}

/* Sidebar Styling - Premium Ultra Glass */
[data-testid="stSidebar"] {
    background: rgba(11, 17, 32, 0.6) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Animations */
.fade-in {
    animation: fadeInScale 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.slide-up {
    animation: slideUp 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.float {
    animation: floating 4s ease-in-out infinite;
}

@keyframes fadeInScale {
    from { opacity: 0; transform: scale(0.95) translateY(15px); }
    to { opacity: 1; transform: scale(1) translateY(0); }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(25px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes floating {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-8px); }
    100% { transform: translateY(0px); }
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
    .kpi-value { font-size: 24px !important; }
    .kpi-label { font-size: 12px !important; }
    .glass { padding: 16px !important; margin-bottom: 12px !important; }
    h2 { font-size: 22px !important; line-height: 1.3 !important; }
    .section-title { font-size: 16px !important; }
    
    /* Ensure header and flex containers wrap properly on small screens */
    .flex-wrap-mobile {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 12px !important;
    }
    
    /* Tabs scaling for mobile */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; padding-right: 0px; overflow-x: auto; }
    .stTabs [data-baseweb="tab"] { margin-right: 8px; font-size: 14px; padding: 10px 4px; }
    
    /* Adjust chat padding for mobile */
    [data-testid="stChatMessage"] { padding: 12px !important; margin-bottom: 12px !important; }
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------

def convert_to_number(value):
    value = str(value).lower().replace(",", "").strip()

    try:
        if "billion" in value:
            return float(value.replace("billion", "")) * 1e9
        elif "million" in value:
            return float(value.replace("million", "")) * 1e6
        elif "crore" in value:
            return float(value.replace("crore", "")) * 1e7
        elif "%" in value:
            return float(value.replace("%", ""))
        else:
            return float(value)
    except:
        return 0


def format_kpi(val):
    val = str(val)

    if "billion" in val:
        return f"₹{val.replace('billion','').strip()}B"
    elif "million" in val:
        return f"₹{val.replace('million','').strip()}M"
    elif "crore" in val:
        return f"₹{val.replace('crore','').strip()}Cr"
    return val[:20]


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
    <div class='slide-up' style='display: flex; align-items: center; margin-bottom: 32px; padding-top: 8px;'>
        <div style='background: linear-gradient(135deg, #3B82F6, #2563EB); color: white; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px; box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);'>FD</div>
        <h1 style='font-size: 22px; font-weight: 700; margin: 0; background: linear-gradient(to right, #F8FAFC, #94A3B8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>FinDash Pro</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="font-size: 13px; color: #9CA3AF; border-bottom: none; margin-bottom: 8px;">DATA SOURCES</div>', unsafe_allow_html=True)
    files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
    
    if files and "uploaded_toast_shown" not in st.session_state:
        st.toast(f"{len(files)} file(s) ready for analysis", icon="✅")
        st.session_state.uploaded_toast_shown = True
        
    st.markdown("<br><br><hr style='border-color: #1F2937;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: left; color: #64748b; font-size: 12px; display: flex; align-items: center;'>
        <div style='width: 8px; height: 8px; border-radius: 50%; background: #10B981; margin-right: 8px;'></div>
        System Online & Secure
    </div>
    """, unsafe_allow_html=True)

# ---------------- MAIN ----------------

if not files:
    st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: center; justify-content: center; height: 75vh; text-align: center;'>
        <div style='background: rgba(59, 130, 246, 0.1); padding: 32px; border-radius: 20px; margin-bottom: 24px; border: 1px solid rgba(59, 130, 246, 0.2);'>
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        </div>
        <h2 style='font-size: 32px; font-weight: 700; color: #f8fafc; margin-bottom: 12px;'>Enterprise Intelligence Hub</h2>
        <p style='color: #94a3b8; font-size: 16px; max-width: 500px; line-height: 1.6;'>
            Upload your financial documents in the sidebar to automatically extract insights, calculate KPIs, and visualize your data securely.
        </p>
    </div>
    """, unsafe_allow_html=True)

else:
    file = files[0]

    # Dashboard Header
    st.markdown("""
    <div class="flex-wrap-mobile" style='margin-bottom: 32px; display: flex; justify-content: space-between; align-items: flex-end;'>
        <div>
            <h2 style='font-size: 28px; font-weight: 700; color: #f8fafc; margin: 0;'>Dashboard Overview</h2>
            <p style='color: #9CA3AF; font-size: 14px; margin-top: 4px; margin-bottom: 0;'>Real-time AI analysis from active documents</p>
        </div>
        <div style='display: flex; align-items: center;'>
            <span style='background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 500; border: 1px solid rgba(16, 185, 129, 0.2);'>
                Model: LLaMA 3.1
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    try:
        # ---------------- PRE-FETCH DATA ----------------
        with st.spinner("Analyzing document and extracting core metrics..."):
            res_analysis = requests.post(
                "http://127.0.0.1:8000/analyze",
                files={"file": ("file.pdf", file.getvalue())}
            )
            
            res_kpis = requests.post(
                "http://127.0.0.1:8000/extract-kpis",
                files={"file": ("file.pdf", file.getvalue())}
            )

        if res_analysis.status_code != 200:
            st.error("⚠️ Backend not responding or error in analysis")
            st.stop()

        result = res_analysis.json()
        raw_kpi = res_kpis.json().get("data", "") if res_kpis.status_code == 200 else ""
        kpis = {}

        # Parse KPIs safely
        try:
            json_match = re.search(r"\{.*\}", raw_kpi, re.DOTALL)
            if json_match:
                json_text = re.sub(r",\s*}", "}", json_match.group())
                kpis = json.loads(json_text)
        except:
            pass

        # Fallback KPI parsing
        if not kpis:
            lines = raw_kpi.split("\n")
            for line in lines:
                match = re.search(r"([\d\.]+(?:\s*(?:billion|million|crore|%))?)", line.lower())
                if match:
                    key = line.split(":")[0][:25].strip().replace('"', '')
                    if key and key.lower() not in ['{', '}']:
                        kpis[key] = match.group(1)

        # ---------------- KPI ROW ----------------
        if kpis:
            items = list(kpis.items())[:4]
            cols = st.columns(4)

            for i, (key, value) in enumerate(items):
                # Mock a positive trend indicator for the enterprise feel
                trend_val = round((i * 1.4) + 2.1, 1)
                cols[i].markdown(f"""
                <div class="glass fade-in" style="padding: 20px; margin-bottom: 24px;">
                    <div class="kpi-label">{key}</div>
                    <div style="display: flex; align-items: baseline;">
                        <span class="kpi-value">{format_kpi(value)}</span>
                        <span class="trend-up">↗ {trend_val}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.toast("No KPI data could be automatically extracted.", icon="⚠️")

        # ---------------- MAIN CONTENT AREA ----------------
        left_col, right_col = st.columns([2.2, 1.2], gap="large")

        # ---------- LEFT COLUMN (Tabs for Insights & Charts) ----------
        with left_col:
            tab1, tab2 = st.tabs(["📌 Executive Summary", "📊 Interactive Analytics"])
            
            with tab1:
                # Use an expander for detailed insights to keep the UI clean
                st.markdown('<div class="section-title" style="margin-top: 16px;">AI Extracted Insights</div>', unsafe_allow_html=True)
                
                summary_content = result.get("result", "No insights generated")
                st.markdown(f"""
                <div class="glass fade-in" style="margin-top: 8px; padding: 24px; font-size: 15px; line-height: 1.6; color: #D1D5DB;">
                {summary_content}
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("View Raw Document Text Preview"):
                    st.text("Preview data not loaded directly to save memory. Check backend logs.")

            with tab2:
                st.markdown('<div class="section-title" style="margin-top: 16px;">Visual Analytics</div>', unsafe_allow_html=True)
                st.markdown("<p style='color:#9CA3AF; font-size:14px; margin-bottom: 24px;'>Generate interactive charts from document metrics.</p>", unsafe_allow_html=True)
                
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    btn_kpi_chart = st.button("📊 Quick KPI Bar Chart", use_container_width=True)
                with btn_col2:
                    btn_pdf_chart = st.button("📈 Deep Data Area Chart", use_container_width=True)
                
                st.markdown("<br>", unsafe_allow_html=True)

                if btn_kpi_chart:
                    if kpis:
                        numeric_data = {k: convert_to_number(v) for k, v in kpis.items() if convert_to_number(v) > 0}
                        if numeric_data:
                            # Plotly Bar Chart
                            fig = px.bar(
                                x=list(numeric_data.keys()), 
                                y=list(numeric_data.values()),
                                labels={'x': 'Key Performance Indicators', 'y': 'Numeric Value'},
                            )
                            fig.update_traces(marker_color='#2563EB', marker_line_color='#1D4ED8', marker_line_width=1, opacity=0.9)
                            fig.update_layout(
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font_color='#F8FAFC',
                                font_family='Inter',
                                xaxis=dict(showgrid=False),
                                yaxis=dict(gridcolor='#1F2937'),
                                margin=dict(l=0, r=0, t=20, b=0),
                                hovermode="x unified"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.error("KPIs could not be converted to numeric values.")
                    else:
                        st.warning("No KPI data available for chart.")
                        
                elif btn_pdf_chart:
                    with st.spinner("Extracting numeric datasets from PDF..."):
                        res_num = requests.post(
                            "http://127.0.0.1:8000/extract-numbers",
                            files={"file": ("file.pdf", file.getvalue())}
                        )
                        data = res_num.json().get("data", "")
                        
                        try:
                            clean_data = data.replace("```json", "").replace("```", "").strip()
                            numbers = {}
                            try:
                                numbers = json.loads(clean_data)
                            except:
                                matches = re.findall(r"([A-Za-z ]+):?\s*(-?\d+(?:\.\d+)?)", clean_data)
                                for k, v in matches:
                                    numbers[k.strip()[:20]] = float(v)

                            if numbers:
                                numbers = {k: convert_to_number(v) for k, v in numbers.items() if convert_to_number(v) > 0}
                                
                                # Plotly Area Chart
                                fig = px.area(
                                    x=list(numbers.keys()), 
                                    y=list(numbers.values()),
                                    labels={'x': 'Financial Metrics', 'y': 'Extracted Value'},
                                )
                                fig.update_traces(line_color='#10B981', fillcolor='rgba(16, 185, 129, 0.2)', mode='lines+markers')
                                fig.update_layout(
                                    plot_bgcolor='rgba(0,0,0,0)',
                                    paper_bgcolor='rgba(0,0,0,0)',
                                    font_color='#F8FAFC',
                                    font_family='Inter',
                                    xaxis=dict(showgrid=False),
                                    yaxis=dict(gridcolor='#1F2937'),
                                    margin=dict(l=0, r=0, t=20, b=0),
                                    hovermode="x unified"
                                )
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.warning("No numeric data extracted")
                        except:
                            st.error("Chart generation failed")
                else:
                    st.info("👆 Select a visualization option above to generate a chart.")

        # ---------- RIGHT COLUMN (Chat Assistant) ----------
        with right_col:
            st.markdown('<div class="section-title" style="margin-top: 16px;">💬 Document Intelligence</div>', unsafe_allow_html=True)
            
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat history in a container
            chat_container = st.container(border=False)
            
            with chat_container:
                if not st.session_state.messages:
                    st.markdown("""
                    <div class="glass fade-in" style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 40px 20px; margin-top: 10px; margin-bottom: 20px; background: rgba(17, 24, 39, 0.4);">
                        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 12px;"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                        <p style='color: #E2E8F0; font-size: 14px; margin: 0; line-height: 1.6; font-weight: 400;'>
                            <span style="color: #3B82F6; font-weight: 600;">Ask anything</span> about the provided document to uncover hidden insights.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Provide a fixed height when there are messages to keep it scrollable
                    scrollable_container = st.container(height=450, border=False)
                    with scrollable_container:
                        for message in st.session_state.messages:
                            with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
                                st.markdown(message["content"])

            # Chat Input (Pinned to bottom of column via Streamlit's native component)
            if prompt := st.chat_input("Ask a question..."):
                # Add user message to state
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Render user message immediately
                with chat_container:
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(prompt)
                
                # Render assistant message
                with chat_container:
                    with st.chat_message("assistant", avatar="🤖"):
                        with st.spinner("Analyzing context..."):
                            file_data = [("files", (f.name, f.getvalue())) for f in files]
                            res_chat = requests.post(
                                "http://127.0.0.1:8000/multi-chat",
                                params={"question": prompt},
                                files=file_data
                            )
                            answer = res_chat.json()
                            bot_reply = answer.get("answer", "No answer found.")
                            st.markdown(bot_reply)
                
                # Add assistant message to state
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})

    except Exception as e:
        st.error("⚠️ System encountered an unexpected error during processing.")
        st.write(e)