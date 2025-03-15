import ollama
import logging
import asyncio
import traceback
import re
import chainlit as cl
from typing import AsyncGenerator, Union
from tools import duckduckgo_search, browse_web, process_pdf
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Tool schema for llama3.2:1b
TOOLS = [
    {
        "name": "duckduckgo_search",
        "description": "Search the internet using DuckDuckGo.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look up on DuckDuckGo."
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "browse_web",
        "description": "Fetch and summarize content from a specific URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to browse and fetch content from."
                }
            },
            "required": ["url"]
        }
    },
    {
        "name": "process_pdf",
        "description": "Extract text from an uploaded PDF file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path of the PDF to process."
                }
            },
            "required": ["file_path"]
        }
    }
]

async def process_text_stream(message: str) -> AsyncGenerator[str, None]:
    """
    Process text messages with streaming using smollm or llama3.1:latest.
    """
    logger.debug(f"Starting process_text_stream with message: {message}")
    try:
        model_name = "llama3.1:latest"  # Switch to "smollm" for lighter usage if preferred
        logger.debug(f"Using model: {model_name}")
        response = ollama.chat(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Be concise and efficient. Perform math calculations following PEMDAS order."},
                {"role": "user", "content": message}
            ],
            stream=True
        )
        for chunk in response:
            content = chunk["message"]["content"]
            if content:
                yield content
    except Exception as e:
        logger.error(f"Text error: {str(e)}")
        logger.error(traceback.format_exc())
        yield f"Error: {str(e)}"

async def process_vision_stream(image_path: str) -> AsyncGenerator[str, None]:
    """
    Process vision tasks with streaming using moondream:1.8b-v2-q3_K_S.
    """
    logger.debug(f"Starting process_vision_stream with image path: {image_path}")
    try:
        with open(image_path, "rb") as img_file:
            image_data = img_file.read()
            logger.debug(f"Image data read, size: {len(image_data)} bytes")
            response = ollama.generate(
                model="moondream:1.8b-v2-q3_K_S",
                prompt="Describe this image.",
                images=[image_data],
                stream=True
            )
            for chunk in response:
                content = chunk["response"]
                if content:
                    yield content
    except Exception as e:
        logger.error(f"Vision error: {str(e)}")
        logger.error(traceback.format_exc())
        yield f"Error: {str(e)}"

