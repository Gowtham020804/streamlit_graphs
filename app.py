import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# PAGE CONFIG
st.set_page_config(
    page_title="Graph Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Streamlit Graph Visualizer")
st.write("Upload a CSV or Excel file, or use the sample dataset to generate charts instantly.")

DATA_PATH = os.path.join("Data", "netflix_titles.csv")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel File",
    type=["csv", "xlsx"]
)

use_sample = False

df = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read file: {exc}")
else:
    if os.path.exists(DATA_PATH):
        if st.button("Use sample dataset"):
            use_sample = True
            df = pd.read_csv(DATA_PATH)
    else:
        st.info("No sample dataset available in the Data folder.")

if df is not None:
    st.subheader("📁 Dataset Preview")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    if len(numeric_cols) == 0:
        st.error("No numeric columns found in dataset. Please upload a dataset with numeric values.")
    else:
        st.sidebar.header("⚙ Graph Settings")

        graph = st.sidebar.selectbox(
            "Select Graph Type",
            [
                "Line Chart",
                "Bar Chart",
                "Area Chart",
                "Scatter Plot",
                "Histogram",
                "Pie Chart",
                "Box Plot",
                "Heatmap"
            ]
        )

        x_col = st.sidebar.selectbox("Select X-axis", df.columns)
        y_col = st.sidebar.selectbox("Select Y-axis", numeric_cols)

        if graph == "Line Chart":
            st.subheader("📈 Line Chart")
            st.line_chart(df.set_index(x_col)[y_col])

        elif graph == "Bar Chart":
            st.subheader("📊 Bar Chart")
            st.bar_chart(df.set_index(x_col)[y_col])

        elif graph == "Area Chart":
            st.subheader("📉 Area Chart")
            st.area_chart(df.set_index(x_col)[y_col])

        elif graph == "Scatter Plot":
            st.subheader("⚪ Scatter Plot")
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                color=y_col,
                size=y_col,
                hover_data=df.columns
            )
            st.plotly_chart(fig, use_container_width=True)

        elif graph == "Histogram":
            st.subheader("📦 Histogram")
            fig, ax = plt.subplots()
            ax.hist(df[y_col].dropna(), bins=20)
            ax.set_xlabel(y_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        elif graph == "Pie Chart":
            st.subheader("🥧 Pie Chart")
            if len(categorical_cols) > 0:
                pie_col = st.selectbox("Select Category Column", categorical_cols)
                pie_data = df.groupby(pie_col)[y_col].sum()
                fig, ax = plt.subplots()
                ax.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%")
                st.pyplot(fig)
            else:
                st.warning("No categorical columns found.")

        elif graph == "Box Plot":
            st.subheader("📋 Box Plot")
            fig, ax = plt.subplots()
            sns.boxplot(y=df[y_col].dropna(), ax=ax)
            st.pyplot(fig)

        elif graph == "Heatmap":
            st.subheader("🔥 Correlation Heatmap")
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
            st.pyplot(fig)
else:
    st.info("Upload a CSV or Excel file to start, or click 'Use sample dataset'.")
