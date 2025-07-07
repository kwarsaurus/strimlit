import openai

client = openai.OpenAI(
    api_key="sk-ce46c47e696542268e5f3745d56ef034",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-turbo",
    messages=[{"role": "user", "content": user_input}]
)
