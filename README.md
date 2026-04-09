# 🎙️ Voice Agent — AI Portfolio Chatbot

An intelligent, voice-enabled AI chatbot that represents the professional profile of **Thirumurugan Subramaniyan**. Users can interact via voice — ask questions, receive spoken responses — all powered by a RAG (Retrieval-Augmented Generation) pipeline with vector similarity search.

---

## 🧠 System Architecture

```
User Voice Input (Base64 Audio)
        │
        ▼
┌──────────────────┐
│  Audio Extraction │  → Decode base64 → Save to temp file
└────────┬─────────┘
         │
         ▼
┌──────────────────────┐
│  Speech Transcription │  → Groq Whisper large-v3-turbo
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────┐
│  Vector Similarity Search │  → Cohere embed-english-v3.0
│  (SingleStore DB / RAG)   │  → dot_product similarity
└──────────┬───────────────┘
           │
           ▼
┌─────────────────────┐
│  LLM Chatbot (RAG)  │  → OpenAI-compatible LLM
│  + Memory Summary   │  → LangChain ConversationSummaryMemory
└──────────┬──────────┘
           │
           ▼
┌──────────────────────┐
│  Text-to-Speech (TTS)│  → ElevenLabs multilingual v2
└──────────┬───────────┘
           │
           ▼
    Audio Response (MP3)
```

---

## 📁 Project Structure

```
├── main.py                          # FastAPI app entry point
├── .env                             # Environment variables (not committed)
├── requirements.txt
│
├── middleware/
│   ├── middleware.py                # CORS configuration
│   ├── controller.py                # voiceAgentController — orchestrates the full pipeline
│   └── model.py                    # Pydantic request model (voiceAgent)
│
├── helper/
│   ├── audioExtraction.py          # Decode base64 audio → temp file
│   ├── speechTranscription.py      # Groq Whisper transcription
│   ├── getEmbedding.py             # Cohere embedding generation
│   ├── rag.py                      # Vector similarity search + chatbot call
│   ├── ConnectChatBot.py           # LLM chat with memory + RAG context
│   └── textToSpeech.py             # ElevenLabs TTS → MP3 bytes
│
└── Database/
    └── dbconnection.py             # SingleStore DB connection
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A [SingleStore](https://www.singlestore.com/) database instance with a vector-enabled `About` table
- API keys for: Cohere, Groq, ElevenLabs, and an OpenAI-compatible LLM endpoint

### Installation

```bash
git clone https://github.com/thirumurugan2001/Voice-Agent.git
cd Voice-Agent
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DB_HOST=your_singlestore_host
PORT=3306
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_NAME=your_database_name

# LLM (OpenAI-compatible endpoint)
OPEN_API_KEY=your_llm_api_key
API_BASE_URL=https://your-llm-api-base-url/v1
MODEL=your-model-name

# Cohere (Embeddings)
COHERE_API_KEY=your_cohere_api_key

# Groq (Speech Transcription)
GROQ_API_KEY=your_groq_api_key

# ElevenLabs (Text-to-Speech)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### Running the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`.

---

## 🗄️ Database Setup

The project uses **SingleStore** with a vector column for semantic search. Your `About` table should follow this schema:

```sql
CREATE TABLE About (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    description TEXT NOT NULL,
    vector    BLOB NOT NULL  -- stores 1024-dim Cohere embedding as JSON_ARRAY_PACK
);
```

Populate it with chunks of Thirumurugan's professional profile (skills, experience, projects, education, etc.) along with their Cohere embeddings.

---

## 📡 API Reference

### `POST /chatbot/voice/`

Accepts a base64-encoded audio file, processes it through the full voice pipeline, and returns an MP3 audio response.

**Request Body**

```json
{
  "base64": "data:audio/ogg;base64,T2dnUwACAAAAAAAAAA...",
  "extension": ".wav"
}
```

| Field       | Type   | Description                                      |
|-------------|--------|--------------------------------------------------|
| `base64`    | string | Base64-encoded audio (with or without data URI prefix) |
| `extension` | string | File extension for the temp audio file (e.g. `.wav`, `.ogg`) |

**Response**

Returns an `audio/mpeg` stream (MP3) — the spoken answer from the chatbot.

**Error Response**

```json
{
  "error": "description of the error",
  "statusCode": 500
}
```

---

## 🔧 Component Details

### Audio Extraction (`audioExtraction.py`)
Decodes the incoming base64 audio string and writes it to a temporary file on disk. Handles both raw base64 and data URI formats (strips the `data:audio/...;base64,` prefix automatically).

### Speech Transcription (`speechTranscription.py`)
Uses **Groq's Whisper large-v3-turbo** model for fast, accurate speech-to-text. Returns the transcribed question as a plain string.

### Vector Embedding + RAG (`getEmbedding.py`, `rag.py`)
Generates a 1024-dimensional embedding via **Cohere's `embed-english-v3.0`** model, then queries SingleStore using `dot_product` similarity to retrieve the top 2 most relevant knowledge base entries.

### Chatbot with Memory (`ConnectChatBot.py`)
Sends the transcribed question + retrieved knowledge base context to an OpenAI-compatible LLM. Uses **LangChain's `ConversationSummaryMemory`** to maintain context across turns. The system prompt enforces the persona of Thirumurugan Subramaniyan and defines relevance boundaries.

### Text-to-Speech (`textToSpeech.py`)
Converts the LLM's response to speech using **ElevenLabs multilingual v2** (voice ID: `JBFqnCBsd6RMkjVDRZzb`), outputting MP3 at 44.1kHz / 128kbps.

---

## 🌐 CORS Configuration

The following origins are allowed by default (configurable in `middleware/middleware.py`):

```
http://localhost:5173    (Vite dev server)
http://127.0.0.1:5173
http://localhost:3000    (React/Next.js dev server)
http://127.0.0.1:3000
```

Update the `origins` list to add your production frontend URL.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API Framework | FastAPI |
| Database | SingleStore (vector search) |
| Embeddings | Cohere `embed-english-v3.0` |
| Speech-to-Text | Groq Whisper `large-v3-turbo` |
| LLM | OpenAI-compatible endpoint |
| Conversation Memory | LangChain `ConversationSummaryMemory` |
| Text-to-Speech | ElevenLabs Multilingual v2 |
| Validation | Pydantic v2 |

---

## ⚠️ Notes & Limitations

- **Memory is per-process**: `ConversationSummaryMemory` is a module-level singleton, so conversation history is shared across all requests in a single server process. For multi-user production deployments, consider session-based memory keyed by user ID.
- **Temporary files**: Audio files are written to the OS temp directory and not cleaned up automatically. Add a cleanup step in `audioExtraction` for production use.
- **CORS**: The allowed origins list is hardcoded for local development. Update before deploying to production.
- **TTS minimum length**: ElevenLabs requires at least 10 characters of text input.

---

## 📄 License

MIT License — feel free to fork and adapt for your own portfolio chatbot.