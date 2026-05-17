"""
LAYER 4: UI - COMPLETE LEGAL AI FRAMEWORK
"""

import streamlit as st
from pypdf import PdfReader
from layer2_agents import SummarizerAgent, RiskAgent, NegotiationAgent, ComparisonAgent, LawsAgent
import nltk

for resource in ['punkt']:
    try:
        nltk.data.find(f'tokenizers/{resource}')
    except:
        nltk.download(resource, quiet=True)

st.set_page_config(page_title="Decisive Legal AI", page_icon="⚖️", layout="wide")

st.title("⚖️ DECISIVE LEGAL AI FRAMEWORK")
st.caption("🔥 4-Layer Agentic Architecture | FIRM Decisions | NEVER says 'consult a lawyer'")

# Initialize agents
if "summarizer" not in st.session_state:
    st.session_state.summarizer = SummarizerAgent()
if "risk_agent" not in st.session_state:
    st.session_state.risk_agent = RiskAgent()
if "negotiation_agent" not in st.session_state:
    st.session_state.negotiation_agent = NegotiationAgent()
if "comparison_agent" not in st.session_state:
    st.session_state.comparison_agent = ComparisonAgent()
if "laws_agent" not in st.session_state:
    st.session_state.laws_agent = LawsAgent()

# Document storage
if "doc1_text" not in st.session_state:
    st.session_state.doc1_text = ""
    st.session_state.doc1_name = ""
if "doc2_text" not in st.session_state:
    st.session_state.doc2_text = ""
    st.session_state.doc2_name = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar
with st.sidebar:
    st.header("📄 DOCUMENT 1")
    uploaded1 = st.file_uploader("Upload PDF or TXT", type=["pdf", "txt"], key="doc1")
    
    if uploaded1:
        if uploaded1.type == "application/pdf":
            reader = PdfReader(uploaded1)
            text = "".join([page.extract_text() for page in reader.pages])
        else:
            text = uploaded1.read().decode("utf-8")
        
        st.session_state.doc1_text = text
        st.session_state.doc1_name = uploaded1.name
        st.success(f"✅ Loaded: {uploaded1.name}")
    
    st.divider()
    st.header("📄 DOCUMENT 2 (For Comparison)")
    uploaded2 = st.file_uploader("Upload Second Document", type=["pdf", "txt"], key="doc2")
    
    if uploaded2:
        if uploaded2.type == "application/pdf":
            reader = PdfReader(uploaded2)
            text = "".join([page.extract_text() for page in reader.pages])
        else:
            text = uploaded2.read().decode("utf-8")
        
        st.session_state.doc2_text = text
        st.session_state.doc2_name = uploaded2.name
        st.success(f"✅ Loaded: {uploaded2.name}")
    
    st.divider()
    if st.session_state.doc1_text:
        st.info(f"📄 Doc 1: {st.session_state.doc1_name[:30]}")
    if st.session_state.doc2_text:
        st.info(f"📄 Doc 2: {st.session_state.doc2_name[:30]}")

# Chat Section
st.header("💬 ASK THE AI")
st.caption("Ask anything - I give FIRM YES/NO answers")

for role, message in st.session_state.chat_history[-5:]:
    with st.chat_message(role):
        st.markdown(message)

col1, col2 = st.columns([4, 1])
with col1:
    question = st.text_input("", placeholder="Ask: 'Should I sign?' | 'What are the risks?'", key="chat_input", label_visibility="collapsed")
with col2:
    ask_button = st.button("ASK", type="primary", use_container_width=True)

if ask_button and question:
    if not st.session_state.doc1_text:
        st.warning("Upload a document first")
    else:
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            with st.spinner("Making FIRM decision..."):
                from layer2_agents import DecisionAgent
                decision_agent = DecisionAgent()
                response = decision_agent.decide(st.session_state.doc1_text, question)
                st.markdown(response)
                st.session_state.chat_history.append(("user", question))
                st.session_state.chat_history.append(("assistant", response))
                st.rerun()

st.divider()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📋 SUMMARY & RISKS", "🔥 NEGOTIATION", "🔄 COMPARISON", "⚖️ RELEVANT LAWS"])

