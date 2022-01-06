"""bank Robbers

    Goal
A gang of R foolish robbers decides to heist a bank. In the bank there are V vaults (indexed from 0 to V - 1). The robbers have managed to extract some information from the bank's director:
- The combination of a vault is composed of C characters (digits/vowels).
- The first N characters consist of digits from 0 to 9.
- The remaining characters consist of vowels (A, E, I, O, U).
- C and N may be the same or different for different vaults.

All the robbers work on the vaults at the same time. A robber can work on one vault at a time, and a vault can be worked on by only one robber. A robber tries the combinations at the speed of 1 second per combination. He tries all the possible combinations, i.e. he continues to try the untried combinations even after he has found the correct combination. Once he finishes one vault, he moves on to the next vault of greater index (robbers work the vaults in increasing order) which nobody has worked on yet, if any. The heist is finished when the robbers have worked on all the vaults.

Assume it takes no time to move from one vault to another.

You have to output the total time the heist takes.
"""
import sys


class Bank_Robbers(object):
    vaults = []
    digits = [i for i in range(10)]
    vowels = ['A', 'E', 'I', 'O', 'U']

    time_taken = 0

    def __init__(self, r):
        print("Robbers:", r, file=sys.stderr)
        self.robbers = [0 for i in range(r)]

    def record_vaults(self, c, n):
        self.vaults.append(len(self.digits)**n * len(self.vowels)**(c-n))

    def give_vault(self):
        try:
            return self.vaults.pop(0)
        except IndexError:
            return 0

    def subtract_time(self):
        x = min(self.robbers)
        self.time_taken += x
        temp = []
        for i in self.robbers:
            new_time = i - x
            if new_time:
                temp.append(new_time)
            else:
                temp.append(self.give_vault())
        self.robbers = temp


this = Bank_Robbers(int(input()))

v = int(input())
vaults = []
for i in range(v):
    this.record_vaults(*[int(j) for j in input().split()])
print('Vaults:', this.vaults, file=sys.stderr)

while this.vaults:
    this.subtract_time()
    print('Time:', this.time_taken, file=sys.stderr)
    print('Activity:', this.robbers, file=sys.stderr)

print(this.time_taken + max(this.robbers))
