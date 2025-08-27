# calc_agent.py
from openai import OpenAI
import json

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "calc_evaluate",
            "description": "高精度で数値や単位の計算を行う",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "計算式。例: '(12 km)/(45 min) -> m/s'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# ダミーの計算関数（本当はpint/sympy等を呼び出す）
def calc_evaluate(expression: str):
    if "12 km" in expression:
        return {"value": "4.44", "unit": "m/s"}
    return {"value": "?", "unit": ""}


def ask(question: str):
    # 1st turn: ツール呼び出しを含む可能性のある応答を取得
    first = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        tools=[{
            "type": "function",
            "function": {
                "name": "calc_evaluate",
                "description": "高精度で数値や単位の計算を行う",
                "parameters": {
                    "type": "object",
                    "properties": {"expression": {"type": "string"}},
                    "required": ["expression"]
                }
            }
        }],
        tool_choice="auto",
    )
    msg = first.choices[0].message

    # ツール呼び出しが無ければそのまま返す
    if not msg.tool_calls:
        return msg.content

    # すべての tool_call に応答を用意
    tool_messages = []
    for call in msg.tool_calls:
        if call.function.name == "calc_evaluate":
            args = json.loads(call.function.arguments)   # ← eval禁止
            result = calc_evaluate(args["expression"])   # ← あなたの関数
            tool_messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": "calc_evaluate",
                "content": json.dumps(result, ensure_ascii=False),  # JSON文字列で返す
            })
        else:
            # 未対応ツールは空応答でも返しておく（本来は実装推奨）
            tool_messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "name": call.function.name,
                "content": json.dumps({"error": "not_implemented"}),
            })

    # 2nd turn: assistant(=tool_calls) の直後に **全て**の tool メッセージを並べる
    follow = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": question},
            # SDKのMessageオブジェクトはそのまま渡さず、素のdictにする
            {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": c.id,
                        "type": "function",
                        "function": {"name": c.function.name, "arguments": c.function.arguments},
                    } for c in msg.tool_calls
                ]
            },
            *tool_messages
        ],
    )
    return follow.choices[0].message.content

if __name__ == "__main__":
    q = "12 km を 45 分で走った平均速度を m/s と km/h で"
    print(ask(q))

