import qrcode

# function to generate a qr code image from a file donwload url
def generate_qr_code(file_id: str):
    # create full download route using file_id
    download_url = f"http://192.168.68.111:8000/download/{file_id}"
    # keep qr code images organized with file ids 
    qr_path = f"outputs/{file_id}_qr.png"

    # create qr code from download route
    img = qrcode.make(download_url)

    # save qr code image
    img.save(qr_path)