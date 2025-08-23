# 🤖 Nova — A Realistic WhatsApp AI Agent

*Nova* is a cutting-edge WhatsApp agent, inspired by the movie *Ex Machina*. No, she’s not fully sentient (yet)  but she’s smart enough to hold rich conversations, respond with voice, see images, generate media, and even talk about her daily activities.

Built entirely with modern AI tooling, Ava is your own mini AGI experiment running in the palm of your hand.

---

## 🧠 What Ava Can Do

-  **Receive & Send WhatsApp Messages** via WhatsApp Business API
-  **Understand Your Voice** with automatic speech-to-text (STT) using Whisper
-  **Send Voice Notes Back** with ElevenLabs TTS
-  **Understand and Generate Images** using VLMs + FLUX Diffusion Models
-  **Maintain Memory** (short- and long-term) with Qdrant vector DB
-  **Run LangGraph Workflows** for reasoning and behavior control
-  **Deploy Seamlessly** to Google Cloud Run (CI/CD ready)

---

## 🧱 Tech Stack

| Component       | Description |
|----------------|-------------|
| **Groq**        | Ultra-fast inference for LLMs (Llama 3.3, Whisper, Vision) |
| **Qdrant**      | Vector database to power Ava’s long-term memory |
| **Cloud Run**   | Serverless app hosting for fast, secure deployment |
| **LangGraph**   | Agent workflow engine to manage conversation flow |
| **ElevenLabs**  | High-quality text-to-speech voice generation |
| **Together AI** | Diffusion model image generation backend |
| **FastAPI**     | API backend to handle message flow and integrations |
| **Chainlit**    | Local testing interface for Ava |

---

## 🚀 Quick Start

### ✅ 1. Clone the Repo

```bash
git clone https://github.com/your-username/nova-whatsapp-agent.git
cd nova-whatsapp-agent
```
### ✅ 2. Set Up Environment

Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
### ✅ 3. Configure Environment Variables

Create a .env file in the root directory and add your secrets:
```bash
GROQ_API_KEY=your_groq_key
ELEVENLABS_API_KEY=your_elevenlabs_key
QDRANT_API_KEY=your_qdrant_key
TOGETHER_API_KEY=your_together_ai_key
```
### ✅ 4.Local testing with chainlit.
Supports local/dev via chainlit ui.
```bash
chainlit run src/nova_companion/interfaces/chainlit/app.py
```
->Test Nova’s responses, image understanding, or memory behavior — all before deploying.

## 📡 Deploy to Google Cloud Run

Nova is containerized and ready for deployment using Google Cloud Build and Artifact Registry.

### 🔧 Build & Push Image
```bash
gcloud config set project YOUR_PROJECT_ID
gcloud builds submit --region=asia-northeast1
```
Make sure your Artifact Registry and Cloud Run are already configured.

### Deploy
```bash
gcloud run deploy ava-service \
  --image asia-northeast1-docker.pkg.dev/YOUR_PROJECT_ID/nova-app/app:latest \
  --region asia-northeast1 \
  --platform managed \
  --allow-unauthenticated
```
---
## Memory, Visual, and Audio Capabilities

Ava is designed to engage users across multiple sensory modalities and retain contextual awareness through robust memory architecture. Here's how:

Memory Architecture

Ava uses a hybrid memory system to maintain both immediate context and long-term memory:

Short-Term Memory
Managed in-session using LangGraph state — allows Ava to track ongoing conversations.

Long-Term Memory
Stored in Qdrant, a vector database, using embedded representations. This allows Ava to recall:

Your name

Previous conversations

Past images and interactions

This persistent memory makes Ava feel more personal and intelligent — she “remembers” you.

Visual Capabilities

Ava can both interpret and generate images using state-of-the-art vision and diffusion models:

Image Generation
Powered by Together AI’s FLUX diffusion models to produce high-quality visuals based on prompts or memory.

Image Understanding
Utilizes Llama-3.2 Vision through Groq to “see” and understand uploaded user images.

Ava doesn’t just talk — she sees and imagines too.

Audio Pipeline

Ava supports fully bidirectional audio communication:

Speech-to-Text (STT)
Real-time transcription using Whisper, accelerated via Groq for lightning-fast performance.

Text-to-Speech (TTS)
Lifelike voice responses using ElevenLabs, making interactions more immersive.

Voice Note Replies
Ava sends back audio messages on WhatsApp, allowing for rich, spoken conversation.

With audio I/O, Ava offers a natural, hands-free way to interact.


