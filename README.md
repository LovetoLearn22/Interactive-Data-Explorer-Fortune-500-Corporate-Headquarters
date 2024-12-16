# Interactive Data Explorer: Fortune 500 Corporate Headquarters

## Project Overview
This project is an interactive web application built with **Streamlit** and **PyDeck**. It allows users to explore **Fortune 500 Corporate Headquarters** data through dynamic visualizations, tables, and maps. Users can interact with filters and charts to gain valuable insights into company **locations**, **revenues**, and **distribution trends**.

---

## Features

### **Geographical Insights**
- Interactive map displaying company headquarters across the United States.
- Heatmap layer weighted by revenue, showing the density of high-revenue companies.
- Hover tooltips that display:
  - **Company Name**
  - **Revenue**

### **Revenue Insights**
- View the **Top 10 Companies** by revenue dynamically filtered by state and revenue range.
- Table showing detailed company-level data, including:
  - **Name**
  - **Revenue** (in millions)
  - **Location** (State)

### **State and City Analysis**
- Bar charts for the **Top 10 States** with the most Fortune 500 headquarters.
- Bar charts for the **Top 10 Cities** with the most corporate presence.

### **Dynamic Filters**
- Filter data by:
  - **State/Region**: Dropdown selection for specific states.
  - **Revenue Range**: Slider for flexible revenue thresholds.

---

## Technologies Used
- **Streamlit**: For building the interactive user interface.
- **PyDeck**: For interactive geographical map visualizations.
- **Pandas**: For data cleaning, preprocessing, and filtering.
- **Matplotlib**: For creating insightful bar charts and graphs.
- **Python**: Core programming language.

---

## Installation Instructions

To run the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Interactive-Data-Explorer-Fortune-500-Corporate-Headquarters.git
   cd Interactive-Data-Explorer-Fortune-500-Corporate-Headquarters
