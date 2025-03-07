from langgraph.graph import MessagesState
from typing import Optional

class AgentWorkflowState(MessagesState):
    user_input: Optional[str] = None
    verified: Optional[bool] = False
    clarification: Optional[str] = None
    output: Optional[str] = None