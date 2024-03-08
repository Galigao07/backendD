' Create a FileSystemObject
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the full path of the VBScript file
scriptFullPath = WScript.ScriptFullName

' Extract the directory from the full path
scriptDirectory = fso.GetParentFolderName(scriptFullPath)

' Set the current working directory to the directory of the VBScript file
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = scriptDirectory

' Run the daphne command
WshShell.Run "cmd /c daphne -b 0.0.0.0 -p 8001 backendD.asgi:application > output.txt && pause", 1, True

If Err.Number <> 0 Then
    MsgBox "Error: " & Err.Description
End If

' Clean up
Set WshShell = Nothing
Set fso = Nothing
