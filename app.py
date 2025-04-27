# app.py
import chainlit as cl
from google import genai
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key with better error handling
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    logger.error("No API key found. Please set GEMINI_API_KEY in your .env file")
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Configure Gemini API
try:
    client = genai.Client(api_key=api_key)
    logger.info("Gemini client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini client: {e}")
    raise

# Setup the model
model_name = "gemini-2.0-flash"


@cl.on_chat_start
async def start():
    logger.info("New chat session started")
    # Send a welcome message
    await cl.Message(
        content="Welcome! How can I help you today?",
        author="AI Assistant"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    # Get user input
    user_message = message.content
    logger.info(f"Received user message: {user_message[:30]}...")

    # Create a message waiting to be populated with a response
    msg = cl.Message(content="Thinking...", author="AI Assistant")
    await msg.send()

    # Generate response using Gemini
    try:
        logger.info(f"Calling Gemini API with model: {model_name}")
        response = client.models.generate_content(
            model=model_name,
            contents=user_message
        )
        logger.info("Received response from Gemini API")
        response_text = response.text

        # Update the waiting message with the response
        await msg.update(content=response_text)
        logger.info("Response sent to user")
    except TypeError as te:
        if "unexpected keyword argument 'content'" in str(te):
            # Try alternative API format
            logger.info("Trying alternative update method")
            try:
                # In newer Chainlit versions, update() might expect different parameters
                await msg.update(content=response_text)
            except:
                # If that also fails, try direct assignment
                msg.content = response_text
                await msg.send()
        else:
            error_msg = f"Sorry, I encountered an error: {str(te)}"
            logger.error(f"TypeError generating response: {te}")
            msg.content = error_msg
            await msg.send()
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        logger.error(f"Error generating response: {e}")
        msg.content = error_msg
        await msg.send()