---
title: "Core / Adapters / Presentation"
summary: "Separare logica pura, accesso ai dati e presentazione: rende un tool personale testabile e convertibile in SaaS cambiando solo lo strato dati e l'hosting."
tags: [concepts, architettura, saas]
status: active
created: 2026-06-30
updated: 2026-06-30
related: ["[[progetto-finance-dashboard]]", "[[concetto-automazione-local-first]]", "[[concetto-saas-metrics]]", "[[doc-stuart-design-system]]"]
---

# Core / Adapters / Presentation

Pattern di struttura usato nella [[progetto-finance-dashboard]] per tenere il progetto pulito e
pronto a diventare prodotto. Tre strati con dipendenze a senso unico:

- **`core/`** — logica pura, niente rete né I/O: calcoli, regole di business, categorizzazione,
  date. Dipende solo dalla standard library → testabile e portabile tale e quale.
- **`adapters/`** — accesso ai dati per-fonte (una banca, un export, un'API). Ogni fonte è un
  adapter sostituibile; il resto del sistema non sa da dove arrivano i dati.
- **`presentation/`** — output verso l'umano (HTML, email, notifiche). Nessuna logica di business.
  Quando l'output va mostrato o presentato a terzi conviene renderlo on-brand: per Stuart vedi
  [[doc-stuart-design-system]].

**Perché conta (il "seam" SaaS):** per trasformare un tool personale in SaaS multi-tenant cambi
solo gli **adapters** (da "leggi il mio file" a "aggregatore con licenza per N utenti") e
l'**hosting**. Il `core` — la parte che vale — resta identico. La versione locale di oggi è il
prototipo che valida il prodotto su un utente reale prima del salto (vedi le [[concetto-saas-metrics]]
che contano nel passaggio a prodotto).

Si combina con [[concetto-automazione-local-first]]: gli adapter sono anche il punto in cui decidi
dove gira l'accesso ai dati (locale vs cloud).
