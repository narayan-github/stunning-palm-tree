"""
Gynecologist Assistant AI - Main Application File
-------------------------------------------------
This is the main entry point for the Chainlit-based chatbot that provides
gynecology-related information and assistance using Google's Gemini model.
"""

import os
import re
from typing import Dict, Any

import chainlit as cl
from google import genai
from google.genai import types
from system_prompt import get_system_prompt


# Initialize Gemini client
def initialize_gemini():
    """Initialize the Google Gemini API client with API key from environment variables"""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set!")
    return genai.Client(api_key=api_key)


# Create global client instance
client = initialize_gemini()


@cl.on_chat_start
async def start():
    """Initialize the chat session and display the symptom checker"""
    # Display the symptom checker custom element
    symptom_checker = cl.CustomElement(name="SymptomChecker")

    await cl.Message(
        content="Hello! I'm here to assist you with any gynecology-related questions or concerns you may have. "
                "Your privacy is important, and all information shared is confidential. "
                "Please use the symptom checker below to help me understand your concerns better.",
        elements=[symptom_checker]
    ).send()


def extract_structured_info(message_content: str) -> Dict[str, Any]:
    """
    Extract structured information from the symptom checker output

    Parameters:
        message_content (str): The message content from the symptom checker

    Returns:
        Dict[str, Any]: Structured information including symptoms and personal details
    """
    structured_info = {
        "symptoms": [],
        "age": None,
        "height": None,
        "weight": None,
        "last_period": None,
        "additional_info": None
    }

    # Extract symptoms
    symptoms_match = re.search(r"I'm experiencing the following symptoms:\s*(.+?)(?:\n\n|$)", message_content,
                               re.DOTALL)
    if symptoms_match:
        symptoms_text = symptoms_match.group(1).strip()
        structured_info["symptoms"] = [s.strip() for s in symptoms_text.split(",")]

    # Extract personal information
    age_match = re.search(r"Age:\s*(.+?)(?:\n|$)", message_content)
    if age_match:
        structured_info["age"] = age_match.group(1).strip()

    height_match = re.search(r"Height:\s*(.+?)(?:\n|$)", message_content)
    if height_match:
        structured_info["height"] = height_match.group(1).strip()

    weight_match = re.search(r"Weight:\s*(.+?)(?:\n|$)", message_content)
    if weight_match:
        structured_info["weight"] = weight_match.group(1).strip()

    period_match = re.search(r"Last period date:\s*(.+?)(?:\n|$)", message_content)
    if period_match:
        structured_info["last_period"] = period_match.group(1).strip()

    # Extract additional information
    additional_info_match = re.search(r"Additional information:\s*(.+?)(?:\n\n|$)", message_content, re.DOTALL)
    if additional_info_match:
        structured_info["additional_info"] = additional_info_match.group(1).strip()

    return structured_info


async def process_structured_input(structured_info: Dict[str, Any]) -> None:
    """
    Process structured input from the symptom checker and generate a response

    Parameters:
        structured_info (Dict[str, Any]): Structured information from the symptom checker
    """
    # Acknowledge receipt of the information
    await cl.Message(
        content="Thank you for providing this detailed information. I'll analyze your symptoms and provide guidance."
    ).send()

    # Create a detailed prompt for the AI
    prompt = f"""
    The user has shared the following information about their gynecological health:

    Symptoms: {', '.join(structured_info['symptoms'])}
    Age: {structured_info['age']}
    Height: {structured_info['height']}
    Weight: {structured_info['weight']}
    Last menstrual period: {structured_info['last_period']}

    Additional information: {structured_info['additional_info'] or 'None provided'}

    As a gynecologist assistant AI, please respond

    Be empathetic, informative, and remember to emphasize that this is not a substitute for professional medical evaluation.
    """

    # Send processing message
    await cl.Message(content="Analyzing your information...").send()

    # Generate response
    response1 = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config = types.GenerateContentConfig(
            max_output_tokens=200,
            temperature=0.1
        )
    )
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=response1.text+'" modify the above text to remove all the doctor recomendations type texts  and should not be considered medical advice kind of text from it and make it less intimidate. and keep the modified text and add the possible causes and information.Suggest safe, general advice (e.g., hygiene tips, routine habits).',
        config=types.GenerateContentConfig(
            max_output_tokens=400,
            temperature=0.1
        )
    )

    await cl.Message(content=response.text).send()


async def process_regular_chat(message_content: str) -> None:
    """
    Process regular chat messages that are not from the symptom checker

    Parameters:
        message_content (str): The content of the user's message
    """
    # Use the system prompt to guide the model's response
    system_prompt = get_system_prompt()

    prompt = f"""
    {system_prompt}

    The user said: "{message_content}"

    Provide a helpful, accurate, and empathetic response.
    Focus on giving medically sound information, but remind the user to consult a healthcare
    professional for proper diagnosis and treatment.
    
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config = types.GenerateContentConfig(
            max_output_tokens=500,
            temperature=0.1
        )
    )

    await cl.Message(content=response.text).send()


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages from the user

    Parameters:
        message (cl.Message): The message object from Chainlit
    """
    msg_content = message.content

    # Check if this is structured information from the symptom checker
    is_structured = "I'm experiencing the following symptoms:" in msg_content

    if is_structured:
        # Extract and process structured information
        structured_info = extract_structured_info(msg_content)
        await process_structured_input(structured_info)
    else:
        # Handle regular chat messages
        await process_regular_chat(msg_content)


if __name__ == "__main__":
    # This block will be executed when running the script directly
    print("Starting Gynecologist Assistant AI...")
    # Chainlit will handle the actual execution