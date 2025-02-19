import os
import wave

def calcular_duracao_total(pasta):
    """
    Calcula a duração total de arquivos .wav em uma pasta.
    :param pasta: Caminho para a pasta contendo os arquivos .wav
    :return: Duração total em segundos
    """
    duracao_total = 0.0
    arquivos_wav = [f for f in os.listdir(pasta) if f.endswith('.wav')]

    for arquivo in arquivos_wav:
        caminho_arquivo = os.path.join(pasta, arquivo)
        try:
            with wave.open(caminho_arquivo, 'rb') as wav_file:
                # Número de frames e taxa de amostragem
                frames = wav_file.getnframes()
                framerate = wav_file.getframerate()
                duracao = frames / float(framerate)
                duracao_total += duracao
        except Exception as e:
            print(f"Erro ao processar {arquivo}: {e}")

    # Converter segundos para horas, minutos e segundos
    horas = int(duracao_total // 3600)
    minutos = int((duracao_total % 3600) // 60)
    segundos = int(duracao_total % 60)

    print(f"Duração total: {horas} horas, {minutos} minutos e {segundos} segundos")
    return duracao_total

# Exemplo de uso
pasta = "flickr\spkr_4"
calcular_duracao_total(pasta)
