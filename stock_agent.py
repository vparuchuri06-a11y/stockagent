#from dotenv import load_dotenv
#load_dotenv()
from crewai import Agent, Task, Crew, LLM
from calculator_tool import calculator
from sec_tools import sec_10k_search, sec_10q_search

# -------------------------
# Local LLM
# -------------------------
llm = LLM(
     model="ollama/llama3.2:3b",
     base_url="http://localhost:11434",
     temperature=0.1
 )
#llm = LLM(
#    model="gpt-4o-mini",  # fast + cheap
#    temperature=0.2
#)

def run_stock_agent(company: str) -> str:
    # -------------------------
    # Agents
    # -------------------------

    financial_agent = Agent(
        role="Financial Analyst",
        goal="Analyze the financial position and SEC filings of {company}",
        backstory=(
            "You are a professional financial analyst. "
            "You analyze SEC filings, business fundamentals, "
            "and financial risks."
        ),
        tools=[calculator, sec_10k_search, sec_10q_search],
        llm=llm,
        verbose=True
    )

    research_analyst = Agent(
        role="Research Analyst",
        goal="Research market trends and competitors for {company}",
        backstory="You focus on industry trends and competitive positioning.",
        llm=llm,
        verbose=True
    )

    investment_advisor = Agent(
        role="Investment Advisor",
        goal="Provide a Buy, Hold, or Sell recommendation for {company}",
        backstory="You synthesize all analysis into an investment decision.",
        llm=llm,
        verbose=True
    )

    # -------------------------
    # Tasks (EXPECTED_OUTPUT IS REQUIRED)
    # -------------------------

    financial_analysis = Task(
        description=(
            "Analyze {company}'s business model, revenue drivers, strengths, "
            "and financial risks. Use the Calculator tool if helpful."
        ),
        expected_output=(
            "A structured financial analysis covering business model, "
            "revenue drivers, strengths, and risks."
        ),
        agent=financial_agent
    )

    research = Task(
        description=(
            "Research {company}'s industry trends, competitors, "
            "and market opportunities."
        ),
        expected_output=(
            "A concise market research summary including key competitors "
            "and industry trends."
        ),
        agent=research_analyst
    )

    filings_analysis = Task(
        description=(
            "Analyze {company}'s 10-K and 10-Q filings. "
            "Identify major risk factors and recent updates."
        ),
        expected_output=(
            "A summary of key SEC filing risks, disclosures, "
            "and recent financial updates."
        ),
        agent=financial_agent
    )

    recommendation = Task(
        description=(
            "Based on all prior analysis, give a Buy, Hold, or Sell "
            "recommendation for {company} with reasoning."
        ),
        expected_output=(
            "A clear Buy, Hold, or Sell recommendation with justification."
        ),
        agent=investment_advisor
    )

    # -------------------------
    # Crew
    # -------------------------

    crew = Crew(
        agents=[financial_agent, research_analyst, investment_advisor],
        tasks=[
            financial_analysis,
            research,
            filings_analysis,
            recommendation
        ],
        verbose=True
    )

    # -------------------------
    # Run Crew
    # -------------------------

    result = crew.kickoff(inputs={"company": company})

    return str(result)
