# BSN_US6

## Aufgabe 1: RTT (7 Punkte)
Note: siehe Skript zur Berechnung der RTT im Anhang

Die Aufgabe besteht darin, die Übertragungszeit (RTT) zwischen zwei Servern mit gegebenen Parametern zu berechnen. Diese Zeiten werden üblicherweise im Kontext von TCP/IP-Netzwerken berechnet.

### Formeln:

- EstimatedRTT = (1 - α) * EstimatedRTT + α * SampleRTT
- DevRTT = (1 - β) * DevRTT + β * |SampleRTT - EstimatedRTT|
- TimeOutInterval = EstimatedRTT + 4 * DevRTT

### In den obigen Formeln:

- EstimatedRTT ist die geschätzte Round-Trip-Time, die sich aus den bisherigen Messungen ergibt.
- DevRTT ist eine Schätzung der Abweichung der Round-Trip-Time, die sich aus den bisherigen Messungen ergibt.
- SampleRTT ist die aktuell gemessene Round-Trip-Time.
- TimeOutInterval ist das Zeitintervall, nach dem eine erneute Übertragung gestartet wird, wenn keine Bestätigung empfangen wurde.
- α und β sind Gewichtungsfaktoren.

Wir haben vier gemessene SampleRTT-Werte: 106 ms, 120 ms, 140 ms und 90 ms. Wir nehmen an, dass der Wert von α = 0,125 und der Wert von β = 0,25 ist.

Zu Beginn betragen EstimatedRTT = 100 ms und DevRTT = 5 ms. Nun werden wir die Werte nach jedem SampleRTT aktualisieren:

### Nach dem 1-ten SampleRTT (106 ms):
- EstimatedRTT = (1 - 0.125) * 100 ms + 0.125 * 106 ms = 100.75 ms
- DevRTT = (1 - 0.25) * 5 ms + 0.25 * |106 ms - 100.75 ms| = 5.06 ms
- TimeOutInterval = 100.75 ms + 4 * 5.06 ms = 121.0 ms

### Nach dem 2-ten SampleRTT (120 ms):
- EstimatedRTT = (1 - 0.125) * 100.75 ms + 0.125 * 120 ms = 103.16 ms
- DevRTT = (1 - 0.25) * 5.06 ms + 0.25 * |120 ms - 103.16 ms| = 8.01 ms
- TimeOutInterval = 103.16 ms + 4 * 8.01 ms = 135.19 ms

### Nach dem 3-ten SampleRTT (140 ms):
- EstimatedRTT = (1 - 0.125) * 103.16 ms + 0.125 * 140 ms = 107.76 ms
- DevRTT = (1 - 0.25) * 8.01 ms + 0.25 * |140 ms - 107.76 ms| = 14.07 ms
- TimeOutInterval = 107.76 ms + 4 * 14.07 ms = 164.02 ms

Nach dem 4-ten SampleRTT (90 ms):
- EstimatedRTT = (1 - 0.125) * 107.76 ms + 0.125 * 90 ms = 105.54 ms
- DevRTT = (1 - 0.25) * 14.07 ms + 0.25 * |90 ms - 105.54 ms| = 14.43 ms
 TimeOutInterval = 105.54 ms + 4 * 14.43 ms = 163.28 ms

## Aufgabe 2 (10 Punkte)

1. Hauptunterschied zwischen Go-Back-N und Selective Repeat (2 Punkte):
    
    Der Hauptunterschied zwischen Go-Back-N und Selective Repeat liegt in der Art und Weise, wie sie auf verlorene oder beschädigte Pakete reagieren. Bei Go-Back-N, wenn ein Fehler in einem Paket erkannt wird, werden dieses Paket und alle nachfolgenden Pakete im Fenster erneut gesendet, unabhängig davon, ob sie erfolgreich empfangen wurden oder nicht.
    Bei Selective Repeat hingegen wird nur das spezifische Paket, bei dem ein Fehler erkannt wurde, erneut gesendet. Daher ist Selective Repeat effizienter bei hohen Bitfehlerraten.
    
