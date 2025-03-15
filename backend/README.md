Raznet WebUI Assistant
Overview

The Raznet WebUI Assistant is an advanced, multimodal AI application built with Chainlit and powered by Ollama models. This assistant integrates text processing, image description, web searching, web browsing, and PDF processing into a single, user-friendly interface. It leverages lightweight and efficient models such as any Ollama model to provide a robust, scalable solution for diverse tasks.

This project supports real-time streaming responses (akin to ChatGPT), tool-calling for external searches and browsing, and a modular architecture. It is designed to run locally on modest hardware (e.g., as small as 4G,8,16G RAM and up depending on your device's hardware strength) and is extensible with additional tools or models. Recent enhancements include PDF text extraction and summarization, with exciting new features on the horizon.

License: MIT

This project is licensed under the MIT License. See the LICENSE file for details.
Changelog

    March 15, 2025:
        Added llama3 for tool-calling with DuckDuckGo search.
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


