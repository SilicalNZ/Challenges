;--------------------------------------------------------------------
;InputCQ Script
;--------------------------------------------------------------------
Sleep 2000
;--------------------------------------------------------------------
;Opening GDrive
;--------------------------------------------------------------------
Run https://drive.google.com/drive/u/1/folders/0Bxh5OsOPx65mUHhkWFpPSThDc1U
SetWinDelay, 10
WinGet, Drive, ID, A
Sleep 10000
;--------------------------------------------------------------------
;Creating 4 variables for 2 respective mouse positions
;--------------------------------------------------------------------
ocrx1 = 515
ocry1 = 390
ocrx2 = 715
ocry2 = 410
;--------------------------------------------------------------------
;Locating latest CQ Attack Screenshot
;--------------------------------------------------------------------
Send, {Down}
Sleep 500
Send,  {Up}
Sleep 500
Send, {Enter}
Loop 6
{
Send, {Down}
}
Loop 7
{
  If UpCheck = 1
  {
       Send, {up}
  }
  Upcheck = 1
  Send, {Enter}
  Sleep 500
  Loop 2
  {
      Send, {+}
  }
  Loop 6
  {
;--------------------------------------------------------------------
;Altering Mouse Positions specific to which line to read from
;--------------------------------------------------------------------
    ocry1 = (ocry1 + 35)
    ocry2 = (ocry2 + 35)
    Array = Name
    Loop 2 
    {
;--------------------------------------------------------------------
;Capturing name or Value from OCR for Array
;--------------------------------------------------------------------
      MouseClick, Left, %ocrx1%, %ocry1%, 50
      Sleep 100
      Send, {LWin down}
      Sleep 100
      Send, {q}
      Sleep 100
      Send, {LWin up}
      Sleep 500
      MouseClick, Left, %ocrx2%, %ocry2%, 50
      Sleep 500
      Send ^{a}
      Sleep 500
      Send ^{c}
      Sleep 500
      Send, {Esc}
;=============================
;Find = [Array Functions] (Developmental script)
;=============================
;--------------------------------------------------------------------
;Changes above section to access the Values
;--------------------------------------------------------------------    
      ocrx1 = (ocrx1 + 215)
      ocrx2 = (ocrx2 + 385)
      Array = Value
    }
  }
}
;--------------------------------------------------------------------
;Spreadsheet input Phase
;--------------------------------------------------------------------    
Run https://docs.google.com/spreadsheets/d/1gbj0cLVRuQI02LdSJnOenDKnM0RGfERoKJYlh6uqW1k/edit#gid=1239498060
Loop
{
;=============================
;Retrieve Name1 = [Array Functions] (Developmental script)
;=============================
Send, ^{g}
Send, ^{v}
Send, {Esc}
Loop  7
{
    Send, {Right}
}
}
