import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def extract_audio_features(folder_path):
    """
    Extrai características acústicas de arquivos WAV dentro de uma pasta.
    """
    features = []
    wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".wav")]
    
    for file_path in wav_files:
        wav, sr = librosa.load(file_path, sr=16000)
        mfcc = librosa.feature.mfcc(y=wav, sr=sr, n_mfcc=13)
        mfcc_mean = np.mean(mfcc, axis=1)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=wav))
        spectral_contrast = np.mean(librosa.feature.spectral_contrast(S=np.abs(librosa.stft(wav)), sr=sr), axis=1)
        feature_vector = np.hstack([mfcc_mean, zcr, spectral_contrast])
        features.append(feature_vector)
    
    return np.array(features)

def plot_tsne(folders_dict, output_path):
    """
    Plota o t-SNE com os diferentes conjuntos de arquivos a partir de pastas.
    """
    all_features, labels = [], []
    label_map = {}
    label_counter = 0
    
    for label, folder in folders_dict.items():
        if os.path.isdir(folder):
            features = extract_audio_features(folder)
            if features.size > 0:
                all_features.append(features)
                labels += [label_counter] * len(features)
                label_map[label_counter] = label
                label_counter += 1
    
    if not all_features:
        print("Nenhum dado disponível para o t-SNE.")
        return
    
    all_features = np.vstack(all_features)
    tsne = TSNE(n_components=2, random_state=42)
    reduced_features = tsne.fit_transform(all_features)
    
    plt.figure(figsize=(10, 8))
    colors = ["blue", "green", "red", "purple", "orange"]
    for label, color in zip(label_map.keys(), colors):
        indices = [i for i, lbl in enumerate(labels) if lbl == label]
        plt.scatter(reduced_features[indices, 0], reduced_features[indices, 1], label=label_map[label], color=color, marker="o", edgecolor="k", alpha=0.6)
    
    plt.title("t-SNE Visualization of Audio Features")
    plt.xlabel("t-SNE Dimension 1")
    plt.ylabel("t-SNE Dimension 2")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Gráfico salvo em {output_path}")

if __name__ == "__main__":
    dataset_folders = {
        "Feminino 1": "C:/utfpr/tt-vae-gan/vctk1/spkr_1",
        "Masculino 1": "C:/utfpr/tt-vae-gan/vctk1/spkr_2",
        "Feminino 2": "C:/utfpr/tt-vae-gan/vctk1/spkr_4",
        "Masculino 2": "C:/utfpr/tt-vae-gan/vctk1/spkr_3",
    }
    # dataset_folders = {
    #     "Medieval Flutes": "C:/utfpr/tt-vae-gan/pablo/spkr_1",
    #     "Broken Oboe": "C:/utfpr/tt-vae-gan/pablo/spkr_2",
    #     "Dance Piano": "C:/utfpr/tt-vae-gan/pablo/spkr_3",
    #     "Recorder": "C:/utfpr/tt-vae-gan/pablo/spkr_4",
    # }
    output_path = "tsne_audio_features.png"
    plot_tsne(dataset_folders, output_path)
