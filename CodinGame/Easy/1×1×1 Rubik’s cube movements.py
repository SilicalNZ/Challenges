"""1×1×1 Rubik’s cube movements

    Goal
A 2×2×2 Rubik's cube is quite complicated. In this puzzle, we will focus on the mono-cube, the 1×1×1 Rubik's cube!

You are given a set of rotations and two faces. Apply the rotations to the cube and locate the two faces after the rotations.

Face notation
F (Front): the side currently facing the observer
B (Back): the side opposite the front
U (Up): the side above or on top of the front side
D (Down): the side opposite the top, underneath the cube
L (Left): the side directly to the left of the front
R (Right): the side directly to the right of the front

Rotation notation
A rotation without the prime symbol ' is a quarter turn clockwise.
A rotation with the prime symbol ' is a quarter turn counter-clockwise.
x, x': rotate cube on R (R and L still face the same directions after rotation)
y, y': rotate cube on U (U and D still face the same directions after rotation)
z, z': rotate cube on F (F and B still face the same directions after rotation)

Example 1
z
D
L
Means: rotate cube clockwise on F and identify the new directions of D and L.
Answer: Output L in line 1 because the initial down face now faces left. Output U in line 2 because the initial left face now faces up.

Example 2
z z'
U
R
Means: rotate cube clockwise on F then counter-clockwise on F, and identify the new directions of U and R.
Answer: Output U in line 1 and R in line 2 because both faces do not change directions after the rotations.
"""
import sys


DISTANCE = 2
REVERSED = '\''


def list_wrap_around(lst: list, x):
    return lst[x + 1:] + lst[:x]


class Cube1x1x1:
    _cube_template = ['F', 'U', 'R', 'B', 'D', 'L']
    # order is important
    _cube_faces = {'x': ('R', 'L'), 'y': ('U', 'D'), 'z': ('F', 'B')}

    def __init__(self):
        self.cube = self._cube_template[:]

        self.map = {}
        self._pair()

    def rotate(self, axis, reverse=False):
        f"""Rotates cube on axis

        :param axis: {list(self._cube_faces)}
        :param reverse:
        :return:
        """
        if axis in self._cube_faces:
            faces = list(self._cube_faces)
            x, y = list_wrap_around(faces, faces.index(axis))

            face1, face2 = self._cube_faces[x], self._cube_faces[y]

            obj = ''.join(self.cube)
            obj = obj\
                .replace(face2[0], f"{face1[0]}.") \
                .replace(face2[1], f"{face1[1]}.") \
                .replace(face1[0], f"{face2[0]}.") \
                .replace(face1[1], f"{face2[1]}.") \
                .replace('.', '')
            self.cube = list(obj)

            self._pair()

    def _pair(self):
        self.map = {a: b for a, b in zip(self._cube_template, self.cube)}

    def show(self, face):
        return self.map[face]


this = Cube1x1x1()
print(this.cube, file=sys.stderr)

rotations = input().split()
print(rotations, file=sys.stderr)
for i in rotations:
    if REVERSED in i:
        this.rotate(i[0], reverse=True)
    else:
        this.rotate(i)
    print(this.cube, file=sys.stderr)



for _ in range(2):
    direction = input()
    print(direction, file=sys.stderr)
    print(this.show(direction))




