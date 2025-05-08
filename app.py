import streamlit as st
import re
import os
import sys
import PyPDF2
import docx2txt
import litellm
from dotenv import load_dotenv
from crewai import Crew, Process
import time

# Set up Streamlit UI
st.set_page_config(page_title="NoteCrew", layout="wide")

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

# @st.cache_data
def load_markdown(file_path: str) -> str:
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# Function to parse markdown sections for Cornell Method
def parse_markdown_sections(text):
    import re

    sections = {"Cues": "", "Notes": "", "Summary": ""}
    current_section = None

    # Use normalized line endings
    lines = text.replace('\r\n', '\n').split('\n')

    for line in lines:
        # Match headers exactly: "## Cues", "## Notes", "## Summary"
        match = re.match(r'^##\s*(Cues|Notes|Summary)\s*$', line.strip(), re.IGNORECASE)
        if match:
            current_section = match.group(1).capitalize()
            continue

        if current_section in sections:
            sections[current_section] += line + "\n"

    # Cleanup
    for key in sections:
        sections[key] = sections[key].strip() or f"❌ {key} Section not found."

    return sections



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

# Examplesnotes for each method
txt_content = """
    An AI agent is an autonomous system capable of perceiving its environment through sensors, reasoning about what it perceives, and taking actions through actuators to achieve specific goals. AI agents can operate partially autonomously without full sensory input or complete understanding of their environment. These agents operate in a continuous cycle of observation, decision-making, and action. While many AI agents possess the ability to adapt over time based on feedback, this characteristic does not apply universally to all types of agents, particularly simple reflex agents that operate on basic rules. AI agents can be categorized into several types based on their complexity and functionality: simple reflex agents respond directly to immediate stimuli in their environment and are limited in decision-making capacity; goal-based agents plan their actions based on desired outcomes, assessing their goals and making decisions to effectively achieve them, often utilizing models of their environment; utility-based agents, similar to goal-based agents, focus on maximizing optimal utility by making decisions that provide the greatest benefit or satisfaction; and learning agents that improve their performance over time by utilizing data from previous experiences, thereby allowing them to adapt to new situations and enhance their decision-making processes. AI agents are widely utilized across various domains, making them an integral part of modern artificial intelligence systems. Notable applications include virtual assistants that help users manage tasks and inquiries, recommendation systems providing personalized content suggestions, smart home devices automating household functions, autonomous vehicles navigating real-time traffic conditions, natural language processing for understanding and generating human language, and gaming applications where agents adapt strategies based on player actions. Through these applications, AI agents significantly contribute to the development and functionality of intelligent systems in today’s technology landscape.
    """
pdf_content = "NeuralNetworkNotes2.pdf"
docx_content = "CRNNArchitectureNotes.docx"

# Initialize session state for notes
if "notes" not in st.session_state:
    st.session_state["notes"] = ""


# User inputs : PDF, Word Document, or Text
# Streamlit’s widgets often preserve their own state unless you explicitly give them keys and clear those entries too.
with st.sidebar:
    st.header("Configuration")
  
    input_type = st.sidebar.selectbox("Select the type of input", ["Select...", "PDF", "Word Document", "Text"], key="input_type")

    if input_type == "PDF":
        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("Load Example PDF", key="load_example_pdf"):
                placeholder = st.empty()
                try:
                    with open(pdf_content, "rb") as f:
                        st.session_state["notes"] = extract_pdf_text(f)
                    placeholder.success("Loaded Example PDF!")
                except FileNotFoundError:
                    placeholder.error(f"Could not find example PDF at {pdf_content}")
                time.sleep(1)
                placeholder.empty()

        with col2:
            if st.button("Clear Example PDF Selected", key="clear_example_pdf"):
                placeholder = st.empty()
                st.session_state["notes"] = ""
                placeholder.success("Example PDF cleared!")
                time.sleep(1)
                placeholder.empty()
               
        #  Uploader 
        uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"], key="uploader_pdf")
        if uploaded_file:
            raw_text = extract_pdf_text(uploaded_file)
            st.session_state["notes"] = re.sub(r'\n{2,}', '\n\n', raw_text.strip())
        

    elif input_type == "Word Document":
        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button("Load docx", key="load_example_docx"):
                placeholder = st.empty()
                try:
                    with open(docx_content, "rb") as f:
                        st.session_state["notes"] = extract_docx_text(f)
                    placeholder.success("Loaded Example Word Document!")
                except FileNotFoundError:
                    placeholder.error(f"Could not find example Word Document at {docx_content}")
                time.sleep(1)
                placeholder.empty()

        with col2:
            if st.button("Clear docx", key="clear_example_docx"):
                placeholder = st.empty()
                st.session_state["notes"] = ""
                placeholder.success("Example Word Document cleared!")
                time.sleep(1)
                placeholder.empty()

        # Keep your uploader below
        uploaded_file = st.file_uploader("Upload a DOCX file", type=["docx"], key="uploader_docx")
        if uploaded_file:
            st.session_state["notes"] = extract_docx_text(uploaded_file)


    elif input_type == "Text":
        # ─── Example controls in two columns ───
        col1, col2 = st.columns(2, gap="small")
        with col1:
            if st.button(" Load Example Notes", key="load_example"):
                st.session_state["notes"] = txt_content.strip()
        with col2:
            if st.button(" Clear Example Notes", key="clear_example"):
                st.session_state["notes"] = ""

        st.text_area("Paste your class notes here", height=300, placeholder="e.g., AI notes ...", key="notes")
        
    method = st.selectbox("Choose a formatting method", ["Select...", "Outline Method", "Cornell Method", "Boxing Method"], key="method")

    flashcards_opt = st.checkbox("Generate Flashcards", value=False, help="Generate 5 to 15 flashcards from the notes.")

    run = st.button("Run Note Structuring")

