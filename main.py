from datetime import datetime
import logging
from timeit import default_timer as timer

import streamlit as st
import pandas as pd
import altair as alt

from streamlit.logger import get_logger

LOGGER = get_logger(__file__)
LOGGER.setLevel(logging.DEBUG)

from pmc_api import search_api, transform_search_result


end_date = datetime.now()

end_date_year = int(end_date.year)
start_date_year = int(end_date.year) - 20

st.title(f"Publication Counts based on the Europe PMC RESTful Web Service")

search_form = st.form("search_form")

text_input = search_form.text_input(label="Search for", placeholder="covid-19")
search_option = search_form.radio(label="Search option:", key="visibility", options=["any", "title", "abstract"])

# Create a double-ended datetime slider
selected_date_range = search_form.slider(
    "Select a year range",
    min_value=start_date_year,
    max_value=end_date_year,
    value=(start_date_year, end_date_year),
    step=1,
)

submitted = search_form.form_submit_button('Submit my search')

if submitted:
    if not text_input:
        search_form.error(f"Please enter a search term.")
    else:
        start = timer()

        LOGGER.info(f"Search for {text_input}")

        search_api_results = search_api(
            search_term=text_input,
            search_option=search_option,
            year_range=selected_date_range,
        )

        results = transform_search_result(search_api_results)

        end = timer()

        # Rendered historgram
        years = pd.RangeIndex(start=results["start_year"], stop=results["end_year"]+1)
        publication_counts = results["hitCounts"] 

        chart_data = pd.DataFrame({
            'Year': years,
            'Publication Count': publication_counts
        })

        # Create the horizontal bar chart using Altair
        horizontal_bar_chart = (
            alt.Chart(chart_data)
            .mark_bar()
            .encode(
                x=alt.X("Publication Count:Q", axis=alt.Axis(format=",d")),
                y=alt.Y("Year:O", axis=alt.Axis(title="Year")),
            )
            .properties(
                width=700,
                height=500,
                title=f"Publication Counts for search term :'{text_input}' in the year {selected_date_range[0]} - {selected_date_range[1]}.\
                 \n Time taken: {round((end-start), 2)}",
            )
        )

        # Display the chart in Streamlit
        st.altair_chart(horizontal_bar_chart, use_container_width=True)
