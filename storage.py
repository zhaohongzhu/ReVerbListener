import wave

audio_storage = bytearray()
tem_count = 0

def __init__():
    pass


def add_new_slice(slice:bytes):
    global audio_storage
    audio_storage += slice


def pick_slice_from_time(start:float, end:float):
    return audio_storage[get_cnt_from_time(start):get_cnt_from_time(end)]


def get_wav_from_time(start:float, end:float):
    global tem_count
    filename = "output_" + str(tem_count) + ".wav"
    output = wave.open(filename, 'wb')
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(16000)
    audio_slice = pick_slice_from_time(start, end)
    output.writeframes(audio_slice)
    tem_count += 1
    return filename


def get_wav_string_from_time(file_io, start:float, end:float):
    global tem_count
    output = wave.open(file_io, 'wb')
    output.setnchannels(1)
    output.setsampwidth(2)
    output.setframerate(16000)
    audio_slice = pick_slice_from_time(start, end)
    output.writeframes(audio_slice)
    tem_count += 1


def get_cnt_from_time(second:float) -> int:
    return int(second * 16000 * 2)