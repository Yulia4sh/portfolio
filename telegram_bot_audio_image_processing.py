"""
Telegram bot functionality for handling audio and image processing:

1. Audio Processing:
   - For voice messages:
     a) Plot amplitude vs. time and frequency vs. amplitude after Fourier transform.
     b) Use AI to transcribe the message and return the text with word frequency statistics.
     c) Transform the frequency-amplitude pairs to time-amplitude pairs using inverse Fourier transform and return the altered audio.
     d) Apply custom audio processing (e.g., noise reduction, pitch alteration) and return the processed audio.

2. Image Processing:
   - For color images:
     a) Convert RGB vectors to their dual coordinate system components.
     b) Convert RGB vectors to a new coordinate system.
     c) Compute the vector product of each RGB vector with a constant vector.
     d) Apply custom image processing (e.g., rotation, resizing, blurring) and return the processed image.
"""


from vector import Vector
import sympy
from sympy import Matrix
from config import TOKEN_API
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ContentType
import librosa
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import os
import speech_recognition as sr
from PIL import Image
from scipy.fft import fft, fftfreq


class SkewCoordinateSystem:
    def __init__(self, e1, e2, e3=None):
        basis_vectors = [np.array(e1.coordinates, dtype=np.float64),
                         np.array(e2.coordinates, dtype=np.float64)]
        if e3 is not None:
            basis_vectors.append(np.array(e3.coordinates, dtype=np.float64))

        self.e1 = e1
        self.e2 = e2
        if e3 is not None:
            self.e3 = e3
        else:
            self.e3 = None

        self.basis_vectors = [self.e1, self.e2]
        if e3:
            self.basis_vectors.append(self.e3)

        self.dim = 2 if e3 is None else 3

        self.metric = self.compute_metric()

    def compute_metric(self):
        metric = Matrix([[v1.dot(v2) for v2 in self.basis_vectors] for v1 in self.basis_vectors])
        return metric

    def compute_dual_basis(self):
        try:
            metric_inv = self.metric.inv()
            self.dual_basis = [Vector(*metric_inv.row(i)) for i in range(self.dim)]
        except sympy.matrices.common.NonInvertibleMatrixError:
            self.dual_basis = [Vector(*self.metric.row(i)) for i in range(self.dim)]

    def display_vector(self, vector):
        components = vector.coordinates
        e_notations = [f"e_{i + 1}" for i in range(self.dim)]
        result_parts = []
        for i in range(self.dim):
            value = components[i]
            if value != 0:
                if value > 0:
                    if result_parts:
                        result_parts.append(f" + {value}{e_notations[i]}")
                    else:
                        result_parts.append(f"{value}{e_notations[i]}")
                else:
                    result_parts.append(f" - {abs(value)}{e_notations[i]}")
        return ''.join(result_parts)

    def display_projection(self, vector):
        projections = [vector.dot(dual) for dual in self.dual_basis]
        e_notations = [f"e^{i + 1}" for i in range(self.dim)]
        result_parts = []
        for i in range(self.dim):
            value = projections[i]
            if value != 0:
                if value > 0:
                    if result_parts:
                        result_parts.append(f" + {value}{e_notations[i]}")
                    else:
                        result_parts.append(f"{value}{e_notations[i]}")
                else:
                    result_parts.append(f" - {abs(value)}{e_notations[i]}")
        return ''.join(result_parts)

    def find_metric_tensors(self):
        return self.metric, self.metric.inv()

    def components_to_projections(self, vector):
        projections = [vector.dot(dual) for dual in self.dual_basis]
        return projections

    def projections_to_components(self, projections):
        components = sum(projection * dual for projection, dual in zip(projections, self.dual_basis))
        return Vector(components[0], components[1], components[2] if self.dim == 3 else None)

    def change_coordinates(self, other_system, old_vector):
        transformation_matrix = Matrix([[v1.dot(v2) for v2 in other_system.basis_vectors] for v1 in self.basis_vectors])
        new_components = transformation_matrix.inv() * Matrix(old_vector.coordinates)
        return Vector(*new_components)

    @staticmethod
    def scalar_product(vector1, vector2):
        return vector1.dot(vector2)

    def cross_product(self, vector1, vector2):
        if self.dim == 3:
            return vector1.cross(vector2)
        else:
            raise ValueError("Cross product is only defined for 3D space")


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)
HELP = """
/help -- the list of commands
/start -- start is start
"""


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(text="❤️ Uhu! We have started ❤️")


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(text=HELP)


