# NoteCrew

## Description

This app, hosted in Streamlit, uses CrewAI agents to structure information into easy-to-review notes. The inputs for the app are text, PDF, or DOCX files.


##  Problem Statement
Like many college students, I have notes scattered across Google Docs, PDFs, Notion pages, and even screenshots of notes I was too lazy to re-copy. Now, you can extract the text using screenshots, as it has become a cool feature(wondering how? It uses OCR (Optical Character Recognition)).

But once the text is extracted, arranging it, fact-checking that you wrote the correct statement, and formatting it into clear, structured notes is still time-consuming. Instead of doing that manually, why not let a team of AI agents handle all that work?

### Features:
- Multi-Format Input Support: Process notes from PDFs, Google Docs, plain text
- Agent -Powered Note Structuring: Automatically formats your notes into popular study structures: Cornell, Outline, or Boxing method
- Grammar EnhancementL: Identifies and corrects grammar issues for improved clarity
- Fact-Checking: validate key facts in your notes for accuracy
- Optional Flashcard Generation: Converts your content into Q&A-style flashcards to help with active recall and better studying.




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

[![CrewAI][CrewAI]][CrewAI-url][![Streamlit][Streamlit]][Streamlit-url][![PyPDF2][PyPDF2]][PyPDF2-url][![docx2txt][docx2txt]][docx2txt-url][![LiteLLM][LiteLLM]][LiteLLM-url][![dotenv][dotenv]][dotenv-url][![Python][Python]][Python-url]

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
Use the Interface:
- Upload your notes as text, PDF, or DOCX
- Choose a note-taking method (Cornell, Outline, or Boxing)
- Optionally enable flashcard generation
- Click Run to let the AI agents process and format your notes

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

This project is licensed under the [MIT License](https://choosealicense.com/licenses/mit/).

---

[CrewAI]: https://img.shields.io/badge/CrewAI-000000?style=for-the-badge&logo=semantic-release&logoColor=white
[CrewAI-url]: https://github.com/joaomdmoura/crewai

[Streamlit]: https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white
[Streamlit-url]: https://streamlit.io/

[PyPDF2]: https://img.shields.io/badge/PyPDF2-3776AB?style=for-the-badge&logo=adobeacrobatreader&logoColor=white
[PyPDF2-url]: https://pypi.org/project/PyPDF2/

[docx2txt]: https://img.shields.io/badge/docx2txt-345?style=for-the-badge&logo=microsoftword&logoColor=white
[docx2txt-url]: https://pypi.org/project/docx2txt/

[LiteLLM]: https://img.shields.io/badge/LiteLLM-007ACC?style=for-the-badge&logo=openai&logoColor=white
[LiteLLM-url]: https://github.com/BerriAI/litellm

[dotenv]: https://img.shields.io/badge/dotenv-232F3E?style=for-the-badge&logo=envoyproxy&logoColor=white
[dotenv-url]: https://pypi.org/project/python-dotenv/
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/


