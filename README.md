# AI Voice Chatbot 🤖🎙️  

This is a voice-enabled AI chatbot powered by **OpenAI's GPT-4** and deployed using **Gradio** on Hugging Face Spaces. The chatbot can process both text and voice inputs, generate meaningful AI responses, and provide text-to-speech (TTS) audio output.

## Features  
- **Chat with GPT-4 AI**: Engage in conversations through text or voice.  
- **Speech-to-Text (STT)**: The app processes audio using `speech_recognition` and converts speech to text.  
- **Text-to-Speech (TTS)**: The bot responds with audio output using `gTTS`.  
- **Customizable Personality Prompt**: The bot's personality reflects AI expertise and creative pursuits.  
- **Gradio UI with Styling**: A user-friendly interface with styled buttons, text boxes, and audio components.


## How to Use  
1. **Text Chat**: Type your query in the text box and click "Ask (Text)." The bot will respond with a text and voice message.  
2. **Voice Chat**: Upload or record your voice by clicking the microphone option, then click "Ask (Voice)."  
3. Listen to the AI's audio response under "Bot's Voice Response."


### Setup Instructions (for Hugging Face Space Deployment)

1. **Create a new Hugging Face Space**:
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces) and create a new Gradio Space.

2. **Upload files**:
   - Upload `app.py` and `requirements.txt` to your Space.

3. **Set the API key**:
   - In your Hugging Face Space, go to **Settings > Variables and Secrets**.
   - Add your **OpenAI API key** as a variable:  
     - Name: `OPENAI_API_KEY`  
     - Value: `(your actual key)`

4. **Launch the Space**:
   - The app will automatically build and launch after detecting your files and settings.
  
Deployed Version
This app is also deployed on Hugging Face Spaces. You can try it here: Live Demo (https://huggingface.co/spaces/shreykishore19/voice-bot)


