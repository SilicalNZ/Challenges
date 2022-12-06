data ["(" + " ".join(i.split("\n")) + ")" for i in x.split("\n\n")]

⌈/+/¨data
+/{{⍵[3↑⍒⍵]}+/¨⍵}data
