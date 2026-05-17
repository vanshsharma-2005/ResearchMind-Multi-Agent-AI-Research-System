<div align="center">

# 🧠 ResearchMind

### Multi-Agent AI Research System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Google Gemini](https://img.shields.io/badge/Gemini_2.0_Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![Tavily](https://img.shields.io/badge/Tavily-Search_API-FF6B35?style=for-the-badge)](https://tavily.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **A production-grade, multi-agent AI pipeline that autonomously transforms any topic into a structured, critically evaluated research report — in under 3 minutes.**

[🚀 Live Demo](#) · [📖 How It Works](#how-it-works) · [🐛 Report Bug](https://github.com/vanshsharma-2005/ResearchMind-Multi-Agent-AI-Research-System/issues) · [✨ Request Feature](https://github.com/vanshsharma-2005/ResearchMind-Multi-Agent-AI-Research-System/issues)

</div>

---

## 📌 Overview

**ResearchMind** is an agentic AI system that mimics how a human research team works — searching, reading, writing, and peer-reviewing — but does it autonomously in minutes. You provide a topic, and the system orchestrates 4 specialized AI agents in sequence to deliver a polished, citation-backed research report with a built-in quality critique.

Built on **LangChain + Google Gemini 2.0 Flash + Tavily Search API**, it demonstrates real-world multi-agent orchestration where each agent has a distinct role and passes its output downstream — just like a production LLM pipeline.

---

## ✨ Features

- 🔍 **Real-Time Web Search** — Tavily API retrieves live, up-to-date sources (no hallucinated citations)
- 🌐 **Deep Content Scraping** — BeautifulSoup scrapes full article content beyond search snippets
- ✍️ **Structured Report Generation** — Introduction, Key Findings, Conclusion, and Sources — auto-formatted
- 🧐 **AI Critic & Quality Scoring** — Independent agent reviews the report, gives a score out of 10, and flags gaps
- ⚡ **Live Pipeline Status** — Real-time UI updates as each agent completes its step
- 📥 **1-Click Report Download** — Export the final report instantly
- 🎨 **Custom Dark UI** — Per-agent output cards with status indicators
- 🔐 **Secure Key Management** — API keys handled via Streamlit Secrets

---

## 🤖 The 4-Agent Architecture

ResearchMind orchestrates 4 specialized agents in a sequential pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT (Topic)                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  🔵  AGENT 1 — Search Agent   │
            │  Tool: Tavily Search API      │
            │  Queries web, retrieves top   │
            │  5 results, summarises into   │
            │  structured bullet points     │
            └───────────────┬───────────────┘
                            │  Search Summary + Raw URLs
                            ▼
            ┌───────────────────────────────┐
            │  🟣  AGENT 2 — Reader Agent   │
            │  Tool: BeautifulSoup Scraper  │
            │  Picks best URL, scrapes full │
            │  content (up to 3,000 chars), │
            │  extracts key facts & data    │
            └───────────────┬───────────────┘
                            │  Deep Content Analysis
                            ▼
            ┌───────────────────────────────┐
            │  🟡  CHAIN 3 — Writer Chain   │
            │  Model: Gemini 2.0 Flash      │
            │  Synthesises search + scraped │
            │  content into a structured    │
            │  report with cited sources    │
            └───────────────┬───────────────┘
                            │  Full Research Report
                            ▼
            ┌───────────────────────────────┐
            │  🟢  CHAIN 4 — Critic Chain   │
            │  Model: Gemini 2.0 Flash      │
            │  Independently evaluates the  │
            │  report: Score, Strengths,    │
            │  Improvements, Verdict        │
            └───────────────┬───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │   📄  FINAL OUTPUT            │
            │   Report + Critique + Score   │
            │   Available for download      │
            └───────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Role |
|-----------|-----------|------|
| **LLM** | Google Gemini 2.0 Flash | Powers all 4 agents for reasoning & generation |
| **Orchestration** | LangChain (Chains + Prompts) | Manages agent prompts, chaining, and output parsing |
| **Web Search** | Tavily Search API | Real-time grounded web search (top 5 results) |
| **Web Scraping** | BeautifulSoup + Requests | Deep content extraction from source URLs |
| **Frontend** | Streamlit | Interactive UI with live pipeline updates |
| **Output Parsing** | LangChain `StrOutputParser` | Cleans and formats LLM outputs |
| **Env Management** | python-dotenv / Streamlit Secrets | Secure API key handling |

---

## 📁 Project Structure

```
ResearchMind-Multi-Agent-AI-Research-System/
│
├── app.py                  # Streamlit frontend — UI, pipeline triggers, download
├── research_pipeline.py    # Core pipeline — all 4 agents, generator logic
├── requirements.txt        # Python dependencies
└── README.md               # You are here
```

### Key File: `research_pipeline.py`

This is the brain of the system. It contains:

- `web_search()` — Tavily API wrapper returning top 5 results
- `scrape_url()` — BeautifulSoup scraper with noise removal (scripts, nav, footers)
- `extract_first_url()` — Parses URL from search output for the Reader agent
- `search_agent()` — Agent 1: searches + summarises with LLM
- `reader_agent()` — Agent 2: scrapes best source + extracts insights
- `build_writer_chain()` — Agent 3: LangChain chain for report writing
- `build_critic_chain()` — Agent 4: LangChain chain for quality review
- `run_research_pipeline()` — **Generator function** yielding live `(step, status, data)` tuples for Streamlit real-time updates

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- [Google AI Studio API Key](https://aistudio.google.com/app/apikey) (free)
- [Tavily API Key](https://tavily.com) (free tier available)

### 1. Clone the Repository

```bash
git clone https://github.com/vanshsharma-2005/ResearchMind-Multi-Agent-AI-Research-System.git
cd ResearchMind-Multi-Agent-AI-Research-System
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up API Keys

Create a `.env` file in the root:

```env
GOOGLE_API_KEY=your_google_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run the App

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501` 🎉

---

## ☁️ Deploy on Streamlit Cloud

1. Push the repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in
3. Click **New App** → select this repo
4. Set **Main file path** → `app.py`
5. Under **Advanced Settings → Secrets**, add:

```toml
GOOGLE_API_KEY = "your_google_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
```

6. Click **Deploy** — live in ~2 minutes!

---

## 📖 How It Works

```
1. 🔍  User inputs a research topic in the Streamlit UI
2. ⚡  Pipeline generator starts — Streamlit listens for live updates
3. 🔵  Search Agent queries Tavily → top 5 web results → LLM summarises
4. 🟣  Reader Agent picks best URL → scrapes up to 3,000 chars of content → LLM extracts insights
5. 🟡  Writer Chain receives both outputs → Gemini writes structured report with sources
6. 🟢  Critic Chain receives report → independently scores (X/10) and reviews
7. 📄  Final report + critique displayed in UI → available for 1-click download
```

---

## ⚙️ Configuration

Tunable parameters inside `research_pipeline.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_results` | `5` | Number of Tavily search results per query |
| `scraped content limit` | `3000 chars` | Max content extracted per URL |
| `timeout` | `8 sec` | HTTP request timeout for scraping |
| `temperature` | `0.3` | LLM creativity — lower = more factual |
| `model` | `gemini-2.0-flash` | Gemini model variant used for all agents |

---

## ⚠️ Limitations

- Scraping may fail on JavaScript-heavy or paywalled websites
- Quality depends on availability and richness of online sources for the topic
- Currently scrapes only the **top 1 URL** — extending to top 3–5 would improve depth
- No persistent storage — reports are lost on session refresh unless downloaded

---

## 🔮 Future Improvements

- [ ] Scrape top 3–5 URLs instead of just 1 for richer research
- [ ] Add LangGraph for more flexible, conditional agent routing
- [ ] Support PDF/DOCX export of the final report
- [ ] Add memory so the system can do multi-turn iterative research
- [ ] Integrate Wikipedia and arXiv as additional knowledge sources
- [ ] Add a human-in-the-loop feedback step after the Critic

---

## 🤝 Contributing

1. Fork the project
2. Create your branch (`git checkout -b feature/NewAgent`)
3. Commit your changes (`git commit -m 'Add new agent'`)
4. Push to branch (`git push origin feature/NewAgent`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👤 Author

**Vansh Sharma**

- GitHub: [@vanshsharma-2005](https://github.com/vanshsharma-2005)

---

<div align="center">

Made with ❤️ by **Vansh Sharma**

*Built to demonstrate how multi-agent LLM systems can automate end-to-end knowledge work — from raw search to polished, peer-reviewed output.*

*If this project helped you, consider giving it a ⭐ on GitHub!*

</div>
