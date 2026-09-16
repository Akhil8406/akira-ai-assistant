# ⚡ AKIRA — AI Desktop Assistant

AKIRA is a Python-based AI desktop assistant designed to combine voice interaction, local AI, desktop automation, email intelligence, and a custom wake-word system into a single assistant.

Instead of continuously sending microphone audio to speech recognition, AKIRA uses a custom-trained **"Hey Akira"** wake-word model locally. Once activated, it listens for a command, processes the request, performs the required action, and responds through speech.

---

## ✨ Features

### 🎙️ Custom Wake Word

AKIRA uses a custom wake-word model trained specifically for:

> **"Hey Akira"**

The model was trained using **openWakeWord** and exported to ONNX for local inference.

The wake-word detector continuously processes microphone audio locally and activates the full assistant only after the wake phrase is detected.

---

### 🧠 AI Assistant

AKIRA can process natural-language commands and generate conversational responses.

The project is designed to support local AI models through **Ollama**, allowing many assistant operations to run locally.

Example:

```text
User: Hey Akira

AKIRA: Yes?

User: What is machine learning?

AKIRA: Machine learning is when computers learn patterns from data
to make predictions or decisions without being explicitly programmed
for every individual case.
```

---

### 🖥️ Desktop Automation

AKIRA can execute desktop-related commands such as opening applications and performing supported system actions.

Example:

```text
Hey Akira
→ Yes?
→ Open calculator
→ Calculator launches
```

---

### 📧 Gmail Integration

AKIRA integrates with Gmail and can retrieve recent emails.

The email monitoring system periodically checks for new unread messages and can classify whether an email is important.

Important messages can then be announced through AKIRA's voice interface.

OAuth credentials and authentication tokens are intentionally excluded from this repository.

---

### 🔵 Interactive Orb UI

AKIRA includes a desktop orb built using **PySide6**.

The orb visually represents different assistant states:

```text
IDLE
LISTENING
THINKING
SPEAKING
```

The interface appears when AKIRA activates and hides when the assistant returns to its background state.

---

### 🔊 Voice Interaction

The voice pipeline combines:

- Local wake-word detection
- Microphone input
- Speech recognition
- Natural-language command processing
- Text-to-speech responses

This creates a hands-free interaction flow.

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │     Microphone      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   openWakeWord      │
                    │  hey_akira.onnx     │
                    └──────────┬──────────┘
                               │
                         Wake detected
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Speech Recognition  │
                    │  Command Listener   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   AKIRA Assistant   │
                    │ Command Processing  │
                    └───────┬─────┬───────┘
                            │     │
              ┌─────────────┘     └─────────────┐
              ▼                                 ▼
     ┌─────────────────┐               ┌─────────────────┐
     │ Desktop / Tools │               │   Local LLM     │
     │ Gmail / System  │               │     Ollama      │
     └────────┬────────┘               └────────┬────────┘
              │                                 │
              └──────────────┬──────────────────┘
                             ▼
                    ┌─────────────────────┐
                    │    Text-to-Speech   │
                    │   Spoken Response   │
                    └─────────────────────┘
```

---

## 🔄 Assistant Workflow

```text
AKIRA running in background
          ↓
Local microphone monitoring
          ↓
User says "Hey Akira"
          ↓
Custom ONNX model detects wake word
          ↓
AKIRA activates
          ↓
Orb UI appears
          ↓
AKIRA listens for command
          ↓
Speech → Text
          ↓
Command processing
          ↓
Tool execution / AI response
          ↓
AKIRA speaks response
          ↓
Orb disappears
          ↓
