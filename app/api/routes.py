import json
import logging
import uuid

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

router = APIRouter()

# Lazy-loaded agent (built on first request)
_agent = None


def _get_agent():
    global _agent
    if _agent is None:
        from app.agent.graph import build_supervisor

        _agent = build_supervisor()
    return _agent


class QueryRequest(BaseModel):
    text: str
    thread_id: str | None = Field(
        default=None,
        description="Conversation thread ID. Omit to start a new conversation.",
    )


class QueryResponse(BaseModel):
    response: str
    thread_id: str


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    agent = _get_agent()
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": request.text}]},
        config,
    )

    response_text = result["messages"][-1].content
    return QueryResponse(response=response_text, thread_id=thread_id)


@router.post("/query/stream")
async def query_stream(request: QueryRequest):
    agent = _get_agent()
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    async def event_generator():
        # Send thread_id as first event
        yield f"data: {json.dumps({'type': 'metadata', 'thread_id': thread_id})}\n\n"

        for chunk in agent.stream(
            {"messages": [{"role": "user", "content": request.text}]},
            config,
            stream_mode="messages",
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, metadata = chunk["data"]
                if hasattr(token, "content") and token.content:
                    yield f"data: {json.dumps({'type': 'token', 'content': token.content})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )
