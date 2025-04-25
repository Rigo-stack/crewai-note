import streamlit as st
import textwrap
from dotenv import load_dotenv
from crewai import Crew, Process
from IPython.display import Markdown, display
import sys
import os
import re
import litellm


# Ensure Python can find project1 inside src/
# This is a workaround for the fact that we are running this script from the root directory
# and not from within the src directory.
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from project1.crew import Project1

load_dotenv()  # This  loads the  OpenAI key from .env

openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

# Check if API keys exist
if not openai_api_key:
    st.error("Missing OPENAI_API_KEY. Please check your .env file.")
else:
    litellm.api_key = openai_api_key

if not serper_api_key:
    st.error("Missing SERPER_API_KEY. Please check your .env file.")


@st.cache_resource
def load_project():
    from project1.crew import Project1
    return Project1()

@st.cache_data
def load_markdown(file_path: str) -> str:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

st.set_page_config(page_title="AI Note Structurer", layout="centered")
st.title("AI-Powered Note Structuring App")

notes = st.text_area("Paste your class notes here", height=300, placeholder="e.g., Ai notes ...")

method = st.selectbox("Choose a formatting method", ["Select...", "Outline Method", "Cornell Method", "Boxing Method"])

if st.button("Run Note Structuring") and notes and method != "Select...":
    with st.spinner("Running CrewAI agents..."):
        try:
            # Initialize the project and load tasks
            # project = Project1()
            project = load_project()



            # Load shared tasks
            grammar = project.grammar_task()
            fact_check = project.fact_check_task()
            flashcards = project.flashcard_task()

            # Select method-specific formatting
            if method == "Outline Method":
                formatting = project.outline_task()
            elif method == "Cornell Method":
                formatting = project.cornell_task()
            elif method == "Boxing Method":
                formatting = project.boxing_task()
            else:
                raise ValueError("Invalid method selected.")

            # Build and execute the Crew
            crew = Crew(
                agents=[grammar.agent, fact_check.agent, formatting.agent, flashcards.agent],
                tasks=[grammar, fact_check, formatting, flashcards],
                process=Process.sequential,
                verbose=True
            )
            print("\nRunning your selected Crew task...\n")
            crew.kickoff(inputs={"notes": notes})

            # Read structured markdown report
            # with open("report.md", "r", encoding="utf-8") as f:
            #     final_text = f.read()
            # with open("flashcards.md", "r", encoding="utf-8") as f:
            #     flashcards_text = f.read()

            final_text = load_markdown("report.md")
            flashcards_text = load_markdown("flashcards.md")


            # Display Output
            st.markdown("## 📄 Output", unsafe_allow_html=True)

            ########################################################################
            if method == "Boxing Method":
                def parse_markdown_into_boxes(text):
                    pattern = r'(^#+ .*$)'
                    parts = re.split(pattern, text, flags=re.MULTILINE)
                    sections = []

                    for i in range(1, len(parts), 2):
                        header = parts[i].strip()
                        content = parts[i + 1].strip() if i + 1 < len(parts) else ""
                        sections.append({"header": header, "content": content})

                    return sections
                st.subheader("📦 Formatted Output")
                for section in parse_markdown_into_boxes(final_text):
                    with st.container(border=True):
                        if section["header"]:
                            st.markdown(f"#### {section['header']}")
                        st.markdown(section["content"])
            #########################################################################
            elif method == "Cornell Method":
                st.subheader("📚 Cornell Notes Formated")

                def parse_markdown_sections(text):
                    sections = {}
                    current_section = None
                    for line in text.splitlines():
                        if line.startswith("## "):
                            current_section = line.replace("##", "").strip()
                            sections[current_section] = ""
                        elif current_section:
                            sections[current_section] += line + "\n"
                    return sections

                sections = parse_markdown_sections(final_text)

                cue_column = sections.get("Cues", "Cues Column not found.")
                notes_section = sections.get("Notes", "Notes Section not found.")
                summary = sections.get("Summary", "Summary not found.")

                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("### Cue Column")
                    st.markdown(cue_column)

                with col2:
                    st.markdown("### Notes Section")
                    st.markdown(notes_section)

                st.markdown("---")
                st.markdown("### Summary")
                st.markdown(summary)

            ################################################################
            elif method == "Outline Method":
                st.subheader("🗂️ Outline Notes Formated")
                sections = {}
                sections = final_text.strip().split("\n\n")
                for section in sections:
                    lines = section.strip().split("\n")
                    if lines:
                        title = lines[0]
                        content = "\n".join(lines[1:]) if len(lines) > 1 else ""
                        with st.container(border=True):
                            st.markdown(f"**{title}**")
                            st.markdown(content)
            #################################################################
            else:
                st.markdown(final_text)

            st.markdown("## 🃏 Flashcards", unsafe_allow_html=True)
            st.markdown(flashcards_text, unsafe_allow_html=True)
            
            st.download_button("Download Markdown", final_text, file_name="final_notes.md")
            st.download_button("Download Flashcards", flashcards_text, file_name="flashcards.md")

        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    st.caption("Please paste your notes and choose a note format to get starte.")
