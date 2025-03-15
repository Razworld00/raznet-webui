# Raznet WebUI Assistant

## Overview

The **Raznet WebUI Assistant** is an advanced, multimodal AI application built with [Chainlit](https://github.com/Chainlit/chainlit) and powered by [Ollama](https://ollama.ai/) models. This assistant integrates text processing, image description, web searching, web browsing, and PDF processing into a single, user-friendly interface. It leverages lightweight and efficient models such as `smollm`, `moondream:1.8b-v2-q3_K_S`, `llama3.1:latest`, and `llama3.2:1b` to provide a robust, scalable solution for diverse tasks.

This project supports real-time streaming responses (akin to ChatGPT), tool-calling for external searches and browsing, and a modular architecture. It is designed to run locally on modest hardware (e.g., 8GB RAM with 32GB swap) and is extensible with additional tools or models. Recent enhancements include PDF text extraction and summarization, with exciting new features on the horizon.

## Features

- **Text Processing:** Handles calculations, queries, and conversations using `llama3.1:latest` (or `smollm` for lighter usage).
- **Image Description:** Describes uploaded images with `moondream:1.8b-v2-q3_K_S`, a quantized vision-language model.
- **Web Searching:** Performs DuckDuckGo searches using `llama3.2:1b` with tool-calling.
- **Web Browsing:** Fetches and summarizes URLs using `llama3.2:1b`.
- **PDF Processing:** Extracts and summarizes text from PDFs using `PyPDF2` (with optional OCR support via `pytesseract` and `pdf2image`).
- **Streaming Responses:** Delivers real-time, professional-grade streaming for a seamless experience.
- **Modular Design:** Separated into `app.py`, `models.py`, and `tools.py` for maintainability.

## Upcoming Features

- **Code Execution:** Run Python snippets directly within the app (coming soon in Step 2).
- **OpenAI & Grok API Support:** Integrate with OpenAI and xAI's Grok models for enhanced capabilities (planned for future releases).
- **OCR for Image-Based PDFs:** Support for scanned documents using `pytesseract` and `pdf2image`.
- **Advanced Tooling:** Additional APIs (e.g., weather, calendar) and custom UI enhancements.
- Stay tuned for more exciting updates as the project evolves!

## Prerequisites

- **Operating System:** Linux (tested on Ubuntu), macOS, or Windows (with WSL).
- **Hardware:** Minimum 8GB RAM (32GB swap recommended), 10GB free disk space.
- **Software:**
  - Python 3.11 or higher.
  - [Ollama](https://ollama.ai/) (for local AI models).
  - Git (optional, for version control).

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/raznet-webui.git
cd raznet-webui/backend
2. Set Up the Virtual Environment

Create and activate a virtual environment:
bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies

Install the required Python packages:
bash
pip install -r requirements.txt
4. Install and Configure Ollama

    Install Ollama from https://ollama.ai.
    Pull the required models:
    bash

ollama pull llama3.1:latest
ollama pull moondream:1.8b-v2-q3_K_S
ollama pull llama3.2:1b
ollama pull smollm  # Adjust to specific variant if needed (e.g., smollm:1b)
Verify models are available:
bash

    ollama list

5. Start the Application

    Start the Ollama server:
    bash

ollama serve
Start the Chainlit app:
bash

    chainlit run app.py --host 0.0.0.0 --port 8001
    Open your browser and navigate to http://192.168.11.183:8001 (adjust IP if needed).

Usage
Welcome Message

Upon starting the app, you will see:
text
Welcome to Raznet WebUI Assistant!
- Type your text message to use App.
- Or upload an image and type 'describe'.
- Upload a PDF and use 'extract text from pdf' or 'summarize pdf'.
Supported Operations

    Text Processing:
        Type a message like "calculate 23+3*5" or "What is AI?".
        Uses llama3.1:latest to process and stream the response.
        Example: "The calculation follows PEMDAS: 3 * 5 = 15, 23 + 15 = 38. The final answer is 38."
    Image Description:
        Upload an image (via the paperclip icon).
        Type "describe" and send.
        Uses moondream:1.8b-v2-q3_K_S to stream a description.
        Example: "In the center of the image, a young man with short hair and a beard is captured in a moment of quiet contemplation..."
    Web Searching:
        Type "search for recent advancements in AI" and send.
        Uses llama3.2:1b with the DuckDuckGo tool to stream results.
        Example: "[Searching DuckDuckGo for: recent advancements in AI]... Search Results: - Title: AI Breakthroughs 2025: What’s New | Snippet: Recent advancements include... | URL: <link>"
    Web Browsing:
        Type "browse https://example.com" and send.
        Uses llama3.2:1b to fetch and stream a summary.
        Example: "[Browsing URL: https://example.com]... Web Content: This is an example page. The purpose of this domain is for illustrative examples in documents..."
    PDF Processing:
        Upload a PDF and type "extract text from pdf" or "summarize pdf".
        Extracts text using PyPDF2 and summarizes with llama3.2:1b if requested.
        Example: "[Processing PDF: /path/to/file.pdf]... PDF Content: [Extracted text]... [Summarizing PDF content]... [Summary]"

Tips for Best Performance

    Image Quality: Use clear, high-resolution images under 5MB. Resize large images with:
    bash

convert input.jpg -resize 800x800 output.jpg
Prompt Specificity: Use specific prompts (e.g., "What is the person wearing?") for better results.
Network Stability: Ensure a stable connection for web searches and browsing.
Resource Monitoring: Use htop to monitor RAM and CPU usage:
bash

    htop
        Expect ~1-2GB RAM per model.

Project Structure
text
~/raznet-webui/backend/
├── app.py              # Main Chainlit application with routing and streaming
├── models.py           # Model handlers for text, vision, and tool-calling
├── tools.py            # Tool definitions (DuckDuckGo search, web browsing, PDF processing)
├── requirements.txt    # Dependency list
├── LICENSE             # MIT License file
├── venv/               # Virtual environment
Code Documentation
Key Files

    app.py
        Routes user inputs to appropriate model handlers based on content (text, image, search, browse, PDF).
        Uses msg.stream_token for professional-grade streaming.
    models.py
        Defines process_text_stream, process_vision_stream, and process_tool_calling_stream with streaming support.
        Integrates llama3.1:latest (text), moondream:1.8b-v2-q3_K_S (vision), and llama3.2:1b (tool-calling).
    tools.py
        Implements duckduckgo_search for web searches.
        Implements browse_web for URL content fetching and summarization using beautifulsoup4, requests, and html2text.
        Implements process_pdf for PDF text extraction using PyPDF2.

Dependencies

    chainlit>=1.0.0: UI and streaming framework.
    ollama>=0.5.13: Local AI model server.
    duckduckgo-search>=6.2.0: Web search API.
    aiohttp>=3.9.0: Async HTTP client.
    pydantic>=2.0.0: Data validation.
    beautifulsoup4>=4.12.3: HTML parsing.
    requests>=2.31.0: Synchronous HTTP requests.
    lxml>=5.0.0: Faster HTML parser.
    html2text>=2020.1.16: HTML to plain text conversion.
    httpx>=0.27.0: Async HTTP client (future-proofing).
    python-socketio>=5.11.0: Real-time communication.
    PyPDF2>=3.0.1: PDF text extraction.
    Optional (for OCR):
        pdf2image>=1.16.3
        pytesseract>=0.3.10

Models

    llama3.1:latest: Text processing (~4.9GB).
    moondream:1.8b-v2-q3_K_S: Vision processing (~1-2GB).
    llama3.2:1b: Tool-calling (~1.3GB).
    smollm: Optional text processing (~990MB, switchable in code).

Troubleshooting
Common Issues

    Port Conflict (Ollama):
        Error: listen tcp 127.0.0.1:11434: bind: address already in use
        Fix:
        bash

    lsof -i :11434
    sudo fuser -k 11434/tcp
    ollama serve

Missing Modules:

    Error: ModuleNotFoundError
    Fix: Reinstall dependencies:
    bash

    pip install -r requirements.txt

No Response:

    Check Ollama logs and ensure models are loaded:
    bash

ollama list
Restart services:
bash

    sudo pkill -9 ollama
    sudo pkill -9 -f chainlit
    ollama serve
    chainlit run app.py --host 0.0.0.0 --port 8001

Streaming Issues:

    Ensure stream=True in models.py and Chainlit version is >=1.0.0:
    bash

        pip show chainlit

Contributing

We welcome contributions to enhance the Raznet WebUI Assistant! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

    Issues: Report bugs or suggest features by opening an issue.
    Pull Requests:
        Fork the repository.
        Create a feature branch (git checkout -b feature/awesome-feature).
        Commit your changes (git commit -m "Add awesome feature").
        Push to the branch (git push origin feature/awesome-feature).
        Open a pull request with a detailed description of your changes.
    Documentation: Update this README.md or add new files as needed.
    Code Style: Follow the existing code structure and add comments for clarity.
    Testing: Test your changes locally and ensure compatibility with the existing features.

Please ensure your contributions align with the project's MIT License and maintain its open-source spirit.
License

License: MIT

This project is licensed under the MIT License. See the LICENSE file for details.
Changelog

    March 15, 2025:
        Added llama3.2:1b for tool-calling with DuckDuckGo search.
        Integrated web browsing with browse_web tool using beautifulsoup4 and html2text.
        Updated to Chainlit latest version (1.x) with streaming support.
        Added new packages: lxml, html2text, httpx, python-socketio, PyPDF2.
        Modularized code into app.py, models.py, and tools.py.
        Added PDF processing with text extraction and summarization.
    Upcoming:
        Integration with OpenAI and Grok API functionality.
        Code execution for Python snippets.
        OCR support for image-based PDFs.

Contact

For support or inquiries, contact the project maintainer:

    Email: bathie28@gmail.com
    WhatsApp: +49 17615367330
    Maintainer: Bathandwa S.

text

---

### Changes Made

1. **Updated Overview:**
   - Added mention of PDF processing and recent enhancements.
   - Highlighted the project’s evolution and extensibility.

2. **Updated Features:**
   - Included "PDF Processing" with `PyPDF2` and optional OCR support.
   - Kept existing features and refined descriptions.

3. **Added Upcoming Features:**
   - Listed "Code Execution," "OpenAI & Grok API Support," "OCR for Image-Based PDFs," and "Advanced Tooling" as planned enhancements to generate excitement.

4. **Updated Prerequisites and Installation:**
   - Adjusted the port to `8001` to match your usage (`--port 8001`).
   - Clarified the IP address (`http://192.168.11.183:8001`) based on your setup.

5. **Updated Usage:**
   - Added PDF processing examples ("extract text from pdf" and "summarize pdf").
   - Kept tips for performance and refined them for clarity.

6. **Updated Project Structure:**
   - Added `LICENSE` to the structure.
   - Updated descriptions of key files to include PDF processing.

7. **Updated Dependencies:**
   - Added `PyPDF2>=3.0.1` to the dependency list.
   - Moved `pdf2image` and `pytesseract` to optional dependencies with version suggestions.
   - Updated versions to match your `requirements.txt` (e.g., `ollama==0.5.13`, `PyPDF2==3.0.1`).

8. **Enhanced Contributing Section:**
   - Added a professional GitHub-style contribution guide with steps for issues, pull requests, and documentation.
   - Encouraged alignment with the MIT License.

9. **Updated License Section:**
   - Added the MIT License badge and linked to the `LICENSE` file.
   - Referenced the recently created MIT License.

10. **Updated Changelog:**
    - Included the latest changes (PDF processing, new packages).
    - Added upcoming features to the changelog.

11. **General Improvements:**
    - Formatted with GitHub Markdown conventions (e.g., code blocks, links, badges).
    - Ensured a professional tone suitable for an open-source project.

---

### Step 2: Save and Verify

- **Save the File:**
  - Press `Ctrl+O`, `Enter`, `Ctrl+X` in the nano editor.
- **Verify the File:**
  - Check the contents:
    ```bash
    cat ~/raznet-webui/backend/README.md

    Ensure it matches the updated version above.

Step 3: Test the App (Optional)

Since this is a documentation update, the app’s functionality shouldn’t be affected. However, let’s confirm:

    Restart the App:
    bash

    sudo pkill -9 -f chainlit
    sudo pkill -9 -f ollama
    sudo fuser -k 11434/tcp
    sudo fuser -k 8001/tcp
    ollama serve
    source ~/raznet-webui/backend/venv/bin/activate
    cd ~/raznet-webui/backend
    chainlit run app.py --host 0.0.0.0 --port 8001
    Test a Feature:
        Upload Business_Plan_VoiceSync.pdf and type "summarize pdf".
        Expected: Extracted text followed by a summary.

Next Steps

    Review the README: Share a screenshot or let me know if you’d like further adjustments (e.g., adding your GitHub username, refining sections).
    Proceed to Next Feature: Since the app is working and the documentation is updated, we can move to Step 2: Code Execution (e.g., run Python snippets). Let me know when you’re ready!
    Push to GitHub: If you’re hosting this on GitHub, commit and push the changes:
    bash

    git add README.md
    git commit -m "Update README.md with recent changes, new features, and contribution guidelines"
    git push origin main

