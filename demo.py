from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
load_dotenv()
import os
import warnings
warnings.filterwarnings('ignore')

llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key=os.getenv('GOOGLE_API_KEY'))

async def main():
    agent = Agent(
        task="""Go to Google Chrome ,Search for Virat Kohli stats and return the results""",
        llm =llm
    )        

    result = await agent.run()
    print (result)

asyncio.run(main())
