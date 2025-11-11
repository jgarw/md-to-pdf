from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from converter import convert_md_to_pdf
import os, uuid

app = FastAPI()

# function to convert md to pdf 
@app.post("/convert/")
async def convert(file: UploadFile):
    
    # create directories 
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # create unique file name to avoid overwriting files    
    file_id = str(uuid.uuid4())[:8]

    input_path = f"uploads/{file_id}.md"
    output_path = f"outputs/{file_id}.pdf"

    with open(input_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    convert_md_to_pdf(input_path, output_path)

    # return generated pdf
    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename=f"{file_id}.pdf",
    )    
