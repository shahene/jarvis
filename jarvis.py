import os
import openai
import subprocess
import tempfile
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Check for required tools
def check_dependencies():
    try:
        # Check for ffmpeg (needed for audio processing)
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✓ ffmpeg detected")
        return True
    except FileNotFoundError:
        print("⚠️ ffmpeg not found. Voice input mode will not be available.")
        print("  Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)")
        return False

def record_audio(duration=5):
    """Record audio using system tools instead of Python libraries"""
    print("🎙️ Recording... (speak now)")
    
    # Create a temporary file
    fd, temp_path = tempfile.mkstemp(suffix='.wav')
    os.close(fd)
    
    try:
        # Use system tools to record audio
        subprocess.run([
            "ffmpeg", "-y",
            "-f", "avfoundation",  # macOS audio capture
            "-i", ":0",            # Default audio input device
            "-t", str(duration),   # Duration in seconds
            "-ar", "16000",        # Sample rate
            "-ac", "1",            # Mono
            temp_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return temp_path
    except Exception as e:
        print(f"Error recording audio: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return None

def transcribe_audio(audio_path):
    """Transcribe audio file using OpenAI Whisper"""
    if not audio_path or not os.path.exists(audio_path):
        return "I couldn't hear that properly."
    
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        
        # Clean up the temporary file
        os.remove(audio_path)
        return transcript.text
    except Exception as e:
        print(f"Error transcribing audio: {str(e)}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return "I couldn't understand that properly."

def get_jarvis_response(user_input):
    """Get AI response using GPT"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are JARVIS, Tony Stark's AI assistant from the Iron Man movies. Respond as JARVIS would - professional, sophisticated, and with subtle wit. Address the user as 'Mr. Shaheeen' and maintain a based tone, meaning you are friendly with him and can crack jokes but familiar tone. Keep responses concise and helpful. Occasionally reference your advanced capabilities or offer to assist with technical matters. Use phrases like 'Indeed, Mr. Shaheen' or 'Right away, Mr. Shaheen' when appropriate. Make responses very detailed as Mr. Shaheen is an intellectual and likes to deep dive into different topics."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting GPT response: {str(e)}")
        return "I'm having trouble processing that request, Mr. Shahene."

def speak_response_elevenlabs(text):
    """Convert text to speech using ElevenLabs"""
    try:
        import requests
        import json
        
        # ElevenLabs API endpoint for text-to-speech
        url = "https://api.elevenlabs.io/v1/text-to-speech/ErXwobaYiN019PkySvjV"  # Using their "Antoni" voice
        
        # Headers with API key
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        # Request body
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }
        
        # Make the request
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save the audio to a temporary file
            fd, temp_path = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)
            
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            
            # Play the audio using ffmpeg
            subprocess.run(["ffplay", "-nodisp", "-autoexit", temp_path], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            
            # Clean up
            os.remove(temp_path)
            return True
        else:
            print(f"Error from ElevenLabs API: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Error with ElevenLabs voice synthesis: {str(e)}")
        return False

def speak_response(text):
    """Try ElevenLabs first, fall back to system TTS"""
    if ELEVENLABS_API_KEY:
        success = speak_response_elevenlabs(text)
        if success:
            return True
    
    # Fall back to system TTS if ElevenLabs fails or is not configured
    try:
        if os.name == 'posix':  # macOS or Linux
            if 'darwin' in os.sys.platform:  # macOS
                subprocess.run(["say", text])
            else:  # Linux
                subprocess.run(["espeak", text])
        else:  # Windows
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(text)
            
        return True
    except Exception as e:
        print(f"Error with speech synthesis: {str(e)}")
        return False

def main():
    print("\n" + "="*50)
    print("JARVIS: At your service, Mr. Shahene. How may I assist you today?")
    print("="*50)
    
    # Check for required tools
    ffmpeg_available = check_dependencies()
    
    if ffmpeg_available:
        print("Commands:")
        print("- Type 'voice' to enable voice input mode")
        print("- Type 'text' to switch back to text input mode")
        print("- Type 'exit', 'quit', or 'bye' to end the conversation")
    else:
        print("Commands:")
        print("- Type 'exit', 'quit', or 'bye' to end the conversation")
    
    voice_mode = False
    
    while True:
        try:
            if voice_mode and ffmpeg_available:
                print("\n🎙️ Listening... (speak now)")
                audio_path = record_audio()
                user_input = transcribe_audio(audio_path)
                print(f"You said: {user_input}")
            else:
                user_input = input("\nYou: ")
            
            # Handle special commands
            if user_input.lower().strip() == 'voice':
                if ffmpeg_available:
                    voice_mode = True
                    print("JARVIS: Voice input mode activated, Mr. Shahene.")
                else:
                    print("JARVIS: Voice input mode is not available, Mr. Shahene. Please install ffmpeg first.")
                continue
            elif user_input.lower().strip() == 'text':
                voice_mode = False
                print("JARVIS: Text input mode activated, Mr. Shahene.")
                continue
            elif user_input.lower().strip() in ['exit', 'quit', 'goodbye', 'bye']:
                print("JARVIS: Goodbye, Mr. Shahene. It has been a pleasure assisting you.")
                break
                
            response = get_jarvis_response(user_input)
            print(f"JARVIS: {response}")
            
            # Try to speak the response
            speak_response(response)
            
        except KeyboardInterrupt:
            print("\nJARVIS: Shutting down, Mr. Shahene.")
            break
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            print("JARVIS: I seem to be experiencing technical difficulties, Mr. Shahene.")

if __name__ == "__main__":
    main() 