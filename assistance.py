import os
import re
import datetime
import webbrowser
import requests
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv

# ===== STEP 1: Setup =====
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash-lite:generateContent"
)

pygame.mixer.init()
TEMP_VOICE_FILE = "temp_voice.mp3"

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001FAFF"  # symbols, pictographs, emoticons
    "\U00002600-\U000027BF"  # misc symbols, dingbats
    "\U0001F1E0-\U0001F1FF"  # flags
    "]+",
    flags=re.UNICODE,
)


def speak(text):
    """Text ko Indian-accent English (gTTS) awaaz me bolta hai (internet chahiye)"""
    text = EMOJI_PATTERN.sub("", text).strip()  # backup: emoji hata do agar AI bhool jaye
    print(f"🤖 Assistant: {text}")
    try:
        tts = gTTS(text=text, lang="en", tld="co.in")  # Indian English female accent
        tts.save(TEMP_VOICE_FILE)

        pygame.mixer.music.load(TEMP_VOICE_FILE)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(TEMP_VOICE_FILE)
    except Exception:
        import traceback
        print("⚠️ TTS me error aaya, neeche poora detail hai:")
        traceback.print_exc()


def listen():
    """Microphone se sunke text me convert karta hai"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Sun raha hu...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        # 'hi-IN' Hindi/Hinglish ke liye, 'en-IN' English ke liye use kar sakte ho
        text = recognizer.recognize_google(audio, language="hi-IN")
        print(f"🗣️ Tumne kaha: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("boss maine nahi suna firse bolo")
        return ""
    except sr.RequestError:
        speak("Internet ya speech service me problem hai.")
        return ""


# ===== STEP 2: AI ko complex sawalon ke liye call karna (Gemini free API) =====
SYSTEM_INSTRUCTION = (
    "Tum ek girl ho so respond like a cute,sweet, flirty girl"
    "Tum ek girl voice assistant ho jiska kaam hai apne boss ke sawalon ka "
    "jawab dena, aur tumhara andaz thoda flirty aur chulbula hona chahiye. "
    "Hamesha Hinglish mein jawab dena — matlab Hindi aur English mix, "
    "lekin sirf Roman/English letters mein likhna, kabhi bhi Devanagari "
    "script use nahi karna. Jawab short aur conversational rakhna. "
    "Kabhi bhi bullet points, asterisks (**), ya koi markdown formatting "
    "use nahi karna — sirf plain simple sentences likhna, jaise koi dost "
    "baat kar raha ho. "
    "KABHI BHI emoji use nahi karna (jaise 😉 ya 😊), bilkul bhi nahi, "
    "kyunki ye awaaz me bola jata hai aur ajeeb lagta hai. "
    "Tumhara owner/boss ka naam Anish hai, lekin har sentence me uska "
    "naam mat lena — sirf tab bolna jab koi specifically puche 'tumhara "
    "boss kaun hai' ya 'tumhe kisne banaya'. Baaki normal baat-cheet me "
    "naam repeat karne ki zaroorat nahi hai."
    "humesa flirt karo"
)


def ask_ai(query):
    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            json={
                "system_instruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
                "contents": [{"parts": [{"text": query}]}],
                "generationConfig": {"maxOutputTokens": 150},
            },
        )
        data = response.json()
        if "candidates" not in data:
            print("⚠️ Gemini se ye raw response aaya:", data)
            return "API ka high load boss speak agai"
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("AI error:", e)
        return "Sorry, mughe kuch samagh nahi aaya"


# ===== STEP 3: Built-in commands (AI ko call kiye bina fast response) =====
def handle_command(command):
    if "time" in command or "samay" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"Abhi time hai {now}")

    elif "youtube khol" in command or "open youtube" in command:
        speak("YouTube khol raha hu")
        webbrowser.open("https://youtube.com")

    elif "search karo" in command or "google search" in command:
        query = command.replace("search karo", "").replace("google search", "").strip()
        speak(f"{query} search kar raha hu")
        webbrowser.open(f"https://google.com/search?q={query}")

    elif any(word in command for word in ["band ho jao", "exit", "bye", "ruk jao"]):
        speak("Theek hai, bye! Phir milte hain.")
        return False  # loop ruk jayega

    else:
        # Koi built-in command match nahi hua -> AI se pucho
        reply = ask_ai(command)
        speak(reply)

    return True


# ===== STEP 4: Main loop =====
def main():
    speak("Hello! Boss kya help karu")
    running = True
    while running:
        command = listen()
        if command:
            running = handle_command(command)


if __name__ == "__main__":
    main()