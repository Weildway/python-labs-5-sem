import random

from node import Node


class Source:
    def __init__(self, data):
        self.data = data


class Encoder:
    def calculate_probability(self):
        symbols = dict()
        for element in self.input_data:
            if self.same_probability:
                symbols[element] = 1
            else:
                if symbols.get(element) is None:
                    symbols[element] = 1
                else:
                    symbols[element] += 1
        return symbols

    def encode_data(self, codes):
        encoded_output = ''
        for symbol in self.input_data:
            encoded_output += codes[symbol]
        return encoded_output

    def huffman_encoding(self):
        if self.blocks_method:
            n = 2
            self.input_data = [str(self.input_data[i:i + n]) for i in range(0, len(self.input_data), n)]
        symbol_probability_pair = self.calculate_probability()
        nodes = []

        # добавляем символы и их вероятности в качестве узлов древа Хаффмана
        for symbol, probability in symbol_probability_pair.items():
            nodes.append(Node(symbol, probability))

        while len(nodes) > 1:
            # сортируем узлы в порядке возрастания по их вероятностям
            nodes = sorted(nodes, key=lambda x: x.probability)

            # выбираем два наименьших узла
            right = nodes[0]
            left = nodes[1]

            left.code = 0
            right.code = 1

            # объединяем 2 узла в новый
            new_node = Node(left.symbol + right.symbol, left.probability + right.probability, left, right)

            nodes.remove(left)
            nodes.remove(right)
            nodes.append(new_node)

        huffman_codes = nodes[0].calculate_codes()
        encoded_output = self.encode_data(huffman_codes)
        return encoded_output, nodes[0]

    def __init__(self, data, blocks_method=False, same_probability=False):
        self.input_data = data
        self.blocks_method = blocks_method
        self.same_probability = same_probability
        self.encoded_data, self.root = self.huffman_encoding()


class TransferChannel:
    def __init__(self, data):
        self.data = data

    def make_noise(self, probability):
        noisy_data = ''
        for bit in self.data:
            if probability > random.randint(0, 100):
                bit = ('0' if bit == '1' else '1')
            noisy_data += bit
        self.data = noisy_data


class Decoder:
    def huffman_decoding(self):
        current_node = self.root
        decoded_output = ''
        for symbol in self.encoded_data:
            if symbol == '1':
                current_node = current_node.right
            elif symbol == '0':
                current_node = current_node.left
            try:
                if current_node.left.symbol is None and current_node.right.symbol is None:
                    pass
            except AttributeError:
                decoded_output += current_node.symbol
                current_node = self.root
        return decoded_output

    def __init__(self, data, root):
        self.encoded_data = data
        self.root = root
        self.decoded_data = self.huffman_decoding()


class Destination:
    def __init__(self, data):
        self.data = data
