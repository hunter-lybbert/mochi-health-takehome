# mochi-health-takehome
Takehome assessment for Mochi Health

In the `streamlit_mood_tracker.py` we create a streamlit app which tracks and visualizes customers survey responses about their mood.
* We first have to authenticate to google sheets to access the location which the data is being stored.
Specifically our application is backed by [this google sheet](https://docs.google.com/spreadsheets/d/1UptyEDla8n5vaEa6fHjVJyqPUw1k43riLJm6Lm_Xx4Y/edit?gid=0#gid=0).
* Secondly we record the users input to the streamlit widgets.
* When a streamlit widget input is altered and the user clicks `submit` a record is recorded to the google sheet and the graphs are updated.

Future improvements:
* I would make the visualizations interactive so you could select subsets of the mood types to compare more closely against one another.
* I Would also add another interaction to the visualization which would allow the user to slide a window over the line chart selecting a subset of time to plot the bar chart for
* Additionally I would stylize the whole interface a little better.