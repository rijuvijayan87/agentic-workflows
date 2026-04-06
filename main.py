import asyncio
import os

from agents import Agent, OpenAIChatCompletionsModel, Runner
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv(override=True)

client = AsyncOpenAI(
    api_key=os.environ["ZLLAMA_API_KEY"],
    base_url=os.environ["ZLLAMA_BASE_URL"].rstrip("/") + "/v1",
)

model = OpenAIChatCompletionsModel(
    model="claude-4-sonnet",
    openai_client=client,
)

agent = Agent(
    name="ZllamaAgent",
    instructions="Be concise and helpful.",
    model=model,
)


async def main():
    result = await Runner.run(
        agent, "Write a 1-paragraph summary of Browser Isolation."
    )
    print(result.final_output)


asyncio.run(main())
