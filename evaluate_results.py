import os
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist
import json

def evaluate_dimensionality_reduction(features, labels):
    """
    Avalia os resultados de redução de dimensionalidade.
    
    Args:
        features (numpy.ndarray): Matriz 2D das features reduzidas ([n_amostras, n_dimensões]).
        labels (numpy.ndarray): Rótulos das amostras ([n_amostras]).
    
    Returns:
        dict: Métricas de avaliação (silhouette_score, intracluster_distance, intercluster_distance).
    """
    metrics = {}

    # Silhouette Score
    metrics["silhouette_score"] = silhouette_score(features, labels)

    # Distâncias intracluster
    unique_labels = np.unique(labels)
    intracluster_distances = []
    intercluster_distances = []

    for label in unique_labels:
        cluster_points = features[labels == label]
        if len(cluster_points) > 1:
            intracluster_distances.append(
                np.mean(cdist(cluster_points, cluster_points))
            )

    metrics["intracluster_distance"] = np.mean(intracluster_distances) if intracluster_distances else float('inf')

    # Distâncias intercluster
    for i, label_i in enumerate(unique_labels):
        for j, label_j in enumerate(unique_labels):
            if i < j:
                points_i = features[labels == label_i]
                points_j = features[labels == label_j]
                intercluster_distances.append(
                    np.mean(cdist(points_i, points_j))
                )

    metrics["intercluster_distance"] = np.mean(intercluster_distances) if intercluster_distances else 0

    return metrics

def evaluate_all_epochs(results_dir):
    """
    Avalia os resultados de t-SNE e PCA para todas as épocas.

    Args:
        results_dir (str): Caminho para o diretório com os resultados.

    Returns:
        dict: Métricas para todas as épocas (t-SNE e PCA).
    """
    all_metrics = {}

    # Percorre cada diretório de época
    for epoch_dir in sorted(os.listdir(results_dir)):
        epoch_path = os.path.join(results_dir, epoch_dir)
        if not os.path.isdir(epoch_path):
            continue

        epoch_metrics = {"tsne": None, "pca": None}

        # Avaliar t-SNE
        tsne_path = os.path.join(epoch_path, "tsne", "tsne_features.csv")
        if os.path.exists(tsne_path):
            tsne_data = pd.read_csv(tsne_path)
            tsne_features = tsne_data[["x", "y"]].values
            tsne_labels = tsne_data["label"].values
            epoch_metrics["tsne"] = evaluate_dimensionality_reduction(tsne_features, tsne_labels)

        # Avaliar PCA
        pca_path = os.path.join(epoch_path, "pca", "pca_features.csv")
        if os.path.exists(pca_path):
            pca_data = pd.read_csv(pca_path)
            pca_features = pca_data[["x", "y"]].values
            pca_labels = pca_data["label"].values
            epoch_metrics["pca"] = evaluate_dimensionality_reduction(pca_features, pca_labels)

        # Salvar métricas da época
        all_metrics[epoch_dir] = epoch_metrics

    return all_metrics

def find_best_epoch(metrics):
    """
    Identifica a melhor época com base nas métricas.

    Args:
        metrics (dict): Métricas para todas as épocas.

    Returns:
        dict: Melhor época para t-SNE e PCA.
    """
    best_epoch = {"tsne": None, "pca": None}

    for method in ["tsne", "pca"]:
        best_score = -float('inf')  # Para silhouette score e intercluster_distance
        best_epoch[method] = {"epoch": None, "score": None}

        for epoch, values in metrics.items():
            if method in values and values[method]:
                silhouette = values[method]["silhouette_score"]
                intercluster = values[method]["intercluster_distance"]
                intracluster = values[method]["intracluster_distance"]

                # Combinar critérios em uma única métrica (peso nos critérios)
                combined_score = silhouette + intercluster - intracluster

                if combined_score > best_score:
                    best_score = combined_score
                    best_epoch[method] = {"epoch": epoch, "score": combined_score}

    return best_epoch

def save_metrics(metrics, output_path):
    """
    Salva as métricas em um arquivo JSON.

    Args:
        metrics (dict): Métricas calculadas para cada época.
        output_path (str): Caminho para salvar o arquivo JSON.
    """
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=4)

# Caminho para o diretório com os resultados
results_dir = "results/pablo"  # Substitua pelo caminho correto

# Avaliar todas as épocas
all_metrics = evaluate_all_epochs(results_dir)

# Identificar a melhor época
best_epoch = find_best_epoch(all_metrics)

# Salvar métricas detalhadas
output_path = os.path.join(results_dir, "dimensionality_reduction_metrics.json")
save_metrics(all_metrics, output_path)

# Exibir a melhor época
print("Melhor Época:")
print(json.dumps(best_epoch, indent=4))
