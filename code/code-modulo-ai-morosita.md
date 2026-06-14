---
title: Modulo AI Previsione Morosità
summary: Componente di AuroraGest che predice la probabilità di morosità per ogni conduttore, lanciato a gennaio 2024.
tags: [code, ai, morosita, auroragest, machine-learning]
status: active
created: 2026-06-14
updated: 2026-06-14
related: ["[[entity-auroragest]]", "[[area-prodotto-tech]]", "[[persona-luca-bianchi]]"]
---

# Modulo AI Previsione Morosità

**Stato:** in produzione da gennaio 2024
**Owner tecnico:** [[area-prodotto-tech]] — team Data & AI (8 persone)

## Funzionamento

Il modulo analizza lo storico dei pagamenti di ogni conduttore all'interno di [[entity-auroragest]] e produce un punteggio di rischio morosità aggiornato mensilmente. In caso di rischio elevato, genera un alert automatico al property manager.

## Performance dichiarata

- Riduce del **60%** le sorprese negative (morosità non anticipate) per i clienti.
- Allenato su 18+ mesi di dati reali al momento del lancio — vantaggio competitivo vs competitor che stanno costruendo la stessa feature nel 2025.

## Infrastruttura

Gira su AWS EU. I dati usati per il training sono anonimizzati e aggregati per cliente. Owner del progetto: [[persona-luca-bianchi]] (CTO).
