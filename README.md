Raznet WebUI
A self-hosted, extensible, and feature-rich web interface for large language models (LLMs). Raznet WebUI is designed for flexibility and power, offering seamless interaction with LLMs, vision capabilities, tool-calling, and internet browsing. Whether you're running local models or integrating advanced features like image analysis and real-time web searches, Raznet WebUI adapts to your workflow with a smooth and customizable experience.

Features
    • Text Chat: Interact with LLMs using deepseek-r1:8b for efficient performance and optimized RAM usage. 
    • Vision: Upload images and get descriptions or analysis using granite3.2-vision:latest. 
    • Tool-Calling: Use llama3.1:latest to perform actions like calculations or other predefined tasks. 
    • Internet Browsing: Search the web using DuckDuckGo for real-time information, integrated via Ollama's tool-calling feature. 
    • Text-to-Speech (TTS): Hear assistant responses aloud with customizable voice settings. 
    • Dark Mode: Toggle between light and dark themes for a comfortable user experience. 
    • Settings: Configure the AI provider and model (currently supports Ollama, with OpenAI and Grok planned for future releases). 

Prerequisites
Before setting up the project, ensure you have the following installed:
    • Python 3.11 or higher: Required for the backend. 
    • Node.js and npm: Required for the React frontend. Download from nodejs.org. 
    • Ollama: A local LLM runtime. Install it by following the instructions at https://ollama.ai. 
        ◦ After installing Ollama, pull the required models: 
bash
