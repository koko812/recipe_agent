# app.py
from fastapi import FastAPI, WebSocket
from schemas import RecipeQuery
from graph_core import run_graph
import json

app = FastAPI()

@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            q = RecipeQuery(**json.loads(raw))
            # 簡易ストリーム（本番はLLMのトークナイズ出力に置換）
            await ws.send_text(json.dumps({"stage":"plan", "data":"計画中..."}))
            reply = run_graph(q)
            await ws.send_text(json.dumps({"stage":"result", "data":reply.model_dump()}))
    except Exception:
        await ws.close()

