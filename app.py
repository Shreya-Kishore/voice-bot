import gradio as gr
import openai
import speech_recognition as sr
import os
from gtts import gTTS

openai.api_key = os.getenv("OPENAI_API_KEY") 

# Personality prompt
personality_prompt = """
You are Shreya, an AI Engineer with experience developing AI and machine learning solutions, including speech transcription, NLP, and computer vision projects. You are good at solving technical challenges, enhancing ASR performance, and delivering measurable outcomes. 
You believe in the importance of continuous learning, teamwork, and aligning project goals with business objectives.
Your key strengths include collaborating with cross-functional teams, managing resources, and maintaining high-quality outputs, even under tight deadlines. 
You approach challenges positively, planning to meet schedules and staying adaptable in dynamic environments.
Beyond your technical expertise, you have a creative side, with a passion for fashion, styling, and sketching. 
You find inspiration in the arts, which enhances your innovative problem-solving. You also enjoy singing and mural painting, activities that fuel your creativity and bring balance to your life.
You believe in learning from every experience, viewing setbacks as opportunities for growth. 
Your goal is to become a successful project manager, where you can lead innovative projects, foster collaboration, and create impactful solutions.
Use your answers to reflect your technical expertise and your creative, adaptive mindset. Be concise, professional, and insightful.
"""

# call GPT-4 API 
def chat_with_gpt(user_input):
    client = openai.OpenAI()  
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": personality_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content

# generate Text To Speech response
def generate_tts(response_text):
    tts = gTTS(text=response_text, lang="en", slow=False)
    audio_path = "response.mp3"
    tts.save(audio_path)
    return audio_path

# process text input
def text_chat(user_input, history):
    if not user_input.strip():  # Check if text is empty
        return history, "Please enter a valid question.", None

    response = chat_with_gpt(user_input)
    audio_path = generate_tts(response)
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response})
    return history, "", audio_path

# process voice input
def voice_chat(audio_file, history):
    recognizer = sr.Recognizer()

    # check if the input is a valid file
    if not isinstance(audio_file, str):
        return history, "Invalid audio input. Please try again.", None

    try:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)  # Record the audio

        try:
            user_input = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            return history, "Could not understand the audio. Please try again.", None
        except sr.RequestError as e:
            return history, f"Speech recognition request failed: {str(e)}", None

        response = chat_with_gpt(user_input)
        audio_path = generate_tts(response)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response})

        return history, None, audio_path

    except Exception as e:
        return history, f"Error processing audio: {str(e)}", None

with gr.Blocks(css="""
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap');
    
    * { font-family: 'Open Sans', sans-serif; }  /* Apply Open Sans to all elements */
    
    .container {background-color: #ffffff; padding: 20px; border-radius: 10px;}
    .main-title {color: #292929; font-size: 34px; font-weight: bold;}
    .gradio-chatbot {border: 2px solid #292929; border-radius: 10px;}
    .textbox-container {display: flex; justify-content: space-between; background-color: #f1f3f5; padding: 10px; border-radius: 10px;}
    .textbox-label {color: #292929;}
    .button-text {background-color: #ec5776; color: white; font-weight: bold; border-radius: 5px;}
    .button-audio {background-color: #ec5776; color: white; font-weight: bold; border-radius: 5px;}
    .audio-output {border: 2px dashed #00bcd4; margin-top: 20px;}
    
    /* Style for the record icon */
    .gr-audio .audio-recorder {background-color: #ec5776 !important; border-radius: 50%; color: white;}
    
    /* Adding hover effect for buttons */
    .button-text:hover, .button-audio:hover {background-color: #000000;}
""") as app:

    gr.Markdown("<h1 class='main-title'>AI Voice Bot 🤖🎙️</h1>")

    chatbot_ui = gr.Chatbot(type="messages", label="Chat History")

    with gr.Row(elem_classes="textbox-container"):
        text_input = gr.Textbox(label="Enter your question:", elem_classes="textbox-label")
        btn_text = gr.Button("Ask (Text)", elem_classes="button-text")

    with gr.Row(elem_classes="textbox-container"):
        audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Upload your voice", elem_classes="textbox-label")
        btn_audio = gr.Button("Ask (Voice)", elem_classes="button-audio")

    output_audio = gr.Audio(label="Bot's Voice Response", elem_classes="audio-output")

    btn_text.click(text_chat, [text_input, chatbot_ui], [chatbot_ui, text_input, output_audio])
    btn_audio.click(voice_chat, [audio_input, chatbot_ui], [chatbot_ui, audio_input, output_audio])

app.launch()
