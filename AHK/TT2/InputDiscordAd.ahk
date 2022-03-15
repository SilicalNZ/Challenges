;--------------------------------------------------------------------
;InputDiscordAd Script
;--------------------------------------------------------------------
Sleep 2000
;--------------------------------------------------------------------
;Opening TT2 Server
;--------------------------------------------------------------------
MouseClick, Left, 40, 145
Sleep 4000
MouseClick, Left, 145, 310
Sleep 4000
;--------------------------------------------------------------------
;Writing advertisement
;--------------------------------------------------------------------
Send, https://goo.gl/9CBiQp
Sleep 100
Send, {Enter}
Sleep 100
Loop 3
{
  Send, ``
  Sleep 100
}
Send, md
Sleep 100
Send, {Enter}
Sleep 100
Send, <Name: TapTitanUniverse>
Sleep 100
Send, {Enter}
Sleep 100
Send, <Code:  vg9e2>
Sleep 100
Send, {Enter}
Sleep 100
Send, <Pass:  ?>
Sleep 100
Send, {Enter}
Sleep 100
Send, <Level: 481> May 1, 2017
Sleep 100
Send, {Enter}
Sleep 100
Send, [Dmg Bonus](17.08aa`%)
Sleep 100
Send, {Enter}
Sleep 100
Send, - CQ Ranking System
Sleep 100
Send, {Enter}
Sleep 100
Send, - Fast Boss Kills
Sleep 100
Send, {Enter}
Sleep 100
Send, - Bot to help you improve your skills
Sleep 100
Send, {Enter}
Sleep 100
Send, - Great People to play and get motivated
Sleep 100
Send, {Enter}
Sleep 100
Send, - Achievements by participation
Sleep 100
Send, {Enter}
Sleep 100
Loop 3
{
  Send, ``
  Sleep 100
}
Send, {Enter}
Sleep 1000
Send, https://discord.gg/E7fxCPc
Sleep 100
Send, ^{a}
Sleep 100
Send, ^{c}
Sleep 100
Send, {Enter}
Sleep 1000
;--------------------------------------------------------------------
;Finishing on TTU server
;--------------------------------------------------------------------
MouseClick, Left, 40, 260
Sleep 4000
ExitApp
F10::ExitApp
