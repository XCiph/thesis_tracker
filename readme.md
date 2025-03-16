# 如何使用：
直接下载dist文件夹即可。
`config.json`用于修改你的prompt（目前里面还是我的论文名字XD）
`api_key.txt`用于放置你的API 

# Mac用户：
请自己下载一个pyinstaller
`pip install pyinstaller`
然后运行以下指令

```python
pyinstaller --onefile --windowed --name=ThesisTracker --icon=favicon.ico     --exclude-module matplotlib     --exclude-module numpy     --exclude-module pandas     --exclude-module scipy     --exclude-module IPython     --exclude-module tkinter.dnd     --exclude-module tkinter.ttk     --exclude-module zmq     --exclude-module pyzmq     --exclude-module certifi     --exclude-module jinja2     --exclude-module pygments     --exclude-module jsonschema     --exclude-module nbformat     --exclude-module traitlets     --exclude-module parso     --exclude-module jedi     --exclude-module wcwidth     --exclude-module psutil     --exclude-module websockets     --exclude-module openpyxl     --exclude-module pytz     --exclude-module win32com     --exclude-module pythoncom     --exclude-module pywintypes     thesis_tracker_gui.py
```