# ResearchMind-Multi-Agent-AI-Research-System
ResearchMind is a production-grade, multi-agent AI research pipeline that autonomously transforms any topic into a structured, critically evaluated research report in minutes.
# ResearchMind — Multi-Agent AI Research System

**ResearchMind** is a production-grade, multi-agent AI research pipeline that autonomously transforms any topic into a structured, critically evaluated research report — in minutes.

Built on **LangChain + Google Gemini 2.5 Flash + Tavily Search**, the system orchestrates four specialized agents in sequence:

- 🔵 **Search Agent** — Queries the web in real-time via Tavily to retrieve the most recent and relevant sources
- 🟣 **Reader Agent** — Scrapes and extracts deep content from the top URLs for richer context
- 🟡 **Writer Chain** — Synthesizes all gathered research into a clean, structured report with introduction, key findings, conclusion, and sources
- 🟢 **Critic Chain** — Independently evaluates the report, assigns a quality score, highlights strengths, and flags areas for improvement

The frontend is a **Streamlit** web application with a custom dark-themed UI, live pipeline status indicators, per-agent output cards, and a one-click report download — making the entire agentic workflow transparent and interactive.

**Tech Stack:** Python · LangChain · Gemini 2.5 Flash · Tavily API · BeautifulSoup · Streamlit

**Key capabilities:**
- Real-time web search grounding (no hallucinated sources)
- Modular agent architecture — each agent is independently swappable
- Streaming pipeline status with live UI updates
- Secure API key management via Streamlit Secrets

---

*Built to demonstrate how multi-agent LLM systems can automate end-to-end knowledge work — from raw search to polished, peer-reviewed output.*

