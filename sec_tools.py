import os
import requests
import html2text
import re
from crewai.tools import tool
from sec_api import QueryApi

SEC_API_KEY = os.getenv("SEC_API_API_KEY")


def fetch_latest_filing(ticker: str, form_type: str) -> str:
    query_api = QueryApi(api_key=SEC_API_KEY)

    query = {
        "query": {
            "query_string": {
                "query": f"ticker:{ticker} AND formType:\"{form_type}\""
            }
        },
        "from": "0",
        "size": "1",
        "sort": [{"filedAt": {"order": "desc"}}],
    }

    filings = query_api.get_filings(query)["filings"]
    if not filings:
        return "No filings found."

    url = filings[0]["linkToFilingDetails"]

    headers = {
        "User-Agent": "StockAgent your_email@example.com",
        "Accept-Encoding": "gzip, deflate",
        "Host": "www.sec.gov",
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(response.text)

    # Clean junk
    text = re.sub(r"[^a-zA-Z0-9$%.,\n ]+", " ", text)
    return text[:12000]  # prevent token explosion


@tool("SEC_10K_Search")
def sec_10k_search(company: str, query: str) -> str:
    """
    Search a company's latest 10-K filing for specific information.
    Example queries: 'risk factors', 'competition', 'revenue'
    """
    filing_text = fetch_latest_filing(company, "10-K")
    return f"Search query: {query}\n\n{filing_text}"


@tool("SEC_10Q_Search")
def sec_10q_search(company: str, query: str) -> str:
    """
    Search a company's latest 10-Q filing for recent financial updates.
    """
    filing_text = fetch_latest_filing(company, "10-Q")
    return f"Search query: {query}\n\n{filing_text}"
