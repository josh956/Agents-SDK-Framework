#imports
#pip install openai-agents

from agents import Agent, Runner, function_tool
from agents.tool import WebSearchTool
import asyncio
import os

# Set the OpenAI API key from the environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("General")

# Initialize a web search tool for use by agents
web_search = WebSearchTool()

# Define an agent specialized in solving math problems
math_tutor_agent = Agent(
    name="Math tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning, but keep to less than 50 words.",
    model="gpt-4.1-nano",
)

# Define an agent specialized in History
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly. Keep to less than 50 words.",
    model="gpt-4.1-mini",
)

# Define an agent specialized in AI research
ai_research_agent = Agent(
    name="ai research agent",
    handoff_description="Specialist agent for AI research",
    instructions=(
        "You're an AI research specialist. "
        "When you need up to date publications from 2025, breakthroughs, or news, "
        "use the web_search_preview tool and cite your sources. keep to less than 50 words."
    ),
    tools=[ web_search ],          # ← include the hosted web‑search tool
)

#Decision maker agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, math_tutor_agent, ai_research_agent],
)

#Questions being asked
async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is 5+5")
    print(result.final_output)

    result = await Runner.run(triage_agent, "Recent AI News")
    print(result.final_output)

#Running the program
if __name__ == "__main__":
    asyncio.run(main())