async def process_tool_calling_stream(message: Union[str, cl.Message]) -> AsyncGenerator[str, None]:
    """
    Process tool-calling requests with streaming using llama3.2:1b.
    """
    logger.debug(f"Starting process_tool_calling_stream with message: {message}")
    try:
        # Handle message content based on type
        message_content = message.content if isinstance(message, cl.Message) else message
        message_elements = message.elements if isinstance(message, cl.Message) else []

        # Determine the appropriate tool based on the message
        use_duckduckgo = "search for" in message_content.lower()
        use_browse_web = bool(re.search(r'https?://[^\s]+', message_content))
        use_pdf = any(phrase in message_content.lower() for phrase in ["process pdf", "read pdf", "what is contained in this pdf", "extract text from pdf", "summarize pdf"]) and \
                  any(elem for elem in message_elements if isinstance(elem, cl.File) and elem.mime == "application/pdf")

        if use_duckduckgo and (use_browse_web or use_pdf):
            # Prioritize duckduckgo_search for "search for"
            use_browse_web = False
            use_pdf = False

        response = ollama.chat(
            model="llama3.2:1b",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Use the provided tools to answer queries requiring external information. If the message contains 'search for', use duckduckgo_search with the query following 'search for'. If the message contains a valid URL starting with 'http://' or 'https://', use browse_web with that URL. If the message contains phrases like 'process pdf', 'read pdf', 'what is contained in this pdf', 'extract text from pdf', or 'summarize pdf' and an uploaded PDF file is provided, use process_pdf with the file path."},
                {"role": "user", "content": message_content}
            ],
            tools=TOOLS,
            stream=True
        )
        for chunk in response:
            if "message" in chunk:
                content = chunk["message"]["content"]
                if content:
                    yield content
                # Check if the model wants to use a tool
                if "tool_calls" in chunk["message"] and chunk["message"]["tool_calls"]:
                    try:
                        tool_call = chunk["message"]["tool_calls"][0]
                        func_name = tool_call["function"]["name"]
                        arguments = tool_call["function"]["arguments"]
                        # Override tool selection if necessary
                        if use_duckduckgo and func_name != "duckduckgo_search":
                            yield f"\n[Correcting tool selection: Using duckduckgo_search for search query]...\n"
                            query = message_content.split("search for", 1)[-1].strip() if "search for" in message_content.lower() else "No query provided"
                            yield f"\n[Searching DuckDuckGo for: {query}]...\n"
                            search_result = duckduckgo_search(query)
                            yield f"\nSearch Results:\n{search_result}\n"
                        elif use_browse_web and func_name != "browse_web":
                            yield f"\n[Correcting tool selection: Using browse_web for URL]...\n"
                            url = re.search(r'https?://[^\s]+', message_content).group(0)
                            yield f"\n[Browsing URL: {url}]...\n"
                            web_content = browse_web(url)
                            yield f"\nWeb Content:\n{web_content}\n"
                        elif use_pdf and func_name != "process_pdf":
                            yield f"\n[Correcting tool selection: Using process_pdf for PDF]...\n"
                            pdf_element = next((elem for elem in message_elements if isinstance(elem, cl.File) and elem.mime == "application/pdf"), None)
                            if pdf_element:
                                file_path = pdf_element.path
                                yield f"\n[Processing PDF: {file_path}]...\n"
                                pdf_text = process_pdf(file_path)
                                if pdf_text.startswith("Error"):
                                    yield f"\n{pdf_text}\n"
                                else:
                                    yield f"\nPDF Content:\n{pdf_text}\n"
                                    # If the user asked to summarize, pass the text to the model for summarization
                                    if "summarize" in message_content.lower():
                                        yield "\n[Summarizing PDF content]...\n"
                                        summary_response = ollama.chat(
                                            model="llama3.2:1b",
                                            messages=[
                                                {"role": "system", "content": "You are a helpful AI assistant. Summarize the following text."},
                                                {"role": "user", "content": pdf_text}
                                            ],
                                            stream=True
                                        )
                                        for summary_chunk in summary_response:
                                            summary_content = summary_chunk["message"]["content"]
                                            if summary_content:
                                                yield summary_content
                                os.remove(file_path)  # Clean up temporary file
                            else:
                                yield "\nError: No PDF file uploaded.\n"
                        else:
                            if func_name == "duckduckgo_search":
                                query = arguments.get("query", message_content.split("search for", 1)[-1].strip() if "search for" in message_content.lower() else "No query provided")
                                yield f"\n[Searching DuckDuckGo for: {query}]...\n"
                                search_result = duckduckgo_search(query)
                                yield f"\nSearch Results:\n{search_result}\n"
                            elif func_name == "browse_web":
                                url = arguments.get("url")
                                if not url or not re.match(r'^https?://', url):
                                    url = re.search(r'https?://[^\s]+', message_content)
                                    url = url.group(0) if url else "https://example.com"
                                yield f"\n[Browsing URL: {url}]...\n"
                                web_content = browse_web(url)
                                yield f"\nWeb Content:\n{web_content}\n"
                            elif func_name == "process_pdf":
                                file_path = arguments.get("file_path")
                                if file_path and os.path.exists(file_path):
                                    yield f"\n[Processing PDF: {file_path}]...\n"
                                    pdf_text = process_pdf(file_path)
                                    if pdf_text.startswith("Error"):
                                        yield f"\n{pdf_text}\n"
                                    else:
                                        yield f"\nPDF Content:\n{pdf_text}\n"
                                        # If the user asked to summarize, pass the text to the model for summarization
                                        if "summarize" in message_content.lower():
                                            yield "\n[Summarizing PDF content]...\n"
                                            summary_response = ollama.chat(
                                                model="llama3.2:1b",
                                                messages=[
                                                    {"role": "system", "content": "You are a helpful AI assistant. Summarize the following text."},
                                                    {"role": "user", "content": pdf_text}
                                                ],
                                                stream=True
                                            )
                                            for summary_chunk in summary_response:
                                                summary_content = summary_chunk["message"]["content"]
                                                if summary_content:
                                                    yield summary_content
                                    os.remove(file_path)  # Clean up temporary file
                                else:
                                    yield "\nError: Invalid or missing PDF file path.\n"
                    except Exception as e:
                        logger.error(f"Error in tool call processing: {str(e)}")
                        logger.error(traceback.format_exc())
                        yield f"Error in tool call: {str(e)}\n"
    except Exception as e:
        logger.error(f"Tool-calling error: {str(e)}")
        logger.error(traceback.format_exc())
        yield f"Error: {str(e)}"