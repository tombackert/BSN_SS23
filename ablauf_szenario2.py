import matplotlib.pyplot as plt
import numpy as np

# Parameter festlegen
window_size = 3
sequence_numbers = np.array([0, 1, 2])
send_time = np.array([1, 2, 3, 7, 8, 9])  # Wiederholtes Senden nach Timeout hinzugefügt
recv_time = np.array([2, 3, 4, 8, 9, 10])  # Empfangszeiten für wiederholtes Senden hinzugefügt, ein Paket fehlt
ack_send_time = np.array([2, 3, 4, 8, 9, 10])  # Keine wiederholten ACKs in diesem Szenario
ack_recv_time = np.array([3, 4, 5, 9, 10, 11])  # Keine wiederholten ACKs in diesem Szenario
recieved = (True, True, True, False, True, True)  # Empfangsbestätigungen für wiederholtes Senden hinzugefügt

# Erstelle ein Diagramm und Achsen
fig, ax = plt.subplots()

# Linien für Sender und Empfänger erstellen
ax.plot([1, 1], [0, 14], 'k-', marker='v')
ax.plot([2, 2], [0, 14], 'k-', marker='v')


# Beschriftung für Sender und Empfänger
ax.text(1, 15, "Sender", ha="center")
ax.text(2, 15, "Empfänger", ha="center")

# Pfeile für ERSTE Paketübertragung erstellen
for i in range(window_size):  # Wiederholte Sendung berücksichtigen
    ax.annotate(f"SEQ = {sequence_numbers[i]}",
                xy=(2, 14 - recv_time[i]),
                xytext=(1, 14 - send_time[i]),
                arrowprops=dict(arrowstyle="->", color="grey"), 
                horizontalalignment='right',
                verticalalignment='bottom')

# Pfeile für ERSTE ACK-Übertragung erstellen
for i in range(window_size):  # Nur erste Runde von ACKs
    ax.annotate(f"ACK = {sequence_numbers[i]}",
                xy=(1, 14 - ack_recv_time[i]),
                xytext=(2, 14 - ack_send_time[i]), 
                arrowprops=dict(arrowstyle="->", color="r"),
                horizontalalignment='left',
                verticalalignment='top')
    
# Pfeile für ZWEITE Paketübertragung erstellen
for i in range(window_size):  # Wiederholte Sendung berücksichtigen
    xy =(2, 12 - recv_time[i+3]) if recieved[i+3] is True else (1.8, 12 - recv_time[i+3])
    ax.annotate(f"SEQ = {sequence_numbers[i]}",
                        xy=xy,
                        xytext=(1, 12 - send_time[i+3]),
                        arrowprops=dict(arrowstyle="->", color="grey"), 
                        horizontalalignment='right')

# Pfeile für ZWEITE ACK-Übertragung erstellen
for i in range(window_size):  # Nur erste Runde von ACKs
    if recieved[i+3] is True:
        ax.annotate(f"ACK = {sequence_numbers[i]}",
                    xy=(1, 12 - ack_recv_time[i+3]),
                    xytext=(2, 12 - ack_send_time[i+3]), 
                    arrowprops=dict(arrowstyle="->", color="r"),
                    horizontalalignment='left',
                    verticalalignment='top')
# Titel hinzufügen
ax.set_title("Ablaufdiagramm für Szenario 2")
# Legende hinzufügen
ax.legend(["Sender", "Empfänger", "Paketübertragung", "ACK-Übertragung"])

# Achsenticks entfernen
ax.set_yticks([])
ax.set_xticks([])

# Diagramm anzeigen
plt.show()