2. Zeitlicher Ablauf beider Szenarien (4 Punkte):
    
    ### Szenario 1:
    
    ![Ablaufdiagramm_Szenario1.png](https://github.com/tombackert/BSN_SS23/blob/master/US6/Ablaufdiagramm_Szenario1.png?raw=true)
    
    - Sender sendet Paket 0,1,2
    - Empfänger empfängt Paket 0,1,2
    - Empfänger sendet ACK 0,1,2, aber diese gehen verloren
    - Nach Timeout sendet der Sender erneut die Pakete 0,1,2
    
    ### Szenario 2:
    
    ![Ablaufdiagramm_Szenario2.png](https://github.com/tombackert/BSN_SS23/blob/master/US6/Ablaufdiagramm_Szenario2.png?raw=true)
    
    - Sender sendet Paket 0,1,2
    - Empfänger empfängt Paket 0,1,2
    - Empfänger sendet ACK 0,1,2 und der Sender empfängt diese
    - Sender sendet die nächsten drei Pakete, aber das Paket mit der Sequenznummer 0 geht verloren.
    
    Was fällt auf?
    
    Auffällig in beiden Szenarien ist, dass die Verluste in der Kommunikation zu einer Wiederholung der Pakete führen, was zu einer geringeren Effizienz führt.

    Im ersten Szenario gehen die Bestätigungen (ACKs) vom Empfänger verloren, was dazu führt, dass der Sender alle drei Pakete erneut sendet. Dies bedeutet, dass trotz des erfolgreichen Empfangs der Pakete durch den Empfänger, die Pakete aufgrund des Fehlens einer Bestätigung erneut gesendet werden müssen.

    Im zweiten Szenario gehen die Pakete, die vom Sender gesendet werden, verloren. Obwohl der Sender eine Bestätigung für die ersten drei Pakete erhält, führt der Verlust des ersten der nächsten drei Pakete dazu, dass dieses Paket erneut gesendet werden muss.

    In beiden Fällen führen Verluste in der Kommunikation zu Redundanzen und Ineffizienzen in der Datenübertragung. Dies zeigt die Wichtigkeit von Bestätigungen und Fehlerkontrollen in Protokollen zur Übertragungssteuerung wie Go-Back-N und Selective Repeat.
    
3. Maximale Fenstergröße bei Selective-Repeat (2 Punkte):
    
    Bei Selective Repeat darf die Fenstergröße maximal k/2 sein, wobei k die Größe des Sequenznummernbereichs ist. Das liegt daran, dass wir sicherstellen müssen, dass die Sequenznummern der Pakete, die sich noch im Umlauf befinden (also gesendet, aber noch nicht bestätigt), eindeutig sind. Wenn wir eine Fenstergröße größer als k/2 hätten, könnten wir in eine Situation geraten, in der wir nicht unterscheiden könnten, ob ein empfangenes Paket eine neue Übertragung oder eine veraltete Kopie eines zuvor gesendeten Pakets ist.
    
4. Möglichkeit eines ACK für ein Paket außerhalb des gegenwärtigen Fensters bei Selective-Repeat (2 Punkte):
    
    Nein, in Selective-Repeat ist es nicht möglich, dass ein Sender ein ACK für ein Paket erhält, das außerhalb seines gegenwärtigen Fensters liegt. Das liegt daran, dass der Sender nur Pakete innerhalb seines Sendefensters überträgt und der Empfänger nur ACKs für Pakete innerhalb seines Empfangsfensters sendet. Wenn der Sender ein ACK für ein Paket außerhalb seines Fensters erhält, wäre dies auf einen Fehler zurückzuführen.
    

## Links:
1. Berechnung der RTT: https://github.com/tombackert/BSN_SS23/blob/master/US6/calculate_sampleRTT.py
2. 
