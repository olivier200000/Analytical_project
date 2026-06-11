import streamlit as st
import pandas as pd
import plotly.express as px


df = pd.read_csv(r"titanic.csv")


st.title("Titanic Survival Analytics Dashboard")

st.markdown(
"""
This dashboard explores passenger demographics,
survival outcomes, and factors that influenced
survival aboard the Titanic.
"""
)

survival_rate = round(df["Survived"].mean() * 100, 1)

average_age = round(df["Age"].mean(), 1)

average_fare = round(df["Fare"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Passengers", len(df))

col2.metric("Survivors", int(df["Survived"].sum()))

col3.metric("Survival Rate", f"{survival_rate}%")

col4.metric("Average Age", average_age)

st.divider()


gender = st.selectbox(
    "Filter by Gender",
    ["All"] + list(df["Sex"].unique())
)

if gender != "All":
    df = df[df["Sex"] == gender]


st.header("Passenger Overview")

col1, col2 = st.columns(2)

class_counts = df["Pclass"].value_counts().reset_index()
class_counts.columns = ["Class", "Count"]

fig1 = px.bar(
    class_counts,
    x="Class",
    y="Count",
    title="Passengers by Class"
)

fig2 = px.pie(
    df,
    names="Sex",
    title="Gender Distribution"
)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)


st.header("Survival Analysis")

survival_gender = (
    df.groupby("Sex")["Survived"]
    .mean()
    .reset_index()
)

survival_gender["Survived"] *= 100

fig3 = px.bar(
    survival_gender,
    x="Sex",
    y="Survived",
    title="Survival Rate by Gender (%)"
)

st.plotly_chart(fig3, use_container_width=True)

survival_class = (
    df.groupby("Pclass")["Survived"]
    .mean()
    .reset_index()
)

survival_class["Survived"] *= 100

fig4 = px.bar(
    survival_class,
    x="Pclass",
    y="Survived",
    title="Survival Rate by Passenger Class (%)"
)

st.plotly_chart(fig4, use_container_width=True)

st.header("Age Analysis")

fig5 = px.histogram(
    df,
    x="Age",
    nbins=20,
    title="Age Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

st.header("Fare Analysis")

fig6 = px.box(
    df,
    x="Survived",
    y="Fare",
    title="Fare Distribution by Survival Status"
)

st.plotly_chart(fig6, use_container_width=True)

st.header("Passenger Records")

st.dataframe(df)

st.header("Key Insights")

st.success(
"""
1. Female passengers had a substantially higher survival rate than male passengers.

2. First-class passengers were more likely to survive than passengers in lower classes.

3. Higher ticket fares were generally associated with better survival outcomes.

4. Passenger class appears to be an important factor influencing survival.

5. The overall survival rate was relatively low, indicating the severity of the disaster.
"""
)

st.header("Recommendation")

st.info(
"""
• Prioritize vulnerable groups during emergency situations.

• Improve access to emergency resources regardless of socioeconomic status.

• Ensure safety procedures are communicated clearly to all passengers.

• Use passenger demographic information to support emergency preparedness planning.

• Monitor whether resource allocation practices create unequal outcomes among passenger groups.
"""
)
