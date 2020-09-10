---
title: "Wie füge ich meine Kommune hinzu?"
description: "Du sammelst Daten, wir visualisieren!"
menu: main
draft: false
---

# Wie kann ich die Daten meiner Kommune visualisieren lassen?

## Daten suchen

Viele Kommunen erstellen Bilanzen, in denen sie ihre CO<sub>2</sub>-Emissionen der
vergangenen Jahre aufführen.
Diese Bilanzen kannst Du z.B. über das Ratsinformationssystem Deiner Kommune bekommen.
Vielleicht hast Du Glück und Deine Kommune ist so fortschrittlich, dass
Du die Daten über ["Politik bei Uns"](https://politik-bei-uns.de/) finden kannst.
Ansonsten versuche mal, nach "Ratsinformationssystem [Deine Kommune]" mit einer
Suchmaschine Deiner Wahl zu suchen.

Wenn Du das Ratsinformationsystem gefunden hast, dann versuche es mal mit folgenden
oder ähnlichen Suchbegriffen:

- Klimabilanz
- Energiebilanz
- CO2-Bilanz

Alternativ könntest Du auch dem Umweltamt Deiner Kommune eine E-Mail schreiben
und nach den Daten fragen. Oder einfach mal anrufen!

## Welche Daten brauche ich?

Am interessanten und wichtigsten ist die Gesamtmenge der Emissionen.
Diese bräuchten wir in der Einheit tausend Tonnen CO<sub>2</sub>.

Oft sind diese Gesamtwerte auch in Kategorien unterteilt, zum Beispiel in: Strom, Wärme, Verkehr.
Da diese Kategorien sich von Kommune zu Kommune unterscheiden, ist unser Programm flexibel.
Schreib einfach die Kategorien auf, die Deine Kommune benutzt (und die visualisiert werden sollen),
und unser Programm erstellt die richtigen Grafiken.

## Parislimit

Für das Parislimit brauchen wir nur zwei Datenpunkte: Die Anzahl der EinwohnerInnen
Deiner Kommune und den aktuellsten CO<sub>2</sub>-Ausstoß Deiner Kommune (mit Jahresangabe).
Diese beiden Daten musst Du besonders kennzeichnen. Im nächsten Abschnitt wird erklärt, wie genau.

## Wie soll ich die Daten aufschreiben?

Du erleichterst unsere Arbeit enorm, wenn Du eine CSV-Datei mit allen gesammelten Daten
erstellst. Eine CSV-Datei ist eine einfache Textdatei, in der Werte mit Kommas getrennt sind.
Du kannst sie entweder mit einem einfachem Texteditor schreiben oder mit
einem Tabellenkalkulationsprogramm wie LibreOffice Calc (oder Microsoft Excel)
erstellen. Wenn Du ein Tabellenkalkulationsprogramm benutzt, dann speichere
die Tabelle bitte als CSV-Datei, Trenner: Komma, keine Anführungszeichen um Textfelder.

Die CSV-Datei soll bitte wie folgt aussehen (Auszüge aus der Datei für Münster;
es können beliebig viele Zeilen hinzugefügt werden):

```
year,category,type,co2,note
2016,Verkehr,real,491,
2017,Verkehr,real,484,
2016,Strom,real,710,estimated from plot
2017,Strom,real,690,estimated from plot
2016,Wärme,real,780,estimated from plot
2017,Wärme,real,780,estimated from plot
1990,Gesamt,real,2517,
2016,Gesamt,real,1981,
2017,Gesamt,real,1954,last_emissions
2019,Einwohner,Einwohner,310521,
```

Die Spalten erklärt:

- `year`: das Jahr der CO<sub>2</sub>-Emissionen
- `category`: die Kategorie der CO<sub>2</sub>-Emissionen. Mindestens eine Zeile sollte hier den Wert `Gesamt` haben
- `type`: `real` für tatsächliche Emissionen, `geplant` für Ziele, die z.B. in Klimaschutzplänen stehen
- `value`: Die CO<sub>2</sub>-Emissionen in tausend Tonnen
- `note`: Hier lassen sich Notizen eintragen, die wichtig sein könnten (z.B. Daten nur geschätzt).

Die letzten beiden Zeilen im obigen Beispiel sind besonders wichtig zur automatischen
Berechnung des Parislimits für Deine Kommune:

- Den aktuellsten CO<sub>2</sub>-Ausstoß Deiner Kommune bitte mit `last_emissions` in der Spalte `note` markieren.
- Für die Einwohnerzahl bitte sowohl in die Spalte `category` als auch `type` das Wort `Einwohner` eintragen.

## Quellenangaben

Wichtig: Bitte schreibe auf, aus welcher Quelle Deine Daten kommen, am
liebsten auch mit Links zu diesen Quellen
(z.B.: "Energie- und Klimabilanz 2011 und 2017 der Stadt Münster",
verfügbar unter [1](https://www.stadt-muenster.de/sessionnet/sessionnetbi/vo0050.php?__kvonr=2004035809)
und [2](https://www.stadt-muenster.de/sessionnet/sessionnetbi/vo0050.php?__kvonr=2004044154)).
So können andere die Werte möglichst einfach nachvollziehen, mögliche
Fehler zu finden und überhaupt gehört es sich einfach immer und überall zu
sagen woher man seine Informationen hat.
Es reicht, wenn Du eine einfache Textdatei mit diesen Quellenangaben schreibst,
am besten in vollständigen Sätzen. Dann können wir diese Angaben einfach
rüberkopieren.

## Kontaktdaten

Um Fragen, Diskussionen und Anregungen direkt vor Ort zu klären, schicke Doch bitte Kontaktdaten mit, die wir auf Klimawatch veröffentlichen dürfen (Name, E-Mail-Adresse, oder so etwas).

## Okay, ich habe alles zusammen!

Super, vielen Dank schonmal!
Bitte nenne Deine Datei, so wie Deine Kommune heißt, aber ohne Umlaute (z.B. `muenster.csv` oder `koeln.csv`).
Vergiss nicht, auch eine Datei mit Quellenangaben zu schreiben.

Dann kannst Du diese beiden Dateien entweder
[per E-Mail an Thomas](mailto:ed.rofedoc@retsneum?subject=Klimawatch-Daten für KOMMUNE&body=Hallo%20Thomas,%0D%0A%0D%0Aim%20Anhang%20schicke%20ich%20Dir%20die%20gewünschten%20zwei%20Dateien%20%28Daten%20und%20Quellenangaben%29,%20damit%20es%20Klimawatch%20bald%20auch%20für%20MEINEKOMMUNE%20gibt.%0D%0A%0D%0AViele Grüße%0D%0AMaria%20Musterfrau%0D%0A) schicken
oder, wenn Du Dich mit `github` auskennst, kannst Du auch gerne [einen Pull Request](https://github.com/codeformuenster/klimawatch#wie-kann-ich-die-daten-meiner-kommune-visualisieren) stellen.
(Falls Dich der letzte Teil des vorigen Satzes verwirrt, ignoriere ihn einfach
und schicke eine E-Mail).

In wenigen Tagen ist Deine Kommune dann online unter
https://klimawatch.codefor.de/kommunen/DEINEKOMMUNE

## Klimaschutzmodule

Anleitung folgt.
