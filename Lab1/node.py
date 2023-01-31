codes = dict()


class Node:

    def calculate_codes(self, code=''):
        new_code = code + str(self.code)
        if self.left:
            self.left.calculate_codes(new_code)
        if self.right:
            self.right.calculate_codes(new_code)
        if not (self.left or self.right):
            codes[self.symbol] = new_code
        return codes

    def __init__(self, symbol, probability, left=None, right=None):
        self.symbol = symbol
        self.probability = probability
        self.left = left
        self.right = right
        self.code = ''
