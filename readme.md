# Personal AI Assistant (Python)

Ye ek voice-based assistant hai — bolo, ye sunega, samjhega, aur bolkar jawab dega.
Time batana, YouTube/Google kholna khud handle karta hai; baki kisi bhi sawal ke liye Claude AI ko call karta hai.

---

## Step 1: Prerequisites

1. Python 3.9+ install hona chahiye.
2. Microphone working honi chahiye (laptop ka built-in bhi chalega).
3. **Free API key (Gemini):** https://aistudio.google.com/apikey se lo — sirf Google account se sign in, koi credit card nahi chahiye, daily 1500 requests tak free milte hain.

---

## Step 2: PyAudio install karna (platform ke hisaab se thoda alag hai)

`pyaudio` microphone access ke liye chahiye, aur ye seedha `pip install` se kabhi kabhi fail ho jata hai. Pehle ye karo:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

Iske baad baki dependencies install karo:

```bash
pip install -r requirements.txt
```

---

## Step 3: API key set karo

```bash
cp .env.example .env
```

`.env` file kholke apni real key daal do:
```
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Step 4: Run karo

```bash
python assistant.py
```

Assistant "Hello! Main tumhara personal AI assistant hu" bolega, uske baad jo bhi bologe wo suno karega.

Try karo:
- "Abhi time kya hai?"
- "YouTube khol do"
- "Search karo best pizza recipe"
- Koi bhi general sawal jaise "Python aur JavaScript me kya difference hai?"
- "Bye" bolne se assistant band ho jayega

---

## Code kaise kaam karta hai

| Function | Kaam |
|---|---|
| `listen()` | Microphone se awaaz record karke Google Speech API se text me convert karta hai |
| `speak()` | Text ko `pyttsx3` se awaaz me bolta hai (offline kaam karta hai, internet nahi chahiye) |
| `handle_command()` | Pehle dekhta hai ki ye koi built-in command hai (time, search, youtube) — agar nahi, to AI ko bhej deta hai |
| `ask_ai()` | Google Gemini ke free API ko call karke general sawalon ka jawab leta hai |

---

## Video content ke liye tips

- Pehli baar demo karte waqt mic permission allow karna mat bhoolna (screen recording me dikhega).


