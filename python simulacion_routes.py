import networkx as nx
import matplotlib.pyplot as plt

def simulate_network_activity(graph):
    print("Estado inicial de la red:")
    print(graph.edges())

    # Representa el estado inicial de la red
    nx.draw(graph, with_labels=True, font_weight='bold')
    plt.show()

    # Desconecta un enlace aleatorio
    edges = list(graph.edges())
    if edges:
        disconnect_edge = edges[0]
        graph.remove_edge(*disconnect_edge)
        print(f"\nSe desconectó el enlace: {disconnect_edge}\n")

        # Representa el estado después de desconectar el enlace
        nx.draw(graph, with_labels=True, font_weight='bold')
        plt.show()
    else:
        print("La red ya está desconectada.")

if __name__ == "__main__":
    # Crea una red de ejemplo
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1)])

    # Simula la actividad de los routes
    simulate_network_activity(G)
