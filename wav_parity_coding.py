import numpy as np
import scipy.io.wavfile as wav
import aifc

def message_to_bits(message):
    return ''.join(format(ord(char), '08b') for char in message)

def bits_to_message(bits):
    chars = [chr(int(bits[i:i + 8], 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def read_aiff(file_path):
    with aifc.open(file_path, 'r') as f:
        nframes = f.getnframes()
        audio = np.frombuffer(f.readframes(nframes), dtype=np.int16)
        rate = f.getframerate()
    return rate, audio

def write_aiff(file_path, rate, audio):
    with aifc.open(file_path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(rate)
        f.writeframes(audio.tobytes())

def read_pcm(file_path, rate=44100, channels=1, sampwidth=2):
    audio = np.fromfile(file_path, dtype=np.int16)
    if channels > 1:
        audio = audio.reshape(-1, channels)
    return rate, audio

def write_pcm(file_path, rate, audio):
    audio.tofile(file_path)

def parity_encode(file_path, message):
    if file_path.endswith('.wav'):
        rate, audio = wav.read(file_path)
    elif file_path.endswith('.aiff'):
        rate, audio = read_aiff(file_path)
    elif file_path.endswith('.pcm'):
        rate, audio = read_pcm(file_path)
    else:
        raise ValueError("Unsupported file format")

    if audio.ndim == 2:  # If stereo, take one channel
        audio = audio[:, 0]
    audio = audio.astype(np.int16)

    # Convert the secret message into a bitstream
    message = f"#{message}#"
    message_bits = message_to_bits(message)
    message_bits = [int(bit) for bit in message_bits]

    # Encode the secret message bits into the audio signal
    encoded_audio = audio.copy()
    for i, bit in enumerate(message_bits):
        block = encoded_audio[i*8:(i+1)*8]
        parity = np.sum(block) % 2
        if parity != bit:
            encoded_audio[i*8] ^= 1  # Flip the first bit to change the parity

    if file_path.endswith('.wav'):
        output_file = 'parity_encoded.wav'
        wav.write(output_file, rate, encoded_audio)
    elif file_path.endswith('.aiff'):
        output_file = 'parity_encoded.aiff'
        write_aiff(output_file, rate, encoded_audio)
    elif file_path.endswith('.pcm'):
        output_file = 'parity_encoded.pcm'
        write_pcm(output_file, rate, encoded_audio)
    else:
        raise ValueError("Unsupported file format")

    return output_file

def parity_decode(file_path):
    if file_path.endswith('.wav'):
        rate, audio = wav.read(file_path)
    elif file_path.endswith('.aiff'):
        rate, audio = read_aiff(file_path)
    elif file_path.endswith('.pcm'):
        rate, audio = read_pcm(file_path)
    else:
        raise ValueError("Unsupported file format")

    if audio.ndim == 2:  # If stereo, take one channel
        audio = audio[:, 0]
    audio = audio.astype(np.int16)

    # Decode the secret message bits from the audio signal
    message_bits = []
    for i in range(len(audio) // 8):
        block = audio[i*8:(i+1)*8]
        parity = np.sum(block) % 2
        message_bits.append(str(parity))

    message_bits = ''.join(message_bits)
    message = bits_to_message(message_bits)

    # Find the message within the delimiters
    if '#' in message:
        start = message.find('#') + 1
        end = message.find('#', start)
        if end != -1:
            return message[start:end]
        else:
            return "Message not properly terminated"
    else:
        return "Message not found"

