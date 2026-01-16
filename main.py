from crewai import Agent, Task, Crew, LLM

# -------------------------
# Tools
# -------------------------
from calculator_tool import calculator
from sec_tools import sec_10k_search, sec_10q_search

# -------------------------
# Local LLM (Ollama)
# -------------------------
llm = LLM(
    model="ollama/llama3.1:8b",
    base_url="http://localhost:11434",
    temperature=0.2
)

# -------------------------
# Agents
# -------------------------

financial_agent = Agent(
    role="Financial Analyst",
    goal="Analyze the financial position and SEC filings of {company}",
    backstory=(
        "You are a professional financial analyst. "
        "You extract insights from SEC filings (10-K and 10-Q), "
        "evaluate business fundamentals, and identify financial risks."
    ),
    tools=[
        calculator,
        sec_10k_search,
        sec_10q_search
    ],
    llm=llm,
    allow_delegation=False,
    verbose=True
)

research_analyst_agent = Agent(
    role="Research Analyst",
    goal="Research market trends and competitors for {company}",
    backstory=(
        "You are a market research analyst. "
        "You focus on industry trends, competitive landscape, "
        "and external market forces affecting the company."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True
)

investment_advisor_agent = Agent(
    role="Investment Advisor",
    goal="Provide a Buy, Hold, or Sell recommendation for {company}",
    backstory=(
        "You are an investment advisor. "
        "You combine financial analysis, SEC disclosures, "
        "and market research to give a clear recommendation."
    ),
    llm=llm,
    allow_delegation=False,
    verbose=True
)

# -------------------------
# Tasks
# -------------------------

financial_analysis = Task(
    description=(
        "Analyze {company}'s business and finances.\n"
        "Include:\n"
        "1. Business model\n"
        "2. Revenue drivers\n"
        "3. Strengths\n"
        "4. Financial risks\n\n"
        "FIRST, use the Calculator tool to compute:\n"
        "- If current revenue is 100000 and growth rate is 15%, "
        "calculate next year's revenue."
    ),
    expected_output=(
        "A structured financial analysis with calculated revenue growth."
    ),
    agent=financial_agent
)

research = Task(
    description=(
        "Research {company} from a market and industry perspective.\n"
        "Cover:\n"
        "1. Industry trends\n"
        "2. Key competitors\n"
        "3. Market threats and opportunities"
    ),
    expected_output=(
        "A concise market and competitive analysis."
    ),
    agent=research_analyst_agent
)

filings_analysis = Task(
    description=(
        "Use SEC filings to analyze {company}.\n"
        "Specifically:\n"
        "1. Identify major risk factors from the 10-K\n"
        "2. Identify recent financial or operational updates from the 10-Q\n"
        "3. Note any regulatory or legal concerns"
    ),
    expected_output=(
        "A summary grounded in SEC filings with concrete examples."
    ),
    agent=financial_agent
)

recommend = Task(
    description=(
        "Using the financial analysis, SEC filings, and market research, "
        "provide an investment recommendation for {company}.\n"
        "Choose ONE: Buy, Hold, or Sell.\n"
        "Explain your reasoning clearly."
    ),
    expected_output=(
        "A clear Buy, Hold, or Sell recommendation with justification."
    ),
    agent=investment_advisor_agent
)

# -------------------------
# Crew
# -------------------------

crew = Crew(
    agents=[
        financial_agent,
        research_analyst_agent,
        investment_advisor_agent
    ],
    tasks=[
        financial_analysis,
        research,
        filings_analysis,
        recommend
    ],
    verbose=True
)

# -------------------------
# Run
# -------------------------

company_name = input("\nEnter the company ticker (e.g., AAPL, MSFT, AMZN): ").upper()

result = crew.kickoff(
    inputs={"company": company_name}
)

print("\n================ FINAL RESULT ================\n")
print(result)
