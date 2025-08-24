"""
Main module for the AI Agent Boilerplate application.

This module sets up a FastAPI application with a LangGraph-based AI agent
that can use tools to respond to user queries.
"""

import os
from typing import Dict, Any, TypedDict, Optional

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from pydantic import SecretStr

from utils import build_prompt
from tools import get_tools

load_dotenv()

app = FastAPI()

# Initialize LLM (OpenRouter via OpenAI API)
api_key = os.getenv('OPENROUTER_API_KEY')
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable is not set")

llm = ChatOpenAI(
    api_key=SecretStr(api_key),
    base_url='https://openrouter.ai/api/v1',
    model=os.getenv('OPENROUTER_MODEL', 'openai/gpt-4o-mini')
)

# Define state
class State(TypedDict):
    """State representation for the agent workflow."""
    input: str
    response: Optional[Any]

# Bind tools to LLM
tools = get_tools()
llm_with_tools = llm.bind_tools(tools)

def execute_tool(tool_call: Dict[str, Any]) -> str:
    """
    Execute a tool based on the tool call specification.
    
    Args:
        tool_call: Dictionary containing tool name and arguments
        
    Returns:
        Result of the tool execution
    """
    tool_name = tool_call['name']
    tool_args = tool_call['args']
    
    # Find and execute the appropriate tool
    for tool in tools:
        if tool.name == tool_name:
            return tool.invoke(tool_args)
    return "Tool not found"

def agent_node(state: State) -> State:
    """
    Agent node that processes user input and generates a response.
    
    Args:
        state: Current state containing user input
        
    Returns:
        Updated state with the LLM response
    """
    prompt = build_prompt('system_prompt')
    response = llm_with_tools.invoke(prompt + "\n\n" + state['input'])
    return {'input': state['input'], 'response': response}

def tool_node(state: State) -> State:
    """
    Tool node that executes tools based on LLM response.
    
    Args:
        state: Current state containing LLM response
        
    Returns:
        Updated state with tool execution results
    """
    # Execute tools based on LLM response
    response = state['response']
    tool_calls = response.tool_calls if response is not None and hasattr(response, 'tool_calls') else []

    results = []
    for tool_call in tool_calls:
        result = execute_tool(tool_call)
        results.append(f"Tool {tool_call['name']} result: {result}")

    # Join results or return a default message
    response_text = '\n'.join(results) if results else 'No tools executed'
    return {'input': state['input'], 'response': response_text}

# Build agent graph
workflow = StateGraph(State)
workflow.add_node('agent', agent_node)
workflow.add_node('tools', tool_node)
workflow.set_entry_point('agent')

def route_agent(state: State) -> str:
    """
    Route the agent to tools or end based on response.
    
    Args:
        state: Current state containing agent response
        
    Returns:
        'tools' if tool calls are present, END otherwise
    """
    response = state['response']
    if response is not None and hasattr(response, 'tool_calls') and response.tool_calls:
        return 'tools'
    return END

workflow.add_conditional_edges('agent', route_agent)
workflow.add_edge('tools', END)
graph = workflow.compile()

@app.get('/health')
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok'}

@app.post('/query')
async def query(user_input: Dict[str, str]) -> Dict[str, Any]:
    """
    Query endpoint that processes user input and returns agent response.
    
    Args:
        user_input: Dictionary containing user text input
        
    Returns:
        Dictionary with agent response or error message
    """
    try:
        result = graph.invoke({'input': user_input['text'], 'response': None})  # type: ignore
        return {'response': result['response']}
    except Exception as e:
        return {'error': f"An error occurred: {str(e)}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)