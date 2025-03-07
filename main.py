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
    
@app.get("/")
async def root():
    return {"message": "Working 🥸"}
    