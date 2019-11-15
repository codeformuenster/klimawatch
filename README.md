# Seite anzeigen

[Hugo installieren](https://gohugo.io/)

Dann mit 

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
