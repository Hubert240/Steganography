def encode_message_in_pcm(input_pcm, output_pcm, message):
    with open(input_pcm, 'rb') as pcm_file:
        pcm_data = bytearray(pcm_file.read())

    message = message + int((len(pcm_data) - (len(message) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))

    for i, bit in enumerate(bits):
        pcm_data[i] = (pcm_data[i] & 254) | bit

    with open(output_pcm, 'wb') as pcm_file:
        pcm_file.write(pcm_data)

def decode_message_from_pcm(input_pcm):
    with open(input_pcm, 'rb') as pcm_file:
        pcm_data = bytearray(pcm_file.read())

    extracted = [pcm_data[i] & 1 for i in range(len(pcm_data))]
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    decoded = string.split("###")[0]

    return decoded