# ============================================
# TAB 1: SUMMARY & RISKS - FIXED
# ============================================
with tab1:
    if st.session_state.doc1_text:
        # Check if we have second document
        has_doc2 = bool(st.session_state.doc2_text)
        
        if has_doc2:
            # Two columns when both documents exist
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader(f"📄 {st.session_state.doc1_name}")
                
                if st.button("📝 SUMMARIZE", key="sum1_btn", use_container_width=True):
                    with st.spinner("Generating summary..."):
                        result = st.session_state.summarizer.summarize(st.session_state.doc1_text, st.session_state.doc1_name)
                        st.markdown("---")
                        st.markdown(result)
                        st.markdown("---")
                
                if st.button("⚠️ RISK ASSESSMENT", key="risk1_btn", use_container_width=True):
                    with st.spinner("Analyzing risks..."):
                        result = st.session_state.risk_agent.analyze(st.session_state.doc1_text, st.session_state.doc1_name)
                        st.markdown("---")
                        st.markdown(result)
                        st.markdown("---")
            
            with col_right:
                st.subheader(f"📄 {st.session_state.doc2_name}")
                
                if st.button("📝 SUMMARIZE", key="sum2_btn", use_container_width=True):
                    with st.spinner("Generating summary..."):
                        result = st.session_state.summarizer.summarize(st.session_state.doc2_text, st.session_state.doc2_name)
                        st.markdown("---")
                        st.markdown(result)
                        st.markdown("---")
                
                if st.button("⚠️ RISK ASSESSMENT", key="risk2_btn", use_container_width=True):
                    with st.spinner("Analyzing risks..."):
                        result = st.session_state.risk_agent.analyze(st.session_state.doc2_text, st.session_state.doc2_name)
                        st.markdown("---")
                        st.markdown(result)
                        st.markdown("---")
        else:
            # Single column when only one document exists
            st.subheader(f"📄 {st.session_state.doc1_name}")
            
            if st.button("📝 SUMMARIZE", key="sum1_btn", use_container_width=True):
                with st.spinner("Generating summary..."):
                    result = st.session_state.summarizer.summarize(st.session_state.doc1_text, st.session_state.doc1_name)
                    st.markdown("---")
                    st.markdown(result)
                    st.markdown("---")
            
            if st.button("⚠️ RISK ASSESSMENT", key="risk1_btn", use_container_width=True):
                with st.spinner("Analyzing risks..."):
                    result = st.session_state.risk_agent.analyze(st.session_state.doc1_text, st.session_state.doc1_name)
                    st.markdown("---")
                    st.markdown(result)
                    st.markdown("---")
            
            st.info("📄 Upload a second document for side-by-side comparison")
    else:
        st.warning("Upload a document to begin")

# ============================================
# TAB 2: NEGOTIATION
# ============================================
with tab2:
    if st.session_state.doc1_text:
        has_doc2 = bool(st.session_state.doc2_text)
        
        if has_doc2:
            col_left, col_right = st.columns(2)
            
            with col_left:
                st.subheader(f"🔥 {st.session_state.doc1_name}")
                if st.button("GET NEGOTIATION ADVICE", key="nego1_btn", use_container_width=True):
                    with st.spinner("Preparing negotiation strategy..."):
                        result = st.session_state.negotiation_agent.get_advice(st.session_state.doc1_text, st.session_state.doc1_name)
                        st.markdown("---")
                        st.markdown(result)
                        st.markdown("---")
            
            with col_right:
                st.subheader(f"🔥 {st.session_state.doc2_name}")
                if st.button("GET NEGOTIATION ADVICE", key="nego2_btn", use_container_width=True):
                    with st.spinner("Preparing negotiation strategy..."):
                        result = st.session_state.negotiation_agent.get_advice(st.session_state.doc2_text, st.session_state.doc2_name)
                        st.markdown("---")
                        st.markdown(result)
                        st.markdown("---")
        else:
            st.subheader(f"🔥 {st.session_state.doc1_name}")
            if st.button("GET NEGOTIATION ADVICE", key="nego1_btn", use_container_width=True):
                with st.spinner("Preparing negotiation strategy..."):
                    result = st.session_state.negotiation_agent.get_advice(st.session_state.doc1_text, st.session_state.doc1_name)
                    st.markdown("---")
                    st.markdown(result)
                    st.markdown("---")
            st.info("📄 Upload a second document for comparison")
    else:
        st.warning("Upload a document first")

# ============================================
# TAB 3: COMPARISON
# ============================================
with tab3:
    if st.session_state.doc1_text and st.session_state.doc2_text:
        if st.button("🏆 COMPARE & PICK WINNER", type="primary", use_container_width=True):
            with st.spinner("Comparing documents..."):
                result = st.session_state.comparison_agent.compare(
                    st.session_state.doc1_text,
                    st.session_state.doc2_text,
                    st.session_state.doc1_name,
                    st.session_state.doc2_name
                )
                st.markdown("---")
                st.markdown(result)
                st.markdown("---")
    else:
        st.info("📄 Upload TWO documents to enable comparison")

# ============================================
# TAB 4: RELEVANT LAWS
# ============================================
with tab4:
    if st.session_state.doc1_text:
        if st.button("📜 SHOW RELEVANT LAWS", use_container_width=True):
            with st.spinner("Finding relevant laws..."):
                result = st.session_state.laws_agent.get_relevant_laws(st.session_state.doc1_text, st.session_state.doc1_name)
                st.markdown("---")
                st.markdown(result)
                st.markdown("---")
    else:
        st.warning("Upload a document first")

st.divider()
st.caption("⚖️ **4-Layer Agentic Framework** | Layer 1: Tools | Layer 2: Agents | Layer 3: Orchestrator | Layer 4: UI")