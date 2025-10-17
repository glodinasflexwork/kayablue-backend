from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import io
import subprocess
import tempfile
import os
from pathlib import Path

app = FastAPI(
    title="KAYABLUE Backend API",
    description="Backend API for PDF processing and other tools",
    version="1.0.0"
)

# CORS configuration - allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.kayablue.nl",
        "https://kayablue.vercel.app",
        "http://localhost:5173",  # Local development
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "KAYABLUE Backend API",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    # Check if Ghostscript is available
    gs_available = False
    try:
        result = subprocess.run(
            ["gs", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        gs_available = result.returncode == 0
    except Exception:
        pass
    
    return {
        "status": "healthy",
        "ghostscript_available": gs_available,
        "endpoints": {
            "compress_pdf": "/api/compress-pdf",
            "health": "/health"
        }
    }

@app.post("/api/compress-pdf")
async def compress_pdf(
    file: UploadFile = File(...),
    quality: str = "medium"  # low, medium, high
):
    """
    Compress a PDF file using Ghostscript
    
    Parameters:
    - file: PDF file to compress
    - quality: Compression quality level (low, medium, high)
    
    Returns:
    - Compressed PDF file
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Map quality levels to Ghostscript settings
    quality_settings = {
        "low": "/screen",      # 72 dpi - maximum compression
        "medium": "/ebook",    # 150 dpi - balanced
        "high": "/printer"     # 300 dpi - minimal compression
    }
    
    pdf_setting = quality_settings.get(quality, "/ebook")
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as input_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output_file:
            try:
                # Save uploaded file
                content = await file.read()
                input_file.write(content)
                input_file.flush()
                
                input_path = input_file.name
                output_path = output_file.name
                
                # Run Ghostscript compression
                gs_command = [
                    "gs",
                    "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.4",
                    f"-dPDFSETTINGS={pdf_setting}",
                    "-dNOPAUSE",
                    "-dQUIET",
                    "-dBATCH",
                    "-dDetectDuplicateImages=true",
                    "-dCompressFonts=true",
                    "-r150",  # Resolution
                    f"-sOutputFile={output_path}",
                    input_path
                ]
                
                # Execute compression
                result = subprocess.run(
                    gs_command,
                    capture_output=True,
                    text=True,
                    timeout=60  # 60 second timeout
                )
                
                if result.returncode != 0:
                    raise HTTPException(
                        status_code=500,
                        detail=f"PDF compression failed: {result.stderr}"
                    )
                
                # Read compressed file
                with open(output_path, 'rb') as f:
                    compressed_content = f.read()
                
                # Calculate sizes
                original_size = len(content)
                compressed_size = len(compressed_content)
                reduction = ((original_size - compressed_size) / original_size) * 100
                
                # Return compressed PDF with metadata in headers
                return StreamingResponse(
                    io.BytesIO(compressed_content),
                    media_type="application/pdf",
                    headers={
                        "Content-Disposition": f"attachment; filename=compressed_{file.filename}",
                        "X-Original-Size": str(original_size),
                        "X-Compressed-Size": str(compressed_size),
                        "X-Size-Reduction": f"{reduction:.2f}",
                    }
                )
                
            except subprocess.TimeoutExpired:
                raise HTTPException(
                    status_code=504,
                    detail="PDF compression timed out. File may be too large."
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error processing PDF: {str(e)}"
                )
            finally:
                # Clean up temporary files
                try:
                    os.unlink(input_path)
                except:
                    pass
                try:
                    os.unlink(output_path)
                except:
                    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

