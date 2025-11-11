import subprocess

def convert_md_to_pdf(inputFile, outputFile):
    subprocess.run(["pandoc", inputFile, "-o", outputFile], check=True)