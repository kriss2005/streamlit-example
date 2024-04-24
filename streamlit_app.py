import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

"""
# Streamlit trial App




"""

import streamlit as st
import pandas as pd
import numpy as np
import time
import altair as alt





@st.cache_data
def load_data():
    df = pd.read_csv("apl_aq_sample.csv")
    return df

df = load_data()
df['date'] = pd.to_datetime(df['time_']).dt.date
df['time'] = pd.to_datetime(df['time_']).dt.time
df['time'] = df['time'].astype(str).str[-8:]

# Dropdown filter
selected_category = st.selectbox('Select Date', df['date'].sort_values(ascending=False).unique())

# Filter data based on selected category
filtered_df = df[df['date'] == selected_category]

# Checkbox filters
selected_metric = st.selectbox('Select Metrics', filtered_df['metric'].unique())

if selected_metric:
    filtered_df = filtered_df[filtered_df['metric'] == selected_metric]

# Checkbox filters
selected_direction = st.selectbox('Select Direction', ['All'] + list(filtered_df['direction'].unique()))

if selected_direction != 'All':
    filtered_df = filtered_df[filtered_df['direction'] == selected_direction]


# Checkbox filters
selected_sensor_name = st.selectbox('Select Sensor', ['All'] + list(filtered_df['name'].unique()))

if selected_sensor_name != 'All':
    filtered_df = filtered_df[filtered_df['name'] == selected_sensor_name]

# Checkbox filters
view_deed_goal = st.selectbox('Display Deed Goal', ['No', 'Yes'])

if selected_direction != 'All':
    filtered_df = filtered_df[filtered_df['direction'] == selected_direction]

if selected_metric == 'VIS':
    avg_df = filtered_df.groupby(['time', 'name', 'direction', 'deed_goal'])['value'].mean().reset_index()
    # Create line chart
    st.write("### Tunnel Sensor Values for Visibility (K) Sensors")
    line_chart = alt.Chart(avg_df).mark_line().encode(
        x='time',
        y='value',
        color='name:N',  # 'N' indicates a nominal (categorical) variable
    ).properties(
        width=800,
        height=400
    )
    

    limit_chart = alt.Chart(avg_df).mark_line(strokeWidth=3).encode(
        x='time',
        y='deed_goal',
          # 'N' indicates a nominal (categorical) variable
    ).properties(
        width=800,
        height=400
    )
    if view_deed_goal == 'Yes':
        st.altair_chart(line_chart + limit_chart, use_container_width=True)
    else:
        st.altair_chart(line_chart, use_container_width=True)
else:

    avg_df = filtered_df.groupby(['time', 'direction', 'deed_goal'])['value'].mean().reset_index()


    # Create line chart
    st.write(f"### Tunnel Average for {selected_metric} Sensors")
    line_chart = alt.Chart(avg_df).mark_line().encode(
        x='time',
        y= 'value',
        color='direction:N',  # 'N' indicates a nominal (categorical) variable
    ).properties(
        width=800,
        height=400
    )
    #st.altair_chart(line_chart, use_container_width=True)

    limit_chart = alt.Chart(avg_df).mark_line(strokeWidth=3).encode(
        x='time',
        y='deed_goal',
          # 'N' indicates a nominal (categorical) variable
    ).properties(
        width=800,
        height=400
    )

    if view_deed_goal == 'Yes':
        st.altair_chart(line_chart + limit_chart, use_container_width=True)
    else:
        st.altair_chart(line_chart, use_container_width=True)
