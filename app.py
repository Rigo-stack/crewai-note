import streamlit as st
import re
import os
import sys
import PyPDF2
import docx2txt
import litellm
from dotenv import load_dotenv
from crewai import Crew, Process

# Set up Streamlit UI
st.set_page_config(page_title="AI Note Structurer", layout="centered")
st.title("AI-Powered Note Structuring App")

# Ensure Python can find project1 inside src/
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from project1.crew import Project1

# File helpers

def extract_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def extract_docx_text(uploaded_file):
    return docx2txt.process(uploaded_file)

@st.cache_data
def load_markdown(file_path: str) -> str:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Loads API keys from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")

if not openai_api_key:
    st.error("Missing OPENAI_API_KEY in your .env file.")
else:
    litellm.api_key = openai_api_key

if not serper_api_key:
    st.error("Missing SERPER_API_KEY in your .env file.")

@st.cache_resource
def load_project():
    return Project1()

# User inputs : PDF, Word Document, or Text
notes = ""
input_type = st.selectbox("Select the type of input", ["Select...", "PDF", "Word Document", "Text"])

if input_type == "PDF":
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file:
        raw_text = extract_pdf_text(uploaded_file)
        notes = re.sub(r'\n{2,}', '\n\n', raw_text.strip())

elif input_type == "Word Document":
    uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"])
    if uploaded_file:
        notes = extract_docx_text(uploaded_file)

elif input_type == "Text":
    notes = st.text_area("Paste your class notes here", height=300, placeholder="e.g., AI notes ...")

method = st.selectbox("Choose a formatting method", ["Select...", "Outline Method", "Cornell Method", "Boxing Method"])
# Tracks and resets on input type change : Not sure if this is needed
if "selected_input" not in st.session_state:
    st.session_state.selected_input = input_type
elif st.session_state.selected_input != input_type and input_type != "Select...":
    st.session_state.clear()
    st.session_state.selected_input = input_type
    st.rerun()

# Tracks and resets on format method change : Not sure if this is needed
if "selected_method" not in st.session_state:
    st.session_state.selected_method = method
elif st.session_state.selected_method != method and method != "Select...":
    st.session_state.clear()
    st.session_state.selected_method = method
    st.rerun()


flashcards_opt = st.checkbox("Generate Flashcards", value=False, help="Generate 5 to 10 flashcards from the notes.")

if st.button("Run Note Structuring") and input_type != "Select..." and method != "Select..." and notes:
    with st.spinner("Running CrewAI agents..."):
        try:
            project = load_project()
            grammar = project.grammar_task()
            fact_check = project.fact_check_task()
            flashcards = project.flashcard_task()

            if method == "Outline Method":
                formatting = project.outline_task()
            elif method == "Cornell Method":
                formatting = project.cornell_task()
            elif method == "Boxing Method":
                formatting = project.boxing_task()
            else:
                st.error("Invalid formatting method selected.")
                st.stop()

            agents = [grammar.agent, fact_check.agent, formatting.agent]
            tasks = [grammar, fact_check, formatting]

            if flashcards_opt:
                agents.append(flashcards.agent)
                tasks.append(flashcards)

            crew = Crew(
                agents=agents,
                tasks=tasks,
                process=Process.sequential,
                verbose=True
            )

            crew.kickoff(inputs={"notes": notes})

            st.session_state["final_notes"] = load_markdown("report.md")
            if flashcards_opt:
                st.session_state["flashcards_md"] = load_markdown("flashcards.md")

        except Exception as e:
            st.error(f"An error occurred: {e}")            

# Output rendering
if "final_notes" in st.session_state:
    final_text = st.session_state["final_notes"]
    st.markdown("## 📄 Output", unsafe_allow_html=True)

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

    elif method == "Cornell Method":
        st.subheader("📚 Cornell Notes Formatted")

        def parse_markdown_sections(text):
            sections = {}
            current_section = None
            for line in text.splitlines():
                if line.strip().startswith("## "):
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

    elif method == "Outline Method":
        st.subheader("🗂️ Outline Notes Formatted")
        sections = final_text.strip().split("\n\n")
        for section in sections:
            lines = section.strip().split("\n")
            if lines:
                title = lines[0]
                content = "\n".join(lines[1:]) if len(lines) > 1 else ""
                with st.container(border=True):
                    st.markdown(f"**{title}**")
                    st.markdown(content)
    else:
        st.markdown(final_text)

# Flashcards output:
if flashcards_opt and "flashcards_md" in st.session_state:
    flashcards_text = st.session_state["flashcards_md"]
    st.markdown("## 🃏 Flashcards", unsafe_allow_html=True)
    st.subheader("📝 Flashcards")

    pattern = r"- \*\*Q: (.*?)\*\*.*?\*\*A:\*\* (.*?)\n"
    qa_pairs = re.findall(pattern, flashcards_text, re.DOTALL)

    for i, (question, answer) in enumerate(qa_pairs, 1):
        with st.expander(f"Q{i}: {question.strip()}"):
            st.markdown(f"**Answer:** {answer.strip()}")

# Downloads Options
if "final_notes" in st.session_state:
    st.download_button("📥 Download Markdown", st.session_state["final_notes"], file_name="final_notes.md")

if flashcards_opt and "flashcards_md" in st.session_state:
    st.download_button("📥 Download Flashcards", st.session_state["flashcards_md"], file_name="flashcards.md")
