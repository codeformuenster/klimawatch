Sind die kommunalen Klimaschutzbemühungen noch im Plan?
Wir möchten ein einfach zu verstehendes Tool erstellen, welches diese Frage beantwortet.
Dazu wollen wir geplante Emmissionsminderungsziele mit tatsächliche Emissionsdaten verknüpfen.

[![Diskussion im Chat](https://img.shields.io/matrix/klimawatch:matrix.allmende.io?server_fqdn=matrix.allmende.io&label=Diskussion%20im%20Chat&style=for-the-badge)](https://matrix.to/#/#klimawatch:matrix.allmende.io)

# Wie kann ich die Daten meiner Kommune visualisieren?

In nur zwei Schritten: Du sammelst die Daten, wir visualisieren sie für Dich!
Hier gibt es [eine detaillierte Anleitung dazu](https://codeformuenster.org/klimawatch).


# Technisches

Folgendes mit `python3` laufen lassen (entwickelt unter Fedora 31):

```
pip install plotly pandas numpy scipy --user
python plots.py [stadt.csv]
```

Die `stadt.csv`-Datei sollte dabei wie oben beschrieben erstellt sein.
