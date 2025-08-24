# client_plamo_openai.py
import os, requests

API_BASE = "http://<lab-server-ip>:8001/v1"
prompt = r"""<|plamo:op|>dataset
translation
<|plamo:op|>input lang=English
Honey Vanilla Ice Cream

1 pint heavy cream
1 cup milk (whole milk recommended)
2 Tbsp vanilla extract

Add milk and sugar to medium sized bowl and mix until dissolved.
Add heavy cream and vanilla extract and mix.
Stir in honey.
<|plamo:op|>output lang=Japanese
"""

payload = {
    "model": "pfnet/plamo-2-translate",
    "prompt": prompt,
    "max_tokens": 1024,
    "temperature": 0,
    "stop": ["<|plamo:op|>"]
}

r = requests.post(f"{API_BASE}/completions", json=payload, timeout=120)
r.raise_for_status()
print(r.json()["choices"][0]["text"].strip())

