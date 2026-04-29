# FinDash Pro - Enterprise Financial Dashboard

FinDash Pro is an advanced, AI-powered financial dashboard designed to automatically analyze financial documents (PDFs and Excel files), extract core metrics (KPIs), generate visual analytics, and provide a secure, interactive intelligence hub for asking questions about your data.

It features a sleek, premium, "glassmorphism" user interface using **Streamlit** and a robust, high-performance backend powered by **FastAPI**, **FAISS**, and **Groq (LLaMA 3.1)**.

## 🌟 Features
- **Automated KPI Extraction:** Automatically extracts key performance indicators (Revenue, Profit, Growth, etc.) from financial documents using LLaMA 3.1.
- **AI-Powered Executive Summary:** Generates comprehensive insights, business highlights, and risk factors strictly derived from the uploaded documents.
- **Interactive Visual Analytics:** Dynamically creates Plotly-based Bar and Area charts based on the extracted numerical metrics.
- **Document Intelligence (RAG Chat):** Uses `sentence-transformers` and `FAISS` to embed document chunks and provide precise, context-aware answers to user queries.
- **Hybrid PDF Processing:** Extracts text efficiently via `PyMuPDF` with a fallback to OCR (`pytesseract`) for scanned images.

## 🛠️ Technology Stack
- **Frontend:** Streamlit, Plotly
- **Backend:** FastAPI, Uvicorn, Python
- **AI/LLM:** Groq API (LLaMA-3.1-8b-instant)
- **RAG & Embeddings:** Sentence Transformers (`all-MiniLM-L6-v2`), FAISS
- **Document Parsing:** PyMuPDF, pdf2image, pytesseract, pandas
- **Environment Management:** python-dotenv

## ⚙️ Installation Prerequisites
Before running the application, ensure you have the following installed on your system:
1. **Python 3.9+**
2. **Tesseract-OCR**: Required for scanning images/PDFs. 
   - Download and install from [UB-Mannheim Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
   - Ensure it is installed at the default path: `C:\Program Files\Tesseract-OCR\tesseract.exe` (or update `main.py` if installed elsewhere).
3. **Poppler**: Required by `pdf2image`. Download and add it to your System PATH.

## 🚀 Setup & Installation

**1. Clone the repository and navigate to the directory:**
```bash
cd Financial_dashboard
```

**2. Create and activate a Virtual Environment:**
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

**3. Install Python Dependencies:**
*(If a `requirements.txt` is missing, you can install the necessary packages manually)*:
```bash
pip install fastapi uvicorn streamlit pandas pdfplumber groq sentence-transformers faiss-cpu numpy pytesseract pdf2image python-dotenv pymupdf plotly requests openpyxl python-multipart
```

**4. Configure Environment Variables:**
Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## 🏃 Running the Application

To run the application, you must start both the backend server and the frontend interface.

**1. Start the Backend Server (FastAPI):**
Open a terminal, ensure your virtual environment is active, and run:
```bash
python -m uvicorn main:app --port 8000 --reload
```
*Note: On the first run, the backend will download the Sentence-Transformer model, which may take a minute.*

**2. Start the Frontend (Streamlit):**
Open a **new** terminal, activate the virtual environment, and run:
```bash
python -m streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`.

## 📖 Usage
1. Open the dashboard in your web browser.
2. In the left sidebar, drag and drop one or multiple Financial PDF documents.
   For testing some of the example documents are provided please click on the following links:
         * "https://drive.google.com/file/d/1lOLyaDs-685BVt32GIKmj6U6PgUVQKzV/view?usp=drivesdk"
         * "https://drive.google.com/file/d/1ujyhYI4WXvizgpx5tPwsT6iSkviU3x1L/view?usp=drivesdk"
         * "https://drive.google.com/file/d/1Z47VYnHQkS_kWGMO5OWEwlhfAN25YOeG/view?usp=drivesdk"
3. Wait for the backend to process the document and extract KPIs.
4. Explore the **Executive Summary** and **Visual Analytics** tabs.
5. Use the **Document Intelligence** chat on the right to query the contents of your documents.

## 📝 License
This project is proprietary and built for enterprise financial analysis.
