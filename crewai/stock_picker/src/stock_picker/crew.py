from enum import Enum

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field


class MarketCap(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class TrendingCompanyPicker(BaseModel):
    """A company that is in the news and attracting attention"""

    name: str = Field(description="company name")
    ticker: str = Field(description="stock ticker symbol")
    reason: str = Field(description="reason for picking")


class TrendingCompanyPickerList(BaseModel):
    """List of multiple trending companies that are in the news"""

    trending_companies: list[TrendingCompanyPicker] = Field(
        description="list of trending companies"
    )


class CompanyMarketResearch(BaseModel):
    """Detailed research on a company"""

    name: str = Field(description="Company name")
    market_position: str = Field(
        description="Current market position and competitive analysis"
    )
    current_price: float = Field(description="Current price of the stock")
    forcast_in_5_years: float = Field(description="Forcast it's price in in 5 years")
    forcast_in_10_years: float = Field(description="Forcast it's price in 10 years")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    should_invest: bool = Field(description="recommendation on whether to invest")


class CompanyMarketResearchList(BaseModel):
    """List of detailed research on multiple companies"""

    market_research: list[CompanyMarketResearch] = Field(
        description="list of market research"
    )


class SelectedStock(BaseModel):
    "Details of a selected stock"

    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    cap: MarketCap = Field(
        description="Market capitalization size (small/medium/large)"
    )
    reason: str = Field(description="Reason for selecting")


class SelectedStockList(BaseModel):
    """List of selected stocks"""

    selected_stocks: list[SelectedStock] = Field(description="list of selected stocks")


@CrewBase
class StockPicker:
    """StockPicker crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def trending_company_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_picker"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["market_researcher"],
            verbose=True,
            tools=[SerperDevTool()],
        )

    @agent
    def analyst_and_report_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst_and_report_writer"], verbose=True
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config["stock_picker"], verbose=True)

    @task
    def trend_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config["trend_analysis_task"],
            output_pydantic=TrendingCompanyPickerList,
        )

    @task
    def fundamental_research_task(self) -> Task:
        return Task(
            config=self.tasks_config["fundamental_research_task"],
            output_pydantic=CompanyMarketResearchList,
        )

    @task
    def technical_analysis_and_reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["technical_analysis_and_reporting_task"],
        )

    @task
    def stock_selection_task(self) -> Task:
        return Task(
            config=self.tasks_config["stock_selection_task"],
            output_pydantic=SelectedStockList,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""

        manager = Agent(config=self.agents_config["manager"], verbose=True)

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
        )
