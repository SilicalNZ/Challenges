;--------------------------------------------------------------------
;SilicalBot Reader Script
;--------------------------------------------------------------------
Sleep 10000
;--------------------------------------------------------------------
;Scanning
;--------------------------------------------------------------------
Loop
{
  MouseClick, Left, 388, 200
  Sleep 2000
  MouseClickDrag, Left, 388, 200, 930, 200, 50
  Sleep 2000
  Send, ^{c}
  Sleep 2000
  MouseClick, Left, 1000, 205
  Sleep 2000
  MouseClick, Left, 1000, 255
  Sleep 2000
  MouseClick, Left, 820, 460
;--------------------------------------------------------------------
;Runs OutputCQ Script
;--------------------------------------------------------------------
  if clipboard = OutputCQ
  {
    Loop 3
    {
;--------------------------------------------------------------------
;Sends activation message though discord
;--------------------------------------------------------------------
        Send, ``
        Sleep 100
     }
     Send, CQOutput is running
     Sleep 100
     Loop 3
    {
      Send, ``
      Sleep 100
    }
    Send, {Enter}        
    Sleep 2000
    Run  %A_AhkPath% "C:\Bots\OutputCQ.ahk"
    Sleep 600000
    WinActivate, ahk_exe Discord.exe
    Sleep 2000
    MouseClick, Left, 1000, 270
    Sleep 2000
    MouseClick, Left, 820, 460
  }
;--------------------------------------------------------------------
;SilicalBot Reader Script
;--------------------------------------------------------------------
  if clipboard = InputCQ
  {
    Run %A_AhkPath% "C:\Bots\InputCQ.ahk"    
    Sleep 300000
    WinActivate, ahk_exe Discord.exe
    Sleep 2000
    MouseClick, Left, 1000, 270
    Sleep 2000
    MouseClick, Left, 820, 460
  }
;--------------------------------------------------------------------
;SilicalBot Reader Script
;--------------------------------------------------------------------
  if clipboard = InputTimer
  {
    Run %A_AhkPath% "C:\Bots\InputTimer.ahk"
    Sleep 60000
    WinActivate, ahk_exe Discord.exe
    Sleep 2000
    MouseClick, Left, 1000, 270
    Sleep 2000
    MouseClick, Left, 820, 460
  }
;--------------------------------------------------------------------
;SilicalBot Reader Script
;--------------------------------------------------------------------
  if clipboard = InputDiscordAd
  {
    Run %A_AhkPath% "C:\Bots\InputDiscordAd.ahk"    
    Sleep 120000
    WinActivate, ahk_exe Discord.exe
    Sleep 2000
    MouseClick, Left, 1000, 270
    Sleep 2000
    MouseClick, Left, 820, 460
  }
;--------------------------------------------------------------------
;SilicalBot Reader Script
;--------------------------------------------------------------------
  if clipboard = InputRedditAd
  {
    Run %A_AhkPath% "C:\Bots\InputRedditAd.ahk"    
    Sleep 120000
    WinActivate, ahk_exe Discord.exe
    Sleep 2000
    MouseClick, Left, 1000, 270
    Sleep 2000
    MouseClick, Left, 820, 460
  }
  else
;--------------------------------------------------------------------
;SilicalBot Reader Script
;--------------------------------------------------------------------
  {
    Sleep 60000
  }
}
F10::ExitApp 
