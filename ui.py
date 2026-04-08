import streamlit as st
import requests

st.write("App loaded")
API_URL = "https://market-intelligence-340869982336.us-central1.run.app"

st.write("App loaded")
st.set_page_config(page_title="Market Intelligence AI", layout="wide")

st.title("📊 Market Intelligence AI Agent")
st.write("Generate business insights using multi-agent AI")

topic = st.text_input("Enter a topic", placeholder="e.g. AI in healthcare startups")

if st.button("Generate Report"):
    if topic:
        with st.spinner("Analyzing market trends..."):
            response = requests.post(
                f"{API_URL}/generate",
                json={"topic": topic}
            )

            if response.status_code == 200:
                data = response.json()

                st.success("Report Generated ✅")

                st.subheader("📈 Insights")
                st.write(data["report"])
            else:
                st.error("Something went wrong")

# History section
st.divider()
st.subheader("📚 Previous Reports")

history_topic = st.text_input("Enter topic to fetch history")

if st.button("Get History"):
    if history_topic:
        response = requests.get(f"{API_URL}/history/{history_topic}")

        if response.status_code == 200:
            data = response.json()

            for i, report in enumerate(data["reports"], 1):
                st.markdown(f"**Report {i}:**")
                st.write(report)