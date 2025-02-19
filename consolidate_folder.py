import os
import shutil

def merge_datasets(input_dirs, output_dir):
    """
    Combina múltiplos diretórios em um único diretório, garantindo que não haja sobrescrita
    ao renomear arquivos duplicados automaticamente.

    Args:
        input_dirs (list): Lista de diretórios de entrada.
        output_dir (str): Diretório consolidado onde os arquivos serão salvos.
    """
    os.makedirs(output_dir, exist_ok=True)
    saved_files = set()

    for input_dir in input_dirs:
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith('.wav'):  # Apenas arquivos PNG
                    base_name = os.path.splitext(file)[0]
                    output_file = os.path.join(output_dir, f"{base_name}.wav")
                    counter = 1

                    # Garante que não haverá sobrescrita
                    while output_file in saved_files or os.path.exists(output_file):
                        output_file = os.path.join(output_dir, f"{base_name}_{counter}.wav")
                        counter += 1

                    # Copia o arquivo para o diretório consolidado
                    source = os.path.join(root, file)
                    shutil.copy(source, output_file)
                    saved_files.add(output_file)

                    print(f"Copiado: {source} -> {output_file}")

# Diretórios de entrada e saída
input_dirs = ["C:/utfpr/tt-vae-gan/output2/Bridge", "C:/utfpr/tt-vae-gan/output2/Bridge-Middle", "C:/utfpr/tt-vae-gan/output2/Middle", "C:/utfpr/tt-vae-gan/output2/Middle-Neck", "C:/utfpr/tt-vae-gan/output2/Neck"]  # Substitua pelos caminhos reais
output_directory = "C:/utfpr/tt-vae-gan/output2-flat"  # Diretório de saída

# Realiza o merge dos datasets
merge_datasets(input_dirs, output_directory)
