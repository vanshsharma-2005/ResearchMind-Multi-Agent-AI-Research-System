import os
from langchain.tools import tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient

# ── Tool definitions ──────────────────────────────────────────────────────────

def get_tavily_client(api_key: str) -> TavilyClient:
    return TavilyClient(api_key=api_key)

def make_web_search_tool(tavily_client: TavilyClient):
    @tool
    def web_search(query: str) -> str:
        """Search the web for recent and reliable information on a topic. Returns Titles, URLs and snippets."""
        results = tavily_client.search(query=query, max_results=5)
        out = []
        for r in results['results']:
            out.append(
                f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
            )
        return "\n----\n".join(out)
    return web_search

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"

# ── Agent / Chain builders ────────────────────────────────────────────────────

def build_llm(google_api_key: str) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        google_api_key=google_api_key,
    )

def build_search_agent(llm, web_search_tool):
    tools = [web_search_tool]
    prompt = PromptTemplate.from_template(
        "You are a research assistant. Use the web_search tool to find information.\n\n"
        "Tools available: {tools}\nTool names: {tool_names}\n\n"
        "Question: {input}\n\nThought: {agent_scratchpad}"
    )
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True, max_iterations=5)

def build_reader_agent(llm):
    tools = [scrape_url]
    prompt = PromptTemplate.from_template(
        "You are a web scraper. Use scrape_url to extract content from URLs.\n\n"
        "Tools available: {tools}\nTool names: {tool_names}\n\n"
        "Task: {input}\n\nThought: {agent_scratchpad}"
    )
    agent = create_react_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False, handle_parsing_errors=True, max_iterations=5)

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

# ── Main pipeline (generator for streaming status) ───────────────────────────

def run_research_pipeline(topic: str, tavily_api_key: str, google_api_key: str):
    """
    Generator that yields (step_name, status, data) tuples so Streamlit
    can update the UI in real-time.
    """
    state = {}

    llm = build_llm(google_api_key)
    tavily_client = get_tavily_client(tavily_api_key)
    web_search_tool = make_web_search_tool(tavily_client)

    # ── Step 1: Search Agent ──────────────────────────────────────────────────
    yield ("search", "running", None)
    try:
        search_agent = build_search_agent(llm, web_search_tool)
        search_result = search_agent.invoke({
            "input": f"Find recent, reliable and detailed information about: {topic}"
        })
        state["search_results"] = search_result.get("output", "No results found.")
        yield ("search", "done", state["search_results"])
    except Exception as e:
        yield ("search", "error", str(e))
        return

    # ── Step 2: Reader Agent ──────────────────────────────────────────────────
    yield ("reader", "running", None)
    try:
        reader_agent = build_reader_agent(llm)
        reader_result = reader_agent.invoke({
            "input": (
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        })
        state["scraped_content"] = reader_result.get("output", "No content scraped.")
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
