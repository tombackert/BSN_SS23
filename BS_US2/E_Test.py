import heapq

# ---PROZESSE--- #

processes = [
    {'name': 'P', 'arrival_time': 0, 'processing_time': 6, 'priority': 1},
    {'name': 'Q', 'arrival_time': 0, 'processing_time': 3, 'priority': 4},
    {'name': 'R', 'arrival_time': 4, 'processing_time': 13, 'priority': 3},
    {'name': 'S', 'arrival_time': 7, 'processing_time': 1, 'priority': 2},
    {'name': 'T', 'arrival_time': 9, 'processing_time': 7, 'priority': 4},
]


# ---SCHEDULING VERFAHREN---

def sjf_non_preemptive_scheduling(processes):
    processes.sort(key=lambda x: (x['arrival_time'], x['processing_time']))

    queue = []
    time = 0

    for process in processes:
        while processes and time >= processes[0]['arrival_time']:
            queue.append(processes.pop(0))

        if not queue:
            queue.append(processes.pop(0))
            time = queue[0]['arrival_time'] 

        queue.sort(key=lambda x: x['processing_time'])

        current_process = queue.pop(0)
        print(f"Process {current_process['name']} is running from time {time} to {time + current_process['processing_time']}")
        time += current_process['processing_time']

    while queue:
        queue.sort(key=lambda x: x['processing_time'])

        current_process = queue.pop(0)
        print(f"Process {current_process['name']} is running from time {time} to {time + current_process['processing_time']}")
        time += current_process['processing_time']

def rr_scheduling(processes, quantum_time):
    n = len(processes)

    wait_time = [0] * n
    turnaround_time = [0] * n
    completion_time = [0] * n
    temp_burst = [processes[i]['processing_time'] for i in range(n)]
    finish = [False] * n
    timer = 0
    queue = []
    execution_list = []

    # Füge Prozesse zur Queue hinzu, die bereits bei Ankunft vorhanden sind
    queue += [i for i in range(n) if processes[i]['arrival_time'] == timer]
    
    while True:
        done = True

        # Überprüfe alle Prozesse in der Warteschlange
        for i in range(len(queue)):
            index = queue.pop(0)
            start_time = timer
            if temp_burst[index] > quantum_time:
                # Erhöhe die Zeit
                timer += quantum_time
                temp_burst[index] -= quantum_time
                done = False
                
                # Füge weitere Prozesse zur Queue hinzu, die während dieser Zeitscheibe angekommen sind
                queue += [i for i in range(n) if not i in queue and not finish[i] and processes[i]['arrival_time'] <= timer and i != index]
                
                # Setze den aktuellen Prozess wieder in die Queue, wenn er noch nicht abgeschlossen ist
                if temp_burst[index] > 0:
                    queue.append(index)

            else:
                # Wenn die Ausführungszeit des Prozesses kleiner als die Zeitscheibe ist, erhöhe die Zeit um die verbleibende Ausführungszeit
                timer += temp_burst[index]
                wait_time[index] = timer - processes[index]['processing_time'] - processes[index]['arrival_time']
                turnaround_time[index] = timer - processes[index]['arrival_time']
                completion_time[index] = timer
                temp_burst[index] = 0
                finish[index] = True

                # Füge weitere Prozesse zur Queue hinzu, die während dieser Zeitscheibe angekommen sind
                queue += [i for i in range(n) if not i in queue and not finish[i] and processes[i]['arrival_time'] <= timer and i != index]

            execution_list.append(f"Process {processes[index]['name']} is running from time {start_time} to {timer}") 
                
        # Wenn alle Prozesse fertig sind, brich die Schleife ab
        if done:
            break

    # Rückgabe der Wartezeit, Umlaufzeit und Fertigstellungszeit für jeden Prozess
    for process in execution_list:
        print(process)


def non_preemptive_priority_scheduling(processes):
    # Initialisiere die Ausführungszeit auf 0
    execution_time = 0

    while len(processes) > 0:
        # Filtere die Prozesse, die zur aktuellen Ausführungszeit angekommen sind
        arrived_processes = [p for p in processes if p['arrival_time'] <= execution_time]

        if arrived_processes:
            # Sortiere die angekommenen Prozesse nach Priorität (höchste zuerst) und dann nach Namen (lexikografische Reihenfolge)
            sorted_processes = sorted(arrived_processes, key=lambda k: (-k['priority'], k['name']))

            # Wähle den Prozess mit der höchsten Priorität aus
            current_process = sorted_processes[0]

            # Speichere die Startzeit des Prozesses
            start_time = execution_time

            # Füge die Verarbeitungszeit des Prozesses zur Ausführungszeit hinzu
            execution_time += current_process['processing_time']

            print(f"Process {current_process['name']} is running from time {start_time} to {execution_time-1}")

            # Entferne den ausgeführten Prozess aus der Liste
            processes.remove(current_process)
        else:
            # Wenn keine Prozesse angekommen sind, erhöhe die Ausführungszeit um 1
            execution_time += 1

def preemptive_priority_scheduling(processes):
    # Sortiere die Prozesse nach Ankunftszeit und bei gleicher Ankunftszeit lexikographisch nach Namen
    processes.sort(key=lambda x: (x['arrival_time'], x['name']))
    n = len(processes)

    # Lege eine Priority Queue an, höhere Priorität hat höhere Präferenz
    # und bei gleicher Priorität wird der Prozess, der zuerst angekommen ist, bevorzugt
    queue = []
    
    # Um die endgültige Reihenfolge der Prozesse zu speichern
    res = []
    
    # Initialisiere die Zeit mit der Ankunftszeit des ersten Prozesses
    time = processes[0]['arrival_time']
    
    # Lege den ersten Prozess in die Queue
    heapq.heappush(queue, (-processes[0]['priority'], processes[0]['arrival_time'], processes[0]['name'], processes[0]))
    
    # Gehe durch alle Prozesse
    for i in range(1, n):
        process = processes[i]
        # Während die Zeit kleiner ist als die Ankunftszeit des nächsten Prozesses und die Queue nicht leer ist
        while queue and time < process['arrival_time']:
            # Wähle den Prozess mit der höchsten Priorität (größter Prioritätswert)
            _, _, name, current_process = heapq.heappop(queue)
            if current_process['processing_time'] > 1:
                current_process['processing_time'] -= 1
                heapq.heappush(queue, (-current_process['priority'], current_process['arrival_time'], current_process['name'], current_process))
                res.append(f"Process {name} is running from time {time} to {time + 1}")
                time += 1
            else:
                res.append(f"Process {name} is running from time {time} to {time + current_process['processing_time']}")
                time += current_process['processing_time']
                
        # Lege den Prozess in die Queue
        heapq.heappush(queue, (-process['priority'], process['arrival_time'], process['name'], process))
        
    # Verarbeite die restlichen Prozesse in der Queue
    while queue:
        _, _, name, current_process = heapq.heappop(queue)
        if current_process['processing_time'] > 1:
            current_process['processing_time'] -= 1
            heapq.heappush(queue, (-current_process['priority'], current_process['arrival_time'], current_process['name'], current_process))
            res.append(f"Process {name} is running from time {time} to {time + 1}")
            time += 1
        else:
            res.append(f"Process {name} is running from time {time} to {time + current_process['processing_time']}")
            time += current_process['processing_time']
        
    for line in res:
        print(line)


# ---HIER VERFAHREN AUSWÄHLEN---

# preemptive_priority_scheduling(processes)
# non_preemptive_priority_scheduling(processes)
# rr_scheduling(processes, 5)
# sjf_non_preemptive_scheduling(processes)