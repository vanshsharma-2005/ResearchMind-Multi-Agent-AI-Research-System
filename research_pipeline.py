import os
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage


# ── LLM builder ──────────────────────────────────────────────────────────────

def build_llm(google_api_key: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.3,
        google_api_key=google_api_key,
    )


# ── Tool functions (plain Python — no LangChain agent needed) ────────────────

def web_search(query: str, tavily_api_key: str) -> str:
    """Search the web via Tavily and return titles, URLs and snippets."""
    try:
        client = TavilyClient(api_key=tavily_api_key)
        results = client.search(query=query, max_results=5)
        out = []
        for r in results.get("results", []):
            out.append(
                f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
            )
        return "\n----\n".join(out) if out else "No results found."
    except Exception as e:
        return f"Search failed: {str(e)}"


def scrape_url(url: str) -> str:
    """Scrape and return clean text from a URL."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"


def extract_first_url(search_text: str) -> str:
    """Pull the first URL out of search results text."""
    for line in search_text.split("\n"):
        line = line.strip()
        if line.startswith("URL:"):
            return line.replace("URL:", "").strip()
    return ""


# ── LLM-powered agent wrappers (using plain chat calls) ──────────────────────

def search_agent(topic: str, tavily_api_key: str, llm) -> str:
    """Agent 1: search the web and return a summary of findings."""
    raw = web_search(topic, tavily_api_key)

    messages = [
        SystemMessage(content="You are a research assistant. Summarise the search results below into clear bullet points, keeping all URLs intact."),
        HumanMessage(content=f"Topic: {topic}\n\nSearch Results:\n{raw}"),
    ]
    response = llm.invoke(messages)
    # Attach raw results so writer has full URL list
    return response.content + "\n\n---RAW---\n" + raw


def reader_agent(topic: str, search_summary: str, llm) -> str:
    """Agent 2: pick the best URL from search results and scrape it."""
    url = extract_first_url(search_summary)
    if not url:
        return "No URL found to scrape."

    scraped = scrape_url(url)

    messages = [
        SystemMessage(content="You are a web content analyst. Extract the most relevant facts, data points, and insights from the scraped text below."),
        HumanMessage(content=f"Topic: {topic}\nSource URL: {url}\n\nScraped Content:\n{scraped}"),
    ]
    response = llm.invoke(messages)
    return response.content


# ── Writer & Critic chains ────────────────────────────────────────────────────

def build_writer_chain(llm):
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
        ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
    ])
    return writer_prompt | llm | StrOutputParser()


def build_critic_chain(llm):
    critic_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a sharp and constructive research critic. Be honest and specific."),
        ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
    ])
    return critic_prompt | llm | StrOutputParser()


# ── Main pipeline (generator for live Streamlit updates) ─────────────────────

def run_research_pipeline(topic: str, tavily_api_key: str, google_api_key: str):
    """
    Generator yielding (step, status, data) tuples so Streamlit
    can update the UI in real-time.

    Steps: search | reader | writer | critic | complete
    Status: running | done | error
    """
    state = {}
    llm = build_llm(google_api_key)

    # ── Step 1: Search Agent ──────────────────────────────────────────────────
    yield ("search", "running", None)
    try:
        state["search_results"] = search_agent(topic, tavily_api_key, llm)
        yield ("search", "done", state["search_results"])
    except Exception as e:
        yield ("search", "error", str(e))
        return

    # ── Step 2: Reader Agent ──────────────────────────────────────────────────
    yield ("reader", "running", None)
    try:
        state["scraped_content"] = reader_agent(topic, state["search_results"], llm)
        yield ("reader", "done", state["scraped_content"])
    except Exception as e:
        yield ("reader", "error", str(e))
        return

    # ── Step 3: Writer Chain ──────────────────────────────────────────────────
    yield ("writer", "running", None)
    try:
        writer_chain = build_writer_chain(llm)
        research_combined = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })
        yield ("writer", "done", state["report"])
    except Exception as e:
        yield ("writer", "error", str(e))
        return

    # ── Step 4: Critic Chain ──────────────────────────────────────────────────
    yield ("critic", "running", None)
    try:
        critic_chain = build_critic_chain(llm)
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        yield ("critic", "done", state["feedback"])
    except Exception as e:
        yield ("critic", "error", str(e))
        return

    yield ("complete", "done", state)
