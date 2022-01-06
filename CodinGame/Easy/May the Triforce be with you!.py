"""May the Triforce be with you!

    Goal
Link has been sent to the Secret Realm to find the Triforce and save Hyrule. But the vile Ganondorf followed Link into the Temple of Time, trapped him, and took the Triforce for himself.

The Temple of Time has been closed for a thousand years now, but the Sages finally found you, one of the greatest Nerds ever born, and they need your help to open the Temple of Time's door and join Link in the ultimate battle!

The Temple of Time's surface contains several incrusted Triforces of different sizes, and the Sages believe that by creating Triforces of the corresponding sizes, the door will open. Even though no magic has worked until now, your programming skills will surely make the difference.

The program:

You must create a program that echoes a Triforce of a given size N.

- A triforce is made of 3 identical triangles
- A triangle of size N should be made of N lines
- A triangle's line starts from 1 star, and earns 2 stars each line
- Take care, a . must be located at the top/left to avoid automatic trimming

For example, a Triforce of size 3 will look like:


.    *
    ***
   *****
  *     *
 ***   ***
***** *****


Another example, a Triforce of size 5 will look like:


.        *
        ***
       *****
      *******
     *********
    *         *
   ***       ***
  *****     *****
 *******   *******
********* *********


Don't forget: you're Hyrule's only hope!
Good luck!
"""
class TriForce(object):
    def __init__(self, x, char1='*', char2=' '):
        self.x = x
        self.char1 = char1
        self.char2 = char2

    def execute(self):
        obj = self.build_triangle(self.x, self.char1)
        obj = self.duplicate_triangle(2, obj)
        return obj

    def _generic_calc(self, x):
        return x * 2 + 1

    def _center_string(self, length, *args):
        result = []
        for arg in args:
            if len(arg) == length:
                result.append(arg)
            else:
                blanks = self.char2 * int((length - len(arg)) / 2)
                result.append(blanks + arg + blanks)
        return result

    def build_triangle(self, size, char):
        result = [char * self._generic_calc(i) for i in range(size)]
        return self._center_string(len(max(result, key=len)), *result)

    def duplicate_triangle(self, size, triangle: list):
        triangle_length = len(max(triangle, key=len))
        full_length = size * triangle_length + size - 1
        plus_one = [i + self.char2 for i in triangle]

        result = []
        for i in range(size):
            for x, line in enumerate(triangle):
                line = plus_one[x] * i + line
                result.append(''.join(self._center_string(full_length, line)))
        return result


def show_for_challenge(args, char):
    for x, i in enumerate(args[:-1]):
        i = i.replace(' ', '.', 1)
        i = i.strip()
        if x != 0:
            i = i.replace('.', ' ', 1)
        args[x] = i

    for i in args:
        print(i)


this = (TriForce(int(input()), '*').execute())
show_for_challenge(this, '*')
