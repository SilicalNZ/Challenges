data = """"""

print(sum(int(z[0] + z[-1]) for z in ([j for j in i if j.isdigit()] for i in data.split("\n"))))

numbers = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}

res = 0

for word in data.split("\n"):
    found = ""
    org_word = word

    while len(found) == 0:
        if word[0].isdigit():
            found += word[0]
            break
        
        for name, number in numbers.items():
            if word.startswith(name):
                found += number
                break
            
        word = word[1:]
    
    word = org_word    
    
    while len(found) == 1:
        if word[-1].isdigit():
            found += word[-1]
            break
        
        for name, number in numbers.items():
            if word.endswith(name):
                found += number
                break
            
        word = word[:-1]
    
    res += int(found)

print(res)
