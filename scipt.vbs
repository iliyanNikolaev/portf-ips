Dim nameInp
Dim ageInp
Dim infoInp

nameInp = InputBox("Name:", "Enter name")

If nameInp = "" Then
    MsgBox "Invalid Name!", vbExclamation, "Error"
    WScript.Quit 
End If

ageInp = InputBox("Age:", "Enter age")

If ageInp = "" Then
    MsgBox "Invalid Age!", vbExclamation, "Error"
    WScript.Quit
End If

infoInp = InputBox("Info:", "Enter information")

If ageInp = "" Then
    MsgBox "Invalid Info!", vbExclamation, "Error"
    WScript.Quit
End If

Set xmlhttp = CreateObject("MSXML2.ServerXMLHTTP")

url = "http://localhost:6161/survey"

data = "{""name"":""" & nameInp & """,""age"":" & ageInp & ",""team"":""" & infoInp & """}"

xmlhttp.Open "POST", url, False
xmlhttp.setRequestHeader "Content-Type", "application/json"
xmlhttp.send data

If xmlhttp.Status = 200 Then
    MsgBox "Data sent successfully!", vbInformation, "Success"
Else
    MsgBox "Error sending data!", vbExclamation, "Error"
End If