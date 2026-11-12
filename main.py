from src.langchain_multi_agent_research_system.pipelines.pipelines import (
    run_research_pipeline,
)

# topic = "What is the current status of Nvidia stocks after reveal of Jensen Huang affair with chinese spy Alice Huang?"

topic = "What is the weather forcast for next 5 days in noida?"

run_research_pipeline(topic)
