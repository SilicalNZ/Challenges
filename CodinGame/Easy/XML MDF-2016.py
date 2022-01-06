"""XML MDF-2016

    Goal
In this challenge, a data format that is a simplified version of XML is used. Tags are identified by a lowercase letter. A start tag is represented by that single letter, and the closing tag is represented by the - character, followed by that letter.

For example, the string "ab-bcd-d-c-ae-e" is the equivalent of <a> <b> </ b> <c> <d> </ d> </ c> </a> <e> </ e> in XML. The supplied string will always be properly formed.

Now we define the depth of a tag as 1 + the number of tags in which it is nested.

In the previous example:
a and e have a depth of 1,
b and c have a depth of 2
and d has a depth of 3.


The weight of a tag name is defined as the sum of the reciprocals of the depths of each of its occurrences.

For example, in the chain a-abab-b-a-b, there are:
- Two tags a with depths of 1 and 2
- Two tags b with depths of 1 and 3.

thus the weight of a is (1/1) + (1/2) = 1.5 and the weight of b is (1/1) + (1/3) = 1.33.

In this challenge you must determine the letter of the tag with the greatest weight in the string argument.
"""
import sys


class XMLNestedStructure(object):
    def __init__(self, sequence):
        self.sequence = sequence
        obj = self.sequence_split(self.sequence)
        obj = self.execute(obj)
        print(self.get_max(obj)[0])

    def sequence_split(self, arg):
        arg = '|' + arg
        return [i[1:] for i in arg.split('-') if i[1:]]

    def execute(self, arg):
        weights = {}
        for nest in arg:
            for x, position in enumerate(nest, 1):
                if position not in weights:
                    weights[position] = 0
                weights[position] += 1/x
        result = sorted(weights.items(), key=lambda x: x[1])
        result = {i: j for i, j in result}
        return result

    def get_max(self, arg):
        result = ('1', 0)
        for character, weight in arg.keys():
            if round(weight, 1) > round(result[1], 1):
                result = (character, weight)
        return result


XMLNestedStructure(input())
