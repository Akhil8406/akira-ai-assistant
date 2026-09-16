Set shell = CreateObject("WScript.Shell")

shell.CurrentDirectory = "D:\study\ai assistant"

shell.Run """D:\study\ai assistant\.venv\Scripts\pythonw.exe"" -m src.main", 0, False