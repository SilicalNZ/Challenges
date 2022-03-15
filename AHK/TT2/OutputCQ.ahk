;--------------------------------------------------------------------
;OutputCQ Script
;--------------------------------------------------------------------
Sleep 2000
;--------------------------------------------------------------------
;Opening Bluestacks Window (Default state is minimized)
;--------------------------------------------------------------------
WinActivate, ahk_exe BlueStacks.exe
Sleep 10000
;--------------------------------------------------------------------
;Opening Clan Quest Attacks
;--------------------------------------------------------------------
MouseClick, Left, 520, 50
Sleep 4000
MouseClick, Left, 520, 650
Sleep 10000
;--------------------------------------------------------------------
;Prepping first screenshot
;--------------------------------------------------------------------
MouseClickDrag, Left, 520, 600, 520, 560, 75
Sleep 2000
;--------------------------------------------------------------------
;Capturing Clan Quest Attack through OCR
;--------------------------------------------------------------------
MouseClick, Left, 530, 380, 75
Sleep 2000
Send, {LWin down}
Sleep 100
Send, {q}
Sleep 100
Send, {LWin up}
Sleep 2000
MouseClick, Left, 555, 397, 75
Sleep 2000
Send, ^{a}
Sleep 2000
Send, ^{c}
Sleep 2000
Send, {Esc}
Sleep 2000
;--------------------------------------------------------------------
;Saving Clan Quest Attack as a variable
;--------------------------------------------------------------------

CQValue = %Clipboard%
;--------------------------------------------------------------------
;Taking First Screenshot
;--------------------------------------------------------------------
Send, !{PrintScreen} 
Sleep 2000
Run, mspaint.exe
Sleep 2000
Send, ^{v}
Sleep 2000
Send, {Esc}
Sleep 2000
;--------------------------------------------------------------------
;Zooming out of paint and cropping the image.
;--------------------------------------------------------------------
Send, ^{PgDn}
Sleep 2000
MouseClickDrag, Left, 240, 166, 423, 513, 75
Sleep 2000
Send, ^+{x}
Sleep 2000
;--------------------------------------------------------------------
;Saving File
;--------------------------------------------------------------------
Send, {F12}
Sleep 2000
;--------------------------------------------------------------------
;Locating Save Location
;--------------------------------------------------------------------
Send, !{d}
Sleep 2000
Send, C:\Bot Memory
Sleep 2000
Send, {Enter}
Sleep 2000
Loop 4
{
  Send, {Tab}
  Sleep 1500
}
Send, {End}
Sleep 1500
Sleep 1500
;--------------------------------------------------------------------
;Cross-checking a saved CQ Attack vs the latest 
;    If it's False, the script will continue
;--------------------------------------------------------------------
Send, {f2}
Sleep 1500
Send, ^{c}
Sleep 1500
if clipboard != CQValue
{   
  Sleep 2000
  Send, {Enter}    
  Sleep 2000
;--------------------------------------------------------------------
;Creating folder based off of CQ Attack
;--------------------------------------------------------------------

  Send, ^+{n}
  Sleep 2000
  Send, %CQValue%
  Loop 3
  {
    Sleep 2000
    Send, {Enter}
  }
  Sleep 2000
  Send, !{d}
  Sleep 2000
  Loop 6
  {
    Send, {Tab}
    Sleep 2000
  }
;--------------------------------------------------------------------
;Saving the first ScreenShot
;--------------------------------------------------------------------
    
  Sleep 2000
  var = 1
  Send, %var%
  Sleep 2000
  Send, {Enter}
  Sleep 2000
;--------------------------------------------------------------------
;Repeats the action of taking a screenshot -> cropping -> saving
;-------------------------------------------------------------------- 
  Loop 6
  {
    WinActivate, ahk_exe BlueStacks.exe
    Sleep 2000
;--------------------------------------------------------------------
;Scrolling and taking screenshot
;--------------------------------------------------------------------
    MouseClick, Left, 520, 600
    Sleep 2000
    MouseClickDrag, Left, 520, 600, 520, 380, 75
    Sleep 2000
    Send, !{PrintScreen} 
    Sleep 2000 
    WinActivate, ahk_exe mspaint.exe
    Send, ^{v}
    Sleep 2000
    Send, {Esc}
    Sleep 2000
;--------------------------------------------------------------------
;Cropping
;--------------------------------------------------------------------
    MouseClickDrag, Left, 240, 166, 423, 513, 75
    Sleep 2000
    Send, ^+{x}
    Sleep 2000    
;--------------------------------------------------------------------
;Saving
;--------------------------------------------------------------------        
    Send, {F12}
    Sleep 2000
    var++
    Send, %var%
    Sleep 2000
    Send, {Enter}
    Sleep 2000
  }
  WinClose, ahk_exe mspaint.exe
  Sleep 2000
;--------------------------------------------------------------------
;Open GDrive
;-------------------------------------------------------------------- 
  Run https://drive.google.com/drive/u/1/folders/0Bxh5OsOPx65mUHhkWFpPSThDc1U
  SetWinDelay, 10
  Sleep 20000
  Send, {Down}
  Sleep 2000
  Send, {up}
  Sleep 2000
  Send, {n}
  Sleep 2000
  Send, ^{c}
  Sleep 2000
  Send, {Enter}
;--------------------------------------------------------------------
;Cross-checking a saved CQ Attack vs the latest 
;    If it's False, the script will continue
;--------------------------------------------------------------------    
  Sleep 2000
  if clipboard != CQValue
  {
  clipboard++
 ;--------------------------------------------------------------------
;Uploading Files
;--------------------------------------------------------------------     
;--------------------------------------------------------------------
;Creating folder
;--------------------------------------------------------------------        
  Send, +{f}
  Sleep 2000
  Send, %CQValue%
  Sleep 2000
  Loop 3
  {
    Send, {Enter}
    Sleep 2000
  }
;--------------------------------------------------------------------
;Locating upload folder and then uploading
;--------------------------------------------------------------------      
  Loop 10
  {
     Send, {Tab}
    Sleep 2000
  }
  Send, {Enter}
  Sleep 2000
  Send, {Down}
  Sleep 2000
  Send, {Enter}
  Sleep 2000
  Send, !{d}
  Sleep 2000
  Send, C:\Bot Memory
  Sleep 2000
  Send, {Enter}
  Loop 4
  {
    Sleep 2000
    Send, {Tab}
  }
  Sleep 2000
  Send, {End}
  Sleep 2000
  Send, {Up}
  Sleep 2000
  Send, {Enter}
  Sleep 2000
  Send, ^{a}
  Sleep 2000
  Send, {Enter}
  Sleep 2000
  }
    Else 
  {
    Send, !{F4}{
  }
}
else
{
  Sleep 2000    
  Send, !{F4}
  Sleep 2000
  Send, !{F4}
  Sleep 2000
}
;--------------------------------------------------------------------
;Resets TT2 and closes the script
;Will switch back to discord when a seperate timer expires.
;--------------------------------------------------------------------  
Sleep 2000
WinActivate, ahk_exe BlueStacks.exe
Sleep 10000
MouseClick, Left, 790, 75, 75
Sleep 2000
MouseClick, Left, 790, 75, 75
Sleep 2000
ExitApp
F10::ExitApp

