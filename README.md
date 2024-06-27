# Publication Counts based on the Europe PMC RESTful Web Service
##  Streamlit Framework Exploration Repository
Welcome to this self-exploratory repository designed for experimenting with the Streamlit framework.

You can access the published Streamlit application via this link: https://publicationeuropepmc.streamlit.app/

This repository generates a histogram of the most cited publication papers using data from the [Europe PMC RESTful Web Service](https://europepmc.org/RestfulWebService).


Main Takeaway | Future Improvement
--- | ---
Streamlit offers a date_input component but lacks a component specifically for selecting only the year. Therefore, a 'year range' slider has been created to limit the selection to a maximum of 20 years in the past, ensuring that the number of queries remains manageable. | To include a year-only picker if it becomes available. Alternatively, a text box input that only accepts valid years, such as `2024`, but rejects invalid ones, such as `1002`.
Cache: Currently returning results faster if the same search term is being queried. To explore more on cache/session_state | ~~Update the `time_taken` if data from cache is being returned, now it returns the time_taken from the cached response.~~ Action: move timer in the form between `search_api` and `transform_search_result` methods to make more sense.
Streamlit is an excellent Python-based tool for front-end visualization. As a backend engineer, I found it straightforward to make API calls and transform the responses for front-end visualization. | To further enhance the Python methods used (such as try-catch blocks, annotated returns, unit testing, asynchronous call), a message display for cases when there is no response from the query (currently, only an empty chart is displayed).
