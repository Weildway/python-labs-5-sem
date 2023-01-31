import elements


def count_transferred_symbols(encoded_data):
    print(f'Transferred {len(encoded_data)} binary characters')


def count_0_and_1(encoded_data):
    print(f"Transferred {encoded_data.count('0')} zeroes and {encoded_data.count('1')} ones")


def cmp(input, output):
    right = 0
    for i in range(len(output)):
        try:
            if input[i] == output[i]:
                right += 1
        except:
            pass
    return right / len(input) * 100


try:
    with open('input.txt', encoding='utf-8') as file:
        data = file.read()
except FileNotFoundError:
    print('File not found')
except:
    print('Error while working with file')
source = elements.Source(data)
encoder = elements.Encoder(source.data)
encoded_output = encoder.encoded_data
codeword_dictionary = encoder.codeword_dictionary
k = encoder.k
r = encoder.r
try:
    with open('encoded.txt', 'w') as file:
        file.write(encoded_output)
except FileNotFoundError:
    print('File not found')
except:
    print('Error while working with file')
transfer_channel = elements.TransferChannel(encoded_output)
p = int(input('Input probability of mistake: '))
transfer_channel.make_noise(p)
decoder = elements.Decoder(transfer_channel.data, k, r, codeword_dictionary)
destination = elements.Destination(decoder.decoded_data)
try:
    with open('output.txt', 'w', encoding='utf-8') as file:
        file.write(destination.data)
except FileNotFoundError:
    print('File not found')
except:
    print('Error while working with file')
count_transferred_symbols(encoded_output)
count_0_and_1(encoded_output)
print(f'Number of data bits is {k}')
print(f'Number of redundant bits is {r}')
print(f'Codeword length is {k+r}')
print("Input and output are equal") if data == destination.data else print("Input and output are not equal")
print(f'Match percentage is {cmp(source.data, destination.data)}')
