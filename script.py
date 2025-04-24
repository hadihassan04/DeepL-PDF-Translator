import os
import time
import requests
from pathlib import Path
from tqdm import tqdm

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
if not DEEPL_API_KEY:
    raise EnvironmentError("Please set the DEEPL_API_KEY environment variable.")

# Determine the appropriate API endpoint based on the API key
if DEEPL_API_KEY.endswith(":fx"):
    API_URL = "https://api-free.deepl.com/v2"
else:
    API_URL = "https://api.deepl.com/v2"

def translate_pdf(file_path, output_path, target_lang="EN"):
    with open(file_path, "rb") as f:
        files = {
            "file": (file_path.name, f, "application/pdf")
        }
        data = {
            "target_lang": target_lang
        }
        headers = {
            "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
        }
        # Step 1: Upload the document
        response = requests.post(f"{API_URL}/document", headers=headers, files=files, data=data)
        response.raise_for_status()
        result = response.json()
        document_id = result["document_id"]
        document_key = result["document_key"]

    # Step 2: Check the document status
    status_url = f"{API_URL}/document/{document_id}"
    params = {
        "document_key": document_key
    }
    while True:
        status_response = requests.get(status_url, headers=headers, params=params)
        status_response.raise_for_status()
        status = status_response.json()
        if status["status"] == "done":
            break
        elif status["status"] == "error":
            raise Exception(f"Translation failed: {status['message']}")
        time.sleep(5)  # Wait before checking the status again

    # Step 3: Download the translated document
    download_url = f"{API_URL}/document/{document_id}/result"
    download_response = requests.get(download_url, headers=headers, params=params)
    download_response.raise_for_status()
    with open(output_path, "wb") as out_file:
        out_file.write(download_response.content)

def process_directory(input_dir, output_dir, target_lang="EN"):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    pdf_files = list(input_path.rglob("*.pdf"))
    for pdf_file in tqdm(pdf_files, desc="Translating PDFs"):
        relative_path = pdf_file.relative_to(input_path)
        output_file = output_path / relative_path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            translate_pdf(pdf_file, output_file, target_lang=target_lang)
        except Exception as e:
            print(f"Failed to translate {pdf_file}: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate scanned PDFs using DeepL API.")
    parser.add_argument("input_dir", help="Directory containing PDF files to translate.")
    parser.add_argument("output_dir", help="Directory to save translated PDF files.")
    parser.add_argument("--target_lang", default="EN", help="Target language code (e.g., 'EN' for English).")
    args = parser.parse_args()
    process_directory(args.input_dir, args.output_dir, target_lang=args.target_lang)
