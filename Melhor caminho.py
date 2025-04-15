import heapq
import matplotlib.pyplot as plt
from PIL import Image

# ---------- GRAFO ----------
grafo = {
    "AC": [("AM", 1400)],
    "AM": [("AC", 1400), ("RR", 4000), ("RO", 1500), ("PA", 5000), ("MT", 6000)],
    "RR": [("AM", 4000), ("PA", 5300)],
    "RO": [("AM", 1500), ("MT", 2100)],
    "PA": [("AM", 5000), ("RR", 5300), ("AP", 2200), ("MT", 3000), ("TO", 2500), ("MA", 2400)],
    "MT": [("RO", 2100), ("AM", 6000), ("PA", 3000), ("TO", 1500), ("GO", 1100), ("MS", 2000)],
    "AP": [("PA", 2200)],
    "MS": [("MT", 2000), ("GO", 1800)],
    "TO": [("GO", 1500), ("MT", 1500), ("PA", 2500), ("MA", 1700)],
    "GO": [("MS", 1800), ("MT", 1100), ("TO", 1500)],
    "MA": [("PA", 2400), ("TO", 1700)]
}

# ---------- ALGORITMO DE DIJKSTRA ----------
def dijkstra(grafo, inicio):
    distancias = {estado: float('inf') for estado in grafo}
    distancias[inicio] = 0
    anteriores = {}
    fila = [(0, inicio)]

    while fila:
        dist_atual, atual = heapq.heappop(fila)

        for vizinho, peso in grafo[atual]:
            nova_dist = dist_atual + peso
            if nova_dist < distancias[vizinho]:
                distancias[vizinho] = nova_dist
                anteriores[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))

    return distancias, anteriores

# ---------- RECONSTRUÇÃO DO CAMINHO ----------
def reconstruir_caminho(anteriores, destino):
    caminho = []
    atual = destino
    while atual in anteriores:
        caminho.insert(0, atual)
        atual = anteriores[atual]
    caminho.insert(0, atual)
    return caminho

# ---------- EXECUÇÃO ----------
origem = "GO"
destino = "RR"
distancias, anteriores = dijkstra(grafo, origem)
rota = reconstruir_caminho(anteriores, destino)
distancia_total = distancias[destino]

# ---------- EXIBIR ROTA E DISTÂNCIA ----------
print("🔹 Rota ótima de GO até RR:", " → ".join(rota))
print(f"📏 Distância total: {distancia_total} km\n")

# ---------- TABELA DE DISTÂNCIAS ----------
print("📊 Tabela de distâncias:")
print("Estado  Distância (km)")
for estado, dist in sorted(distancias.items(), key=lambda x: x[1]):
    print(f"{estado:5} {dist:>8} km")

# ---------- COORDENADAS PARA PLOTAGEM ----------
coordenadas_estados = {
    "GO": (1200, 1060),
    "MT": (990, 880),
    "RO": (650, 860),
    "AM": (600, 620),
    "RR": (620, 260),
}

# ---------- PLOTAR ROTA SOBRE IMAGEM ----------
img = Image.open("mapaBrasil.png")  # Caminho relativo para uso no repositório
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(img)

# Plotar rota
for i in range(len(rota) - 1):
    x1, y1 = coordenadas_estados[rota[i]]
    x2, y2 = coordenadas_estados[rota[i + 1]]
    ax.plot([x1, x2], [y1, y2], color="red", linewidth=3)

# Marcar pontos no mapa
for estado in rota:
    x, y = coordenadas_estados[estado]
    ax.plot(x, y, 'o', color='blue', markersize=8)

# Remover eixos
ax.axis('off')
plt.title("Rota ótima de bicicleta: GO até RR", fontsize=14)
plt.savefig("melhor_caminho.png", dpi=300)
plt.show()
