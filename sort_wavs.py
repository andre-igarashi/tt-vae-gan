import os
import shutil

# Caminho do arquivo de mapeamento (wav2spk.txt)
map_file = "C:/utfpr/tt-vae-gan/wav2spk.txt"

# Caminho da pasta onde os arquivos .wav estão localizados (atualize conforme necessário)
base_folder = "C:/utfpr/tt-vae-gan/wavs"  # Substitua pelo caminho correto

# Definir os speakers a serem mapeados
speakers_to_map = {"2", "24", "57", "25"}

# Criar pastas para cada speaker, se não existirem
for speaker in speakers_to_map:
    speaker_folder = os.path.join(base_folder, f"spkr_{speaker}")
    os.makedirs(speaker_folder, exist_ok=True)

# Lista para armazenar arquivos movidos
moved_files = set()

# Processar o arquivo wav2spk.txt e mover os arquivos correspondentes
with open(map_file, "r") as f:
    for line in f:
        file_name, speaker = line.strip().rsplit(" ", 1)
        
        if speaker in speakers_to_map:
            source_path = os.path.join(base_folder, file_name)
            destination_folder = os.path.join(base_folder, f"spkr_{speaker}")
            destination_path = os.path.join(destination_folder, file_name)

            # Mover o arquivo se ele existir no diretório original
            if os.path.exists(source_path):
                shutil.move(source_path, destination_path)
                moved_files.add(file_name)
                print(f"Movido: {file_name} -> {destination_folder}")
            else:
                print(f"Arquivo não encontrado: {source_path}")

# Apagar os arquivos remanescentes na pasta de origem
for file_name in os.listdir(base_folder):
    file_path = os.path.join(base_folder, file_name)
    
    # Verifica se o item é um arquivo (não uma pasta) e não foi movido
    if os.path.isfile(file_path) and file_name.endswith(".wav") and file_name not in moved_files:
        os.remove(file_path)
        print(f"Arquivo deletado: {file_name}")

print("Organização concluída. Arquivos restantes na pasta de origem foram deletados.")
