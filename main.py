import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile
import pandas as pd
import pdfplumber
from groq import Groq
import io

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


import pytesseract
from pdf2image import convert_from_bytes

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

import json

import fitz

rag_cache = {}

model = SentenceTransformer('all-MiniLM-L6-v2')


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI()

model = SentenceTransformer('all-MiniLM-L6-v2')


DOCUMENT_TEXT = ""

CHUNKS = []
INDEX = None

def create_chunks(text, size=500):
    return [text[i:i+size] for i in range(0, len(text), size)]


def read_pdf(file_bytes):
    text = ""
    try:
        # Fast text extraction using PyMuPDF
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text() + "\n"
            
        # Fallback to OCR if no text found (e.g. scanned image PDFs)
        if not text.strip():
            print("No text found, falling back to OCR...")
            images = convert_from_bytes(file_bytes)
            for i, img in enumerate(images):
                page_text = pytesseract.image_to_string(img)
                text += page_text + "\n"
    except Exception as e:
        print("PDF Extraction Error:", e)

    return text

def highlight_text_in_pdf(file_bytes, answer):
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    for page in doc:
        text_instances = page.search_for(answer[:50])  # partial match

        for inst in text_instances:
            page.add_highlight_annot(inst)

    output_path = "highlighted.pdf"
    doc.save(output_path)

    return output_path

def read_excel(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes))
    return df.to_string()


def build_index(text):

    sentences = text.split(". ")
    chunks = []

    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < 500:
            chunk += sentence + ". "
        else:
            chunks.append(chunk)
            chunk = sentence

    if chunk:
        chunks.append(chunk)

    embeddings = model.encode(chunks, batch_size=16)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    return index, chunks

def search_index(index, chunks, query):
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), k=3)

    results = [chunks[i] for i in I[0]]
    return "\n".join(results)


@app.post("/analyze")
async def analyze(file: UploadFile):

    global DOCUMENT_TEXT

    file_bytes = await file.read()

    if file.filename.endswith(".pdf"):
        DOCUMENT_TEXT = read_pdf(file_bytes)

    elif file.filename.endswith(".xlsx"):
        DOCUMENT_TEXT = read_excel(file_bytes)

    else:
        return {"error": "Unsupported file type"}

    content = DOCUMENT_TEXT

    print("TOTAL CONTENT LENGTH:", len(content))

    if not content.strip():
        return {"result": "⚠️ No readable text found in file"}
    
   
    global CHUNKS, INDEX

    CHUNKS = create_chunks(DOCUMENT_TEXT)

    embeddings = model.encode(CHUNKS)

    dimension = embeddings.shape[1]
    INDEX = faiss.IndexFlatL2(dimension)
    INDEX.add(np.array(embeddings))

    prompt = f"""
You are a financial analyst.

STRICT RULES:
- Only use information from the document
- Do NOT make up data
- If missing, say "Not mentioned"

Extract:
1. Key insights
2. Important numbers
3. Business highlights
4. Risks

Explain in simple words.

DOCUMENT:
{content[:15000]}
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )

        result = chat_completion.choices[0].message.content

    except Exception as e:
        return {"result": f"❌ AI Error: {str(e)}"}

    return {"result": result}



@app.post("/chat")
async def chat(question: str):

    global CHUNKS, INDEX

    if INDEX is None:
        return {"answer": "⚠️ Please analyze a document first"}

    query_embedding = model.encode([question])

    D, I = INDEX.search(np.array(query_embedding), k=3)

    relevant_chunks = [CHUNKS[i] for i in I[0]]

    context = "\n".join(relevant_chunks)

    prompt = f"""
Answer ONLY from the context.

CONTEXT:
{context}

QUESTION:
{question}
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    return {"answer": chat_completion.choices[0].message.content}

@app.post("/extract-numbers")
async def extract_numbers():

    global DOCUMENT_TEXT

    if not DOCUMENT_TEXT:
        return {"data": {}}

    prompt = f"""
Extract ONLY financial metrics from the document.

IGNORE:
- Dates
- ZIP codes
- IDs
- Serial numbers

ONLY INCLUDE:
- Revenue
- Profit
- Cost
- Growth %
- Financial amounts

Return STRICT JSON:
{{
  "Revenue": 100,
  "Profit": 20
}}

DOCUMENT:
{DOCUMENT_TEXT[:15000]}
"""

    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant"
        )

        text = chat_completion.choices[0].message.content.strip()

        print("RAW LLM OUTPUT:", text)  # 🔥 DEBUG

        return {"data": text}

    except Exception as e:
        return {"data": str(e)}
    

@app.post("/suggest-chart")
async def suggest_chart():

    global DOCUMENT_TEXT

    prompt = f"""
Return ONLY JSON.

NO explanation.
NO text outside JSON.

Format:
{{
  "type": "bar",
  "data": {{"Revenue": 100, "Cost": 50}}
}}

DOCUMENT:
{DOCUMENT_TEXT[:15000]}
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    return {"data": chat_completion.choices[0].message.content}

@app.post("/extract-kpis")
async def extract_kpis(file: UploadFile):

    file_bytes = await file.read()

    if file.filename.endswith(".pdf"):
        content = read_pdf(file_bytes)
    else:
        return {"error": "Only PDF supported"}

    prompt = f"""
Extract ONLY financial KPIs.

STRICT:
- Return ONLY JSON
- No explanation
- No markdown
- No trailing commas

Example:
{{
  "Revenue": "27.2 billion",
  "Profit": "489 million",
  "Growth": "51%",
  "Cost": "4.8 billion"
}}

DOCUMENT:
{content[:6000]}
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    result = chat_completion.choices[0].message.content

    return {"data": result}

@app.post("/multi-chat")
async def multi_chat(question: str, files: list[UploadFile]):

    all_text = ""

    for file in files:
        file_bytes = await file.read()
        all_text += read_pdf(file_bytes)

    doc_hash = hash(all_text)

    if doc_hash in rag_cache:
        index, chunks = rag_cache[doc_hash]
    else:
        index, chunks = build_index(all_text)
        rag_cache[doc_hash] = (index, chunks)

    context = search_index(index, chunks, question)

    kpi_response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"""
    Extract key financial KPIs from this document.

    Return ONLY JSON.

    DOCUMENT:
    {all_text[:4000]}
    """
        }],
        model="llama-3.1-8b-instant"
    )

    raw_kpi = kpi_response.choices[0].message.content


    clean_kpi = raw_kpi.replace("```json", "").replace("```", "").strip()

    try:
        kpis = json.loads(clean_kpi)
    except:
        kpis = {}


    kpi_text = "\n".join([f"{key}: {value}" for key, value in kpis.items()])

    prompt = f"""
You are a financial analyst.

Use CONTEXT + KPIs.

CONTEXT:
{context}

KPIs:
{kpi_text}

QUESTION:
{question}

Rules:
- Answer ONLY from context
- Use KPI numbers if relevant
- Be precise
"""

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant"
    )

    return {"answer": chat_completion.choices[0].message.content}