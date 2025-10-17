# KAYABLUE Backend API

Backend API for KAYABLUE PDF processing and other tools.

## Features

- **PDF Compression** - Reduce PDF file sizes using Ghostscript
- **CORS Enabled** - Ready for frontend integration
- **Health Checks** - Monitor service status
- **Fast & Scalable** - Built with FastAPI

## Tech Stack

- **Framework:** FastAPI
- **Server:** Uvicorn
- **PDF Processing:** Ghostscript
- **Deployment:** Railway

## API Endpoints

### Health Check
```
GET /
GET /health
```

### PDF Compression
```
POST /api/compress-pdf
Content-Type: multipart/form-data

Parameters:
- file: PDF file (required)
- quality: "low" | "medium" | "high" (optional, default: "medium")

Response Headers:
- X-Original-Size: Original file size in bytes
- X-Compressed-Size: Compressed file size in bytes
- X-Size-Reduction: Percentage reduction
```

## Local Development

### Prerequisites
- Python 3.10+
- Ghostscript

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ghostscript:
```bash
# Ubuntu/Debian
sudo apt-get install ghostscript

# macOS
brew install ghostscript
```

3. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Test the API

```bash
# Health check
curl http://localhost:8000/health

# Compress PDF
curl -X POST http://localhost:8000/api/compress-pdf \
  -F "file=@test.pdf" \
  -F "quality=medium" \
  --output compressed.pdf
```

## Deployment on Railway

### Quick Deploy

1. Create a new project on [Railway](https://railway.app)
2. Connect this GitHub repository
3. Railway will automatically detect the configuration
4. Deploy!

### Environment Variables

No environment variables required for basic operation.

Optional:
- `PORT` - Server port (Railway sets this automatically)

### Configuration Files

- `railway.json` - Railway deployment config
- `nixpacks.toml` - Package dependencies (includes Ghostscript)
- `requirements.txt` - Python dependencies

## Compression Quality Levels

- **Low** (`/screen`) - 72 dpi, maximum compression, smallest file
- **Medium** (`/ebook`) - 150 dpi, balanced compression and quality
- **High** (`/printer`) - 300 dpi, minimal compression, best quality

## CORS Configuration

The API allows requests from:
- `https://www.kayablue.nl`
- `https://kayablue.vercel.app`
- `http://localhost:5173` (local development)
- `http://localhost:3000` (local development)

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `400` - Bad request (invalid file type)
- `500` - Server error (compression failed)
- `504` - Timeout (file too large)

## Performance

- Typical compression time: 1-5 seconds
- Maximum file size: Limited by Railway plan
- Timeout: 60 seconds per request

## Future Features

- Resume builder API
- PDF to Images conversion
- Images to PDF conversion
- Batch processing
- User authentication

## License

MIT

## Support

For issues or questions, please open an issue on GitHub.

