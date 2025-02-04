# Browser Use Agent with Gemini-2.0-flash-exp

An open-source browser automation agent powered by the **Gemini-2.0-flash-exp** model. This tool interacts with web browsers, performing tasks like clicking, typing, scrolling, and extracting data.

## 🚀 Features
- **Automates browser tasks** like searching, clicking, and extracting data.
- **Powered by Gemini-2.0-flash-exp** for intelligent web interactions.
- **Fully open-source** and free to use.
- **Supports Playwright** for robust browser automation.

## 🛠 Installation

To install the required dependencies, run the following commands:

```sh
pip install browser-use
playwright install
```

## 🔧 Usage

Example: Automating a Google search for **Virat Kohli Stats** and extracting player statistics.

```python
from browser_use import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio

# Initialize Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key="YOUR_GOOGLE_API_KEY")

# Define the task
task = "Go to Google Chrome, search for 'Virat Kohli Stats', click on the first post, and extract the player stats from the page."

async def run_task():
    agent = Agent(task=task, llm=llm)
    result = await agent.run()
    print(result)

# Run the automation
asyncio.run(run_task())
```

## 🎯 What Can It Do?
- Automate **Google searches** and extract information.
- **Click buttons, fill forms, and navigate** websites.
- **Scrape structured data** from web pages.

## 📌 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

## ⚖️ License
This project is licensed under the **MIT License**.

---

✨ **Empower your workflow with AI-powered browser automation!**


