import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def extract_mel_spectrogram(input_dir, output_dir, sr=22050, n_mels=128, fmax=8000):
    """
    Converte arquivos .wav em imagens de mel-espectrogramas salvas como .png, incluindo arquivos em subdiretórios.

    Args:
        input_dir (str): Caminho para o diretório contendo os arquivos .wav.
        output_dir (str): Caminho para o diretório onde as imagens .png serão salvas.
        sr (int): Taxa de amostragem para carregar os arquivos de áudio.
        n_mels (int): Número de bandas de frequências mel.
        fmax (int): Frequência máxima para o espectrograma.
    """
    # Cria o diretório de saída, se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Percorre recursivamente os arquivos .wav
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.wav'):
                try:
                    # Caminho completo para o arquivo .wav
                    wav_path = os.path.join(root, file)

                    # Carregar o áudio
                    y, _ = librosa.load(wav_path, sr=sr)

                    # Gerar o mel-espectrograma
                    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, fmax=fmax)
                    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

                    # Caminho de saída mantendo a estrutura de pastas
                    relative_path = os.path.relpath(root, input_dir)
                    output_subdir = os.path.join(output_dir, relative_path)
                    os.makedirs(output_subdir, exist_ok=True)

                    # Criar a figura do espectrograma
                    plt.figure(figsize=(10, 4))
                    librosa.display.specshow(mel_spectrogram_db, sr=sr, x_axis='time', y_axis='mel', fmax=fmax, cmap='viridis')
                    plt.axis('off')

                    # Salvar como .png
                    output_file = os.path.join(output_subdir, os.path.splitext(file)[0] + '.png')
                    plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
                    plt.close()

                    print(f"Convertido: {wav_path} -> {output_file}")

                except Exception as e:
                    print(f"Erro ao processar {wav_path}: {e}")

# Configurações
input_directory = "C:/utfpr/tt-vae-gan/rave"  # Substitua pelo caminho do seu diretório de arquivos .wav
output_directory = "C:/utfpr/tt-vae-gan/rave"  # Substitua pelo caminho para salvar os .png

# Converter .wav para .png
extract_mel_spectrogram(input_directory, output_directory)
