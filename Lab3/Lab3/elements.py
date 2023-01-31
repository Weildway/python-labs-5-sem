import random
import math


class Source:
    def __init__(self, data):
        self.data = data


class Encoder:
    def calculate_datawords(self):
        unique_symbols = set(self.input_data)
        alphabet_length = len(unique_symbols)
        dataword_length = int(math.ceil(math.log2(alphabet_length)))
        dataword_dictionary = {}
        i = 0
        for symbol in unique_symbols:
            dataword_dictionary[symbol] = bin(i)[2::].zfill(dataword_length)
            i += 1
        return dataword_dictionary

    @staticmethod
    def calculate_redundant_bits(k):
        # 2 ^ r >= k + r + 1
        # k - информационные биты
        # r - проверочные биты
        for r in range(k):
            if 2 ** r >= k + r + 1:
                return r

    @staticmethod
    def set_redundant_bits(dataword, r):
        # Проверочные биты ставятся на места соответствующие степеням 2
        power = 0
        data_bit = 1
        k = len(dataword)
        codeword = [] * (k + r)

        # Если позиция это степень 2, то ставим 0, иначе вставляем бит исходного сообщения
        for bit in range(1, k + r + 1):
            if bit == 2 ** power:
                codeword.append(0)
                power += 1
            else:
                codeword.append(int(dataword[-1 * data_bit]))
                data_bit += 1

        # Реверсируем результат, так как проверочные биты отсчитывались справа налево
        return codeword[::-1]

    @staticmethod
    def calculate_parity_bits(codeword, r):
        n = len(codeword)
        for parity_bit_number in range(r):
            value = 0
            for bit in range(1, n + 1):
                if bit & (2 ** parity_bit_number) == (2 ** parity_bit_number):
                    value ^= codeword[-1 * bit]
            codeword[-(2 ** parity_bit_number)] = value
        return codeword

    def encode_data(self):
        dataword_dictionary = self.calculate_datawords()
        random_dataword = dataword_dictionary[self.input_data[0]]
        k = len(random_dataword)
        r = self.calculate_redundant_bits(k)
        encoded_output = ''
        codeword_dictionary = {}
        for symbol in self.input_data:
            dataword = dataword_dictionary[symbol]
            codeword = self.set_redundant_bits(dataword, r)
            codeword = self.calculate_parity_bits(codeword, r)
            string_codeword = ''.join(str(bit) for bit in codeword)
            codeword_dictionary[string_codeword] = symbol
            encoded_output += string_codeword
        self.codeword_dictionary = codeword_dictionary
        self.k = k
        self.r = r
        return encoded_output

    def __init__(self, data):
        self.input_data = data
        self.encoded_data = self.encode_data()


class TransferChannel:
    def __init__(self, data):
        self.data = data

    def make_noise(self, probability):
        noisy_data = ''
        for bit in self.data:
            if probability >= random.randint(1, 100):
                bit = '0' if bit == '1' else '1'
            noisy_data += bit
        self.data = noisy_data


class Decoder:

    @staticmethod
    def detect_error(codeword, r):
        n = len(codeword)
        erroneous_bit_number = ''
        for parity_bit_number in range(r):
            value = 0
            for bit in range(1, n + 1):
                if bit & (2 ** parity_bit_number) == (2 ** parity_bit_number):
                    value ^= int(codeword[-1 * bit])
            erroneous_bit_number = str(value) + erroneous_bit_number
        return int(erroneous_bit_number, 2)

    @staticmethod
    def correct_error(codeword, erroneous_bit_number):
        n = len(codeword)
        position = n - erroneous_bit_number
        codeword = list(codeword)
        codeword[position] = '1' if codeword[position] == '0' else '0'
        return ''.join(str(bit) for bit in codeword)

    def decode_data(self):
        n = self.k + self.r
        i = 0
        decoded_output = ''
        while i < len(self.encoded_data):
            codeword = self.encoded_data[i:i + n]
            erroneous_bit_number = self.detect_error(codeword, self.r)
            correct_codeword = self.correct_error(codeword, erroneous_bit_number) if erroneous_bit_number else codeword
            try:
                decoded_output += self.codeword_dictionary[correct_codeword]
            except KeyError:
                decoded_output += ' '
                # decoded_output += random.choice(list(self.codeword_dictionary.values()))
            i += n
        return decoded_output

    def __init__(self, data, k, r, codeword_dictionary):
        self.encoded_data = data
        self.k = k
        self.r = r
        self.codeword_dictionary = codeword_dictionary
        self.decoded_data = self.decode_data()


class Destination:
    def __init__(self, data):
        self.data = data
