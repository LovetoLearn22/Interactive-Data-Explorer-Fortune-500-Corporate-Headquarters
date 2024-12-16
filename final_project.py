"""Class: CS230--Section 1
Name: Francisco Cunha
Description: Final Project
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student. """

import os
import pandas as pd
import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt

# File path
file_path = "fortune_500_hq.csv"
# Load the data
try:
    data = pd.read_csv(file_path)
except Exception as e:
    st.error(f"Error loading the file: {e}")
    st.stop()

# Clean and preprocess data
data['REVENUES'] = pd.to_numeric(data['REVENUES'], errors='coerce')
data['LATITUDE'] = pd.to_numeric(data['LATITUDE'], errors='coerce')
data['LONGITUDE'] = pd.to_numeric(data['LONGITUDE'], errors='coerce')
data = data.dropna(subset=['LATITUDE', 'LONGITUDE', 'REVENUES'])

# Streamlit app
st.title("Interactive Data Explorer: Fortune 500 Corporate Headquarters")
st.sidebar.title("Navigation")

# Sidebar options
tab = st.sidebar.radio("Choose an option:", ["Overview", "Geographical Insights", "Top Companies", "Interactive Map"])

# Filters
state_filter = st.sidebar.selectbox("Select State/Region:", ["All"] + sorted(data['STATE'].unique()))
revenue_range = st.sidebar.slider("Revenue Range (in millions):",
                                  int(data['REVENUES'].min()),
                                  int(data['REVENUES'].max()),
                                  (int(data['REVENUES'].min()), int(data['REVENUES'].max())))

# Apply filters
filtered_data = data.copy()
if state_filter != "All":
    filtered_data = filtered_data[filtered_data['STATE'] == state_filter]
filtered_data = filtered_data[(filtered_data['REVENUES'] >= revenue_range[0]) & (filtered_data['REVENUES'] <= revenue_range[1])]

# Overview tab
if tab == "Overview":
    st.subheader("Dataset Overview")
    st.write("This dataset contains information about the Fortune 500 companies, including their headquarters, revenues, and more.")
    st.dataframe(filtered_data)

# Geographical Insights tab
elif tab == "Geographical Insights":
    st.subheader("Geographical Distribution of Fortune 500 Headquarters")
    top_states = filtered_data['STATE'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    plt.bar(top_states.index, top_states.values, color='skyblue')
    plt.xlabel("State")
    plt.ylabel("Number of Headquarters")
    plt.title("Top 10 States by Number of Headquarters")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    # Total Revenue by State
    st.subheader("Top States by Total Revenue")
    top_states_revenue = filtered_data.groupby('STATE')['REVENUES'].sum().nlargest(10)
    plt.figure(figsize=(10, 6))
    plt.bar(top_states_revenue.index, top_states_revenue.values, color='lightblue')
    plt.xlabel("State")
    plt.ylabel("Total Revenue (in millions)")
    plt.title("Top 10 States by Total Revenue")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

    st.subheader("Average Revenue by State")
    avg_revenue_state = filtered_data.groupby('STATE')['REVENUES'].mean().nlargest(10)
    plt.figure(figsize=(10, 6))
    plt.bar(avg_revenue_state.index, avg_revenue_state.values, color='lightcoral')
    plt.xlabel("State")
    plt.ylabel("Average Revenue (in millions)")
    plt.title("Top 10 States by Average Revenue")
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)



# Top Companies tab
elif tab == "Top Companies":

    st.subheader("Search and Sort Companies")
    search_query = st.text_input("Search for a Company:")
    sort_by = st.radio("Sort By:", ['REVENUES', 'EMPLOYEES'])

    if search_query:
        filtered_search = filtered_data[filtered_data['NAME'].str.contains(search_query, case=False)]
    else:
        filtered_search = filtered_data

    filtered_search = filtered_search.sort_values(by=sort_by, ascending=False)
    st.table(filtered_search[['NAME', 'REVENUES', 'EMPLOYEES', 'STATE']])

    st.subheader("Top Companies by Revenue")
    top_companies = filtered_data.nlargest(10, 'REVENUES')
    st.write("Here are the top 10 companies based on revenue within the selected filters:")
    st.table(top_companies[['NAME', 'REVENUES', 'STATE']])

    # Revenue Per Employee Calculation
    st.subheader("Top Companies by Revenue Per Employee")
    filtered_data['REVENUE_PER_EMPLOYEE'] = filtered_data['REVENUES'] / filtered_data['EMPLOYEES']
    top_per_employee = filtered_data.nlargest(10, 'REVENUE_PER_EMPLOYEE')
    st.table(top_per_employee[['NAME', 'REVENUE_PER_EMPLOYEE', 'EMPLOYEES', 'REVENUES']])

    st.subheader("Top Employers in the Fortune 500 List")
    top_employers = filtered_data.nlargest(10, 'EMPLOYEES')
    st.table(top_employers[['NAME', 'EMPLOYEES', 'REVENUES', 'STATE']])

    # Profit Margin Calculation
    if 'PROFIT' in filtered_data.columns:
        st.subheader("Top Companies by Profit Margin")
        filtered_data['PROFIT_MARGIN'] = (filtered_data['PROFIT'] / filtered_data['REVENUES']) * 100
        top_profit_margin = filtered_data.nlargest(10, 'PROFIT_MARGIN')
        st.table(top_profit_margin[['NAME', 'PROFIT_MARGIN', 'REVENUES', 'STATE']])





# Interactive Map tab
elif tab == "Interactive Map":
    st.subheader("Interactive Map of Fortune 500 Headquarters")

    # Prepare map data
    map_data = filtered_data[['LATITUDE', 'LONGITUDE', 'NAME', 'REVENUES']]
    map_data = map_data.rename(columns={"LATITUDE": "lat", "LONGITUDE": "lon"})

    if not map_data.empty:
        # Scatterplot Layer: Individual headquarters
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[lon, lat]",
            get_radius=2500,  # Adjust marker size
            get_color="[200, 30, 0, 160]",  # Red with some transparency
            pickable=True,  # Enables hover functionality
        )

        # Heatmap Layer: Density of headquarters
        heatmap_layer = pdk.Layer(
            "HeatmapLayer",
            data=map_data,
            get_position='[lon, lat]',
            get_weight="REVENUES",  # Weight heatmap based on revenue
            radius_pixels=50,  # Controls heatmap radius
        )

        # Define the tooltip content
        tooltip = {
            "html": "<b>Company:</b> {NAME} <br><b>Revenue:</b> ${REVENUES}M",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }

        # View State: Controls the camera position
        view_state = pdk.ViewState(
            latitude=map_data["lat"].mean(),
            longitude=map_data["lon"].mean(),
            zoom=4,
            pitch=40
        )

        # Combine both layers (scatterplot + heatmap)
        r = pdk.Deck(
            layers=[scatter_layer, heatmap_layer],
            initial_view_state=view_state,
            tooltip=tooltip  # Attach the tooltip
        )

        # Render the map
        st.pydeck_chart(r)

    else:
        st.write("No data available for the selected filters.")


st.write("Explore the data interactively using the filters and visualizations above!")
