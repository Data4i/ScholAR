from langchain_community.agent_toolkits import SQLDatabaseToolkit
from AgentWorkflow.utils.models import llm
from AgentWorkflow.utils.db import db

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()