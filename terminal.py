import asyncio
import os
import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent

# Load environment variables
load_dotenv()

# Initialize Gemini Model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=os.getenv('GOOGLE_API_KEY'))

@dataclass
class ActionResult:
    is_done: bool
    extracted_content: Optional[str]
    error: Optional[str]
    include_in_memory: bool

@dataclass
class AgentHistoryList:
    all_results: List[ActionResult]
    all_model_outputs: List[dict]

def parse_agent_history(history_str: str) -> None:
    console = Console()
    sections = history_str.split('ActionResult(')

    for i, section in enumerate(sections[1:], 1):  
        content = ''
        if 'extracted_content=' in section:
            content = section.split('extracted_content=')[1].split(',')[0].strip("'")

        if content:
            header = Text(f'Step {i}', style='bold blue')
            panel = Panel(content, title=header, border_style='blue')
            console.print(panel)
            console.print()

async def run_browser_task(task: str, headless: bool = True) -> Dict[str, Any]:
    try:
        agent = Agent(
            task=task,
            llm=llm
        )
        result = await agent.run()
        
        # If result is already JSON, return as-is
        if isinstance(result, dict):
            return result
        
        # If result is string, wrap it in JSON
        return {"response": result}
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    task_description = input("Enter the task description: ")
    
    # Run the async function synchronously
    result = asyncio.run(run_browser_task(task_description))

    # Print JSON output
    print(json.dumps(result, indent=4))
