Dim objShell
Set objShell = CreateObject("WScript.Shell")

' Command to run Ubuntu and execute a command
Dim command
command = "wsl bash -c ""echo lsi2010| sudo -S service redis-server start"""

' Run command
objShell.Run command, 1, True

' Release object
'Set objShell = Nothing
