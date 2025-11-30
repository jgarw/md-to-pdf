from fastapi import FastAPI, UploadFile, Request, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .converter import convert_md_to_pdf
from .qr_generator import generate_qr_code
from .mail import send_qr_email
import os, uuid

app = FastAPI()

# adjust path to be relative to where docker runs from
static_path = os.path.join(os.path.dirname(__file__), "..", "static")
os.makedirs(static_path, exist_ok=True)

# mount static files
app.mount("/static", StaticFiles(directory=static_path), name="static")

# serve index.html at root
@app.get("/")
async def read_root():
    return FileResponse(os.path.join(static_path, "index.html"))

# function to convert md to pdf 
@app.post("/convert/")
async def convert(request: Request, file: UploadFile, email: str = Form(None)):
    
    # create directories 
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # create unique file name to avoid overwriting files    
    file_id = str(uuid.uuid4())[:8]

    input_path = f"uploads/{file_id}.md"
    output_path = f"outputs/{file_id}.pdf"

    # save uploaded file contents into new uuid filename
    with open(input_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    # convert md to pdf, storing pdf in output_path
    convert_md_to_pdf(input_path, output_path)

    if email:
        # get base url of service
        base_url = f"{request.url.scheme}://{request.headers.get('host', request.client.host)}"
        download_url = f"{base_url}/download/{file_id}"
        qr_path = generate_qr_code(file_id, base_url)
        send_qr_email(file_id, qr_path, download_url, email)

    # return generated pdf
    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename=f"{file_id}.pdf",
    )    

# function to download specific file from route
@app.get("/download/{file_id}")
async def download(file_id: str):

    output_path = f"outputs/{file_id}.pdf"

    if not os.path.exists(output_path):
        return {"error": "File not found"}
    
    # return generated pdf
    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename=f"{file_id}.pdf",
    )    
