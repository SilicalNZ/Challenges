;--------------------------------------------------------------------
;InputTimer Script
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
MouseClick, Left, 501, 654
Sleep 2000
;--------------------------------------------------------------------
;Capturing Timer through OCR
;--------------------------------------------------------------------
Send, {LWin down}
Sleep 100
Send, {q}
Sleep 100
Send, {LWin up}
Sleep 2000
MouseClick, Left, 577, 673
Sleep 2000
Loop 2
{
  Send, +{Right}
  Sleep 200
}
Send, ^{c}
;--------------------------------------------------------------------
;Storing two variables and taking 2 “minutes” away from original
;--------------------------------------------------------------------
Sleep 200
Timer1 := clipboard
Loop 2
{
 Send, {Right}
 Sleep 200
}
Loop 2
{
 Send, +{Right}
 Sleep 200
}
Send, ^{c}
Sleep 200
Send, {Esc}
Sleep 200
if clipboard >= 2
{
  Timer2 := (clipboard - 2)
}
if clipboard = 01
{
  Timer2 := 59
  Timer1 := (Timer1 - 1)
}
if clipboard = 00
{
  Timer2 := 58
  Timer1 := (Timer1 - 1)
}
;--------------------------------------------------------------------
;Communicating with BrainXBot
;--------------------------------------------------------------------
WinActivate, ahk_exe Discord.exe
Sleep 2000
Send, Cq{!}add %Timer1%:%Timer2%:00
Sleep 200
Send, {Enter}
Sleep 200
Loop 2
{
  MouseClick, Left, 1000, 205
  Sleep 2000
  MouseClick, Left, 1000, 275
  Sleep 2000
  MouseClick, Left, 820, 460
  Sleep 2000
}
ExitApp
F10::ExitApp
