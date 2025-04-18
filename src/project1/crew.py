from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Project1():
    """Project1 crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def grammar_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['grammar_expert'],
            verbose=True
        )

    @agent
    def factual_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['factual_expert'],
            verbose=True
        )

    @agent
    def outline_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['outline_expert'],
            verbose=True
        )

    @agent
    def cornell_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['cornell_expert'],
            verbose=True
        )

    # @agent
    # def final_editor(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['final_editor'],
    #         verbose=True
    #     )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def grammar_task(self) -> Task:
        return Task(
            config=self.tasks_config['grammar_task'],
        )   

    @task
    def fact_check_task(self) -> Task:
        return Task(
            config=self.tasks_config['fact_check_task'],
        )

    @task
    def outline_task(self) -> Task:
        return Task(
            config=self.tasks_config['outline_task'],
            output_file='report.md'
        )

    @task
    def cornell_task(self) -> Task:
        return Task(
            config=self.tasks_config['cornell_task'],
            output_file='report.md'
        )

    # @task
    # def final_editing_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['final_editing_task'],
    #         output_file='report.md',
    #         alowed_delegation=True  # This will allow the task to be delegated to another agent if needed
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the Project1 crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
