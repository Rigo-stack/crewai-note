#!/usr/bin/env python
import sys
import warnings
from crewai import Crew, Process

from project1.crew import Project1

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Runs the crew for the selected note-taking method.
    """
    try:
        # Step 1: Get input from user
        print("Please paste your class notes below. Press Enter twice when you're done:\n")
        notes = []
        while True:
            line = input()
            if line == "":
                break
            notes.append(line)
        notes = "\n".join(notes)

        # Step 2: Let user choose method
        print("\nWhich method do you want to apply?")
        print("1. The Outline Method")
        print("2. The Cornell Method")
        print("3. The Boxing Method")
        choice = input("Enter number: ").strip()

        # Get selected task
        project = Project1()
        if choice == "1":
            format_task = project.outline_task()
        elif choice == "2":
            format_task = project.cornell_task()
        elif choice == "3":
            format_task = project.boxing_task()
        else:
            raise ValueError("Invalid selection. Please enter valid number.")
        
        grammar_task = project.grammar_task()
        fact_check_task = project.fact_check_task()
        
        # final_task = project.final_editing_task()
        # Build crew with only the selected task/agent
        crew = Crew(
            agents=[
                grammar_task.agent,
                fact_check_task.agent,
                format_task.agent,
                # final_task.agent
            ],
            tasks=[
                grammar_task,
                fact_check_task,
                format_task,
                # final_task
            ],

            process=Process.sequential,
            verbose=True
        )

        print("\nRunning your selected Crew task...\n")
        crew.kickoff(inputs={"notes": notes})
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Project1().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Project1().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        Project1().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

