from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langgraph_workflow import build_langgraph_flow, stream_graph_updates

graph = build_langgraph_flow()
app = FastAPI()


@app.post("/summarize")
async def request_handler(doc_type: str, document: str):
    stream_response = stream_graph_updates(graph, document, doc_type)
    return StreamingResponse(stream_response, media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")