import requests

data = {
    "language": "python",
    "version": "3.10.0",
    "files": [
        {"content": """
import time
time.sleep(1)
print("Hello")
"""}
    ]
}

resp = requests.post("https://emkc.org/api/v2/piston/execute", json=data)
result = resp.json()

print("Output:", result['run']['stdout'])
print("Exit code:", result['run']['code'])
print("Execution time (s):", result['run']['time'])  # nechchi soniyada bajarildi
print("Memory used (bytes):", result['run']['memory'])  # qancha xotira ishlatildi
