from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from typing import List, Optional
import os
import json
from datetime import datetime
import re

app = FastAPI(title="Smart Resume Screener API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
candidates_db = []

# Import our modules
from resume_parser import parse_resume
from llm_matcher import match_candidate_with_job

@app.get("/")
async def root():
    return {"message": "Smart Resume Screener API", "status": "running"}

@app.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Upload and process a resume against a job description"""
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.txt')):
            raise HTTPException(400, "Only PDF and TXT files supported")
        
        # Read file content
        content = await file.read()
        
        # Parse resume
        parsed_data = parse_resume(content, file.filename)
        
        # Match with job description using LLM
        match_result = match_candidate_with_job(parsed_data, job_description)
        
        # Store in database
        candidate_record = {
            "id": len(candidates_db) + 1,
            "filename": file.filename,
            "uploaded_at": datetime.now().isoformat(),
            "parsed_data": parsed_data,
            "match_score": match_result["score"],
            "justification": match_result["justification"],
            "job_description": job_description
        }
        
        candidates_db.append(candidate_record)
        
        return JSONResponse({
            "success": True,
            "candidate_id": candidate_record["id"],
            "match_score": match_result["score"],
            "justification": match_result["justification"],
            "parsed_data": parsed_data
        })
    
    except Exception as e:
        raise HTTPException(500, f"Error processing resume: {str(e)}")

@app.get("/candidates")
async def get_candidates(min_score: Optional[int] = 0):
    """Get all candidates filtered by minimum score"""
    filtered = [c for c in candidates_db if c["match_score"] >= min_score]
    sorted_candidates = sorted(filtered, key=lambda x: x["match_score"], reverse=True)
    return {"candidates": sorted_candidates}

@app.get("/candidate/{candidate_id}")
async def get_candidate(candidate_id: int):
    """Get specific candidate details"""
    candidate = next((c for c in candidates_db if c["id"] == candidate_id), None)
    if not candidate:
        raise HTTPException(404, "Candidate not found")
    return candidate

@app.delete("/candidate/{candidate_id}")
async def delete_candidate(candidate_id: int):
    """Delete a candidate"""
    global candidates_db
    candidates_db = [c for c in candidates_db if c["id"] != candidate_id]
    return {"success": True, "message": "Candidate deleted"}

@app.post("/batch-upload")
async def batch_upload(
    files: List[UploadFile] = File(...),
    job_description: str = Form(...)
):
    """Upload multiple resumes at once"""
    results = []
    
    for file in files:
        try:
            content = await file.read()
            parsed_data = parse_resume(content, file.filename)
            match_result = match_candidate_with_job(parsed_data, job_description)
            
            candidate_record = {
                "id": len(candidates_db) + 1,
                "filename": file.filename,
                "uploaded_at": datetime.now().isoformat(),
                "parsed_data": parsed_data,
                "match_score": match_result["score"],
                "justification": match_result["justification"],
                "job_description": job_description
            }
            
            candidates_db.append(candidate_record)
            results.append({
                "filename": file.filename,
                "success": True,
                "score": match_result["score"]
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {"results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)