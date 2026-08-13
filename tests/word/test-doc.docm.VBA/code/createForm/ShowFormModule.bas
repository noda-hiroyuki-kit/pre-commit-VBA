Attribute VB_Name = "ShowFormModule"
'@Folder("createForm")
Option Explicit
Option Private Module

Public Sub CreateInvitation()
    Dim form As IForm
    Set form = New CreateInvitationForm

    Dim newCustomer As Customer: Set newCustomer = New Customer
    If Not form.ShowForm(newCustomer) Then Exit Sub
    CreateInvitationDocument newCustomer
End Sub
