import os
from agents import Agent, Runner
import asyncio

from dotenv import load_dotenv
load_dotenv(override=True)

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# Define the Task Generator agent
task_generator = Agent(
    name="Task Generator",
    instructions="""You help users break down their specific LLM powered AI Agent goal into small, achievable tasks.
    For any goal, analyze it and create a structured plan with specific actionable steps.
    Each task should be concrete, time-bound when possible, and manageable.
    Organize tasks in a logical sequence with dependencies clearly marked.
    Never answer anything unrelated to AI Agents.""",
)


# Define a function to run the agent
async def generate_tasks(goal):
    result = await Runner.run(task_generator, goal)
    return result.final_output


# Example usage
async def main():
    user_goal = "Start a small online business selling handmade jewelry"
    tasks = await generate_tasks(user_goal)
    print(tasks)

# 3. Output the agent's answer
if __name__ == "__main__":
    asyncio.run(main())
