import os

# Caminho para a pasta com os arquivos
folder_path = "C:/utfpr/tt-vae-gan/vctk1/wav48_silence_trimmed - álbum desconhecido"

# Itera sobre todos os arquivos na pasta
for filename in os.listdir(folder_path):
    if filename.endswith(".wav"):  # Filtra apenas os arquivos .wav
        # Divide o nome do arquivo em partes e monta o novo nome
        parts = filename.split(" - ")
        if len(parts) > 1:
            details = parts[-1].replace(".wav", "").split()  # Remove .wav antes de dividir
            new_name = f"{details[0]}_{details[1]}_{details[2]}.wav"  # Formata o novo nome

            # Caminhos completos para o arquivo original e renomeado
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)

            # Renomeia o arquivo
            os.rename(old_path, new_path)
            print(f"Renomeado: {filename} -> {new_name}")

print("Renomeação concluída!")
