---
title: "Doc — Dashboard sul telefono via screenshot in email"
summary: "Pattern per portare una dashboard HTML sul telefono senza hosting né VPN: Playwright headless fotografa ogni tab e le immagini vengono incorporate inline nell'email."
tags: [docs, automation, dashboard]
status: active
created: 2026-06-30
updated: 2026-06-30
related: ["[[doc-email-da-script-macos]]", "[[progetto-finance-dashboard]]", "[[doc-launchd-automazioni-mac]]"]
---

# Doc — Dashboard sul telefono via screenshot in email

Problema: vedere una dashboard locale dal telefono **ovunque** (anche rete dati), senza esporre un
server in internet né installare una VPN. Le alternative live (server locale solo-WiFi, Tailscale,
tunnel pubblici) hanno ciascuna un limite (stessa rete, install, esposizione).

**Soluzione semplice e robusta:** la pipeline che genera la dashboard la **fotografa** e incorpora
le immagini nell'email che invii già ogni mattina (schedulata via [[doc-launchd-automazioni-mac]]).
Sul telefono scorri l'email e vedi tutto; nessun server, nessun allegato da aprire, nessuna
dipendenza dalla WiFi di casa. È uno snapshot, non live.

## Ricetta
1. **Screenshot** con Playwright headless (Chromium): apri `file://.../dashboard.html`, clicca ogni
   tab (`page.evaluate("showTab(i)")`), aspetta il rendering dei grafici (~1.3s), e fai lo
   screenshot dell'elemento attivo. Usa una larghezza ampia (es. 1100px) così le tabelle larghe non
   vengono tagliate, e `device_scale_factor=2` per nitidezza.
2. **Email multipart/related**: corpo `multipart/alternative` (testo + HTML), più ogni PNG come
   `MIMEImage` con header `Content-ID: <tabN>`; nell'HTML referenzi `<img src="cid:tabN">`.

Dettagli di invio (app-password, Keychain, certifi) in [[doc-email-da-script-macos]].
Implementazione concreta in [[progetto-finance-dashboard]].
