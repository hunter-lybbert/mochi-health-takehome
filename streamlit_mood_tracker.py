import json
import altair as alt
from altair import datum
import streamlit as st

import gspread
import pandas as pd
from datetime import datetime, timedelta
from gspread_dataframe import get_as_dataframe
from google.oauth2.service_account import Credentials



GOOGLE_API_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def authenticate_google_sheets() -> gspread.Client:
    """
    Authenticate and return a Google Sheets client using service account credentials.
    This function uses the credentials stored in Streamlit secrets to authorize access to Google Sheets.
    :return: gspread client object.
    """
    creds_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
    creds = Credentials.from_service_account_info(creds_info, scopes=GOOGLE_API_SCOPES)
    client = gspread.authorize(creds)
    return client


def built_altair_charts(
    data: pd.DataFrame,
    mood_options: list,
) -> alt.Chart:
    """
    Build Altair charts for the mood data.
    
    :param data: DataFrame containing mood data.
    :param mood_options: List of mood options for the radio button.
    
    :return: Altair chart object.
    """
    last_24_hours = datetime.now() - timedelta(days=1)

    bar_chart = alt.Chart(data).mark_bar().encode(
        x=alt.X("mood:N", axis=alt.Axis(labelAngle=0), title="Mood", sort=mood_options),
        y=alt.Y("count(mood)"),
        color=alt.Color("mood:N", legend=alt.Legend(title="Mood"), scale=alt.Scale(domain=mood_options, scheme="redyellowgreen", reverse=True)),
    ).transform_filter(datum.timestamp > last_24_hours).properties(
        width=600,
        height=250,
        title=alt.Title("Total Counts for each Mood in the Last 24 Hours", fontSize=25),
    )

    data["count"] = 1
    time_trends = data.groupby(
        [pd.Grouper(key="timestamp", freq="h"), "mood"],
        as_index=False,
    ).agg({"count": "count"})

    line_trend_chart = alt.Chart(time_trends).mark_line(point=True).encode(
        x=alt.X("timestamp:T", title="Date"),
        y=alt.Y("count:Q", title="Count"),
        color=alt.Color("mood:N", legend=alt.Legend(title="Mood"), scale=alt.Scale(domain=mood_options, scheme="redyellowgreen", reverse=True)),
    ).transform_filter(datum.timestamp > last_24_hours).properties(
        width=600,
        height=250,
        title=alt.Title("Mood Trends in the Last 24 Hours", fontSize=25)
    )
    chart = alt.vconcat(bar_chart, line_trend_chart)
    return chart


def main():
    """
    Main function to run the Streamlit app.
    """
    st.title("Mochi Health Mood Tracker")
    st.write("Please fill out the form below to help us track the Customer's mood.")

    google_client = authenticate_google_sheets()
    my_sheet = google_client.open("mochi health mood tracker")
    worksheet = my_sheet.sheet1

    mood_options = ["Happy 😀", "Okay 🙂", "Neutral 😐", "Not Okay 🙁", "Very Unhappy 😒"]

    form = st.form("Customer Mood Form")
    mood = form.radio(
        "How are you feeling at the moment?",
        mood_options,
        horizontal=True,
        index=None
    )
    note = form.text_input("(Optional) Please add a note about your mood:", max_chars=250)
    submit = form.form_submit_button("Submit Respsonse")

    if submit:
        worksheet.append_row([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mood, note])

    chart_data = get_as_dataframe(worksheet=worksheet, header=0)
    chart_data["timestamp"] = pd.to_datetime(chart_data["timestamp"])

    chart = built_altair_charts(data=chart_data, mood_options=mood_options)
    st.altair_chart(altair_chart=chart, use_container_width=None)


if __name__ == "__main__":
    main()
