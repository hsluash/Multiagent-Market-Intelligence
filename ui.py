import streamlit as st
import requests

st.set_page_config(page_title="Market Intelligence AI", layout="wide")

API_URL = "https://market-intelligence-340869982336.us-central1.run.app"

st.title("📊 Market Intelligence AI Agent")
st.write("Research any market topic — get a report, action tasks, and a follow-up schedule automatically.")

topic = st.text_input("Enter a topic", placeholder="e.g. AI in healthcare startups")

if st.button("Generate Report"):
    if topic:
        with st.spinner("Researching, analyzing, and planning actions..."):
            response = requests.post(
                f"{API_URL}/generate",
                json={"topic": topic}
            )

            if response.status_code == 200:
                data = response.json()

                st.success("Report Generated ✅")

                st.subheader("📈 Market Intelligence Report")
                st.write(data.get("report", ""))

                # if data.get("actions"):
                #     st.subheader("✅ Action Plan")
                #     st.write(data["actions"])

            else:
                st.error(f"Something went wrong (status {response.status_code})")
    else:
        st.warning("Please enter a topic.")

# History section
st.divider()
st.subheader("📚 Previous Reports")

history_topic = st.text_input("Enter topic to fetch history")

if st.button("Get History"):
    if history_topic:
        response = requests.get(f"{API_URL}/history/{history_topic}")

        if response.status_code == 200:
            data = response.json()
            count = data.get("history_count", 0)
            if count == 0:
                st.info(f"No reports found for '{history_topic}'. Generate one first.")
            else:
                st.write(f"Found {count} report(s) for **{history_topic}**")
                for i, report in enumerate(data["reports"], 1):
                    with st.expander(f"Report {i} — {report.get('timestamp', 'unknown time')}"):
                        st.write(report.get("report", ""))
        else:
            st.error(f"Could not fetch history (status {response.status_code}). Check that the topic matches exactly.")
    else:
        st.warning("Please enter a topic.")

