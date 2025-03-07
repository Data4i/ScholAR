from langgraph.graph import START, StateGraph, END
from langgraph.types import interrupt, Command
from AgentWorkflow.utils.db import db
from AgentWorkflow.utils.tools import tools
from AgentWorkflow.utils.models import llm
from typing import Literal
from AgentWorkflow.utils.state import AgentWorkflowState
from langchain_core.prompts import PromptTemplate
from langgraph.prebuilt import create_react_agent
from AgentWorkflow.utils.prompts import VERIFICATION_SYSTEM_PROMPT, QUERY_SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.checkpoint.memory import MemorySaver
import json


verification_template = PromptTemplate.from_template(VERIFICATION_SYSTEM_PROMPT)
query_template = PromptTemplate.from_template(QUERY_SYSTEM_PROMPT)

verification_system_message = verification_template.format(dialect=db.dialect)
query_system_message = query_template.format(dialect=db.dialect, top_k=5)


async def verification_node(state: AgentWorkflowState) -> Command[Literal["verification_interrupt_node", "query_node"]]:
    verification_agent = create_react_agent(llm, tools, prompt=SystemMessage(verification_system_message))
    model_response = await verification_agent.ainvoke(
        {"messages": [{"role": "user", "content": state['messages'][-1].content}]}
    )
    print(model_response['messages'][-1].content)
    response = json.loads(model_response['messages'][-1].content)
    
    
        
    goto = 'query_node' if response['input_verified'] else 'verification_interrupt_node'

    return Command(
            update={
                "verified": response['input_verified'],
                "user_input": response['input'],
                "clarification": response['clarification'],
                "messages": model_response['messages'][-1]
        },
        goto=goto
    )
    
async def verification_interrupt_node(state: AgentWorkflowState) -> Command[Literal['verification_node']]:
    user_input = interrupt(value=state['clarification'])
    
    if user_input:
        return Command(
            update = {
                "user_input": user_input,
                "messages": HumanMessage(user_input)
            },
            goto='verification_node'
        )


async def query_node(state: AgentWorkflowState) -> Command[Literal['__end__']]:
    query_agent = create_react_agent(llm, tools, prompt=SystemMessage(query_system_message))
    model_response = await query_agent.ainvoke(
        {"messages": [{"role": "user", "content": state['messages'][-1].content}]}
    )
    cleaned_output = model_response['messages'][-1].content
    return Command(
        update={
            "messages": model_response['messages'][-1],
            "output": cleaned_output
        },
        goto=END
    )

builder = StateGraph(AgentWorkflowState)
builder.add_node("verification_node", verification_node)
builder.add_node("query_node", query_node)
builder.add_node("verification_interrupt_node", verification_interrupt_node)

builder.add_edge(START, "verification_node")

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)
