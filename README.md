Sind die kommunalen Klimaschutzbemühungen (noch) im Plan?
Wir möchten eine einfach zu verstehende Homepage erstellen, welche diese Frage beantwortet.

Dazu wollen wir geplante Emissionsminderungsziele mit tatsächlichen Emissionsdaten
verknüpfen und für möglichst viele Kommunen Deutschland anzeigen.
Darüber hinaus wollen den Status einzelner Module von kommunalen
Klimaschutzkonzepten visualisieren.
Außerdem möchten wir die Ausbauziele der erneuerbaren Energien visualisieren.

[![Diskussion im Chat](https://img.shields.io/matrix/klimawatch:tchncs.de?server_fqdn=matrix.tchncs.de&label=Diskussion%20im%20Chat&style=for-the-badge)](https://matrix.to/#/#klimawatch:tchncs.de)

# Wie kann ich die Daten meiner Kommune visualisieren?

In nur zwei Schritten: Du sammelst die Daten, wir visualisieren sie für Dich!
Hier gibt es [eine detaillierte Anleitung dazu](https://klimawatch.codefor.de/anleitung).
Wer diesen Text hier liest: Wir freuen uns über [einen Pull Request](https://github.com/codeformuenster/klimawatch/pulls)!
Dazu bitte gerne folgendes tun

- die entsprechende CSV-Datei (s. Anleitung) in den Ordner `data` packen
- eine entsprechende Zeile in `meta.csv` hinzufügen
- die Datei `python create_markdown.py kommune` ausführen
- Korrektur lesen (s. Ausgabe vom Skript)
- Pull Request :tada:

Quellen und Ansprechpartner nicht vergessen! Super wäre auch, wenn wir direkt im Pull Request Dateien editieren könnten ([Anleitung](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/allowing-changes-to-a-pull-request-branch-created-from-a-fork)). Danke!

Bei Fragen gerne im Chat melden:
[![Matrix-Chat](https://img.shields.io/matrix/klimawatch:tchncs.de?server_fqdn=tchncs.de&label=Diskussion%20im%20Chat&style=for-the-badge)](https://matrix.to/#/#klimawatch:tchncs.de)
Wer im Open-Knowledge-Foundation-Germany-Slack ist: Es gibt dort einen #klimawatch-Channel (der gleiche Chatraum wie der Matrix-Chat).


# Technisches

## Generierung der Grafiken:

### Mit Docker

1. Conda Docker Image bauen: im Verzeichnis `docker/conda` das Script `docker-build.sh` ausführen
2. Nun können aus dem Hauptverzeichnis heraus die Scripte
	- `docker/generate_plots.sh` und
	- `docker/hugo.sh`
        verwendet werden, ohne dass Conda und Hogo lokal installiert sein müssen.

### Ohne Docker

Folgendes wurde alles mit `python3` getetest.
Benötigte Pakete installieren:

### Mit Conda

```
conda env create -f environment.yml
conda activate klimawatch
```
### Direkt mit pip

```
pip install -e .[dev]
```

### Dann Seite inkl. Plots generieren:

```
python create_markdown.py kommune
```

Das Skript konfiguriert das meiste automatisch.
Dazu wird auch ein anderes Skript aufgerufen, welches die Plots generiert.
Dieses Skript lässt sich bei Bedarf auch unabhängig vom `create_markdown.py` aufrufen:


```
python scripts/generate_plots.py kommune [Jahreszahl ab wann Trend berechnet werden soll (Standard: alles)]
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
- eine Datei `content/kommunen/<kommune>.md`.
  Diese Datei sollte Korrektur gelesen werden (am besten mit laufendem hugo
  direkt im Browser) und ggf. verbessert werden.

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

In der Datei `config.toml` gibt es viele Einstellungen.
Im Ordner `themes/assets` finden sich viele CSS-Einstellungen.

### Deployment

Das Deployment der Webseite läuft über `netlify`,  s. https://github.com/codeformuenster/klimawatch/blob/master/netlify.toml.
Der `master`-Branch läuft somit automatisch auf https://klimawatch.codefor.de.

# Rechtliches

Der Quelltext dieses Projekts ist lizenziert unter der Apache 2.0 Lizenz:

```
Copyright 2019 Klimawatch Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use these files except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

Für die beigefügte Programmbibliothek `hugo/assets/js/d3v4.js` gilt folgende Lizenzbedingung:

```
Copyright 2010-2017 Mike Bostock
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the author nor the names of contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```

Für die beigefügte Programmbibliothek `hugo/assets/js/plotly-1.51.2.min.js` gilt folgende Lizenzbedingung:

```
The MIT License (MIT)

Copyright (c) 2016-2019 Plotly, Inc

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

Für die beigefügte Programmbibliothek `hugo/assets/js/you_draw_it_template.js` gilt folgende Lizenzbedingung:

```
Original file from https://github.com/EE2dev/you-draw-it by Mihael Ankerst

Copyright 2018 Mihael Ankerst
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the author nor the names of contributors may be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```
