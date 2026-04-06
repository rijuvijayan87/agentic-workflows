from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class Debate:
    """Debate crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def debater(self) -> Agent:
        return Agent(config=self.agents_config["debater"], verbose=True)

    @agent
    def judge(self) -> Agent:
        return Agent(config=self.agents_config["judge"], verbose=True)

    @task
    def propose_task(self) -> Task:
        return Task(config=self.tasks_config["propose_task"])

    @task
    def oppose_task(self) -> Task:
        return Task(config=self.tasks_config["oppose_task"])

    @task
    def decide_task(self) -> Task:
        return Task(config=self.tasks_config["decide_task"])

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
