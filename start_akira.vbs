Set shell = CreateObject("WScript.Shell")

' Wait 15 seconds after Windows login
WScript.Sleep 15000

' Set AKIRA project directory
shell.CurrentDirectory = "D:\study\ai assistant"

' Launch AKIRA invisibly
shell.Run """D:\study\ai assistant\.venv\Scripts\pythonw.exe"" -m src.main", 0, False