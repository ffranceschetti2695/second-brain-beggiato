---
title: "Doc — Automazioni locali su Mac con launchd"
summary: "Come schedulare e triggerare automazioni locali su macOS con launchd: esecuzione a orario fisso, trigger su cambiamento di una cartella, e perché è meglio di cron."
tags: [docs, automation, macos]
status: active
created: 2026-06-30
updated: 2026-06-30
related: ["[[concetto-automazione-local-first]]", "[[progetto-finance-dashboard]]", "[[doc-email-da-script-macos]]"]
---

# Doc — Automazioni locali su Mac con launchd

Per automazioni che girano sul Mac, **launchd** è preferibile a cron: recupera un job mancato al
risveglio del Mac (cron lo salta e basta) e gestisce i trigger su eventi. I file `.plist` vanno in
`~/Library/LaunchAgents/`. È lo scheduler con cui si concretizza il principio
[[concetto-automazione-local-first]] (rete e secret sul Mac); il job tipico lancia uno script che,
tra le altre cose, manda un'email (vedi [[doc-email-da-script-macos]]).

## Due trigger usati nella finance dashboard

**A orario fisso** (`StartCalendarInterval`) — es. ogni mattina alle 7:50:
```xml
<key>StartCalendarInterval</key>
<dict><key>Hour</key><integer>7</integer><key>Minute</key><integer>50</integer></dict>
```

**Su cambiamento di una cartella** (`WatchPaths`) — scatta quando il contenuto cambia, es. quando
scarichi un file in ~/Downloads (pattern "auto-ingest"):
```xml
<key>WatchPaths</key>
<array><string>/Users/<user>/Downloads</string></array>
```
Lo script innescato deve essere **idempotente** (WatchPaths scatta a ogni modifica: se non c'è nulla
da fare, esce).

## Attivare / testare / disattivare
```bash
cp tuo.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/tuo.plist   # carica
launchctl kickstart -k gui/$(id -u)/<label>                        # esegui subito (test)
launchctl bootout  gui/$(id -u)/<label>                            # scarica
```
Nota: ri-lanciare `bootstrap` su un agent già caricato dà "Bootstrap failed: 5: Input/output error"
— significa solo che è già attivo; fai prima `bootout`. Usa il path **assoluto** dell'interprete
(es. `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3`), launchd non eredita il PATH.

Esempio completo: i 3 plist (`daily`, `downloads`, `server`) in [[progetto-finance-dashboard]].
