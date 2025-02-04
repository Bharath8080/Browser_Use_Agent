import asyncio
import os
import json
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

import gradio as gr
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

def create_ui():
    with gr.Blocks(title='Browser Use GUI') as interface:
        gr.Markdown('# Browser Use Task Automation')

        with gr.Row():
            with gr.Column():
                task = gr.Textbox(
                    label='Task Description',
                    placeholder='E.g., Search for KL Rahul stats...',
                    lines=3,
                )
                headless = gr.Checkbox(label='Run Headless', value=True)
                submit_btn = gr.Button('Run Task')

            with gr.Column():
                output = gr.JSON(label='JSON Output')

        submit_btn.click(
            fn=lambda *args: asyncio.run(run_browser_task(*args)),
            inputs=[task, headless],
            outputs=output,
        )

    return interface

if __name__ == '__main__':
    demo = create_ui()
    demo.launch()
