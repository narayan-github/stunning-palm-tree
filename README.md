# Gynecologist Assistant AI

A specialized AI chatbot providing gynecology-related information and assistance using Google's Gemini model and the Chainlit framework.
![Image](https://github.com/user-attachments/assets/38dc34c9-5964-45b1-aaa1-3b13b7643558)

## 🌟 Features

- 🩺 **Domain-Specific AI Assistant**: Specialized in gynecology topics
- 📝 **Interactive Symptom Checker**: Multi-step wizard to collect health information
- 🤖 **Gemini-Powered Responses**: Leverages Google's Gemini 2.0 Flash model
- 🛡️ **Privacy-Focused**: All data is processed securely
- 💬 **Conversational Interface**: Natural language chat with the AI assistant
- 📱 **Mobile-Friendly UI**: Responsive design for all devices

## 📋 Prerequisites

- Python 3.8+
- Node.js and npm (for React component development)
- Google Gemini API key

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/narayan-github/stunning-palm-tree.git
   cd stunning-palm-tree
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root with:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## 🏃‍♀️ Running the Application

Start the Chainlit application:
```bash
chainlit run app.py
```

The application will be available at `http://localhost:8000` by default.

## 🧩 Project Structure

```
├── app.py                 # Main application file
├── system_prompt.py       # System prompts for the AI assistant
├── chainlit.md            # Welcome message for Chainlit
├── requirements.txt       # Python dependencies
├── public/                # Public assets
│   ├── css/               # CSS files
│   │   └── custom.css     # Custom CSS styles
│   └── elements/          # Custom React components
│       └── SymptomChecker.jsx  # Symptom checker component
└── .env                   # Environment variables (not tracked in git)
```

## 🔧 Key Components

### Backend (Python)

- **app.py**: Main Chainlit application with chat handlers and Gemini integration
- **system_prompt.py**: Contains prompts that shape the AI's personality and responses

### Frontend (React & CSS)

- **SymptomChecker.jsx**: Multi-step wizard component for collecting symptom and health information
- **custom.css**: Custom styling for the Chainlit UI

## 💻 Symptom Checker Flow

The symptom checker guides users through a 4-step process:

1. **Body Area Selection**: User selects relevant body areas affected
2. **Symptom Selection**: User identifies specific symptoms for each selected body area
3. **Personal Information**: Collection of relevant health data like age, height, weight
4. **Review & Submit**: User reviews all entered information before submission

## 🔄 How It Works

1. When a user starts a chat session, they're presented with the symptom checker
2. The user can either use the symptom checker or ask questions directly
3. If using the symptom checker, the collected data is processed and analyzed
4. The Gemini AI model generates a tailored response with possible causes, recommendations, and guidance
5. For direct questions, the AI responds based on the gynecology-focused system prompt

## 🛠️ Customization

### Modifying the Symptom Checker

Edit the `public/elements/SymptomChecker.jsx` file to add or modify:
- Body areas
- Symptoms for each area
- Personal information fields
- UI elements and styling

### Customizing AI Responses

Modify the system prompts in `system_prompt.py` to adjust:
- AI personality and tone
- Response structure
- Guidance and recommendations
- Domain knowledge constraints

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [Chainlit](https://github.com/Chainlit/chainlit) for the chat interface framework
- [Google Gemini API](https://ai.google.dev/) for the AI model

---

⚠️ **Disclaimer**: This application is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
