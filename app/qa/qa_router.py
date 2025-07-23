# app/qa/qa_router.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.qa.pdf_processor import extract_text_from_pdf
from app.qa.vector_store import create_vector_store, query_vector_store
import tempfile

router = APIRouter()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp_path = tmp.name

        full_text = extract_text_from_pdf(tmp_path)
        create_vector_store(full_text)
        return {"message": "PDF ingested successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF ingestion failed: {e}")


@router.post("/ask/")
async def ask_question(question: str = Form(...)):
    try:
        answer = query_vector_store(question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question failed: {e}")
