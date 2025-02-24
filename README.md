# Windows Voice Assistant

A voice-activated assistant that provides Windows system information using AI-powered responses. The assistant supports both local (Ollama) and cloud-based (Google Gemini) AI models for generating responses.

## Features

- 🎤 Voice activation with customizable wake word (default: "helix")
- 🤖 Dual AI backend support:
  - Google Gemini API
  - Local Ollama model
- 🎯 Windows-specific system information and troubleshooting
- 🔊 Text-to-speech response output
- 🎚️ Automatic ambient noise calibration
- ⚡ Real-time voice processing

## Prerequisites

- Python 3.8+
- Microphone access
- Internet connection (for Gemini API)
- Ollama installed (if using local model)

## Installation

1. Clone the repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Install required packages:
```bash
pip install speech_recognition ollama google-generativeai sounddevice numpy kokoro
```

3. Configure the application:
- For Gemini API: Add your API key in `Config` class
- For Ollama: Ensure Ollama is installed and running

## Configuration

Edit the `Config` class in `main.py` to customize:

```python
@dataclass(frozen=True)
class Config:
    wake_word: str = "helix"              # Customize wake word
    use_gemini: bool = True               # Toggle between Gemini/Ollama
    gemini_api_key: str = "your-api-key"  # Your Gemini API key
    model_name: str = "llama2:latest"     # Ollama model name
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Wait for initialization and calibration

3. Window Controls:
   - Alt+H: Toggle window visibility
   - Minimize: Hides to system tray
   - Window appears automatically for important events

The assistant will continue running in the background even when the window is hidden.

4. Say the wake word ("helix")
5. Ask your Windows-related question
6. Listen to the AI-generated response

## Voice Commands

- Wake word: "helix" (customizable)
- Stop command: "stop"
- Any Windows-related questions:
  - System commands
  - Shortcuts
  - Settings
  - Troubleshooting

## Error Handling

The assistant includes:
- Automatic retry mechanisms
- Ambient noise calibration
- Error status indicators
- Graceful error recovery

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

[Your chosen license]

## Acknowledgments

- Speech Recognition library
- Ollama project
- Google Gemini API
- Kokoro TTS engine
