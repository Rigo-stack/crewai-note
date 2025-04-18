import streamlit as st
import textwrap
from dotenv import load_dotenv
from crewai import Crew, Process
from IPython.display import Markdown, display
import sys
import os

# Ensure Python can find project1 inside src/
# This is a workaround for the fact that we are running this script from the root directory
# and not from within the src directory.
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from project1.crew import Project1

load_dotenv()  # This  loads the  OpenAI key from .env


st.set_page_config(page_title="AI Note Structurer", layout="wide")
st.title("AI-Powered Note Structuring App")

st.markdown("""
        Paste your class notes: 
""")

# User input
notes = st.text_area("Paste your class notes here", height=250)

method = st.selectbox("Choose a note-taking method", ["Select...", "Outline Method", "Cornell Method"])

if st.button("Run Note Structuring") and notes and method != "Select...":
    with st.spinner("Running CrewAI agents..."):
        try:
            #same formatting as in the main.py file
            project = Project1()
            
            # Load all tasks based on the selected method
            grammar = project.grammar_task()
            fact_check = project.fact_check_task()
            if method == "Outline Method":
                formatting = project.outline_task()
            else:
                formatting = project.cornell_task()

            # Build and run the crew
            crew = Crew(
                agents=[
                    grammar.agent,
                    fact_check.agent,
                    formatting.agent
                ],
                tasks=[grammar, fact_check, formatting],
                process=Process.sequential,
                verbose=True
            )

            with open("report.md", "r", encoding="utf-8") as f:
                final_text = f.read()
      
            st.markdown("###Output")
            st.markdown(final_text, unsafe_allow_html=True)
           
            st.download_button("Download Markdown", final_text, file_name="final_notes.md")

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.caption("Please paste your notes and choose a note format to get starte.")
