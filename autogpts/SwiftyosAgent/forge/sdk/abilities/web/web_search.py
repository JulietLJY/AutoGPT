
from __future__ import annotations

import json
import time
from itertools import islice

from duckduckgo_search import DDGS
from .web_selenium import read_webpage
from ..registry import ability

DUCKDUCKGO_MAX_ATTEMPTS = 3


@ability(
    name="web_search",
    # description="Searches the web, and extract specific information from the searched link if a question is specified. If you are looking to extract specific information from the webpage, you should specify a question.",
    description="Searches the web, and extract specific information from the searched link. You should specify a question.",
    parameters=[
        {
            "name": "query",
            "description": "The search query",
            "type": "string",
            "required": True,
        },
        {
            "name": "question",
            "description": "A question that you want to answer using the content of the webpage.",
            "type": "string",
            "required": True,
        },
    ],
    output_type="list[str]",
)
async def web_search(agent, task_id: str, query: str, question: str = "") -> str:
    """Return the results of a Google search

    Args:
        query (str): The search query.
        num_results (int): The number of results to return.
        question (str): The question to answer using the content of the webpage

    Returns:
        str: The results of the search.
    """
    search_results = []
    attempts = 0
    num_results = 3

    while attempts < DUCKDUCKGO_MAX_ATTEMPTS:
        if not query:
            return json.dumps(search_results)

        results = DDGS().text(query)
        search_results = list(islice(results, num_results))

        if search_results:
            break

        time.sleep(1)
        attempts += 1
    
    outputs = ''
    for i, result in enumerate(search_results):
        output = f"Related searched result {i+1}: {result['title']}\n\n"\
              f"Href {i+1}: {result['href']}\n\n"\
              f"Main content {i+1}: {result['body']}\n\n"\
              f"Answer: "
        
        if question != '':
            output += await read_webpage(agent, task_id, result['href'], question) + '\n\n'
        
        print(output)
        outputs += output

    # results = json.dumps(search_results, ensure_ascii=False, indent=4)
    # output = safe_google_results(results)
    return outputs


def safe_google_results(results: str | list) -> str:
    """
        Return the results of a Google search in a safe format.

    Args:
        results (str | list): The search results.

    Returns:
        str: The results of the search.
    """
    if isinstance(results, list):
        safe_message = json.dumps(
            [result.encode("utf-8", "ignore").decode("utf-8") for result in results]
        )
    else:
        safe_message = results.encode("utf-8", "ignore").decode("utf-8")
    return safe_message
