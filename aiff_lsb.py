import aifc

def encode_message_in_aiff(input_aiff, output_aiff, message):
    song = aifc.open(input_aiff, 'rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    message = message + int((len(frame_bytes) - (len(message) * 8 * 8)) / 8) * '#'
    bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in message])))

    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit

    frame_modified = bytes(frame_bytes)

    with aifc.open(output_aiff, 'wb') as fd:
        fd.setparams(song.getparams())
        fd.writeframes(frame_modified)

    song.close()

def decode_message_from_aiff(input_aiff):
    song = aifc.open(input_aiff, 'rb')
    frame_bytes = bytearray(list(song.readframes(song.getnframes())))

    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
    decoded = string.split("###")[0]

    song.close()
    return decoded
