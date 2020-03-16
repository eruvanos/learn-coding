# Learn Coding - Disco ✨🎉💃🕺
Hier lernst du Programmieren an dem Beispiel einer LED Lichterkette. 

Warum ausgerechnet eine LED Lichterkette wirst du dich fragen.
 
Wir wollen dir zeigen, dass du mit ein wenig Programmierkenntnissen und 
einer programmierbaren Lichterkette ziemlich viel erreichen kannst. 

Hier haben wir ein paar Beispiele rausgesucht was mit programmierbaren Lichterketten so alles möglich ist:


![Snake Christmas Tree](/static/images/snake.gif "Snake Christmas Tree")
![Ping Pong LED wall](/static/images/pingpong.gif "Ping Pong LED wall")
![Interactive equalizer](/static/images/equalizer.gif "Interactive equalizer")


# Grundlagen



Zeige einen Text an:

```python
print("Anführungszeichen sind wichtig")

# Dies ist eine Kommentarzeile
# Sie wird komplett ignoriert von Python
```

Zeige Zahlen an
```python
print(100000)
# Bei Zahlen KEINE Anführungszeichen
```


Speicher eine Zahl und gib sie aus
```python
beliebiger_name = 10
print(beliebiger_name)
# Auch Variablen brauchen keine Anführungszeichen
```

Rechne mit Zahlen
```python
# Python kann * / + -
ergebnis = 5 * 5
print(ergebnis)
```

 > **Tipp:** Falls du dich mal verschrieben hast, kannst du mit der Tastenkombination `⌘` + `z` oder `strg` + `z` deine letzte Änderung rückgängig machen.

# LED anschalten
Um ein LED Licht anzuschalten musst du die folgenden Befehle schreiben:

```python
pixels.setPixelColor(3, 'RED')
pixels.show()
```

Der erste Befehl `pixels.setPixelColor(3, 'RED')` sagt dem Programm das die LED an position 4 (die Zählung fängt bei `0` an) die Farbe `RED` (also rot) haben soll. Dieser Befehl alleine reicht dem Computer aber noch nicht. Stattdessen musst du dem Computer noch sagen, dass er deine Änderung anzeigen soll. Dies machst du mit dem zweiten Befehl `pixels.show()`.

**Missionen:**
1. Ändere die Farbe der LED (hier findest du eine Liste von verfügbaren Farbennamen: https://www.w3schools.com/colors/colors_names.asp)
2. Ändere die Farbe von einer weiteren LED
3. Lasse alle 40 Lampen rot leuchten

# Ich bin faul, können wir das nicht einfacher machen?
Anstatt jede LED Lampe einzeln anzusteuern, kannst du auch eine Schleife verwenden. Mithilfe einer Schleife kannst du Code so lange ausführen lassen bis eine Bedingung erfüllt ist:

```python
position = 0
while position < pixels.length(): # Solange position kleiner als 40 ist
  pixels.setPixelColor(position, 'RED')
  position = position + 1
pixels.show()
```

**Missionen:**
1. Gebe allen Lampen eine zufällige Farbe mit der Funktion `random_color()`
1. Ändere die Farbe von allen LEDs erst zu `RED`, `GREEN` und zum schluss zu `BLUE`


> **Hinweis:** Du kannst auch statt einer `while`-Schleife eine `for`-Schleife verwenden

```python
for position in range(4):
  pixels.setPixelColor(position, "RED")
pixels.show()
```

# Wenn dies, dann das
Mit dem Schlüsselwort `if` (deutsch: wenn) kannst du Operationen ausführen wenn eine Bedingung erfüllt ist. Beispielsweise kannst du eine Lampe ausschalten wenn sie rot ist, ansonsten nicht.

Du verwendest `if` wie folgt:

```python
if <Bedingung>:
  # Operation die ausgeführt werden soll
```

In diesem Beispiel ist `<Bedingung>` nur ein Platzhalter und kann für einen Vergleich verwendet werden. Die folgende Liste gibt ein paar Beispiele von Vergleichsoperatoren die du verwenden kannst:

* `wert1 == wert2` Prüft ob `wert1` gleich `wert2` ist
* `wert1 < wert2` Prüft ob `wert1` kleiner `wert2` ist
* `wert1 > wert2` Prüft ob `wert1` größer `wert2` ist
* Es gibt aber noch mehr 


```python
pixels.setPixelColor(3, 'RED')
position = 0
while position < pixels.length():
  if get_color(position) == "RED":
    pixels.setPixelColor(position, 'BLACK')
  position = position + 1
pixels.show()
```

Zusätzlich zu dem Schlüsselwort `if` gibt es das Schlüsselwort `else` (deutsch: dann). Damit kannst du Operationen ausführen die alternativ ausgeführt werden sollen. Beispielsweise: Schalte LED aus wenn sie rot ist, ansonsten mache sie grün.

```python
pixels.setPixelColor(3, 'RED')
position = 0
while position < pixels.length():
  if get_color(position) == "RED":
    pixels.setPixelColor(position, 'BLACK')
  else:
    pixels.setPixelColor(position, 'GREEN')
  position = position + 1
pixels.show()
```

**Missionen:**
1. Mache die erste Hälfte der Lampen `RED` und die andere Hälfte `GREEN`

# Blinkende Lichter
Um die Lichterketter zum blinken zu bekommen, müssen wir dem Computer sagen dass er ein Licht an und nach einer Zeit wieder anschalten soll. Dies kannst du erreichen indem du dem Computer sagst er soll für eine kurze Zeit schlafen `await sleep(<Zeit>)`.

Damit der Computer das auch richtig versteht, müssen wir das folgende Grundgerüst einfügen:

```python
async def main():
  # Füge deinen Code hier ein

if __name__ == '__main__':
  run(main())
```

Mit dieser Änderung kannst du nun LEDs zum blinken bringen:

```python
async def main():
  pixels.setPixelColor(2, 'RED')
  pixels.show()
  await sleep(1)
  pixels.setPixelColor(2, 'WHITE')
  pixels.show()
  await sleep(1)
  pixels.setPixelColor(2, 'RED')
  pixels.show()
  await sleep(1)

if __name__ == '__main__':
  run(main())
```

**Missionen:**
1. Erstelle eine endlos Schleife (`while True:`) und erstelle ein ständig blinkendes Licht

# Move the light
TBD: Move the light using the arrow keys




# TODO:
1. For `if` conditionals we need a `pixels.get(<index>)`
2. For more fun we need a `getRandomColor()` method
3. We need `pixels.length()`