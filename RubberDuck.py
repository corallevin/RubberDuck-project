import time
import openai
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import os
import base64
import requests
from gtts import gTTS
import re

api_key = ""
openai.api_key = api_key

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def play_camera_sound():
    """
    Plays a camera shutter sound using system tools.
    Ensure the sound file exists in the specified path.
    """
    sound_file =  "/home/finalproject/PycharmProjects/RubberDuck/camera_shutter.mp3"  #
    os.system(f"mpg321 --scale 32768 {sound_file} -q")  # Use 'mpg321' for MP3 playback


# Function to capture an image
def capture_image(save_path):
    """
    Captures an image using the `libcamera-jpeg` command and saves it to the specified path.
    """
    command = f"libcamera-jpeg -o {save_path}"
    os.system(command)
    play_camera_sound()



def text_to_speech(text, lang="en", output_file="output.mp3", speed=0.9, pitch=0.7):
    """
    ממיר טקסט לקול, משנה את המהירות והגובה, ומשמיע אותו.
    - text: הטקסט להמרה.
    - lang: שפה (ברירת מחדל אנגלית).
    - output_file: שם קובץ הפלט.
    - speed: מהירות ההשמעה (ברירת מחדל 1.3).
    - pitch: גובה הצליל (ברירת מחדל 1.2, ערך גבוה יותר = צליל גבוה יותר).
    """
    try:
        # יצירת קובץ MP3 עם gTTS
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_file)

        # שינוי המהירות והגובה עם ffmpeg
        ducky_output = "ducky_output.mp3"
        ffmpeg_command = (
            f"ffmpeg -i {output_file} -filter:a "
            f"'atempo={speed},asetrate=44100*{pitch}' -vn {ducky_output} -y"
        )
        os.system(ffmpeg_command)

        # ניגון הקובץ עם mpg321
        os.system(f"mpg321 {ducky_output}")

        # ניקוי קבצים זמניים
        os.remove(output_file)
        os.remove(ducky_output)

    except Exception as e:
        print(f"Error in TTS: {e}")



messages = [
    {"role": "system",
     "content": "You are a rubber ducky for code debugging and assistant. I don't want you to read the code but only answer according to the question. Answer in **exactly** two sentences. Do not exceed two sentences under any circumstances. Never quote anything, never say 'backquote', do not use special characters, and always speak in plain English. Speak slowly like a duck."}
]

# Initial greeting
initial_message = "Quack quack! Hello there! What's the problem you're facing? Say 'please exit' to finish the conversation."
print(initial_message)
text_to_speech(initial_message)

# Record audio from the microphone
fs = 48000  # Sample rate
seconds = 5  # Duration of recording


while True:
    print("You:")
    recorded_audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
    sd.wait()  # Wait until recording is finished

    # Save the recording to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        audio_file_path = tmp_file.name
        write(audio_file_path, fs, recorded_audio)

    # Transcribe the audio file using OpenAI's Whisper model
    with open(audio_file_path, 'rb') as audio_file:
        transcript = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file,
            language="en"  # הגדרת השפה כ"אנגלית"
        )

    # Print and process the transcript
    text = transcript["text"]
    print(f"You said: {text}")

    if "please exit" in text.lower():
        goodbye_message = "Goodbye"
        print(goodbye_message)
        text_to_speech(goodbye_message)
        break

    if "take a picture" in text.lower() or "capture photo" in text.lower():
        # Define the path where the image will be saved
        image_path = "/home/finalproject/PycharmProjects/RubberDuck/captured_image.jpg"

        # Notify user of the delay
        delay_message = "Ok, taking picture in 5 seconds."
        print(delay_message)
        text_to_speech(delay_message)

        # Add a delay
        time.sleep(5)

        # Capture the image
        capture_image(image_path)

        print("Picture taken and saved!")
        text_to_speech("Quack quack! Picture taken and being analyzed!")

        # Encode and analyze the image
        base64_image = encode_image(image_path)
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image?"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]
                }
            ],
            "max_tokens": 300
        }

        response=requests.post("https://api.openai.com/v1/chat/completions", headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }, json=payload)



        if response.status_code == 200:
            response_json = response.json()
            extracted_code = response_json['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": f"The image contains: {extracted_code}"})
            text_to_speech("What the problem you facing?")
        continue

    # Append the user input to the conversation
    messages.append({"role": "user", "content": text})

    # Get a response from OpenAI's ChatGPT model
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = completion.choices[0].message['content']
    reply = re.sub(r'[`"\']', '', reply)
    reply = reply.replace("backquote", "").strip()
    print(f"Assistant: {reply}")
    text_to_speech(reply.replace("backquote", "").strip())


    # Append the assistant's response to the conversation
    messages.append({"role": "assistant", "content": reply})
