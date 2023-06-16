import heapq

def dijkstra(graph, start):
    # Initialisiere die Distanzen und Vorgänger
    distances = {node: (float('infinity'), None, []) for node in graph}
    distances[start] = (0, start, [start])

    # Initialisiere die Warteschlange
    queue = [(0, start)]

    # Initialisiere die Liste der besuchten Knoten
    visited = []

    # Initialisiere die Ergebnisse für jeden Schritt
    results = []

    while queue:
        # Wähle den Knoten mit der kleinsten Distanz
        current_distance, current_node = heapq.heappop(queue)

        # Besuche den Knoten nur, wenn er noch nicht besucht wurde
        if current_node not in visited:
            visited.append(current_node)

            # Aktualisiere die Distanzen der Nachbarknoten
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                # Aktualisiere die Distanz, den Vorgänger und die Route, wenn eine kürzere Distanz gefunden wurde
                if distance < distances[neighbor][0]:
                    distances[neighbor] = (distance, current_node, distances[current_node][2] + [neighbor])
                    heapq.heappush(queue, (distance, neighbor))

            # Speichere die Ergebnisse für diesen Schritt
            results.append((len(results), visited.copy(), {k: v for k, v in distances.items()}))

    return results

graph = {
    'A': {'B': 8, 'C': 9, 'E': 5},
    'B': {'A': 8, 'E': 2, 'F': 4},
    'C': {'A': 9, 'E': 5, 'D': 2},
    'E': {'A': 5, 'B': 2, 'C': 5, 'D': 1},
    'D': {'C': 2, 'E': 1, 'F': 6, 'G': 8},
    'F': {'B': 4, 'D': 6, 'G': 2},
    'G': {'D': 8, 'F': 2}
}

steps = dijkstra(graph, 'A')

# Drucke die Schritte schön formatiert aus
for step, visited, distances in steps:
    print(f"Schritt {step}: N' = {visited}")
    for node in 'BCDEFG':
        dist, prev, path = distances[node]
        prev = prev if prev else '-'
        dist = dist if dist != float('infinity') else 'inf'
        comment = ''
        if path and visited[-1] == path[-2]:
            comment = f'# kürzerer Weg: ' + '->'.join(path)
        print(f"D({node}), p({node}) = ({dist}, {prev}) {comment}")
    print("---")