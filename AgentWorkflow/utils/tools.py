from langchain_community.agent_toolkits import SQLDatabaseToolkit
from AgentWorkflow.utils.models import llm
from AgentWorkflow.utils.db import db
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__))) 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()