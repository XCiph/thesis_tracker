import time
import json
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys
import subprocess
import api_handler  # 导入 API 处理模块


with open("api_key.txt", "r", encoding="utf-8") as key_file:
    API_KEY = key_file.read().strip()

# 存储进度的 JSON 文件
PROGRESS_FILE = "progress.json"
SETTINGS_FILE = "settings.json"

# 加载进度数据
try:
    with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
        progress_data = json.load(file)
except FileNotFoundError:
    progress_data = []

# 加载设置数据
def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"enable_sound": True, "auto_popup": True, "custom_sound": "default", "timer_interval": 3600}

settings = load_settings()

# 保存设置
def save_settings():
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4, ensure_ascii=False)

# 获取 ChatGPT 生成的总结
def get_summary():
    return api_handler.fetch_summary(progress_data, API_KEY)

# 保存进度
def save_progress(progress):
    entry = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "progress": progress}
    progress_data.append(entry)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
        json.dump(progress_data, file, indent=4, ensure_ascii=False)

# 播放提醒铃声
def play_sound():
    if settings["enable_sound"]:
        if sys.platform == "win32":
            if settings["custom_sound"] == "default":
                import winsound
                winsound.Beep(1000, 500)  # 默认音效
            else:
                winsound.PlaySound(settings["custom_sound"], winsound.SND_FILENAME)
        elif sys.platform == "darwin":  # MacOS
            if settings["custom_sound"] == "default":
                subprocess.call(["afplay", "/System/Library/Sounds/Glass.aiff"])  # Mac 默认声音
            else:
                subprocess.call(["afplay", settings["custom_sound"]])  # 播放用户自定义音频

# 倒计时函数
def countdown():
    global remaining_time
    while remaining_time > 0:
        mins, secs = divmod(remaining_time, 60)
        timer_label.config(text=f"下一次提醒：{mins:02}:{secs:02}")
        remaining_time -= 1
        time.sleep(1)
    trigger_reminder()

# 触发提醒
def trigger_reminder():
    play_sound()
    if settings["auto_popup"]:
        ask_progress()
    else:
        messagebox.showinfo("提醒", "时间到！请手动更新进度。")

# 询问进度
def ask_progress():
    progress_window = tk.Toplevel(tk_root)
    progress_window.title("进度更新")
    progress_window.geometry("500x400")

    label = tk.Label(progress_window, text="请填写你的进度：")
    label.pack(pady=5)
    
    text_area = scrolledtext.ScrolledText(progress_window, wrap=tk.WORD, width=60, height=15)
    text_area.pack(padx=10, pady=5)
    
    def submit():
        progress = text_area.get("1.0", tk.END).strip()
        if progress:
            save_progress(progress)
            summary = get_summary()
            summary_text.config(state=tk.NORMAL)
            summary_text.delete("1.0", tk.END)
            summary_text.insert(tk.END, summary)
            summary_text.config(state=tk.DISABLED)
            progress_window.destroy()
            reset_timer()
    
    submit_button = tk.Button(progress_window, text="提交", command=submit)
    submit_button.pack(pady=5)

# 显示所有进度并退出
def show_progress_and_exit():
    progress_window = tk.Toplevel(tk_root)
    progress_window.title("所有进度记录")
    progress_window.geometry("600x400")
    
    text_area = scrolledtext.ScrolledText(progress_window, wrap=tk.WORD, width=70, height=15)
    text_area.pack(padx=10, pady=10)
    
    progress_text = "\n".join([f"{entry['time']}: {entry['progress']}" for entry in progress_data])
    encouragement = "\n\n你已经取得了很大的进步！继续加油，你一定能完成论文！🚀"
    text_area.insert(tk.END, progress_text + encouragement)
    text_area.config(state=tk.DISABLED)
    
    def exit_program():
        tk_root.destroy()
    
    exit_button = tk.Button(progress_window, text="退出", command=exit_program)
    exit_button.pack(pady=5)

# 设置界面
def open_settings():
    settings_window = tk.Toplevel(tk_root)
    settings_window.title("设置")
    settings_window.geometry("350x250")

    def toggle_sound():
        settings["enable_sound"] = sound_var.get()
        save_settings()

    def toggle_popup():
        settings["auto_popup"] = popup_var.get()
        save_settings()
    
    def change_timer():
        settings["timer_interval"] = int(timer_entry.get())
        save_settings()
    
    sound_var = tk.BooleanVar(value=settings["enable_sound"])
    popup_var = tk.BooleanVar(value=settings["auto_popup"])
    
    sound_checkbox = tk.Checkbutton(settings_window, text="启用铃声提醒", variable=sound_var, command=toggle_sound)
    sound_checkbox.pack(pady=5)

    popup_checkbox = tk.Checkbutton(settings_window, text="启用自动弹窗", variable=popup_var, command=toggle_popup)
    popup_checkbox.pack(pady=5)

    tk.Label(settings_window, text="自定义倒计时时间（秒）：").pack(pady=5)
    timer_entry = tk.Entry(settings_window)
    timer_entry.insert(0, str(settings["timer_interval"]))
    timer_entry.pack(pady=5)
    tk.Button(settings_window, text="保存", command=change_timer).pack(pady=5)

# 重置计时器
def reset_timer():
    global remaining_time
    remaining_time = settings["timer_interval"]
    threading.Thread(target=countdown, daemon=True).start()

# GUI 界面
tk_root = tk.Tk()
tk_root.title("论文进度跟踪器")
tk_root.geometry("600x600")

timer_label = tk.Label(tk_root, text="下一次提醒：60:00", font=("Arial", 14))
timer_label.pack(pady=10)

summary_text = scrolledtext.ScrolledText(tk_root, wrap=tk.WORD, width=70, height=20, background="white")
summary_text.pack(padx=10, pady=10)
summary_text.insert(tk.END, "进度总结将在你提交更新后显示。")
summary_text.config(state=tk.DISABLED)

settings_button = tk.Button(tk_root, text="设置", command=open_settings)
settings_button.pack(pady=5)

exit_button = tk.Button(tk_root, text="退出", command=show_progress_and_exit)
exit_button.pack(pady=5)

reset_timer()
tk_root.mainloop()

