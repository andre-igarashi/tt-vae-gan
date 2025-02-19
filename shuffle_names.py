import os
import random

def shuffle_existing_file_names(directory):
    # Coleta todos os arquivos na pasta
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    # Embaralhar a lista de arquivos
    shuffled_files = files.copy()
    random.shuffle(shuffled_files)
    
    # Renomear os arquivos trocando os nomes entre eles
    temp_names = []
    for i, file in enumerate(files):
        temp_name = f'temp_{i}.tmp'
        os.rename(os.path.join(directory, file), os.path.join(directory, temp_name))
        temp_names.append(temp_name)

    for temp_name, shuffled_name in zip(temp_names, shuffled_files):
        original_ext = os.path.splitext(shuffled_name)[1]
        new_name = shuffled_name
        os.rename(os.path.join(directory, temp_name), os.path.join(directory, new_name))
        print(f'Renamed: {temp_name} -> {new_name}')

# Exemplo de uso
directory = 'C:/utfpr/tt-vae-gan/vctk3/spkr_2'  # Altere para o caminho correto
shuffle_existing_file_names(directory)
