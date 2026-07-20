---
title: "FC6 Topline Proposal 2026"
summary: "Proposta per portare il topline FC6 (UK+FR+PL) sopra la soglia di €50m richiesta dagli investitori; lavoro nel folder esterno ~/Desktop/FC6_Topline_Proposal/."
tags: [projects, stuart, fc6, forecasting]
status: active
created: 2026-07-14
updated: 2026-07-14
related: ["[[entity-stuart]]", "[[self-franceschetti]]", "[[persona-ricardo-amorim]]", "[[persona-sonia-gastelum]]", "[[persona-dimitrij-phoursa]]", "[[concetto-pricing-tier-decoupling-ricavo-margine]]", "[[data-tesco-pricing-tiers-fc6]]", "[[concetto-forecast-adjustment-baked-in-vs-bolt-on]]", "[[concetto-ancoraggio-assumption-forecast-vs-actual]]", "[[data-tesco-reforecast-luglio-2026-zone-exits]]"]
---

# FC6 Topline Proposal 2026

## Contesto

Il reforecast FC6 2026 (UK+FR+PL) risulta sotto il ricavo actual 2025, cosa segnalata dagli investitori. [[persona-ricardo-amorim]] (VP Revenue) non ha prodotto una proposta di suo, quindi [[self-franceschetti]] ha costruito l'analisi di scostamento e la proposta topline al posto suo.

## Obiettivo

Identificare segmenti/clienti dove il topline FC6 può essere rivisto al rialzo, in modo che il gruppo superi una soglia minima di **€50m** (hard floor: può essere superata ma non violata).

## Deliverable

Tre output, non tracciati in questo vault (lavoro esterno):
- Documento Word — analisi di scostamento (FC6 vs BP'26, FC6 vs FC3, ogni segmento di ogni mercato) + proposta.
- Excel — copia del file FC6 sorgente con ogni aggiustamento incorporato direttamente negli input del modello (non colonne di overlay — vedi [[concetto-forecast-adjustment-baked-in-vs-bolt-on]]).
- Messaggio Slack (bozza, non inviato) al gruppo con Sonia Gastelum, Ricardo Amorim, Dimitrij Phoursa.

Cartella di lavoro: `~/Desktop/FC6_Topline_Proposal/`. Contiene un proprio `CLAUDE.md` (contesto completo, cifre correnti, regole da seguire) e `EDITS.md` (log delle modifiche round per round) — quei file sono la fonte di verità aggiornata, non questa nota.

## Meccanismo della proposta (sintesi)

Quattro aggiustamenti, tutti incorporati direttamente negli input (Volume/RPO) dei tab del modello, non come overlay separato:
- Tesco UK — giugno sostituito con l'actual DWH; luglio-dicembre ri-prezzato secondo la struttura a tier del contratto Tesco ([[data-tesco-pricing-tiers-fc6]], [[concetto-pricing-tier-decoupling-ricavo-margine]]).
- Zapp UK — volume H2 +2%.

Le assumption percentuali di Tesco (+4%) e Zapp (+2%) sono ancorate al gap tra il forecast FC6 stesso e l'actual/run-rate dello stesso mese (luglio), non a un tasso di crescita YoY vs 2025 — vedi [[concetto-ancoraggio-assumption-forecast-vs-actual]] per il perché (il forecast FC6 di Tesco incorporava già ~+3.9% di crescita YoY, quindi ancorare al 2025 avrebbe fatto doppio conteggio). Per Zapp il gap forecast-vs-actual osservato è molto più ampio (+25.6%) del +2% applicato — scelta deliberatamente conservativa, upside non reclamato lasciato sul tavolo.
- FR Existing SMB — RPO portato all'actual DWH di giugno (+ ancillary SMS/PIN in discussione).
- Sushi Shop FR — volume H2 +15%, **percentuale non ancora ben ancorata a un dato reale** (vedi punti aperti).

Le cifre esatte cambiano round su round — per il numero corrente, consultare `CLAUDE.md` nella cartella di lavoro, non questa nota.

## Punti aperti

- **Tesco (item A) non accettato dall'account manager Stuart** (non da Tesco come cliente): Stuart ha deciso di uscire da alcune zone/città UK non profittevoli o con problemi di performance sull'account Tesco, quindi il re-forecast H2 2026 condiviso mostra volumi in **calo**, non la crescita +4% proposta — vedi [[data-tesco-reforecast-luglio-2026-zone-exits]]. Gli altri tre item (Zapp, FR Existing SMB, Sushi Shop) sono stati accettati. Il landing point revenue 2026 va ricalcolato tenendo conto di questo scostamento su Tesco.
- Sushi Shop: il +15% di volume H2 non ha un'ancora quantitativa solida. Trovato un pilot reale (autodispatcher live in 3 store Parigi, 2 su 3 già al 100% di share of wallet) ma senza piano di rollout confermato per il resto dell'anno — decisione ancora da prendere su come trattarlo.
- Pipeline (UK e FR) e Mid-Market restano leve non quantificate per chiudere ulteriormente il gap vs 2025 actual.
- Il buffer sopra la soglia €50m è stretto — ogni round di modifica va rivalidato per essere sicuri che il floor sia ancora rispettato (sia su base Ricavo che su base Gross Margin).
- Il documento Word vive anche come Google Doc condiviso (link con Sonia/Ricardo/Dimitrij). Lo strumento non ha accesso in scrittura diretta a Google Docs (solo lettura/creazione/copia) — ogni modifica va fatta prima nel `.docx` locale, poi riportata a mano nel Google Doc.
