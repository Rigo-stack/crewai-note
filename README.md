# Agent-Note–Composition

## Description

This app, hosted in Streamlit, uses CrewAI agents to structure information into easy-to-review notes. The inputs for the app are text, PDF, or DOCX files.



### Information Flow

- If the input is not direct text, the app extracts it from the uploaded file.
- The extracted or pasted text is passed to a crew of AI agents.
- The agents process the input sequentially, each performing a distinct part in preparing the final structured notes.

### Agents

- **Grammar Agent**: Corrects grammar and writing inconsistencies in the input.
- **Fact-check Agent**: Validates the factual accuracy of the content.
- **Format Agent**: Applies a selected note-taking method:
  - Outline Method
  - Cornell Method
  - Boxing Method
- **(Optional) Flashcards Agent**: Creates 5 to 15 flashcards summarizing key facts and concepts from the input text.

## Technologies

- **CrewAI**: Multi-agent orchestration framework
- **Streamlit**: User interface and structured Markdown output
- **PyPDF2**: Extracts text from PDF files
- **docx2txt**: Extracts text from Word documents
- **litellm**: Lightweight wrapper to call LLMs like OpenAI
- **python-dotenv**: Loads environment variables for API key management

---

## Installing

### 1. Prerequisites

- Python `>=3.10` and `<3.13` must be installed.
- This project uses [`uv`](https://github.com/astral-sh/uv) for dependency and package management.

### 2. Install `uv`

```bash
pip install uv
```

### 3. Clone the Repository

```bash
git clone https://github.com/Rigo-stack/crewai-note.git
cd crewai-note
```
### 4. Install Dependencies
```bash
uv pip install -r requirements.txt
```
### 5. Set Up Environment Variables
```bash:
OPENAI_API_KEY=your_openai_key
SERPER_API_KEY=your_serper_key
```

### 6. Launch App:
``` bash
Streamlit run app.py
```
---
## Usage:

Customization of Agents:
- Modify 'agents.yaml' to define the agents
- Modify 'tasks.yaml' to define the tasks
- Modify 'crew.py' to add your own logic, tools, and specific args
- Modify 'app.py' to add custom inputs for your agents and tasks

---
## Contributing:

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate


---
## License
[MIT](https://choosealicense.com/licenses/mit/)
