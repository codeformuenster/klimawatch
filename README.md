Sind die kommunalen Klimaschutzbemühungen noch im Plan?
Wir möchten ein einfach zu verstehendes Tool erstellen, welches diese Frage beantwortet.
Dazu wollen wir geplante Emmissionsminderungsziele mit tatsächliche Emissionsdaten verknüpfen.

[![Diskussion im Chat](https://img.shields.io/matrix/klimawatch:matrix.allmende.io?server_fqdn=matrix.allmende.io&label=Diskussion%20im%20Chat&style=for-the-badge)](https://matrix.to/#/#klimawatch:matrix.allmende.io)

# Wie kann ich die Daten meiner Kommune visualisieren?

In nur zwei Schritten: Du sammelst die Daten, wir visualisieren sie für Dich!
Hier gibt es [eine detaillierte Anleitung dazu](https://codeformuenster.org/klimawatch).

```
pip install plotly pandas numpy scipy --user
python plots.py [stadt.csv]
```

Die `stadt.csv`-Datei sollte dabei wie oben beschrieben erstellt sein.

# Seite anzeigen

[Hugo installieren](https://gohugo.io/)

Dann in den Ordner `hugo`gehen und mit 

```
hugo server
```

`hugo` starten. Dann mit dem Browser auf [localhost:1313](http://localhost:1313) gehen.
Nun wird jede Änderung live gezeigt.

Wenn man nur `hugo` ausführt wird der Ordner `public` angelegt, der dann eine vollständig funktionierende Seite enthält.

# Content

Alle Content-Seiten werden als Markdown-Dateien verwaltet.
Für übergreifende Seiten s. z.B. `content/anleitung.md` oder `content/paris-limits.md`.

Für jede Kommune gibt es eine `content/kommunen/<kommune>.md` Datei.
Die Dateien im Ordner `content/sections` erscheinen auf der Startseite als Sections. Die Datei `content/_index.md` ist die Startseite.

# Layout

In der Datei `config.toml` gibt es viele Einstellungen, unter anderem auch Farbeinstellungen, die dringend verbessert werden müssten.