# Pull state values out
notes = st.session_state.get("notes", "")
input_type = st.session_state.get("input_type", "Select...")
method = st.session_state.get("method", "Select...")
# flashcards_opt = st.session_state.get("flashcards_opt", False)

if run:
    if input_type == "Select..." or method == "Select..." or not notes.strip():
        st.sidebar.error("Please choose input, method, and supply some notes.")
    else:
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

# Check if the method has changed
# This is to ensure that the output is cleared when the method changes               
if "prev_method" not in st.session_state:
    st.session_state.prev_method = None

# If method has changed, clear the final_notes to stop output rendering
if method != st.session_state.prev_method:
    st.session_state.pop("final_notes", None)
    st.session_state.pop("flashcards_md", None)  # Clear flashcards if method changes
    st.session_state.prev_method = method          

# Output rendering
if "final_notes" in st.session_state:
    final_text = st.session_state["final_notes"]
    st.markdown("## 📄 Output", unsafe_allow_html=True)

    # # # 🔍 Debug output to inspect actual content
    # with st.expander("🔎 Raw Markdown Output (Debug)"):
    #     st.code(final_text[::], language="markdown")


    if method == "Boxing Method":
        def parse_markdown_into_boxes(text):
            # Remove ```markdown block if it exists
            cleaned = text.strip()
            if cleaned.startswith("```markdown"):
                cleaned = cleaned[len("```markdown"):].strip()
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3].strip()
    
            # Split based on Markdown headers (## Box or ## Summary)
            pattern = r'(^## .*$)'
            parts = re.split(pattern, cleaned, flags=re.MULTILINE)
    
            sections = []
            for i in range(1, len(parts), 2):
                header = parts[i].strip()
                content = parts[i + 1].strip() if i + 1 < len(parts) else ""
                sections.append({"header": header, "content": content})
            return sections
    
        st.subheader("📦 Boxing Method Output")
    
        all_sections = parse_markdown_into_boxes(final_text)
        boxes = [s for s in all_sections if not s["header"].lower().startswith("## summary")]
        summary = next((s for s in all_sections if s["header"].lower().startswith("## summary")), None)
    
        # Display boxes in two columns
        col1, col2 = st.columns(2)
        for i, section in enumerate(boxes):
            target_col = col1 if i % 2 == 0 else col2
            with target_col.container(border=True):
                st.markdown(f"#### {section['header']}")
                st.markdown(section["content"])
    
        # Display summary below full width
        if summary:
            st.markdown("---")
            with st.container(border=True):
                st.markdown(f"### {summary['header']}")
                st.markdown(summary['content'])

    if method == "Cornell Method":
        st.subheader("📚 Cornell Notes Formatted")

        sections = parse_markdown_sections(final_text)
        cue_column = sections["Cues"]
        notes_section = sections["Notes"]
        summary = sections["Summary"]
    

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


    if method == "Outline Method":
        st.subheader("📝 Outline Method Output")
        
        # Remove ```markdown code fences if present
        cleaned_markdown = final_text.strip()
        if cleaned_markdown.startswith("```markdown"):
            cleaned_markdown = cleaned_markdown[len("```markdown"):].strip()
        if cleaned_markdown.endswith("```"):
            cleaned_markdown = cleaned_markdown[:-3].strip()
        
        # Split into sections using '## ' headers
        sections = cleaned_markdown.split("## ")
        for raw_section in sections:
            if not raw_section.strip():
                continue  # skip empty sections
            
            lines = raw_section.strip().splitlines()
            title_line = lines[0] if lines else "Untitled Section"
            content_lines = lines[1:]
        
            with st.container(border=True):
                st.markdown(f"### {title_line.strip()}")
                for line in content_lines:
                    stripped = line.lstrip()
                    indent_level = (len(line) - len(stripped)) // 2  # assume 2 spaces per indent
        
                    if stripped.startswith("- "):
                        st.markdown(f"{'&nbsp;' * 4 * indent_level}{stripped}")
                    else:
                        st.markdown(stripped)

    # else:
    #     # Default case for other methods
    #     st.subheader("📝 Formatted Output")
    #     st.markdown(final_text)

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
