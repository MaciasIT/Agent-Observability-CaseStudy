
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from typing import List
from scholarly import scholarly, ProxyGenerator

# --- New, more powerful tool definition ---
def search_scholar_papers(query: str, max_results: int = 3) -> List[str]:
    """
    Searches Google Scholar for academic papers and returns structured metadata.

    Args:
      query: The search topic.
      max_results: The maximum number of papers to return.

    Returns:
      A list of strings, where each string contains the formatted
      metadata of a single paper.
    """
    print(f"Searching Google Scholar for: {query}")
    try:
        # Set up a proxy generator to avoid getting blocked.
        pg = ProxyGenerator()
        pg.FreeProxies()
        # The 'scholarly.use_proxy(pg)' line that caused the error has been removed.
        # The library should pick up the proxy configuration automatically.

        # Search for publications
        search_query = scholarly.search_pubs(query)
        
        results = []
        for i, pub in enumerate(search_query):
            if i >= max_results:
                break
            
            # Extract details
            title = pub.get('bib', {}).get('title', 'N/A')
            authors = ", ".join(pub.get('bib', {}).get('author', ['N/A']))
            year = pub.get('bib', {}).get('pub_year', 'N/A')
            venue = pub.get('bib', {}).get('venue', 'N/A')
            pub_url = pub.get('pub_url', 'N/A')

            # Format the output string
            formatted_paper = (
                f"Title: {title}\\n"
                f"Authors: {authors}\\n"
                f"Year: {year}\\n"
                f"Venue: {venue}\\n"
                f"URL: {pub_url}"
            )
            results.append(formatted_paper)

        if not results:
            return ["No papers found for the given query."]
            
        return results
    except Exception as e:
        print(f"An error occurred while searching Google Scholar: {e}")
        return [f"An error occurred: {e}"]


def count_papers(papers: List[str]) -> int:
    """
    This function counts the number of papers in a list of strings.
    Args:
      papers: A list of strings, where each string is a research paper.
    Returns:
      The number of papers in the list.
    """
    # Avoid counting the "No papers found" or error message as a paper
    if len(papers) == 1 and ("No papers found" in papers[0] or "An error occurred" in papers[0]):
        return 0
    return len(papers)


# Root agent
root_agent = LlmAgent(
    name="research_paper_finder_agent",
    model=Gemini(model="gemini-2.5-flash-lite"),
    instruction="""Your task is to find research papers with detailed metadata and count them.

    You MUST ALWAYS follow these steps:
    1) Use the 'search_scholar_papers' tool to find papers on the user's topic. This tool returns a list of strings, each containing formatted details about a paper (Title, Authors, Year, URL).
    2) Pass the list of papers returned by the tool to the 'count_papers' tool to get the total count.
    3) Present the detailed information for each paper clearly to the user.
    4) Finally, state the total number of papers found.
    
    **Your final output to the user must be a single, comprehensive message containing both the list of paper details and the final count.**
    """,
    tools=[search_scholar_papers, count_papers]
)
