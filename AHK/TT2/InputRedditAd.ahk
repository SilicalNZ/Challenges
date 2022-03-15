;--------------------------------------------------------------------
;InputRedditAd Script
;--------------------------------------------------------------------
Sleep 2000
;--------------------------------------------------------------------
;Imgur Phase
;--------------------------------------------------------------------
Run http://imgur.com/
Sleep 10000
Loop 2
{
  Send, {Tab}
  Sleep 100
}
Send, {Enter}
Sleep 100
Loop 4
{
  Send, {Tab}
}
;--------------------------------------------------------------------
;Nyctophilia's Poster
;--------------------------------------------------------------------
Send, https://goo.gl/9CBiQp
Sleep 100
Send, !{d}
Sleep 100
Send, ^{c}
;----------------------------
;Reddit Phase
;----------------------------
Run https://www.reddit.com/r/TapTitans2/submit
Sleep 2000
;--------------------------------------------------------------------
;Creating Post
;--------------------------------------------------------------------
Send, ^{g}
Sleep 100
Send, url
Sleep 100
Send, {Esc}
Sleep 100
Send, ^{Tab}
Sleep 100
Send, ^{v}
Sleep 100
Send, {Tab}
Sleep 100
Send, Apply for Top 20 clan - Tap Titan Universe (CQ 490+)
;--------------------------------------------------------------------
;Requires human to complete reCAPTCHA
;--------------------------------------------------------------------
Sleep 10000
;--------------------------------------------------------------------
;Completing Post
;--------------------------------------------------------------------
Loop 5
{
  Send, {Tab}
}
Send, {Enter}
Sleep 10000
;--------------------------------------------------------------------
;Comment Script
;--------------------------------------------------------------------
Send, ^{g}
Sleep 100
Send, best
Sleep 100
Send, {esc}
Sleep 100
Send, {Tab}
Sleep 100
Send, {Tab}
Sleep 100
;--------------------------------------------------------------------
;Writing Advertisement
;--------------------------------------------------------------------
Send, ---
Sleep 100
Send, {Enter}
Sleep 100
Send, ***Tap Titan Universe***
Sleep 100
Send, {Enter}
Sleep 100
Loop 2
{
  Send, ---
  Sleep 100
  Send, {Enter}
  Sleep 100
}
Send, > *Code:* **vg9e2**
Sleep 100
Send, {Enter}
Sleep 100
Send, > *Pass:* **?**
Sleep 100
Send, {Enter}
Sleep 100
Send, > *Level* **490+**
Sleep 100
Send, {Enter}
Sleep 100
Send, > *Dmg Bonus* **33.83aa`%**
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, ---
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, **Features**
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, - CQ Ranking System
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, - Fast Boss Kills
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, - Bots to help you improve your skills
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, - Great People to play and get motivated by
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, - Custom achievements
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, ---
Sleep 100
Loop 2
{
  Send, {Enter}
  Sleep 100
}
Send, [Join us!`](https://discord.gg/E7fxCPc)
Sleep 100
Send, {Enter}
Sleep 100
Send, ---
Sleep 100
;--------------------------------------------------------------------
;Posting Comment
;--------------------------------------------------------------------
Send, {Enter}
Sleep 100
Send, {Tab}
Sleep 100
Send, {Enter}
Sleep 100
Sleep 10000
Send, !{F4}
ExitApp
F10::ExitApp
