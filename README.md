OVERVIEW

This project helps users analyze and simplify legal documents using AI. The application processes legal text and generates AI-based summaries and responses using locally running Large Language Models (LLMs).
The system uses Ollama for local model inference instead of external cloud APIs.

FEATURES

Upload and process legal documents
AI-generated summaries and explanations
Natural language interaction with documents
Local LLM inference using Ollama
Interactive Streamlit interface
NLP-powered text processing

TECH STACK
Python
NLP
Generative AI
Ollama
Streamlit

WORKING

User uploads a legal document.
The document text is processed using NLP techniques.
The application sends prompts to a locally running LLM through Ollama.
The model generates summaries and responses based on the document content.
Results are displayed through the Streamlit interface.

INSTALLATION

1. Clone the Repository
git clone
https://github.com/Yashu123403/AI-Legal-Document-Action-Agent.git
cd AI-Legal-Document-Action-Agent

2. Create Virtual Environment
python -m venv venv

Activate the environment:
Windows
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Install Ollama
ollama.com⁠

5. Pull a Model
ollama pull llama3

6. Run Ollama
ollama serve

7. Start the Application
streamlit run app.pyLearning Outcomes


LEARNING OUTCOMES
Natural Language Processing
Generative AI workflows
Local LLM integration
Streamlit application development

AUTHOR
YASHU A.B.
