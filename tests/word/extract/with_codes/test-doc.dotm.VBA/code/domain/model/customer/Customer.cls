VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Customer"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
'@Folder "domain.model.customer"
Option Explicit

Private Type TCustomer
    Company As CustomerCompany
    Person As CustomerPersonInCharge
End Type

Private this As TCustomer

Public Property Get Company() As CustomerCompany
    Set Company = this.Company
End Property

Public Property Get Person() As CustomerPersonInCharge
    Set Person = this.Person
End Property

Private Sub Class_Initialize()
    Set this.Company = New CustomerCompany
    Set this.Person = New CustomerPersonInCharge
End Sub
