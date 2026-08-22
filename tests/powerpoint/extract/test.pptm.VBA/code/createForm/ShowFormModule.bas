Attribute VB_Name = "ShowFormModule"
'@Folder("createForm")
Option Explicit
Option Private Module

Public Sub ShowInputCompanyForm()
    Dim form As IForm
    Set form = New SetCompanyForm

    Dim newCompany As Company: Set newCompany = New Company
    If Not form.ShowForm(newCompany) Then Exit Sub
    SetCompany newCompany
End Sub
