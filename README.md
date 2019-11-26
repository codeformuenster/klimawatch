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
Wer diesen Text hier liest: Wir freuen uns über [einen Pull Request](https://github.com/codeformuenster/klimawatch/pulls)!
Dann gerne

- mit der entsprechenden CSV-Datei (s. Anleitung) in den Ordner `data`
- den dazugehörigen Quellenangaben als README.md in den Ordner `docs/DEINEKOMMUNE`
- ggf. die mit dem Python-Skript automatisch erstellten Dateien:
    - `hugo/layouts/shortcodes/paris_DEINEKOMMUNE.html`
    - `hugo/layouts/data/you_draw_it_DEINEKOMMUNE_paris_data.json`
- ggf. die manuell angepasste Datei `content/kommunen/DEINEKOMMUNE.md` (gerne an `content/kommunen/template.md` orientieren)

Quellen nicht vergessen! Danke!

# Technisches

## Generierung der Grafiken:

Folgendes wurde alles mit `python3` getetest.
Benötigte Pakete installieren:

### Mit Conda

```
conda env create -f environment.yml
conda activate klimawatch
```
### Direkt mit pip

```
pip install plotly pandas numpy scipy --user
```

### Dann Plots generieren:

```
python generate_plots.py [kommune]
```

Dazu muss eine Datei mit dem Namen `kommune.csv` im Ordner `data` liegen.
Diese Datei sollte wie
[in der Anleitung beschrieben](https://codeformuenster.org/klimawatch/hugo/anleitung)
erstellt worden sein.
Wenn alles erfolgreich war, sollten

- eine Datei mit dem Namen `paris_[kommune].html`
  im Ordner `hugo/layouts/shortcodes/` und
- eine Datei `you_draw_it_[kommune]_paris_data.json` mit dem
  verbleibendem Parisbudget im Ordner `hugo/data/`

erstellt worden sein.

## Webseite bauen

Die Webseite wird mit dem static-site-generator `hugo` erstellt.
Deshalb, falls noch nicht geschehen, [`hugo` installieren](https://gohugo.io/)

Dann in den Ordner `hugo` gehen und mit

```
hugo server
```

`hugo` starten.
Nun sollte man mit einem Browser unter [localhost:1313](http://localhost:1313)
eine lokale Kopie der Webseite erreichen können.
Jede Änderung der zugrunde liegenden Dateien sollte live gezeigt werden.

### Inhalte der Webseite

Alle Content-Seiten werden als Markdown-Dateien verwaltet,
[hier findet sich eine Kurzreferenz](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet).

Für jede Kommune braucht man eine `content/kommunen/<kommune>.md` Datei.
Für eine neue Kommune bietet es sich an die Datei `content/kommunen/template.md`
zu kopieren und für die neue Kommune anzupassen.

Für übergreifende Seiten siehe die Beispielseiten `content/anleitung.md` oder `content/paris-limits.md`.
Die Dateien im Ordner `content/sections` erscheinen auf der Startseite als Sections.
Die Datei `content/_index.md` ist die Startseite.

### Layout

In der Datei `config.toml` gibt es viele Einstellungen,
unter anderem auch Farbeinstellungen, die dringend verbessert werden müssten.
Im Ordner `themes/assets` finden sich viele CSS-Einstellungen.

### Deployment

Das Deployment der Webseite läuft über github-pages. Dafür wird der Branch
`gh-pages` genutzt.
Das Skript `deploy_site.sh` erledigt alles, um eine neue Version zu deployen:
Es wird mit dem Aufruf `hugo` eine statische Seite im Ordner `public` gebaut,
dann werden diese Dateien in den `gh-pages`-Branch geschoben.