@dp.message_handler(commands=['give'])
async def give_command(message: types.Message):
    await bot.send_sticker(message.from_user.id,
                           sticker="CAACAgIAAxkBAAEL_IlmKkIZtb216MLmkoavVBCs17vyOwACEwADwDZPE6qzh_d_OMqlNAQ")


@dp.message_handler()
async def echo(message: types.Message):
    print(message.text)
    await message.answer(text=message.text)
    await message.delete()


@dp.message_handler(content_types=ContentType.VOICE)
async def handle_voice(message: types.Message):
    file_id = message.voice.file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    await bot.download_file(file_path, 'voice.ogg')
    audio_path = 'voice.ogg'
    ogg_audio, sample_rate = sf.read(audio_path)
    sf.write('voice.wav', ogg_audio, sample_rate)
    data = librosa.load(audio_path)
    trumpet_sample = data[0]
    sampling_rate = data[1]
    duration = librosa.get_duration(filename=audio_path)
    time = np.arange(len(trumpet_sample)) / sampling_rate
    fig, ax = plt.subplots(2, 1, figsize=(11, 6))
    ax[0].set_title("Sound wave diagram", fontsize=16)
    ax[0].plot(time, trumpet_sample, c='b', linewidth=0.1)
    ax[0].set_xlim(0, duration)
    ax[0].set_ylabel("Sound amplitude")
    ax[0].set_xlabel("Time, s")
    ax[0].grid()
    size = trumpet_sample.size
    time = len(trumpet_sample) / sampling_rate
    dt = 1 / sampling_rate

    freq = fftfreq(size, dt)
    data_fft = fft(trumpet_sample)
    ax[1].plot(freq[:size // 2], np.abs(data_fft[:size // 2]), color='#d90368', linewidth=0.5)
    ax[1].set_xlabel("Frequency, Hz")
    ax[1].grid(color='#ce796b')
    ax[1].set_xlim([0, 6000])
    ax[1].set_ylim([0, 4100])
    fig.savefig('waveform_and_spectrum.png')
    plt.close()
    r = sr.Recognizer()
    with sr.AudioFile('voice.wav') as source:
        data = r.record(source)
    try:
        transcript = r.recognize_google(data, language="uk-UA")
        word_list = transcript.split()
        word_stats = {word: word_list.count(word) for word in set(word_list)}
    except sr.UnknownValueError:
        transcript = '-'
        word_stats = '-'
    with open('waveform_and_spectrum.png', 'rb') as photo:
        await message.reply_photo(photo, caption=f'{transcript}')
        await message.reply(text=f"Статистика по словах:{word_stats}")
    print(transcript)

    # г) -

    amplitudes = np.abs(data_fft)
    frequencies = np.fft.fftfreq(len(trumpet_sample), d=1 / sampling_rate)
    freq_amp_pairs = list(zip(frequencies, amplitudes))
    skew_coord = SkewCoordinateSystem(Vector(1, 0), Vector(1, 1))
    skew_coord.compute_dual_basis()
    projections_list = []
    for _, (frequency, amplitude) in enumerate(freq_amp_pairs):
        projections = skew_coord.components_to_projections(Vector(frequency, amplitude))
        projections_list.append(projections[0])

    data_ifft = np.fft.ifft(projections_list)
    data_ifft = np.real(data_ifft).astype(trumpet_sample.dtype)
    sf.write('output.wav', data_ifft, sampling_rate)
    with open('output.wav', 'rb') as audio:
        await message.reply_audio(audio, caption='складові векторів у дуальній системі')

    data, samplerate = sf.read('voice.wav')
    delay = 0.2
    decay = 0.4
    delay_samples = int(delay * samplerate)
    echo_data = np.zeros(len(data) + delay_samples)
    echo_data[:len(data)] += data
    echo_data[delay_samples:] += decay * data
    echo_data = echo_data / np.max(np.abs(echo_data))
    sf.write('echoed_voice.wav', echo_data, samplerate)
    music, sr_music = librosa.load('mystery_music.wav')
    voice, sr_voice = librosa.load("echoed_voice.wav")
    min_length = min(len(voice), len(music))
    voice = voice[:min_length]
    music = music[:min_length]
    mixed_audio = voice + music
    sf.write('mixed_audio.wav', mixed_audio, sr_voice)
    with open('mixed_audio.wav', 'rb') as audio:
        await message.reply_audio(audio, caption='на свій розсуд')

    os.remove('voice.ogg')
    os.remove('voice.wav')
    os.remove('waveform_and_spectrum.png')
    os.remove('mixed_audio.wav')
    os.remove("echoed_voice.wav")
    os.remove("output.wav")


@dp.message_handler(content_types=ContentType.PHOTO)
async def handle_photo(message: types.Message):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path
    await bot.download_file(file_path, 'photo.jpg')
    img = Image.open('photo.jpg')
    pixel_data = list(img.convert("RGBA").getdata())
    pixels_array = [(r, g, b, a) for r, g, b, a in pixel_data]

    pixels_array_new1 = []
    skew_coord = SkewCoordinateSystem(Vector(pixels_array[0][0], pixels_array[0][1], pixels_array[0][2]),
                                      Vector(pixels_array[0][0] + 3, pixels_array[0][1] + 2, pixels_array[0][2]),
                                      Vector(pixels_array[0][0] + 1, pixels_array[0][1], pixels_array[0][2] - 1))
    skew_coord.compute_dual_basis()
    for i in range(len(pixels_array)):
        projections = skew_coord.components_to_projections(Vector(pixels_array[i][0], pixels_array[i][1],
                                                                  pixels_array[i][2]))
        pixels_array_new1.append((int(projections[0]),
                                  int(projections[1]),
                                  int(projections[2]),
                                  int(pixels_array[i][3])))
    new_img1 = Image.new("RGBA", img.size)
    new_img1.putdata(pixels_array_new1)
    new_img1.save('modified_photo1.png')

    skew_coord = SkewCoordinateSystem(Vector(pixels_array[0][0], pixels_array[0][1], 1),
                                      Vector(pixels_array[0][0] + 3, pixels_array[0][1] + 2, 0),
                                      Vector(pixels_array[0][0] + 1, pixels_array[0][1], 0))
    skew_coord.compute_dual_basis()
    pixels_array_new2 = []
    for i in range(len(pixels_array)):
        original_vector = Vector(pixels_array[i][0], pixels_array[i][1], pixels_array[i][2])
        projections = skew_coord.components_to_projections(original_vector)
        pixels_array_new2.append((int(projections[0]), int(projections[1]), int(projections[2]),
                                  int(pixels_array[i][3])))
    new_img2 = Image.new("RGBA", img.size)
    new_img2.putdata(pixels_array_new2)
    new_img2.save('modified_photo2.png')

    pixels_array_new3 = []
    for i in range(len(pixels_array)):

        cross_prod = skew_coord.cross_product(Vector(pixels_array[i][0], pixels_array[i][1], pixels_array[i][2]),
                                              Vector(0, 1, 1))
        pixels_array_new3.append((int(cross_prod[0]),
                                  int(cross_prod[1]),
                                  int(cross_prod[2]),
                                  int(pixels_array[i][3])))
    new_img3 = Image.new("RGBA", img.size)
    new_img3.putdata(pixels_array_new3)
    new_img3.save('modified_photo3.png')

    pixels_array_new4 = []
    for i in range(len(pixels_array)):
        pixels_array_new4.append((min(int(pixels_array[i][0])+50, 255),
                                  min(int(pixels_array[i][1])+60, 255),
                                  min(int(pixels_array[i][2])+70, 255),
                                  min(int(pixels_array[i][3])+50, 255)))
    new_img4 = Image.new("RGBA", img.size)
    new_img4.putdata(pixels_array_new4[::-1])
    new_img4.save('modified_photo4.png')

    with open('modified_photo1.png', 'rb') as photo1, open('modified_photo2.png', 'rb') as photo2, \
            open('modified_photo3.png', 'rb') as photo3, open('modified_photo4.png', 'rb') as photo4:
        await message.reply_photo(photo1, caption='у дуальній системі')
        await message.reply_photo(photo2, caption='у новій косокутній системі')
        await message.reply_photo(photo3, caption='векторний добуток')
        await message.reply_photo(photo4, caption='на свій розсуд')
    os.remove('photo.jpg')
    os.remove('modified_photo1.png')
    os.remove('modified_photo2.png')
    os.remove('modified_photo3.png')
    os.remove('modified_photo4.png')


if __name__ == '__main__':
    executor.start_polling(dp)
