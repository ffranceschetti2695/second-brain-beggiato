---
title: "Doc — Inviare email da uno script su macOS"
summary: "Ricetta per mandare email da uno script Python su Mac via Gmail SMTP: app-password (non la password normale), salvata nel Keychain, più il fix dei certificati SSL del Python.framework con certifi."
tags: [docs, automation, macos, email]
status: active
created: 2026-06-30
updated: 2026-06-30
related: ["[[doc-launchd-automazioni-mac]]", "[[progetto-finance-dashboard]]"]
---

# Doc — Inviare email da uno script su macOS

Tre cose non ovvie scoperte mandando l'email mattutina della [[progetto-finance-dashboard]]
(lo script è schedulato via [[doc-launchd-automazioni-mac]]).

## 1. Serve una "app-password", non la password Gmail
Gmail rifiuta il login SMTP con la password normale. Vai su myaccount.google.com → Sicurezza →
(verifica in 2 passaggi ATTIVA) → "Password per le app" → genera 16 caratteri. Togli gli spazi.

## 2. Salva la password nel Keychain, non in un file
```bash
security add-generic-password -s <servizio> -a <account@gmail.com> -w "app-password-16-char"
```
Lo script la legge senza mai scriverla in chiaro:
```bash
security find-generic-password -s <servizio> -a <account@gmail.com> -w
```
(Il comando fallisce stampando l'help se la password ha spazi o `-w` non è l'ultima opzione.)

## 3. Fix certificati SSL del Python.framework
Il Python di python.org su macOS non usa il cert store di sistema → `SSLCertVerificationError`.
Usa il bundle di `certifi`:
```python
import ssl, certifi
ctx = ssl.create_default_context(cafile=certifi.where())
with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as s:
    s.starttls(context=ctx); s.login(sender, pw); s.send_message(msg)
```

Per email visive (immagini inline) vedi [[doc-dashboard-telefono-screenshot-email]].
