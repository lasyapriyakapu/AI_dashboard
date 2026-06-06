import streamlit as st
import pandas as pd
import plotly.express as px



# # Dashboard Title
# st.title("🚢 Titanic AI Dashboard")
st.markdown("""
<div style="
background: linear-gradient(135deg, #1E3A8A, #0F766E);
padding: 40px;
border-radius: 20px;
text-align: center;
margin-bottom: 20px;
">

<h1 style="
color:white;
font-size:48px;
margin:0;
">
🚢 Titanic AI Dashboard
</h1>

<p style="
color:white;
font-size:20px;
margin-top:10px;
">
📊 Smart Analytics | 📈 Interactive Visualizations | 🎯 Actionable Insights
</p>

</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* Sidebar Background */
section[data-testid="stSidebar"] {
    background-color: #E0F2FE;
}

</style>
""", unsafe_allow_html=True)


# Load Dataset
url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"

df = pd.read_csv(url)

st.snow()

# Dataset Overview Section
st.header("📊 Dataset Overview")

st.write("Shape of Dataset (Rows, Columns):")
st.write(df.shape)

st.write("First 5 Records:")
st.write(df.head())
# Data Cleaning Section
st.header("🧹 Data Cleaning")

st.write("Missing Values Before Cleaning")

before_missing = pd.DataFrame(
    df.isnull().sum(),
    columns=["Missing Values"]
)

st.dataframe(
    before_missing.style.background_gradient(cmap="Blues")
)

# Fill Age with median
df["Age"] = df["Age"].fillna(df["Age"].median())

# Fill Embarked with mode
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])

# Drop Cabin column
df.drop(columns=["Cabin"], inplace=True)

st.write("Missing Values After Cleaning")

after_missing = pd.DataFrame(
    df.isnull().sum(),
    columns=["Missing Values"]
)

st.dataframe(
    after_missing.style.background_gradient(cmap="Purples")
)
# KPI Section
st.header("📈 Key Performance Indicators")

# Calculations
total_passengers = len(df)

total_survivors = df["Survived"].sum()

average_age = round(df["Age"].mean(), 2)

survival_rate = round(
    (total_survivors / total_passengers) * 100,
    2
)

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥Passengers", total_passengers)

col2.metric("❤️Survivors", total_survivors)

col3.metric("🎂Average Age", average_age)

col4.metric("📈Survival Rate %", survival_rate)
# Filters
st.sidebar.header("🎛️ Filters")


gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + list(df["Sex"].unique())
)

pclass = st.sidebar.selectbox(
    "Select Passenger Class",
    ["All", "1", "2", "3"]

)


# Create filtered dataframe
filtered_df = df.copy()

# Gender filter
if gender != "All":
    filtered_df = filtered_df[
        filtered_df["Sex"] == gender
    ]

# Passenger class filter
if pclass != "All":
    filtered_df = filtered_df[
        filtered_df["Pclass"] == int(pclass)
    ]

st.write("Filtered Records:", len(filtered_df))
# Chart 1
st.header("📊 Survival Distribution")

survival_counts = (
    filtered_df["Survived"]
    .value_counts()
    .reset_index()
)

survival_counts.columns = [
    "Survived",
    "Count"
]

survival_counts["Survived"] = (
    survival_counts["Survived"]
    .replace({
        0: "Did Not Survive",
        1: "Survived"
    })
)

fig1 = px.bar(
    survival_counts,
    x="Survived",
    y="Count",
    title="Survival Distribution",
    color="Survived",
    color_discrete_sequence=["red","green"]
)

st.plotly_chart(fig1)
st.info(
    "Insight: More passengers died than survived."
)
# Chart 2
st.header("🥧 Gender Distribution")

fig2 = px.pie(
    filtered_df,
    names="Sex",
    title="Gender Distribution",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig2)

st.info(
    "Insight: This chart shows the percentage of male and female passengers."
)
# Chart 3
st.header("📊 Age Distribution")

fig3 = px.histogram(
    filtered_df,
    x="Age",
    title="Age Distribution",
    color_discrete_sequence=["pink"]
)

st.plotly_chart(fig3)

st.info(
    "Insight: Most passengers were young adults."
)
# Chart 4
st.header("🏆 Survival by Passenger Class")

survival_class = (
    filtered_df
    .groupby("Pclass")["Survived"]
    .mean()
    .reset_index()
)

survival_class["Survived"] = (
    survival_class["Survived"] * 100
)

fig4 = px.bar(
    survival_class,
    x="Pclass",
    y="Survived",
    title="Survival Rate by Passenger Class",
    color="Survived",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig4)
best_class = survival_class.loc[
    survival_class["Survived"].idxmax(),
    "Pclass"
]

st.info(
    f"Insight: Passenger Class {best_class} has the highest survival rate."
)
# Chart 5
st.header("💰 Fare Distribution")

fig5 = px.box(
    filtered_df,
    y="Fare",
    title="Fare Distribution",
    color_discrete_sequence=["purple"]
)

st.plotly_chart(fig5)
average_fare = round(
    filtered_df["Fare"].mean(),
    2
)

highest_fare = round(
    filtered_df["Fare"].max(),
    2
)

st.info(
    f"Insight: Average fare is £{average_fare} and the highest fare paid was £{highest_fare}."
)