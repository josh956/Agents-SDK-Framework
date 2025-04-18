from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, ModelSettings, function_tool
from pydantic import BaseModel
from agents.tool import WebSearchTool
import asyncio
import os

os.environ["OPENAI_API_KEY"] = os.getenv("General")
web_search = WebSearchTool()

life_tutor_agent = Agent(
    name="Life tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
    model="gpt-4.1-nano",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
    model="gpt-4.1-mini",
)

ai_research_agent = Agent(
    name="ai research agent",
    handoff_description="Specialist agent for AI research",
    instructions=(
        "You're an AI research specialist. "
        "When you need up to date publications from 2025, breakthroughs, or news, "
        "use the web_search_preview tool and cite your sources."
    ),
    tools=[ web_search ],          # ← include the hosted web‑search tool
)

triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question",
    handoffs=[history_tutor_agent, life_tutor_agent, ai_research_agent],
)

async def main():
    result = await Runner.run(triage_agent, "who was the first president of the united states?")
    print(result.final_output)

    result = await Runner.run(triage_agent, "what is life")
    print(result.final_output)

    result = await Runner.run(triage_agent, "Recent AI News")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())