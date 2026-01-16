import gradio as gr
from stock_agent import run_stock_agent

def analyze(company):
    return run_stock_agent(company.upper())

gr.Interface(
    fn=analyze,
    inputs=gr.Textbox(label="Company Ticker (AAPL, MSFT, AMZN)"),
    outputs=gr.Textbox(label="Stock Analysis Result", lines=30),
    title="📈 Stock Analyzer AI",
    description="CrewAI-powered stock analysis using SEC filings"
).launch()
