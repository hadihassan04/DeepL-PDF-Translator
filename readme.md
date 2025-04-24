# PDF Translation with DeepL API

This script translates PDF documents from one language to another using the DeepL API. It supports both **scanned PDFs** (through OCR) and regular PDFs. Files larger than the max API file size limit (10MB for free users, 30MB for paid users) will be skipped and logged.

## Features

- **OCR Support** for scanned PDFs (DeepL automatically handles OCR).
- **File Size Check**: Automatically skips PDFs that exceed the size limit (10MB for free users, 30MB for paid users).
- **Logging**: Skipped files (either due to size or errors) are logged into a separate text file (`skipped_files.txt`).
- **Output**: Translated PDFs are saved to the output directory, preserving their original format.

## Requirements

- Python 3.7 or later
- DeepL API key (Free or Paid version)

## Installation

1. **Clone this repository** (or download the script):

    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Set your DeepL API Key**:
   
    You need to set your DeepL API key as an environment variable. If you're using the Free API, the key should end with `:fx`.

    On Windows:
    - For Command Prompt (CMD):
        ```bash
        set DEEPL_API_KEY=your_api_key_here
        ```

    - For PowerShell:
        ```powershell
        $env:DEEPL_API_KEY = "your_api_key_here"
        ```

    On Linux/macOS:
    - Add the following line to your `~/.bashrc` or `~/.zshrc` file:
        ```bash
        export DEEPL_API_KEY="your_api_key_here"
        ```

4. **Run the Script**:

    ```bash
    python translate_pdfs.py <input_directory> <output_directory> --target_lang EN --log_file skipped_files.txt
    ```

    - Replace `<input_directory>` with the path to the folder containing PDFs to translate.
    - Replace `<output_directory>` with the path where translated PDFs will be saved.
    - Optionally, specify the `--log_file` flag to specify a custom log file for skipped files.
    - Optionally, specify the target language using the `--target_lang` flag (default is `EN`).

## Example:

```bash
python translate_pdfs.py ./pdfs ./translated_pdfs --target_lang EN --log_file skipped_files.txt
