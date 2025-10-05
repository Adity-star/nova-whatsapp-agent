# 🤖 Nova — A Realistic WhatsApp AI Agent

A WhatsApp agent inspired by the movie *Ex Machina*. While Nova isn’t fully sentient… yet 😏, she can engage in realistic conversations, understand voice notes, react to images, and even send her own voice notes and images.  

Think of Nova as your personal mini-AGI experiment running in WhatsApp — smart, interactive, and a bit mischievous. 😁

![ava_final_design](https://github.com/user-attachments/assets/d546f2b8-7044-4a24-bea6-7c1a8fd49af5)

--- 

## 🧠 What Nova Can Do

- **Receive & Send WhatsApp Messages** via WhatsApp Business API  
- **Understand Your Voice** with automatic speech-to-text (STT) using Whisper  
- **Send Voice Notes Back** with ElevenLabs TTS  
- **Understand and Generate Images** using VLMs + FLUX Diffusion Models  
- **Maintain Memory** (short- and long-term) with Qdrant vector DB  
- **Run LangGraph Workflows** for reasoning and behavior control  
- **Deploy Seamlessly** to Google Cloud Run (CI/CD ready)  

---

## 🧱 Tech Stack

| Component       | Description |
|----------------|-------------|
| **Groq**        | Ultra-fast inference for LLMs (Llama 3.3, Whisper, Vision) |
| **Qdrant**      | Vector database to power Nova’s long-term memory |
| **Cloud Run**   | Serverless app hosting for fast, secure deployment |
| **LangGraph**   | Agent workflow engine to manage conversation flow |
| **ElevenLabs**  | High-quality text-to-speech voice generation |
| **Together AI** | Diffusion model image generation backend |
| **FastAPI**     | API backend to handle message flow and integrations |
| **Chainlit**    | Local testing interface for Nova |

---

## 🚀 Getting Started Start

###  1. Clone the Repo
```bash
git clone https://github.com/your-username/nova-whatsapp-agent.git
cd nova-whatsapp-agent
```

### 2. Install uv

Instead of `pip` or `poetry`, we are using `uv` as the Python package manager. 

To install uv, simply follow this [instructions](https://docs.astral.sh/uv/getting-started/installation/). 


### 3. Install the project dependencies

Once uv is intalled, you can install the project dependencies. First of all, let's create a virtual environment.

```bash
uv venv .venv
# macOS / Linux
. .venv/bin/activate # or source .venv/bin/activate
# Windows
. .\.venv\Scripts\Activate.ps1 # or .\.venv\Scripts\activate
uv pip install -e .
```
Just to make sure that everything is working, simply run the following command:

```bash
 uv run python --version
```


### 4. Environment Variables

Now that all the dependencies are installed, it's time to populate the `.env` file with the correct values.
To help you with this, we have created a `.env.example` file that you can use as a template.

```
cp .env.example .env
```R_API_KEY=your_together_ai_key
```

Now, you can open the `.env` file with your favorite text editor and set the correct values for the variables.
You'll notice there are a lot of variables that need to be set.

```
GROQ_API_KEY=""

ELEVENLABS_API_KEY=""
ELEVENLABS_VOICE_ID=""

TOGETHER_API_KEY=""

QDRANT_URL=""
QDRANT_API_KEY=""

WHATSAPP_PHONE_NUMBER_ID = ""
WHATSAPP_TOKEN = ""
WHATSAPP_VERIFY_TOKEN = ""
```

In this doc, we will show you how to get the values for all of these variables, except for the WhatsApp ones. 
That's something we will cover in a dedicated lesson, so don't worry about it for now, **you can leave the WhatsApp variables empty**.

### Groq
- To create the GROQ_API_KEY, and be able to interact with Groq models, you just need to follow this [instructions](https://console.groq.com/docs/quickstart).

### ElevenLabs
- To create the ELEVENLABS_API_KEY you need to create an account in [ElevenLabs](https://elevenlabs.io/). After that, go to your account settings and create the API key.

- As for the voice ID, you can check the available voices and select the one you prefer! We'll cover this in a dedicated lesson.

### Together AI
-  in to [Together AI](https://www.together.ai/) and, inside your account settings, create the API key.

- Once you have created the API key, you can copy it and paste it into an `.env` file (following the same format as the `.env.example` file).

- As we did with the previous API keys, copy the value and paste it into your own `.env` file.

### Qdrant

- This project uses Qdrant both locally (you don't need to do anything) and in the cloud (you need to create an account in [Qdrant Cloud](https://login.cloud.qdrant.io/)).
- You also need a QDRANT_URL, which is the URL of your Qdrant Cloud instance. You can find it here:
- Copy both values and paste them into your own `.env` file.

**This is everything you need to get the project up and running.**

### 5. First run

Once you have everything set up, it's time to run the project locally. This is the best way to check that everything is working before starting the course.

To run the project locally, we have created a [Makefile](https://github.com/Adity-star/nova-whatsapp-agent/blob/main/Makefile). Use the command `nova-run` to start the project.

```bash
make nova-run
```

###  6. Local Testing with Chainlit
```bash
chainlit run src/nova_companion/interfaces/chainlit/app.py
```
Test Nova’s responses, image understanding, or memory behavior before deployment.

This command will start a Docker Compose application with three services:

* A Qdrant Database (http://localhost:6333/dashboard)
* A Chainlit interface (http://localhost:8000)
* A FastAPI application (http://localhost:8080/docs)

The FastAPI application is necessary for the WhatsApp integration, but that's something we will cover in Lesson 6. So, for now,
you can ignore it. Simply click the link to the Chainlit interface to start interacting with Nova.

You should see something like this:

![Nova Chainlit](img/ava_chainlit.png)

> If you want to clean up the docker compose application and all the related local folders, you can run `make nova-delete`. For more info, check the [Makefile](../Makefile).

---
## 📡 Deploy to Google Cloud Run

**Nova** is containerized and CI/CD ready.

### 🔧 Build & Push Image

```bash
gcloud config set project YOUR_PROJECT_ID
gcloud builds submit --region=asia-northeast1
```
### ✅ Deploy

```bash
gcloud run deploy nova-service \
  --image asia-northeast1-docker.pkg.dev/YOUR_PROJECT_ID/nova-app/app:latest \
  --region asia-northeast1 \
  --platform managed \
  --allow-unauthenticated
```
---
## 🧠 Nova’s Memory, Visual, and Audio Capabilities

### 🧩 Memory

An agent without memory is like the main character in *Memento* — confusing and forgetful. Nova has two types of memory:

#### 🔷 Short-Term Memory

- Stores conversation sequences to maintain context using SQLite  
- Summarizes ongoing interactions for later reference

#### 🔷 Long-Term Memory

- Stores key conversation details in Qdrant as embeddings  
- Remembers names, professions, images, and past interactions  
- Makes Nova feel personal and aware

---

### 🖼️ Visual Capabilities

- **Image Understanding:** Llama-3.2-90b-Vision via Groq  
- **Image Generation:** FLUX Diffusion Models via Together AI

### 🔊 Audio Pipeline

- **STT (Speech-to-Text):** `whisper-large-v3-turbo` from Groq  
- **TTS (Text-to-Speech):** ElevenLabs voices for lifelike responses  
- **Voice Notes:** Nova can reply with spoken audio on WhatsApp

---
## 🧠 Nova’s Brain: LangGraph

Nova’s core is a **LangGraph** node-edge architecture:

- Each **node** handles a task: image processing, voice processing, memory retrieval, etc.  
- **State** maintains all details of the conversation, including text, audio, images, and contextual info.

---
## 🎉 Fun Overview

A WhatsApp agent that responds with text, voice, and images.  
Think of it as a mini-AGI in your pocket:

> “Nova, what are you doing?”

- Generates a voice reply and a small image of her ‘activity’ 😁  
- Maintains context like a real conversation with memory of past chats  
- Learns to provide richer responses over time

---

## 🤝 Contributing

Contributions are welcome! Feel free to fork the repository, raise issues, and submit pull requests.

---

## 📝 License

This project is licensed under the MIT License.

---

## 🌟 Connect with Me

[LinkedIn](https://www.linkedin.com/in/aditya-a-27b43533a/)
