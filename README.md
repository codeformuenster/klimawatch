Sind die kommunalen Klimaschutzbemühungen (noch) im Plan?
Wir möchten eine einfach zu verstehende Homepage erstellen, welche diese Frage beantwortet.

Dazu wollen wir geplante Emissionsminderungsziele mit tatsächlichen Emissionsdaten
verknüpfen und für möglichst viele Kommunen Deutschland anzeigen.
Darüber hinaus wollen den Status einzelner Module von kommunalen
Klimaschutzkonzepten visualisieren.
Außerdem möchten wir die Ausbauziele der erneuerbaren Energien visualisieren.

[![Diskussion im Chat](https://img.shields.io/matrix/klimawatch:matrix.allmende.io?server_fqdn=matrix.allmende.io&label=Diskussion%20im%20Chat&style=for-the-badge)](https://matrix.to/#/#klimawatch:matrix.allmende.io)

# Wie kann ich die Daten meiner Kommune visualisieren?

In nur zwei Schritten: Du sammelst die Daten, wir visualisieren sie für Dich!
Hier gibt es [eine detaillierte Anleitung dazu](https://codeformuenster.org/klimawatch/hugo/anleitung).
Wer diesen Text hier liest: Wir freuen uns über einen Pull Request mit der
entsprechenden CSV-Datei (und ggf. auch mit den mit dem Python-Skript
automatisch erstellten Dateien und markdown-Dateien für die Webseite, s.u.).
Danke!

# Technisches

## Generierung der Grafiken:

Folgendes mit `python3` laufen lassen (entwickelt unter Fedora 31):

```
pip install plotly pandas numpy scipy --user
python generate_plots.py [kommune]
```

Dazu muss eine Datei mit dem Namen `kommune.csv` im Ordner `data` liegen.
Diese Datei sollte wie
[in der Anleitung beschrieben](https://codeformuenster.org/klimawatch/hugo/anleitung)
erstellt worden sein.
Wenn alles erfolgreich war, wurden

- eine Datei mit dem Namen `paris_[kommune].html`
  im Ordner `hugo/layouts/shortcodes/` und
- eine Datei `you_draw_it_[kommune]_paris_data.json` mit dem
  verbleibendem Parisbudget im Ordner `hugo/data/`

erstellt.

## Webseite bauen

Die Webseite wird mit dem static site generator `hugo` erstellt.
Deshalb, falls noch nicht geschehen, [`hugo` installieren](https://gohugo.io/)

Dann in den Ordner `hugo` gehen und mit

```
hugo server
```

`hugo` starten.
Nun sollte man mit einem Browser unter [localhost:1313](http://localhost:1313)
eine lokale Kopie der Webseite erreichen können.
Jede Änderung der zugrunde liegenden Dateien sollte live gezeigt werden.

## Inhalte der Webseite

Alle Content-Seiten werden als Markdown-Dateien verwaltet.

Für jede Kommune braucht man eine `content/kommunen/<kommune>.md` Datei.
Für eine neue Kommune bietet es sich an die Datei `content/kommunen/template.md`
zu kopieren und für die neue Kommune anzupassen.

Für übergreifende Seiten s. z.B. `content/anleitung.md` oder `content/paris-limits.md`.
Die Dateien im Ordner `content/sections` erscheinen auf der Startseite als Sections.
Die Datei `content/_index.md` ist die Startseite.

## Layout

In der Datei `config.toml` gibt es viele Einstellungen,
unter anderem auch Farbeinstellungen, die dringend verbessert werden müssten.

## Deployment

Das Deployment der Webseite läuft über github-pages. Dafür wird der Branch
`gh-pages` genutzt.
Das Skript `deploy_site.sh` erledigt alles, um eine neue Version zu deployen:
Es wird mit dem Aufruf `hugo` eine statische Seite im Ordner `public` gebaut,
dann werden diese Dateien in den `gh-pages`-Branch geschoben.
