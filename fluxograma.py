import matplotlib.pyplot as plt
import networkx as nx

# Criando um gráfico direcionado
G = nx.DiGraph()

# Definição dos nós do fluxograma
nodes = {
    "dataset": "Dataset",
    "audio_treino": "Áudio de Treino",
    "preproc_treino": "Pré-processamento",
    "treinamento": "Treinamento",
    "vae_encoder": "VAE Encoder",
    "espaco_latente": "Espaço Latente (μ, σ)",
    "amostragem": "Amostragem Latente (z)",
    "vae_decoder": "VAE Decoder (Reconstrução)",
    "gan_generator": "GAN Generator (Síntese de Timbre)",
    "gan_discriminator": "GAN Discriminator\n(Treinamento Adversarial)",
    "audio_teste": "Áudio de Teste",
    "preproc_teste": "Pré-processamento",
    "modelo": "Modelo (VAE + GAN)",
    "espectrograma_modelado": "Espectrograma Modelado",
    "reconstrucao_fase": "Reconstrução de Fase\n(Griffin-Lim)",
    "audio_reconstruido": "Áudio Reconstruído",
}

# Adicionando nós ao grafo
G.add_nodes_from(nodes.keys())

# Definição das conexões
edges = [
    ("dataset", "audio_treino"),
    ("audio_treino", "preproc_treino"),
    ("preproc_treino", "treinamento"),
    ("treinamento", "vae_encoder"),
    ("vae_encoder", "espaco_latente"),
    ("espaco_latente", "amostragem"),
    ("amostragem", "vae_decoder"),
    ("amostragem", "gan_generator"),
    ("gan_generator", "gan_discriminator"),
    ("gan_discriminator", "gan_generator"),
    ("dataset", "audio_teste"),
    ("audio_teste", "preproc_teste"),
    ("preproc_teste", "modelo"),
    ("modelo", "espectrograma_modelado"),
    ("espectrograma_modelado", "reconstrucao_fase"),
    ("reconstrucao_fase", "audio_reconstruido"),
]

# Adicionando conexões ao grafo
G.add_edges_from(edges)

# Layout do gráfico
pos = {
    "dataset": (0, 4),
    "audio_treino": (1, 4),
    "preproc_treino": (2, 4),
    "treinamento": (3, 4),
    "vae_encoder": (4, 4),
    "espaco_latente": (5, 4),
    "amostragem": (6, 4),
    "vae_decoder": (6, 3),
    "gan_generator": (7, 4),
    "gan_discriminator": (7, 3),
    "audio_teste": (1, 2),
    "preproc_teste": (2, 2),
    "modelo": (3, 2),
    "espectrograma_modelado": (4, 2),
    "reconstrucao_fase": (5, 2),
    "audio_reconstruido": (6, 2),
}

# Desenhando o fluxograma
plt.figure(figsize=(12, 7))
nx.draw(G, pos, with_labels=True, node_size=5000, node_color="lightgray", font_size=8, edge_color="black")

# Adicionando rótulos personalizados
labels = {key: val for key, val in nodes.items()}
nx.draw_networkx_labels(G, pos, labels, font_size=8)

# Salvando o fluxograma como imagem
plt.title("Fluxograma Completo da Solução para Transferência de Timbre")

plt.show()
