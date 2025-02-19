import os
import wave
import contextlib

def get_wav_stats(folder_paths):
    results = []
    
    for folder_path in folder_paths:
        if not os.path.isdir(folder_path):
            print(f"Aviso: O caminho '{folder_path}' não é um diretório válido.")
            continue

        total_duration = 0.0
        file_count = 0
        
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            
            if file_name.endswith(".wav") and os.path.isfile(file_path):
                try:
                    with contextlib.closing(wave.open(file_path, 'r')) as f:
                        frames = f.getnframes()
                        rate = f.getframerate()
                        duration = frames / float(rate)
                        total_duration += duration
                        file_count += 1
                except Exception as e:
                    print(f"Erro ao processar {file_name}: {e}")
        
        avg_duration = total_duration / file_count if file_count > 0 else 0
        results.append({
            "Pasta": folder_path,
            "Número de Arquivos": file_count,
            "Duração Total (s)": round(total_duration, 2),
            "Duração Média (s)": round(avg_duration, 2)
        })
    
    return results

if __name__ == "__main__":
    # Substitua pelos caminhos das pastas desejadas
    paths = [
        "C:/utfpr/tt-vae-gan/vctk1/spkr_1",
        "C:/utfpr/tt-vae-gan/vctk1/spkr_2",
        "C:/utfpr/tt-vae-gan/vctk1/spkr_3",
        "C:/utfpr/tt-vae-gan/vctk1/spkr_4",
    ]
    
    stats = get_wav_stats(paths)
    for stat in stats:
        print(stat)
