Attribute VB_Name = "SetCompanyModule"
'@IgnoreModule ValueRequired
'@Folder "src"
Option Explicit

Public Sub SetCompany(ByVal companyArg As Company)
    Set ThisPresentation = ActivePresentation
    Dim newPresentation As Presentation: Set newPresentation = Presentations.Add
    Dim thisPageSetup As PageSetup: Set thisPageSetup = ThisPresentation.PageSetup

    With newPresentation.PageSetup
        .SlideOrientation = thisPageSetup.SlideOrientation
        .SlideSize = thisPageSetup.SlideSize
        .SlideHeight = thisPageSetup.SlideHeight
        .SlideWidth = thisPageSetup.SlideWidth
        .FirstSlideNumber = thisPageSetup.FirstSlideNumber
    End With

    Dim index As Slide
    For Each index In ThisPresentation.Slides
        index.Copy
        With newPresentation.Slides.Paste
            .Design = index.Design
            .ColorScheme = index.ColorScheme
            .DisplayMasterShapes = index.DisplayMasterShapes
            .FollowMasterBackground = index.FollowMasterBackground
        End With
    Next

    newPresentation.Slides.Item(1).Shapes.Item("CustomerCompanyTextBox").TextFrame.TextRange.Text _
        = "To: " & companyArg.Value
    newPresentation.Slides.Item(1).Select
End Sub
