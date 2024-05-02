import streamlit as st
from openai import OpenAI
import os
import wave

#client = OpenAI(api_key=os.getenv("API_KEY"))
client = OpenAI(api_key=st.secrets["API_key"])

recording = False  # Flag to track recording state

def transcribe_audio():
    """Transcribes audio data using the OpenAI Whisper model.

    Args:
        audio_data: A byte array containing the recorded audio data in WAV format.

    Returns:
        The transcribed text from the audio, or an error message if transcription fails.
    """
    audio_file = open("./recording.wav", "rb")

    # Send the converted audio data to OpenAI API
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

    return transcription.text

def app():
    st.subheader("Fine-tuned Speech-to-Text Model for Hiligaynon (Ilonggo) Language")

    with st.expander("Display info about the app"):        
        text = """Prof. Louie F. Cervantes, M. Eng. (Information Engineering) \n
        CCS 229 - Intelligent Systems
        Department of Computer Science
        College of Information and Communications Technology
        West Visayas State University
        """
        st.write(text)

    st.write("This app allows you to record audio and transcribe it to text using the OpenAI Whisper model.")
    st.write("Click the 'Start Recording' button to begin recording audio. Once you're done, click the 'Stop Recording' button to transcribe the audio.")
    st.write("The transcribed text will be displayed below.")
    st.write("Note: The model is trained to transcribe Hiligaynon and other Visayan and Languages.")
    st.write("Please speak clearly and avoid background noise for best results.")
    st.write("The model can transcribe up to 5 minutes of audio.")
    st.write("Please note that the model may not be perfect and may make mistakes in transcription.")
    st.write("If you encounter any issues, please try again or contact the developer.")
    st.write("The model can only translate Hiligaynon to English at this time.")

    # Separate buttons for recording and stopping
    if st.sidebar.button("Load Audio File"):
        uploaded_file = st.file_uploader("Choose an audio file to upload:", type=["audio/mpeg", "audio/wav"])
        if uploaded_file is not None:
            # Display a success message
            st.success("File uploaded successfully!")

            # Get details about the uploaded file
            file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type, "filesize": uploaded_file.size}
            st.write("File Details:")
            st.json(file_details)

            # Read the uploaded file content (optional)
            # bytes_data = uploaded_file.read()

        else:
            st.warning("Upload an audio file (MP3 or WAV format).")

if __name__ == "__main__":
    app()