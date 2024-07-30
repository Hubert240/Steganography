import wave
import aiff_lsb
import pcm_lsb
def encode_audio(file_path, secret_message):
    if file_path.endswith('.wav'):
        song = wave.open(file_path, mode='rb')
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))

        secret_message = secret_message + int((len(frame_bytes) - (len(secret_message) * 8 * 8)) / 8) * '#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in secret_message])))

        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit

        frame_modified = bytes(frame_bytes)

        output_file = "song_embedded.wav"
        with wave.open(output_file, 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)

        song.close()
    elif file_path.endswith('.aiff'):
        output_file = "song_embedded.aiff"
        aiff_lsb.encode_message_in_aiff(file_path, output_file, secret_message)
    elif file_path.endswith('.pcm'):
        output_file = "output_embedded.pcm"
        pcm_lsb.encode_message_in_pcm(file_path, output_file, secret_message)
    else:
        raise ValueError("Unsupported file format")

    return output_file

def decode_audio(file_path):
    if file_path.endswith('.wav'):
        song = wave.open(file_path, mode='rb')
        frame_bytes = bytearray(list(song.readframes(song.getnframes())))

        extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
        decoded = string.split("###")[0]

        song.close()
    elif file_path.endswith('.aiff'):
        decoded = aiff_lsb.decode_message_from_aiff(file_path)
    elif file_path.endswith('.pcm'):
        decoded = pcm_lsb.decode_message_from_pcm(file_path)
    else:
        raise ValueError("Unsupported file format")

    return decoded
