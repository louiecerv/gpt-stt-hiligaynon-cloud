import streamlit as st
from openai import OpenAI
import os
import pyaudio
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

if "stream" not in st.session_state:
    st.session_state.stream = None

if "frames" not in st.session_state:
    st.session_state.frames = []

if "p" not in st.session_state:
    st.session_state.p = None   

if "channels" not in st.session_state:
    st.session_state.channels = 2

if "rate" not in st.session_state:
    st.session_state.rate = 44100

if "format" not in st.session_state:
    st.session_state.format = pyaudio.paInt16

if "chunk" not in st.session_state:
    st.session_state.chunk = 1024

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
    if st.sidebar.button("Start Recording"):
        global recording
        recording = True

        # Initialize PyAudio object
        p = pyaudio.PyAudio()
        st.session_state.p = p

        # Define recording parameters
        chunk = 1024  # Chunk size for recording
        format = pyaudio.paInt16  # Audio format
        channels = 2  # Number of channels (stereo)
        rate = 44100  # Sampling rate
        st.session_state.channels = channels    
        st.session_state.rate = rate 
        st.session_state.format = format
        st.session_state.chunk = chunk


        # Open audio stream
        stream = p.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
        st.session_state.stream = stream

        frames = []

        st.write("Recording started...")
        recording = True
        # Record audio for specified duration
        while recording:
            data = stream.read(chunk)
            frames.append(data)
            st.session_state.frames = frames


    if st.sidebar.button("Stop Recording"):
        stream = st.session_state.stream
        frames = st.session_state.frames
        p = st.session_state.p  
        channels = st.session_state.channels
        rate = st.session_state.rate
        format = st.session_state.format
        chunk = st.session_state.chunk

        recording = False
        st.write("Recording stopped.")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()

        # Close PyAudio object
        p.terminate()

        # Combine recorded frames into a single byte array
        audio_data = b''.join(frames)

        # Save audio data as a WAV file (optional)
        wf = wave.open("recording.wav", 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(audio_data)
        wf.close()

        if audio_data:
            transcription = transcribe_audio()
            st.write("Transcription:")
            st.write(transcription if transcription else "No transcription available.")


if __name__ == "__main__":
    app()
