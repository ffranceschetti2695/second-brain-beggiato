---
title: "Sessione 2026-07-14-c"
summary: "Corretta la logica delle assumption Tesco (+4%) e Zapp (+2%) nella proposta FC6: ancorate al gap forecast-vs-actual invece che a un tasso YoY che creava doppio conteggio"
tags: [workspace, type/session]
status: done
created: 2026-07-14
updated: 2026-07-14
related: ["[[progetto-fc6-topline-proposal]]", "[[concetto-ancoraggio-assumption-forecast-vs-actual]]", "[[concetto-forecast-adjustment-baked-in-vs-bolt-on]]", "[[data-tesco-pricing-tiers-fc6]]"]
---

## Fatto

Verificata la sezione "Assumption — why +4%" su Tesco UK nella proposta FC6: il paragrafo giustificava l'uplift citando la crescita YoY di giugno 2026 vs giugno 2025 (+3.7%), ma il forecast FC6 originale per Tesco H2 incorporava già ~+3.9% di crescita YoY — applicare un ulteriore +4% sopra quel forecast avrebbe significato un doppio conteggio (assunzione implicita di ~+8%, non +4%).

Corretta la logica: confrontato il forecast FC6 di luglio con l'actual/run-rate dei primi 12-13 giorni di luglio (dato DWH), trovando un gap di +11.6% *sul forecast stesso* — base molto più solida per giustificare un +4% come frazione conservativa. Applicata la stessa verifica a Zapp UK: gap forecast-vs-actual osservato +25.6%, ben oltre il +2% già usato nel modello — upside reale lasciato sul tavolo, per scelta esplicita di Francesco (tenere +2% invariato, solo riscrivere la motivazione).

Editato il documento Word locale (`FC6_Topline_Variance_Proposal.docx`) in tutti i punti coinvolti per coerenza: paragrafo assumption Tesco (Sezione 5), paragrafo assumption Zapp (Sezione 5), intro item B Zapp, e il finding #1 di Sezione 4 — tutti ora usano lo stesso confronto forecast-vs-actual, senza riferimenti alla vecchia logica YoY né a passaggi di ragionamento intermedi non rilevanti per il lettore finale. Aggiunta anche una tabella con i dati luglio FC6-vs-actual nel documento.

Verificato che lo strumento non ha accesso in scrittura diretta al Google Doc collegato (solo lettura/creazione/copia) — le modifiche fatte nel `.docx` locale vanno riportate a mano nel Google Doc condiviso con Sonia/Ricardo/Dimitrij.

## Deciso

- Le assumption percentuali di forecast vanno ancorate al gap forecast-vs-actual dello stesso periodo, non a un tasso YoY — principio generalizzato in una nuova nota concetto, perché il rischio di doppio conteggio non è specifico di Tesco.
- Zapp: +2% resta invariato nonostante il gap osservato molto più ampio (+25.6%) — scelta conservativa esplicita, non un errore da correggere.
- I documenti esterni (Word, Slack, deck) non devono mai contrastare la giustificazione finale con un approccio scartato in precedenza — quel tipo di riferimento ha senso in conversazione ma confonde chi legge un documento finito senza il contesto del backstage.

## Aperto

Nessun nuovo step aperto da questa sessione.
