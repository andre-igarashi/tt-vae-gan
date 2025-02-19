import json
import matplotlib.pyplot as plt

# Carregar os dados do arquivo JSON
file_path = "training_results.json"  # Substitua pelo caminho correto do arquivo
with open(file_path, "r") as file:
    data = json.load(file)

# Extrair todas as épocas disponíveis e limitar a 200
all_epochs = sorted(data.keys(), key=lambda x: int(x))
limited_epochs = [epoch for epoch in all_epochs if int(epoch) <= 300]

# Extrair os valores de perda do gerador e do discriminador para as épocas limitadas
gen_loss = [data[epoch]["Generator Loss"] for epoch in limited_epochs]
disc_loss = [data[epoch]["Discriminator Loss"] for epoch in limited_epochs]
epoch_labels = [int(epoch) for epoch in limited_epochs]

# Criar o gráfico para até 200 épocas
plt.figure(figsize=(10, 5))
plt.plot(epoch_labels, gen_loss, marker="o", label="Generator Loss", linestyle='-')
plt.plot(epoch_labels, disc_loss, marker="s", label="Discriminator Loss", linestyle='-')

# Configuração do gráfico
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Generator and Discriminator Loss (Up to 200 Epochs)")
plt.legend()
plt.grid(True)

# Salvar o gráfico como PNG
output_file = "loss_plot_limited_200_epochs.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

# Exibir o gráfico
plt.show()

print(f"Gráfico salvo como {output_file}")
