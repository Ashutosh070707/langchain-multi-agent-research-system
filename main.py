from src.langchain_multi_agent_research_system.tools.tools import web_search, scrape_url

r = web_search.invoke({"query": "latest news on Narendera Modi"})
print(r)

# print(scrape_url("https://pulse.zerodha.com"))
