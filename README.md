# JARVIS
Just A Rather Very Intelligent System - A voice-enabled AI assistant inspired by Tony Stark's JARVIS.

## Overview
A Python-based voice assistant that uses:
- OpenAI's Whisper for speech recognition
- GPT for natural conversation
- ElevenLabs for JARVIS-like voice synthesis

## Features
- 🎙️ Voice commands and conversations
- 🤖 Natural language understanding using GPT
- 🗣️ JARVIS-like voice responses
- 💾 Conversation memory
- ⚡ Real-time interaction

## Requirements
- Python 3.8+
- OpenAI API key
- ElevenLabs API key
- Microphone for voice input
- Speakers for voice output

## Installation
```bash
# Clone the repository
git clone https://github.com/shahene/jarvis.git
cd jarvis

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up your API keys in .env file
cp .env.example .env
# Edit .env with your API keys
```

## Quick Start
```bash
python jarvis.py
```

Just start talking to JARVIS after running the script!

## How it Works
1. Your voice is captured through the microphone
2. Whisper converts speech to text
3. GPT processes your request and generates a response
4. ElevenLabs converts the response to JARVIS's iconic voice
5. Response is played through your speakers

## License
MIT License
