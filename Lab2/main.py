import elements


def count_transferred_symbols(encoded_data):
    print(f'Transferred {len(encoded_data)} binary symbols')


def count_0_and_1(encoded_data):
    print(f"Transferred {encoded_data.count('0')} '0' and {encoded_data.count('1')} '1'")


def count_average_coded_symbol_length(root):
    codes = root.calculate_codes()
    total_symbols = 0
    for value in codes.values():
        total_symbols += len(value)
    print(f'Average coded symbol length is {total_symbols / len(codes)}')


try:
    with open('input.txt', encoding='utf-8') as file:
        data = file.read()
except FileNotFoundError:
    print('File not found')
except:
    print('Error while working with file')
source = elements.Source(data)
encoder = elements.Encoder(source.data, blocks_method=False, same_probability=False)
encoded_output = encoder.encoded_data
root = encoder.root
try:
    with open('encoded.txt', 'w') as file:
        file.write(encoded_output)
except FileNotFoundError:
    print('File not found')
except:
    print('Error while working with file')
transfer_channel = elements.TransferChannel(encoded_output)
transfer_channel.make_noise(1.2)
decoder = elements.Decoder(transfer_channel.data, root)
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
count_average_coded_symbol_length(root)
print("Input and output are equal") if data == destination.data else print("Input and output are not equal")
