import chainlit as cl
from chainlit import Action
from models import process_text_stream, process_vision_stream, process_tool_calling_stream
import os
import logging
import traceback
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@cl.on_chat_start
async def start():
    logger.debug("Starting Raznet WebUI Assistant session")
    try:
        cl.user_session.set("provider", "ollama")
        welcome_msg = await cl.Message(
            content="Welcome to Raznet WebUI Assistant!\nUnlock a range of powerful features:\n- **Text Processing:** Perform calculations, ask general questions, or engage in conversations.\n- **Image Description:** Upload an image and type 'describe' to receive detailed insights.\n- **Web Searching:** Search the internet by typing 'search for [topic]'.\n- **Streaming Responses:** Enjoy real-time, professional-grade response streaming for a seamless experience.\n- **Modular Design:** Built for scalability and maintainability.\n- **PDF Processing:** Upload a PDF and type 'process pdf', 'read pdf', 'what is contained in this pdf', or 'extract text from pdf' to extract its text."
        ).send()
        logger.debug("Welcome message sent")
    except Exception as e:
        logger.error(f"Error in on_chat_start: {str(e)}")
        logger.error(traceback.format_exc())

@cl.on_message
async def main(message: cl.Message):
    logger.debug(f"Received message: {message.content}, elements: {message.elements}")
    try:
        # Initialize the response message
        msg = cl.Message(content="")
        await msg.send()

        # Handle image or PDF input
        if message.elements:
            pdf_element = next((elem for elem in message.elements if isinstance(elem, cl.File) and elem.mime == "application/pdf"), None)
            image_element = next((elem for elem in message.elements if isinstance(elem, cl.Image) and elem.mime.startswith("image/")), None)

            if pdf_element:
                logger.debug(f"Processing PDF at path: {pdf_element.path}")
                # Automatically trigger PDF processing if a PDF is uploaded
                constructed_message = f"process pdf {pdf_element.path}"
                async for chunk in process_tool_calling_stream(cl.Message(content=constructed_message, elements=message.elements)):
                    await msg.stream_token(chunk)
            elif image_element and message.content.lower() == "describe":
                logger.debug(f"Processing image at path: {image_element.path}")
                async for chunk in process_vision_stream(image_element.path):
                    await msg.stream_token(chunk)
            else:
                await msg.stream_token("Please type 'describe' for images or upload a PDF to process its content.")
                logger.debug("Invalid command for uploaded file")
        # Handle tool-calling (e.g., search or browse queries)
        elif ("search" in message.content.lower() or 
              "look up" in message.content.lower() or 
              "browse" in message.content.lower() or 
              re.search(r'http[s]?://[^\s]+', message.content)):
            logger.debug("Processing tool-calling message with llama3.2:1b")
            async for chunk in process_tool_calling_stream(message):
                await msg.stream_token(chunk)
        # Handle text input (text test with App)
        else:
            logger.debug("Processing text message with App")
            async for chunk in process_text_stream(message.content):
                await msg.stream_token(chunk)

        await msg.update()
    except Exception as e:
        logger.error(f"Error in on_message: {str(e)}")
        logger.error(traceback.format_exc())
        await cl.Message(content=f"Error processing message: {str(e)}").send()