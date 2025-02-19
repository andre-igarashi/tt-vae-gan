from tqdm import tqdm
import argparse
import shutil
import os

# Argumentos de entrada
parser = argparse.ArgumentParser()
parser.add_argument("--dataroot", type=str, required=True, help="Diretório raiz dos arquivos de áudio (.wav)")
parser.add_argument("--outdir", type=str, required=True, help="Diretório de saída para os arquivos organizados")
parser.add_argument("--patterns", type=str, nargs='+', required=True, help="Nomes das pastas principais (ex: guitarra1 guitarra2)")
args = parser.parse_args()

print("Parâmetros:")
print(f"  Diretório raiz: {args.dataroot}")
print(f"  Diretório de saída: {args.outdir}")
print(f"  Nomes das pastas (patterns): {args.patterns}")

# Função para buscar arquivos .wav dentro de pastas específicas
def get_audio_files_by_pattern(dataroot, patterns):
    matched_files = {}
    for pattern in patterns:
        folder_path = os.path.join(dataroot, pattern)
        if os.path.exists(folder_path):
            matched_files[pattern] = []
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.wav'):
                        relative_subfolder = os.path.relpath(root, folder_path)  # Pega o caminho relativo (subpasta)
                        matched_files[pattern].append((os.path.join(root, file), relative_subfolder))
        else:
            print(f"Aviso: Pasta '{pattern}' não encontrada em {dataroot}")
    return matched_files

# Copia arquivos rotulados para pastas separadas por pattern
def copy_files_with_subfolder_labels(outdir, files_by_pattern):
    for pattern, files in files_by_pattern.items():
        target_dir = os.path.join(outdir, pattern)
        os.makedirs(target_dir, exist_ok=True)

        for f, subfolder in tqdm(files, desc=f"Copiando arquivos de '{pattern}'"):
            base_name = os.path.basename(f)  # Nome original do arquivo
            subfolder_label = subfolder.replace(os.sep, "_") if subfolder != "." else ""  # Rótulo da subpasta
            labeled_name = f"{subfolder_label}_{base_name}" if subfolder_label else base_name  # Novo nome

            dest_path = os.path.join(target_dir, labeled_name)

            # Evita sobrescrita renomeando arquivos duplicados
            counter = 1
            while os.path.exists(dest_path):
                name, ext = os.path.splitext(labeled_name)
                dest_path = os.path.join(target_dir, f"{name}_{counter}{ext}")
                counter += 1

            shutil.copy(f, dest_path)
            print(f"Copiado: {f} -> {dest_path}")

# Executa as funções
all_files_by_pattern = get_audio_files_by_pattern(args.dataroot, args.patterns)
if not all_files_by_pattern:
    print("Nenhum arquivo encontrado nas pastas fornecidas.")
else:
    copy_files_with_subfolder_labels(args.outdir, all_files_by_pattern)
