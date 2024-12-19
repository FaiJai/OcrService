# Introduction

I would like to extend our heartfelt gratitude to [straussmaximilian](https://github.com/straussmaximilian/ocrmac?tab=readme-ov-file) for creating the outstanding project, ocrmac. This project has been a significant contribution to the community, showcasing exceptional skill and dedication.

This repository integrates the ocrmac project with a FastAPI application, providing a seamless and efficient solution for optical character recognition (OCR) tasks.

# Note:

-   This code can only be run on MacOS.
-   It cannot be run inside a Docker image.

# Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/mac_ocr.git
    cd mac_ocr
    ```

1. Create a .env file

    ```.env
    PYTHONPATH=src
    ```

1. [Optional] Create and enter a Python virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

1. Install the required dependencies:

    ```sh
    pip install -r requirements.txt
    ```

1. Install poppler

    Homebrew

    ```sh
    brew install poppler
    ```

1. Run the application:
    ```sh
    python main.py
    ```

# How to use

1. Call the API endpoint `/ocr`:

    - The file should be a PDF file inside form-data, with the key `files`.
    - OR
    - List of images inside form data, with the key `files`.

2. Use Swagger:
    - Navigate to `http://127.0.0.1:8000/docs` in your browser to access the Swagger UI.
    - Use the interactive API documentation to test the `/ocr` endpoint.
