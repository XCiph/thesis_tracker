import openai
import json

# 读取 Prompt 配置
with open("config.json", "r", encoding="utf-8") as config_file:
    config = json.load(config_file)

def fetch_summary(progress_data, api_key):
    client = openai.OpenAI(api_key=api_key)
    
    # 读取 Prompt 和 论文信息
    prompt = config["prompt_template"] + config["thesis_info"]
    
    for entry in progress_data:
        prompt += f"{entry['time']}: {entry['progress']}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一个进度跟踪助手，帮助用户总结进度并给出下一步建议，同时给予更多鼓励。"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"API 请求失败: {str(e)}"

