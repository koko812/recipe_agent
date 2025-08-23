# client_ws.py（短いのでこれだけ）
import asyncio, json, websockets
async def main():
    async with websockets.connect("ws://localhost:8000/ws") as ws:
        q = {"ingredients":["鶏むね肉","長ねぎ"], "constraints":["時短","低脂質"], "servings":2}
        await ws.send(json.dumps(q))
        async for msg in ws:
            obj = json.loads(msg)
            print(json.dumps(obj, ensure_ascii=False, indent=2))
asyncio.run(main())

