from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent



from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model="openai/openai/gpt-oss-120b",
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY"),
    temperature=1.0,
    top_p=1.0,
    max_tokens=4096
)
# ==================================== Base class =========================================
@CrewBase
class Blogdon():
    """Blogdon crew"""

    agents: list[BaseAgent]
    tasks: list[Task]
    agents_config: dict
    tasks_config: dict

# ============================================ Agents ============================================
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            verbose=True,
            llm=llm
        )

    @agent
    def hook_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['hook_generator'], # type: ignore[index]
            verbose=True,
            llm=llm
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config = self.agents_config['writer'],
            verbose = True,
            llm=llm
        )

    @agent
    def humanizer(self) -> Agent:
        return Agent(
            config = self.agents_config['humanizer'],
            verbose = True,
            llm=llm
        )

    @agent
    def seo_specialist(self) -> Agent:
        return Agent(
            config = self.agents_config['seo_specialist'],
            verbose = True,
            llm=llm
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config = self.agents_config['editor'],
            verbose = True,
            llm=llm
        )

    @agent
    def blog_validator(self) -> Agent:
        return Agent(
            config = self.agents_config['blog_validator'],
            verbose = True,
            llm=llm
        )
# ================================================== task ===========================================
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def hook_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['hook_generation_task'], # type: ignore[index]
        )
    
    @task
    def writing_task(self)-> Task:
        return Task(
            config = self.tasks_config['writing_task']
        )
    
    @task
    def humanizer_task(self) -> Task:
        return Task(
            config = self.tasks_config['humanizer_task']
        )
    
    @task
    def seo_specialist_task(self) -> Task:
        return Task(
            config = self.tasks_config['seo_specialist_task']
        )
    
    @task
    def editor_task(self) -> Task:
        return Task(
            config = self.tasks_config['editor_task']
        )

    @task
    def blog_validation_task(self) -> Task:
        return Task(
            config = self.tasks_config['blog_validation_task'],
            output_file = 'final_blog_post.txt'
        )

# ===================================================== crew ========================================
    @crew
    def crew(self) -> Crew:
        """Creates the Blogdon crew"""


        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
