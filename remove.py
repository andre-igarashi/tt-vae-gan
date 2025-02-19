import os
import random

def delete_excess_files(folder_path, max_files=350):
    # Lista todos os arquivos na pasta
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Verifica se o número de arquivos excede o limite
    if len(files) > max_files:
        excess_files = len(files) - max_files
        
        # Seleciona arquivos aleatórios para remoção
        files_to_delete = random.sample(files, excess_files)
        
        # Remove os arquivos selecionados
        for file in files_to_delete:
            os.remove(file)
            print(f"Deleted: {file}")
    else:
        print("No files need to be deleted.")

# Exemplo de uso
folder_path = "flickr/spkr_4"  # Substitua pelo caminho real
delete_excess_files(folder_path)

