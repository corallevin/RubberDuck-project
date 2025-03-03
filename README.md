# RubberDuck Voice Debugging Assistant

This project provides a “rubber duck” style debugging assistant that listens to your voice input (via microphone), transcribes it using OpenAI’s Whisper model, and responds using ChatGPT. It can also capture a photo with a Raspberry Pi camera, analyze the image (via OpenAI), and give a short spoken description.

## Features
- **Voice Input and Output**: Records audio, transcribes it, and provides spoken responses.
- **Image Capture**: Uses `libcamera-jpeg` to capture an image (e.g., on a Raspberry Pi) and then analyzes it using an OpenAI model.
- **Physical Button Control** (via `main.py`): Starts the RubberDuck script with a GPIO-connected button.
- **Text-to-Speech**: Uses `gTTS` and `mpg321` for audio playback.

## Requirements
- Python 3.7+  
- [OpenAI Python client](https://pypi.org/project/openai/) (`pip install openai`)
- [sounddevice](https://pypi.org/project/sounddevice/) + [scipy](https://pypi.org/project/scipy/) (for audio recording)
- [gTTS](https://pypi.org/project/gTTS/) (for text-to-speech)
- [requests](https://pypi.org/project/requests/)
- [`mpg321`](https://packages.debian.org/mpg321) installed on the system (for MP3 playback)
- [libcamera](https://www.raspberrypi.com/documentation/computers/camera_software.html) utilities installed (on Raspberry Pi) if you want to capture images
- A valid OpenAI API key (replace the `api_key` variable in `RubberDuck.py` with your own)

## Hardware (Optional for Button Usage)
- Raspberry Pi (or any device with GPIO support).
- A momentary push-button wired to GPIO pin 17 (as referenced in `main.py`) and ground.

## Installation
1. **Clone or download** this repository.  
2. **Install dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```
   Or install manually:  
   ```bash
   pip install openai sounddevice scipy gTTS requests
   sudo apt-get update && sudo apt-get install mpg321
   ```
3. **Set up OpenAI API Key**:  
   - In `RubberDuck.py`, update `api_key = "<YOUR_OPENAI_KEY>"` with your actual key.

## Usage
1. **Button-based Start (on a Pi)**:
   - Wire the button to the specified GPIO pin (default is pin 17).  
   - Run `python main.py`.  
   - Press the button to start the voice assistant script (`RubberDuck.py`).

2. **Direct Script**:
   - If you don’t use the button, simply run `RubberDuck.py` in a terminal:
     ```bash
     python RubberDuck.py
     ```
   - The script will listen for five seconds of audio, transcribe it, and reply in exactly two spoken sentences.

3. **Capture Images**:
   - While the script is running, say “take a picture” (or “capture photo”) to trigger the camera capture and analysis.
   - Wait for the response about what’s in the image.

## Notes
- Ensure your microphone is recognized by the system (e.g., Raspberry Pi or any Linux machine).
- The script expects `mpg321` for playback of TTS audio and shutter sounds.
- The usage of the camera commands (`libcamera-jpeg`) is specific to Raspberry Pi OS.

## Contributing
Feel free to submit pull requests or open issues to suggest improvements or report bugs.

## License
This project is provided under an open-source license (add your choice here). Feel free to modify and adapt it for your needs!

---
