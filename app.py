import requests
import json

api_key = "sk-ce46c47e696542268e5f3745d56ef034"
url = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "qwen-max",
    "messages": [
        {"role": "user", "content": "Hello"}
    ],
    "max_tokens": 100
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ BERHASIL!")
        print(f"AI Response: {result['choices'][0]['message']['content']}")
    else:
        print("❌ Ada error")
        
except Exception as e:
    print(f"Error: {e}")
