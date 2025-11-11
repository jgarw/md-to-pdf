import subprocess

def convert_md_to_pdf(inputFile, outputFile):
    subprocess.run([
        "pandoc",
        inputFile,
        "-o", outputFile,
        "--pdf-engine=xelatex",
        "--from", "markdown",
        "--highlight-style=tango",
        "--variable", "mainfont=Liberation Mono",
        "--variable", "fontsize=12pt",
        "--variable", "geometry=margin=1in",
        "--standalone"
    ], check=True)