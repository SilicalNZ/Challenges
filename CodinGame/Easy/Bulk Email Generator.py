"""Bulk Email Generator

    Goal
You're coding on CG, minding your own business, when a notification pops out of nowhere. Some level 6 PHP coder is following you! It's all fine and dandy. You click on the dismiss button and move on.

Except it doesn't work. The dreaded red popup appears: “Error 492, please send us an email at coders@codingame.com”. Being the disciplined coder you are, you comply.

But the notification is still there. So you click it again. And read the popup again. And email coders again. But the notification is still there… You can't really send them the same email all the time, that would be boring!

It's time for some automation!

You are given a bulk email template. You are to expand it to an actual email by selecting a clause randomly when given a choice.

Choices are indicated by (parenthesized text), with clauses separated by pipe symbols |.

Random is defined as using the JBM level-0 twister: “for the ith choice, pick the ith clause (modulo the number of clauses)”.
"""
import sys


class Sentence_Randomizer(object):
    define_template = ['(', ')', '|']

    def __init__(self):
        self.JBM_level_0 = 0

        self.options = ''
        self.sentence = ''
        self.occurance = 0

        self.finish = False

    def _get_choice(self):
        discrim = self.define_template[2]
        options = self.options.split(discrim)
        x = self.JBM_level_0
        y = len(options)
        while y <= x:
            x -= y
        self.sentence += options[x]

        self.JBM_level_0 += 1
        self.options = ''

    def build(self, arg):
        """Creates a sentence obj

        If an option isn't able to be selected
        from the defined options withing the obj
        the next input is appended to the current
        with \n.
        """
        enclose, exclose, _ = self.define_template
        for i in arg:
            if i == enclose:
                self.finish = True
            elif i == exclose:
                self._get_choice()
                self.finish = False

            elif self.finish:
                self.options += i
            else:
                self.sentence += i
        if not self.finish:
            result = self.sentence
            self.sentence = ''
            print(result)
        else:
            self.options += '\n'

n = int(input())
this = Sentence_Randomizer()
for i in range(n):
    line = input()
    print('"' + line + '"', file=sys.stderr)
    this.build(line)
