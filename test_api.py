import api_handler

with open("api_key.txt", "r", encoding="utf-8") as key_file:
    API_KEY = key_file.read().strip()
test_progress_data = [
    {"time": "2025-03-14 12:00:00", "progress": "完成了背景调研"},
    {"time": "2025-03-14 14:00:00", "progress": "开始撰写方法部分"}
]

summary = api_handler.fetch_summary(test_progress_data, API_KEY)
print("API 返回的总结：\n", summary)
