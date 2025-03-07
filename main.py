from AgentWorkflow.graph import graph
from pydantic import BaseModel
from typing import Optional, List
from langchain_core.messages import HumanMessage
from fastapi import FastAPI
import uuid
import json

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    chat_history: Optional[List[dict]] = None
    thread_id: Optional[str] = None  
    
    
@app.post("/chat")
async def chat(request: ChatRequest):
    user_message = request.message
    thread_id = request.thread_id or str(uuid.uuid4())
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": user_message}]},
        config={"configurable": {"thread_id": thread_id}}  
    )
    print(result)
    return result["messages"][-1].content
    

# class ChatResponse(BaseModel):
#     message: str
#     requires_clarification: bool
#     thread_id: str

# @app.post("/chat", response_model=ChatResponse)
# async def chat(request: ChatRequest):
#     user_message = request.message
#     thread_id = request.thread_id or str(uuid.uuid4())
#     config = {"configurable": {"thread_id": thread_id}}
    
#     # Invoke the graph with the current input
#     result = await graph.ainvoke(
#         {"messages": [HumanMessage(content=user_message)]},  # Initial input as a HumanMessage
#         config=config
#     )
    
#     # Check if the result is an interrupt (clarification message)
#     if isinstance(result, str):
#         return {
#             "message": result,
#             "requires_clarification": True,
#             "thread_id": thread_id
#         }
#     else:
#         # Extract the last message or output
#         last_message = result.get("output", result["messages"][-1].content)
#         return {
#             "message": last_message,
#             "requires_clarification": False,
#             "thread_id": thread_id
#         }
@app.get("/")
async def root():
    return {"message": "Working 🥸"}
    