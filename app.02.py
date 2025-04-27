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


# Function to display the symptom checker widget
async def show_symptom_checker():
    symptom_checker = cl.CustomElement(name="SymptomChecker")
    await cl.Message(
        content="I'm here to help! You can click on any symptoms you're experiencing below, or describe them in your own words.",
        author="AI Assistant",
        elements=[symptom_checker]
    ).send()


@cl.on_chat_start
async def start():
    logger.info("New chat session started")

    # Initialize chat history
    cl.user_session.set("chat_history", [])

    # Send a welcome message
    welcome_message = "Welcome to your Gynecologist Assistant! How can I help you today?"
    await cl.Message(
        content=welcome_message,
        author="AI Assistant"
    ).send()

    # Add the welcome message to chat history
    chat_history = cl.user_session.get("chat_history")
    chat_history.append({"role": "assistant", "content": welcome_message})
    cl.user_session.set("chat_history", chat_history)

    # Show the symptom checker
    await show_symptom_checker()

    # Inform about file upload capability
    await cl.Message(
        content="If you have any medical documents to share, you can type 'upload file' and I'll help you process them.",
        author="AI Assistant"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    # Get user input
    user_message = message.content
    logger.info(f"Received user message: {user_message[:30]}...")

    # Get chat history
    chat_history = cl.user_session.get("chat_history")

    # Add user message to chat history
    chat_history.append({"role": "user", "content": user_message})
    cl.user_session.set("chat_history", chat_history)

    # Check if this is a file upload request
    if user_message.lower() == "upload file":
        files = await cl.AskFileMessage(
            content="Please upload a text file with your medical information.",
            accept=["text/plain"],
            max_size_mb=2,
            max_files=1
        ).send()

        if files:
            file = files[0]  # Get the first file
            try:
                # Read file content
                with open(file.path, "r") as f:
                    content = f.read()

                # Send acknowledgment message
                ack_message = f"I've received your file '{file.name}'. It contains {len(content)} characters. Let me analyze it."
                await cl.Message(content=ack_message, author="AI Assistant").send()

                # Add acknowledgment to chat history
                chat_history.append({"role": "assistant", "content": ack_message})

                # Create empty message for streaming analysis
                analysis_msg = cl.Message(content="", author="AI Assistant")
                await analysis_msg.send()

                # Generate response about the file using correct streaming method
                prompt = f"This is a medical document from a patient seeking gynecological advice. The document contains: {content}\n\nPlease analyze this document and provide helpful, professional insights."

                # Use the correct streaming method
                response = client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt
                )

                # Stream the analysis
                analysis_text = ""
                for chunk in response:
                    if hasattr(chunk, 'text') and chunk.text:
                        await analysis_msg.stream_token(chunk.text)
                        analysis_text += chunk.text

                # Add to chat history
                chat_history.append({"role": "assistant", "content": analysis_text})
                cl.user_session.set("chat_history", chat_history)

            except Exception as e:
                error_msg = f"Sorry, I couldn't process your file: {str(e)}"
                error_message = cl.Message(content=error_msg, author="AI Assistant")
                await error_message.send()

                # Add error to chat history
                chat_history.append({"role": "assistant", "content": error_msg})
                cl.user_session.set("chat_history", chat_history)
        return

    # Create an empty message for streaming (implements typing indicator)
    msg = cl.Message(content="", author="AI Assistant")
    await msg.send()

    try:
        logger.info(f"Calling Gemini API with model: {model_name}")

        # Add context from chat history
        formatted_history = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history[-5:]])
        full_prompt = f"You are a helpful gynecologist assistant. Provide accurate, professional, and empathetic responses.\n\nConversation history:\n{formatted_history}\n\nUser's latest question: {user_message}\n\nYour response:"

        # Generate response using Gemini with the correct streaming method
        response = client.models.generate_content_stream(
            model=model_name,
            contents=full_prompt
        )

        # Initialize response text
        response_text = ""

        # Stream the response tokens as they come
        for chunk in response:
            if hasattr(chunk, 'text') and chunk.text:
                await msg.stream_token(chunk.text)
                response_text += chunk.text

        # Add to chat history
        chat_history.append({"role": "assistant", "content": response_text})
        cl.user_session.set("chat_history", chat_history)

        logger.info("Response sent to user")

    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        logger.error(f"Error generating response: {e}")

        # Correct way to update a message
        msg.content = error_msg
        await msg.update()

        # Add error message to chat history
        chat_history.append({"role": "assistant", "content": error_msg})
        cl.user_session.set("chat_history", chat_history)
