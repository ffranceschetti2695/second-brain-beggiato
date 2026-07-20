---
title: "Sessione 2026-07-13-f"
summary: "Costruzione nota BP26 topline (paese, cliente/segmento, pipeline ENT/MM/SMB riconciliata), verificata quadratura GM €9.194.636 e coerenza con la nota FC3 esistente"
tags: [workspace, type/session]
status: done
created: 2026-07-13
updated: 2026-07-13
related: ["[[data-bp26-topline-2026]]", "[[data-fc3-baseline-2026]]", "[[data-fc3-2026-mensile]]", "[[entity-stuart]]", "[[concetto-rpo-cpo-slo]]"]
---

## Fatto

Creata la nota `data-bp26-topline-2026` a partire dal file `BP '26 - Topline figures (1).xlsx`: GM/Volume/Gross Revenue/Total Cost mensili e annui per paese (UK/FR/PL), per cliente/segmento e per la pipeline, con RPO/CPO derivati via formula (RPO = GR/Volume, CPO = Total Cost/Volume). Germania (JET-DE) esclusa su richiesta esplicita. Verificata la quadratura: GM globale 2026 = €9.194.636, identico al valore di riferimento dato da Francesco.

Per la pipeline, prima estrazione (tab Pipeline Breakdown, blocco prima di colonna P) dava uno split ENT/MM/SMB che non riconciliava (GM €704.052 invece di €1.042.773) perché quel blocco usa la vecchia cost allocation. Corretto usando il blocco dopo colonna P (rollup "Global" per segmento + check "New Allocation" ≈ 0 nella fonte stessa), che riconcilia esattamente sia a livello globale (ENT/MM/SMB) sia per paese, e aggiunto anche lo split mensile per segmento.

Infine verificata la nota FC3 esistente (`data-fc3-baseline-2026`, `data-fc3-2026-mensile`) contro il file sorgente `FC3 Official Forecast – March '26.xlsx`: i numeri tornano esatti (residuo di gennaio già documentato), la segmentazione pipeline ENT/SMB/MM era già presente ed è il modello replicato per BP26, la Germania non compare in FC3 (già a zero). Nessuna inconsistenza trovata da correggere.

## Deciso

Quando una fonte Excel ha più blocchi che sembrano ridondanti (es. dati prima/dopo una colonna), non fidarsi del primo trovato: verificare quale blocco riconcilia contro un totale di controllo noto prima di usarlo in una nota. La quadratura contro un numero di riferimento fornito dall'utente è il test definitivo, non l'apparente completezza dei dati.

## Aperto

Nessun nuovo step aperto emerso in questa sessione.
