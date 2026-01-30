import gradio as gr
from stock_agent import run_stock_agent
import os
from dotenv import load_dotenv
load_dotenv()

port = int(os.environ.get("PORT", 7860))

def analyze(company):
    company = company.strip().upper()
    if not company:
        return "❌ Please enter a valid stock ticker."

    return run_stock_agent(company)


demo = gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(
        label="Stock Ticker",
        placeholder="AAPL, MSFT, AMZN",
    ),
    outputs=gr.Textbox(
        label="CrewAI Execution Output",
        lines=40,
        max_lines=60
    ),
    title="📈 AI Stock Analyzer (Local Ollama)",
    description=(
        "CrewAI-powered stock analysis using **local Ollama**.\n\n"
        "Displays full step-by-step agent execution like the terminal."
    ),
)

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=port
    )
