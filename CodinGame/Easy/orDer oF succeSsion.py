"""orDer oF succeSsion

    Goal
You have to output the order of succession to the British throne of a list of given people.
The order is simple:
From a descendant A, the next in the order is A’s first child B.
Then, the next one is B’s first child C if any and so on.
If C has no child, then the next one is B’s second child D.
Then D’s children if any. Then B’s third child E… then A’s second child F…

Let’s draw it with a tree:

      A1
    ┌─┴─┐
    B2  F6
 ┌──┼──┐
 C3 D4 E5


You see the order of succession: begin on the left of the tree, walk to the next level whenever possible otherwise continue to the right. Repeat until the whole tree is covered.
Thus, the order is A-B-C-D-E-F.

In fact, in siblings of the same person, the male descendants are ordered before the female descendants. For example, if the order of birth of the children (M for male, F for female) is Fa Ma Me Fe then the order of succession in these siblings is Ma Me Fa Fe.

Ordering rules
(a) in order of generation
(b) in order of gender
(c) in order of age (year of birth)

Outputting rules
(a) exclude dead people
(b) exclude people who are catholic (but include siblings of catholic people)

Note that this puzzle has been written in June, 2017 (some people might have died since this date).
"""
import sys
from pprint import pprint


class Family_Tree:
    family_tree = {}
    null_value = '-'
    track = []

    def _add_child(self, parent, new_child):
        children = self.family_tree[parent]['child']
        if children:
            children.append(new_child)
            info = []
            for i in children:
                j = self.family_tree[i]
                info.append((j['birth'], j['gender'], j['religion']))

            #                                                     age ->      sex
            Z = sorted(zip(info, children), key=lambda obj: (-ord(obj[0][1]), obj[0][0]))
            self.family_tree[parent]['child'] = [x for _, x in Z]
        else:
            self.family_tree[parent]['child'].append(new_child)

    def add(self, name: str, parent: str, birth: str, death: str, religion: str, gender: str):
        # int conversions
        birth = int(birth)
        if death != self.null_value:
            death = int(death)

        # Add person
        self.family_tree[name] = {'parent': parent,
                                  'child': [],
                                  'birth': birth,
                                  'death': death,
                                  'religion': religion,
                                  'gender': gender}

        # Add child to person
        if parent != self.null_value:
            self._add_child(parent, name)

    def _head_of_tree(self):
        for name, info in self.family_tree.items():
            if info['parent'] == self.null_value:
                return name

    def check(self, name):
        obj = self.family_tree[name]
        if (obj['death'] != '-'
            or obj['religion'] != 'Anglican'
        ):
            return False
        return True

    def hierarchy(self, _person=None):
        if _person is None:
            _person = self._head_of_tree()
        if self.check(_person):
            self.track.append(_person)

        if self.family_tree[_person]['child']:
            for child in self.family_tree[_person]['child']:
                self.hierarchy(child)
            return
        else:
            return


n = int(input())
this = Family_Tree()
for i in range(n):
    this.add(*input().split())
this.hierarchy()

[print(i) for i in this.track]