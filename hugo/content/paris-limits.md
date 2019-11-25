---
title: "Was sind die Paris-Limits?"
description: "Und wie berechnet ihr sie für einzelne Kommunen?"
menu: main
draft: false
images: []
---

TODO

# "Unter diesen ganzen Tonnen kann sich doch keiner was vorstellen." (Bundesumweltministerin Schulze)

Svenja Schulze, Bundesumweltministerin (mit Münster-Bezug) hat letztens gesagt:
["Unter diesen ganzen [CO2-]Tonnen kann sich doch keiner was vorstellen."](https://twitter.com/Jumpsteady/status/1177492121143525376)

Dabei ist das gar nicht so schwer. Man kann sich die Atmosphäre wie eine
Badewanne vorstellen, die bald überläuft. Sagen wir, es passen noch 7,3 Liter hinein.
Jeder Tropfen Wasser mehr endet unweigerlich außerhalb der Badewanne.
Nun kann man nicht sicher sagen: In zwei Minuten ist die Badewanne voll.
Wichtig ist nämlich auch die Geschwindigkeit, mit der das Wasser in die
Badewanne läuft. Wenn ich den Hahn voll aufdrehe, dauert es vielleicht nur
eine Minute. Wenn ich den Hahn nur tröpfeln lasse, könnte es zehn Minuten dauern.

Was hat das mit der Klimakrise zu tun? CO2 beeinflusst unser Klima:
Je mehr CO2 wir ausstoßen, desto heißer wird es auf der Erde.
Um katastrophale Zustände zu vermeiden (entspricht dem Überlaufen der Badewanne),
müssen wir also die Gesamtmenge des CO2, die wir ausstoßen, begrenzen.
Basierend auf jahrzehntelanger wissenschaftlicher Expertise wurde genau das
2016 (endlich) im Pariser Klimaschutzabkommen beschlossen: Ein CO2-Restbudget,
um katastrophale Klimabedingungen zu vermeiden. Ab Anfang 2018 waren das
800 Gigatonnen CO2 für die gesamte Welt.

Für Deutschland bleiben [höchstens noch 7,3 Gigatonnen CO2 seit Anfang 2019](https://scilogs.spektrum.de/klimalounge/wie-viel-co2-kann-deutschland-noch-ausstossen/).
Um zu verstehen, was das mit "diesen ganzen Tonnen" für Münster als Beispielkommune
heißt, haben wir diese 7,3 Gigatonnen auf Münster runtergebrochen.
Für Münster bleiben ca. 15 243 tausend Tonnen CO2 Restbudget (Berechnung s. unten).
In [der Grafik auf der Münster-Seite](../kommunen/muenster/)
ist eine Geschwindigkeit der CO2-Reduktion (erinnere Dich an die Öffnung des Wasserhahns!)
visualisiert, die konform mit den völkerrechtlich verbindlichen Beschlüssen
des Pariser Abkommens wäre. Zum Vergleich haben wir die tatsächliche Menge
an CO2, die Münster seit 1990 ausgestoßen hat, visualisiert. Insbesondere
wollen wir transparent machen, wie die bisherigen Fortschritte in der
Geschwindigkeit der CO2-Minderung zu den Pariser Zielen stehen.

## Okay, was heißt das für eine einzelne Kommune?

Wir haben die Pariser Ziele für jede einzelne Kommune wie folgt runtergebrochen:
Zunächst haben wir das Budget pro BürgerIn in Gesamtdeutschland ausgerechnet
(ca. 0,088 tausend Tonnen CO2 pro Kopf). Diese Zahl haben wir dann mit
der Anzahl BürgerInnen in der entsprechenden Kommune multipliziert.
Für Münster macht das ca. 25 405 tausend Tonnen pro MünsteranerIn.
Um eine Vergleichbarkeit mit den Daten in der Grafik zu erreichen, haben
wir von diesem Restbudget pauschal 40% abgezogen. Entsprechend bleiben
[für Münster](../kommunen/muenster/)
die visualisierten 15 243 tausend Tonnen CO2. [Für andere Kommunen](../kommunen/liste/)
ist diese Zahl natürlich anders.

Warum haben wir 40% abgezogen? Das liegt daran, dass in der Bilanz der
Stadt weder individueller Konsum noch die Ernährung der BürgerInnen eingerechnet ist.
Lediglich Strom, Wärme und Verkehr sind in der städtischen Energiebilanz berücksichtigt.
Da ca. 40 % eines individuellen CO2-Fußabdrucks für Ernährung und Konsum draufgehen
(diese Zahl haben wir vom [CO2-Rechner des Umweltbundesamts](https://uba.co2-rechner.de/)), müssen wir
diese für eine Vergleichbarkeit mit den städtischen Bilanzen also abziehen.

Damit wir das nicht für jede einzelne Kommune von Hand ausrechnen müssen,
haben wir ein Skript geschrieben, welches diese Rechnung mit den Daten
erledigt, die uns Freiwillige zuschicken. [Hier ist der Quelltext des Skripts zu finden](https://github.com/codeformuenster/klimawatch/blob/master/generate_plots.py#L53)).

Die Datenquellen für die einzelnen Kommunen sind auf jeder Kommunenseite aufgeführt
(auch die Quellenangaben haben uns Freiwillige zugesandt; wir können eine Prüfung nicht leisten).

Du möchtest uns auch Daten zuschicken? Super, [hier findest Du eine Anleitung dazu](../anleitung)

## Wichtig

Generell gilt immer: **Alle Angaben ohne Gewähr!** Über Hinweise auf
Fehler oder sonstige Anmerkungen freuen wir uns aber natürlich (Kontakt ganz unten)!
