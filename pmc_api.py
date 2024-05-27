import streamlit as st
import requests

from typing import Dict, List, Tuple


def _transform_search_query(search_term: str, search_option: str) -> str:
    if search_option == "any":
        return search_term
    if search_option == "title":
        return f"({search_option.upper()}:{search_term})"
    if search_option == "abstract":
        return f"({search_option.upper()}:{search_term})"

def _transform_year_range(year:int) -> str:
    start_year_date = f"{str(year)}-01-01"
    end_year_date = f"{str(year)}-12-31"

    return f"(FIRST_PDATE:[{start_year_date} TO {end_year_date}])"

@st.cache_data
def _search_api_based_on_year(
    search_term: str,
    search_option: str,
    year:int
) -> Tuple[int, int]:
    """
    Return the Tuple of the hitCounts for the year.
    """
    _search = _transform_search_query(search_term, search_option)
    _date_range = _transform_year_range(year)

    search_query = f"{_search} AND {_date_range}"

    search_url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={search_query}&format=JSON&sort=CITED%20desc&pageSize=1"
    
    response = requests.get(search_url)
    data = response.json()

    if not data:
        return st.warning(f"An error has occured. Please try again later.")

    return year, data.get("hitCount", 0)

@st.cache_data
def search_api(
    search_term: str,
    search_option: str,
    year_range:Tuple[int, int]
) -> List[Tuple[int, int]]:
    """
    Return the list of each year hitCounts and the queries time taken.

    """
    start_year, end_year = year_range

    hit_counts_list = [_search_api_based_on_year(search_term, search_option, year) for year in range(start_year, end_year + 1)]

    return hit_counts_list
@st.cache_data
def transform_search_result(search_result: List[Tuple[int, int]]) -> Dict[str, any]:
    """
    Transform the search result into a dictionary with start_year, end_year, size of the list, and list of the hitCounts.
    """
    if not search_result:
        return {
            "start_year": None,
            "end_year": None,
            "size": 0,
            "hitCounts": []
        }
    
    start_year = search_result[0][0]
    end_year = search_result[-1][0]
    size = len(search_result)
    hitCounts = [count for year, count in search_result]
    
    return {
        "start_year": start_year,
        "end_year": end_year,
        "size": size,
        "hitCounts": hitCounts
    }