Return to wake-word mode
```

---

## 📁 Project Structure

```text
akira-ai-assistant/
│
├── assets/
│   └── wakeword/
│       └── hey_akira.onnx
│
├── src/
│   ├── core/
│   │   └── assistant.py
│   │
│   ├── tools/
│   │   └── email.py
│   │
│   ├── ui/
│   │   └── orb.py
│   │
│   ├── voice/
│   │   ├── listener.py
│   │   ├── speaker.py
│   │   └── wakeword.py
│   │
│   └── main.py
│
├── .gitignore
├── start_akira.vbs
└── README.md
```

The exact structure may evolve as additional capabilities are added.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Wake-word detection | openWakeWord |
| Wake-word inference | ONNX Runtime |
| Audio capture | sounddevice |
| Desktop UI | PySide6 |
| Local AI | Ollama |
| Email integration | Gmail API |
| Voice input | Speech Recognition |
| Voice output | Text-to-Speech |
| Version control | Git / GitHub |

---

## 🚀 Running AKIRA

### 1. Clone the repository

```bash
git clone https://github.com/Akhil8406/akira-ai-assistant.git
cd akira-ai-assistant
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the dependencies required by the project.

A pinned `requirements.txt` will be maintained as the dependency set stabilizes.

### 4. Configure Gmail

Gmail functionality requires your own Google OAuth credentials.

Place your local credentials in the project root as required by the Gmail integration.

> **Never commit OAuth credentials or authentication tokens to GitHub.**

The repository's `.gitignore` excludes sensitive authentication files.

### 5. Start Ollama

Make sure Ollama and the configured local model are available before starting AI features that depend on it.

### 6. Start AKIRA

```powershell
python -m src.main
```

Then say:

```text
Hey Akira
```

---

## 🔐 Security & Privacy

Sensitive files are not included in the repository.

Examples include:

```text
credentials.json
credentials.json.json
token.json
.env
```

The custom wake-word stage runs locally, so AKIRA does not need to continuously send background microphone audio to a cloud speech-recognition service just to determine whether the assistant was called.

Users who clone the repository must configure their own credentials for external services.

---

## 🧪 Custom Wake-Word Model

The **"Hey Akira"** wake-word model was custom trained using openWakeWord.

Model:

```text
assets/wakeword/hey_akira.onnx
```

Basic inference flow:

```text
16 kHz microphone audio
        ↓
Audio feature extraction
        ↓
ONNX wake-word model
        ↓
Detection confidence
        ↓
Threshold reached
        ↓
AKIRA activation
```

This separates lightweight wake-word detection from the more expensive full speech-recognition pipeline.

---

## 🚧 Current Development Status

AKIRA is actively under development.

Working components include:

- Custom "Hey Akira" wake-word detection
- ONNX-based local wake-word inference
- Voice output
- Speech command recognition
- Desktop orb interface
- Gmail retrieval and monitoring
- Important-email classification
- Desktop command handling
- Background startup support
- Local AI integration

Current work is focused on improving the transition between wake-word detection and command capture, reducing response latency, and improving overall voice reliability.

---

## 🗺️ Roadmap

Planned improvements include:

- [ ] Improve wake-word → command-listener handoff
- [ ] Improve microphone reliability
- [ ] Reduce assistant response latency
- [ ] Add conversational memory
- [ ] Expand desktop automation
- [ ] Improve email intelligence
- [ ] Add calendar integration
- [ ] Add reminders and scheduled tasks
- [ ] Add weather and information tools
- [ ] Improve interruption handling
- [ ] Add configurable assistant settings
- [ ] Improve startup/background execution
- [ ] Add automated tests
- [ ] Add dependency locking / `requirements.txt`
- [ ] Expand documentation

---

## 🎯 Project Goal

The long-term goal of AKIRA is to explore how a practical desktop AI agent can combine:

**local AI + voice interfaces + tool use + automation + personalized workflows**

while keeping lightweight operations such as wake-word detection local.

---

## 👨‍💻 Author

**Akhilesh Huddar**

M.Sc. Artificial Intelligence  
Brandenburg University of Technology Cottbus-Senftenberg, Germany

GitHub: [Akhil8406](https://github.com/Akhil8406)

---

## ⚠️ Disclaimer

AKIRA is an experimental personal AI project under active development. Features may change, and some integrations require external services, credentials, or locally installed software.