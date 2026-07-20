# Skill: mbr-finance-section

Costruisce la sezione finance del Monthly Business Review di Stuart: 5 slide — "Next steps", "Company Performance overview", bridge GM del mese (2/3), bridge GM YTD (3/3, doppio grafico GR+GM), weekly pacing del mese in corso — partendo da DWH, export FC3 completo, e OPS Tracker. E' il blueprint end-to-end collaudato il 2026-07-08/09/10 su giugno/luglio 2026, con un secondo ciclo di rifinitura (recap next steps + narrativa parlata + confronto mese precedente) verificato il 2026-07-09/13. Include anche lo stile visivo (brand Stuart) e un prompt pronto per generare le slide con un tool AI (es. Claude Design).

**TRIGGER:**
Invoca questa skill quando l'utente dice "sezione finance del MBR", "MBR finance section", "prepara le slide del MBR", "aggiorna le slide della company performance", o chiede di costruire/aggiornare le slide Next steps / GM performance / weekly breakdown della Monthly Business Review.

---

## Regole generali (applica sempre)

- Date in formato `YYYY-MM-DD`, mai relative.
- Fonte actuals = **DWH**, sempre (query in [[code-query-actuals-dwh]]). Mai i valori della sheet dashboard.
- Baseline di confronto = **FC3** per default. Se l'utente non specifica, chiedi (in passato si e' usato anche BP'26 per lo stesso deck: verifica sempre quale vuole prima di costruire i bridge — non assumerla dal titolo della slide precedente).
- Non inventare numeri: ogni cifra arriva da DWH, dall'export FC3, o dall'OPS Tracker. Se un dato manca, fermati e chiedi.
- Verifica sempre la quadratura dei bridge (Volume, GR, GM): la somma dei delta per barra deve coincidere col delta del totale (check = 0).
- **Le slide di "Company Performance" (overview + 2 bridge) riportano il mese appena chiuso.** La slide "weekly pacing" invece riporta il **mese in corso** (quello non ancora chiuso, tipicamente il mese successivo a quello degli altri slide) — sono due periodi diversi, non confonderli. Verifica sempre con l'utente quale mese/periodo serve per ciascuna slide prima di tirare i dati.
- Il contenuto finale delle slide e' materiale di lavoro mensile, non conoscenza statica: **non salvarlo come nota nel vault** (vedi soglia in CLAUDE.md). Va compilato in un file fuori dal vault (es. sul Desktop) e poi buttato via a fine mese.

---

## Materiali di riferimento (leggi prima di tutto)

1. `docs/doc-flusso-performance-mensile.md` e la skill `performance` — il flusso bridge Actual vs FC3 di base (qui adattato al layout delle slide MBR).
2. `code/code-query-actuals-dwh.md` — query SQL canonica per gli actuals.
3. `data/data-stuart-segmentazione-clienti.md` — mapping cliente -> barra del waterfall.
4. `concepts/concetto-bridge-waterfall.md` — teoria delle 7 barre.
5. `docs/doc-stuart-design-system.md` — brand tokens (colori, font, spaziature) per lo stile delle slide.
6. **Export FC3 completo** (PDF o Excel, tipicamente in `~/Downloads`, titolo tipo "Revenue to GM - FC3 - March 2026 ... Export to DWH") — contiene Volume/GR/GM per cliente per tutti i 12 mesi. E' la fonte primaria per i mesi diversi da maggio: i file del vault (`data/data-fc3-baseline-2026.md`, `data/data-fc3-2026-mensile.md`) coprono solo il dettaglio cliente di maggio e il GM mensile aggregato per paese — non bastano da soli per costruire i bridge di un mese diverso. Se non lo trovi in Downloads, chiedilo all'utente.
7. **OPS Tracker** (Google Sheet, nomi visti finora: "Claude.ia | GM - OPS Tracker", "OPS - GM Tracker") — tab `GM Tracker - Weekly` e `GM Tracker - Monthly`, per la slide weekly pacing.
8. **Stuart Brain App** (fuori dal vault, cartelle viste finora sul Desktop: "Stuart Brain App", `company-brain-app`, `company-brain-rag` — verifica quale esiste ed e' popolata) — fonte primaria e piu' rapida per il "perche'" dietro i numeri quando si costruisce la narrativa parlata (non le slide-bullet, la narrazione da presentare a voce): contiene note gia' sintetizzate su singoli account/temi (es. `concetto-carrefour-rpo-gap-q4-rfp`, `concetto-amrest-slo-volume-decline`, `concetto-tesco-h2-2026-rfp-outcome`, `concetto-fc6-tesco-strategia-investimento-zone-store`). **Controlla sempre qui prima di cercare su Slack/Gmail/Confluence** per il contesto commerciale/operativo dietro un numero — di solito e' piu' rapido e gia' verificato. Cerca su Slack solo se il Brain App non copre il tema o se l'utente chiede esplicitamente un aggiornamento piu' fresco (vedi CLAUDE.md sul divieto di default di cercare su strumenti esterni).

---

## Deviazioni metodologiche note (per non inventare numeri)

### Intermarché

L'export FC3 non isola Intermarché come cliente separato in nessun mese (tranne un valore di riconciliazione manuale gia' fatto per maggio, congelato in `data-fc3-baseline-2026.md`). Per costruire i bridge senza inventare numeri: **tieni Intermarché dentro Mid-Market** (non FR Top) sia lato Actual sia lato FC3, sui due lati allo stesso modo. Questo diverge dal mapping ufficiale DWH (`data-stuart-segmentazione-clienti.md`, che mette Intermarché in FR Top), ma e' l'unico modo per restare metodologicamente coerenti senza stime inventate. Effetto tipico ~€10k/mese: segnalalo sempre nell'output come nota metodologica.

### YTD: escludere i mesi pre-freeze del FC3 (fondamentale, scoperto il 2026-07-09)

**Il bridge YTD non deve includere i mesi precedenti al congelamento del FC3.** FC3 e' stato congelato a marzo 2026: le sue colonne di gennaio e febbraio non sono vere previsioni, sono semplicemente gli actual noti al momento del freeze. Confrontare Actual vs FC3 per gen/feb non misura una vera varianza di forecast, misura solo rumore di restatement (numeri che nel frattempo sono stati corretti/riclassificati nel DWH).

**Il numero di mesi da escludere dipende da QUALE piano e' la baseline, non e' sempre "gennaio-febbraio"**: ogni piano (FC3, FC6, BP, ecc.) e' stato congelato in un mese diverso, e tutti i mesi precedenti al suo freeze vanno esclusi dalla varianza.

- **FC3** → congelato a marzo 2026 → escludi **gennaio-febbraio** (variance parte da marzo).
- **FC6** → congelato a giugno 2026 → escludi **gennaio-maggio** (variance parte da giugno).
- Per qualunque altro piano, verifica/chiedi il mese di freeze prima di impostare il taglio — non assumerlo per analogia con FC3.

**Come verificarlo prima di costruire il bridge YTD (a prescindere dal piano):**
1. Identifica il mese di freeze del piano in uso; i mesi precedenti sono quelli da escludere dalla variance.
2. Calcola il delta (Actual − piano) per quei mesi, sia a livello di singola barra sia totale.
3. Se il delta totale e' vicino a zero, tutto ok, il problema e' trascurabile.
4. Se non e' vicino a zero, scomponi barra per barra: nel caso verificato (FC3, giugno 2026), Tesco e UK Top avevano gia' delta ~€0 per gen+feb, ma **PL Top** aveva un'anomalia di riconciliazione tariffaria enorme e isolata a gennaio (legata alla stessa dinamica di additional RPO PL AmRest/JET, ma eccezionalmente ampia quel mese, ~€17k su GM), e **SMB** aveva un surplus di gen+feb (~+€75k GR) che mascherava un miss reale marzo-giugno. Il netto tra le barre puo' sembrare piccolo pur essendo la somma di errori grandi che si compensano — non fermarti al totale, controlla ogni barra.
5. **Costruisci il bridge YTD usando solo (mese-di-freeze)-mese_corrente come base di variance** (i mesi pre-freeze esclusi dal delta). I totali "di fine anno" mostrati sul grafico possono comunque riportare i valori pieni gennaio-mese_corrente (miscelando i veri actual dei mesi esclusi su entrambi i lati, cosi' il totale resta significativo), ma il delta per barra e la narrativa vanno calcolati solo sul periodo post-freeze.
6. Segnala sempre questa scelta metodologica esplicitamente nella slide (es. sottotitolo "Mar-Jun'26 variance" per FC3, "Jun-Jun'26 variance" o simile per FC6) — non lasciarla implicita.

### Decomposizione volume vs rate (per verificare affermazioni tipo "e' un miss di volume, il rate ha tenuto")

Prima di scrivere in una narrativa che un miss di GM e' "puro volume" o "anche di rate/margine", verifica sempre con questa scomposizione invece di fidarti della frase di un PDF di riferimento o di una nota precedente:

1. `GM-del_FC3 = GM_FC3 / Volume_FC3`; `GM-del_Actual = GM_Actual / Volume_Actual`.
2. `Effetto volume = (Volume_Actual - Volume_FC3) x GM-del_FC3`.
3. `Effetto rate = (GM-del_Actual - GM-del_FC3) x Volume_Actual`.
4. La somma dei due deve tornare (circa) al delta di GM totale della barra — se non torna, c'e' un errore nei dati di input, non nella formula.

**Occhio a non confondere l'effetto rate su GR con l'effetto rate su GM**: un RPO sopra piano (rate positivo su GR) puo' essere quasi completamente eroso da un CPO che sale quasi altrettanto (rate negativo sui costi), lasciando il GM-del praticamente flat — in quel caso il miss di GM resta "puro volume" anche se GR aveva una storia di rate reale. Verificato su Tesco maggio 2026: RPO +€0.58/del vs FC3, ma CPO +€0.57/del vs FC3, quindi GM-del quasi invariato (+€0.008/del) e il miss di GM (-€25k) era per il 100% circa effetto volume (-€28.5k) con un piccolo residuo positivo di rate (+€3.6k) — non un problema di margine. Non scrivere "la natura del miss e' cambiata da rate a volume" tra due mesi senza aver fatto questo calcolo per entrambi: puo' sembrare un cambio di natura guardando solo GR, ma essere identico su GM.

### Verificare i meccanismi prima di spiegarli (non inventare la causa di un numero)

Quando un flag narrativo cita un numero "strano" (es. un RPO che scende improvvisamente, un CPO che sfora), **non improvvisare un meccanismo plausibile** (es. "probabilmente e' una soglia a scaglioni che si applica retroattivamente") senza verificarlo in una nota del Brain App o chiedendolo. Un meccanismo sbagliato ma plausibile e' peggio di dire "non lo so" — l'utente lo puo' presentare live come fatto.

Caso verificato (2026-07-13): Tesco ha davvero un RPO a scaglioni su volume mensile (sotto 400k = £4.68, 400-430k = £4.43, sopra 430k = £4.40, fonte `concetto-fc6-tesco-strategia-investimento-zone-store`), ma lo scaglione si valuta sul **totale di fine mese**, non si applica retroattivamente a meta' mese. Se a meta' mese il tracker mostra gia' il rate del nuovo scaglione, e' quasi certamente una **proiezione del pacing model** (il trend di volume osservato fa prevedere che il mese chiudera' nello scaglione piu' basso), non un rate gia' realizzato sugli ordini fatturati. Distingui sempre, nella narrativa, "il modello ora proietta X" da "abbiamo gia' X" — sono affermazioni diverse e solo la prima e' verificabile a meta' mese.

---

## Passi

### 1. Accesso alla presentazione e scope

Chiedi il link Google Slides e la lista delle slide assegnate all'utente (di solito si ricava dall'agenda, slide 2 del deck). **Se il tool Drive restituisce "ineligible for generative AI contexts"** (capita quando il file ha una sensitivity label — non e' un problema di permessi account, gli altri file Drive dell'utente restano accessibili normalmente), chiedi l'export PDF del deck invece di insistere sul link.

Chiarisci sempre: (a) la baseline (FC3 o BP'26), (b) il mese di riferimento per ciascuna slide (il mese chiuso per overview/bridge, il mese in corso per il weekly pacing).

### 2. Slide 1 — "Next steps from previous MBR"

Leggi il contenuto testuale della slide corrente nel PDF (lista con Sponsor/Owner/Next step per item, categorie tipo Organisational / Strategic-Business / eventuali altre). **Riportalo cosi' com'e'**: e' materiale di lavoro per la review live dell'MBR, non va ricalcolato ne' aggiornato con dati nuovi.

Layout a card colorate (se richiesto): banner navy pieno con titolo + label mese in ciano; pillole categoria (sfondo navy, badge verde col conteggio) affiancate; sotto ogni categoria, card bianche con badge numerato azzurro, titolo bold navy, tag proprietario in pillole azzurre; categoria piu' numerosa a tutta larghezza con card in griglia; footer con nota su quando lo stato viene rivisto.

**Recap risposte owner (se richiesto, es. "raccogli le risposte su Slack ai next steps")**: e' un task separato da questa slide ma spesso richiesto insieme. Cerca su Slack (previa autorizzazione esplicita, vedi CLAUDE.md) i thread/DM dove gli owner hanno risposto al check-in inviato con la skill `stuart-mbr-next-steps-followup`, e produci un recap punto-per-punto breve e presentabile a voce. Se l'utente dice di non aver capito un punto tecnico, fornisci una spiegazione "long form" in linguaggio semplice sotto al recap breve (cosa significa la metrica/processo/problema, perche' conta, senza gergo) — Francesco non e' un esperto di ogni dominio (es. OKR, SLO, breakage fee) e lo ha chiesto esplicitamente il 2026-07-09. Se una ricerca Slack non trova una risposta diretta ma solo conversazioni adiacenti sul tema, dillo chiaramente ("nessuna risposta diretta trovata, ma c'e' discussione correlata in ...") — non presentarlo come "non ha risposto" con certezza assoluta.

### 3. Slide 2 — "Company Performance overview"

KPI globali del mese: Volume, Gross Revenue, GM (+ GM%), RPO, CPO — Actual vs baseline, con delta assoluto e percentuale. Poi una card per paese (UK/FR/PL): ordini, revenue, GM con delta, **piu' una riga di chip per i top client del paese** (nome cliente, delta GM vs baseline, freccia su/giu') — questo dettaglio era nel PDF di riferimento ed e' facile perderlo se non lo si controlla esplicitamente: guarda la slide overview del PDF e riprendi gli stessi client per ogni paese (tipicamente 2-4 per paese, i top account).

Fonte: query DWH del mese (`code-query-actuals-dwh.md`, `month_end_date` = fine mese) aggregata per `country_name` (KPI) e per singolo cliente (chip); baseline dello stesso mese aggregata allo stesso modo dall'export FC3.

### 4. Slide 3 — Bridge del mese (2/3)

Segui il flusso della skill `performance` per costruire i bridge (Volume, GR, GM) a 7 barre per il mese corrente:

1. Actuals DWH con filtro puntuale sul mese, aggregati per `client_forecast_group_adj`.
2. Baseline: leggi dall'export FC3 completo il valore Volume/GR/GM di ogni cliente per quel mese; applica il mapping barra-cliente (vedi deviazione Intermarché sopra).
3. Quadratura: somma dei 7 bar-totali deve combaciare col totale mese noto (da `data-fc3-2026-mensile.md` se disponibile per quel mese).
4. **Narrativa**: replica lo stile del PDF esistente (frase con trattino iniziale, cifre chiave in grassetto, frasi tipo "X e' l'eccezione:", "Y regge meglio del resto"). Non forzare la stessa struttura logica se i fatti sono diversi da quelli del PDF di riferimento — correggi la frase per riflettere il dato vero, non il numero per adattarsi alla frase.

### 5. Slide 4 — Bridge YTD (3/3, due grafici)

**Questa slide ha SEMPRE due grafici affiancati: Revenue Bridge e GM Bridge.** Un errore fatto la prima volta e' stato costruire solo il bridge GM — controlla sempre il PDF di riferimento prima di dare per assodato che serva un solo grafico.

1. Applica la regola "escludere i mesi pre-freeze FC3" (sopra) — di solito significa marzo-mese_corrente, non gennaio-mese_corrente.
2. Servono gli actual DWH di ogni mese nel periodo (query per mese o range, aggregata per barra) e il FC3 di ogni mese dall'export completo.
3. Quadratura sia sul delta totale (somma barre = delta totale) sia sulla plausibilita' di ogni barra presa singolarmente (vedi PL Top/SMB caveat sopra: un errore di segno o di periodo puo' passare inosservato se guardi solo il totale).
4. Narrativa nello stesso stile della slide 3, ma sul periodo YTD (post-freeze) — segnala esplicitamente nel testo che gen-feb sono esclusi e perche'.

### 6. Slide 5 — Weekly pacing (mese in corso, non il mese chiuso)

Fonte: **OPS Tracker**, tab `GM Tracker - Weekly`.

**Non leggere il file intero via Drive connector** — il tab di pacing giornaliero rende il "natural language dump" enorme e costoso in token per pochi dati utili. Chiedi all'utente di scaricare l'Excel (di solito finisce in `~/Downloads`, il nome file puo' cambiare leggermente da un mese all'altro — es. "Claude.ia | GM - OPS Tracker.xlsx" oppure "OPS - GM Tracker (1).xlsx", cerca per pattern `*GM*Tracker*` se il nome esatto non torna), poi parsalo in locale con Python/`openpyxl` leggendo solo i tab `GM Tracker - Weekly` e `GM Tracker - Monthly`.

**Se l'utente dice di aver "aggiornato il file" ma i numeri non cambiano**, controlla `ls -lt` sulla cartella Downloads: probabilmente ha aggiornato il Google Sheet originale ma non ha ancora ri-scaricato/ri-esportato l'Excel — chiedi di ri-scaricarlo.

**Struttura nota del tab "GM Tracker - Weekly"** (verificata 2026-07-08/09/10, puo' cambiare se il file viene ristrutturato — ricontrolla se gli offset non tornano):

- 4 blocchi paese impilati verticalmente, ciascuno con una riga header (colonna B = nome paese: `Global`, `UK`, `FR`, `PL`) seguita da ~40 righe di metriche. Distanza fissa di 41 righe tra un header e il successivo (verificato: header a riga 8/49/90/131).
- Offset fissi dentro ogni blocco (indice riga = riga_header + offset): `Week` +1, `Target Volume` +2, `Actual Volume` +3, `Delta Volume` +4, `Target RPO` +6, `Actual RPO` +7, `Delta RPO` +8, `Target CPO` +10, `Actual CPO` +11, `Delta CPO` +12, `Rate effect` +14, `Volume effect` +15, `Total Cost deviation` +16, `Actual GM` +18, `Target GM-del` +20, `Actual GM-del` +21, `Delta GM-del` +22, `GM RPO Rate effect` +24, `GM CPO Rate effect` +25, `GM Rate effect` +26, `GM Volume effect` +27, `GM Impact` +28. Riga di stato Actual/Forecast a offset +... (riga 6 del foglio, non del blocco — leggi `rows[6]` per la riga globale di status, allineata alle stesse colonne).
- Le colonne sono le settimane: la riga header (riga 8 del foglio) contiene le date di inizio settimana ("Beg. of the week"). Trova le colonne del mese/periodo richiesto filtrando quelle date. La riga 9 contiene il numero di settimana ISO; occhio che una settimana a cavallo di due mesi puo' apparire in entrambi i mesi con lo stesso numero ISO ma in colonne diverse (es. la settimana di fine giugno/inizio luglio appare sia come coda di giugno sia come apertura di luglio).
- **Il "Target" del tab coincide con FC3**, ripartito sulle settimane in proporzione ai giorni (verificato: somma dei Target Volume/RPO/CPO settimanali di un mese = il valore FC3 mensile di quel mese, dentro l'arrotondamento). Non serve ricostruire un target FC3 settimanale a mano.
- `GM Impact` = `Actual GM` − `Target GM` (il delta). `Target GM` settimanale = `Target Volume` × `Target GM-del` (utile se serve isolarlo).
- Il tab `GM Tracker - Monthly` ha la stessa logica ma a livello mensile, con Global/UK/FR/PL in colonne affiancate invece che a blocchi impilati. **E' sempre puntato sul "mese corrente"**: controlla la riga "Month" prima di usarlo, potrebbe gia' essere sul mese successivo a quello che ti serve.
- **Controllo obbligatorio prima di presentare i numeri come reali**: leggi la riga di status (Actual/Forecast) per ogni colonna/settimana usata. Se piu' settimane consecutive mostrano **valori numerici identici** tra loro (Volume/RPO/CPO/GM impact tutti uguali), e' un segnale che il tracker non ha ancora agganciato i dati DWH reali per quelle settimane — sta ripetendo una proiezione flat basata sul target, non pacing reale settimana-per-settimana. Segnalalo esplicitamente nell'output (non presentarlo come se fossero settimane osservate indipendentemente) e usa i tag appropriati: `ACTUAL` per settimane confermate, `CURRENT WEEK` per la settimana che contiene la data di oggi (ancora forecast se non aggiornata), `FORECAST` per le settimane future.

**Output della slide**: card GM landing (globale + 3 paesi, per il **mese in corso**), tabella settimanale (Volume Δ, RPO Δ, CPO Δ, GM impact per settimana e per paese, con tag ACTUAL/CURRENT WEEK/FORECAST), commento narrativo per paese nello stile "Country performance" del PDF di riferimento (RPO outperformance vs CPO overspend, settimana peggiore o punto di svolta, trend nel mese), segnalando dove i dati sono ancora proiezione.

**Sui "flag" narrativi** (es. Tesco RFP, Carrefour RFP): sono narrativa commerciale/deal-specific, non derivano dal tracker. Aggiornali solo se l'utente lo chiede esplicitamente, e solo cercando su Slack se esplicitamente autorizzato (il vault vieta di default la ricerca su strumenti esterni senza richiesta esplicita, vedi CLAUDE.md).

### 7. Output finale (contenuto)

Compila tutto in un documento markdown fuori dal vault (es. `~/Desktop/MBR-<mese>-<anno>-slide-content.md`) con il contenuto di ogni slide, pronto per essere trasferito manualmente nel deck o usato per generare le slide (vedi sezione stile/prompt sotto). Segnala sempre eventuali slide fuori scope (es. accounting/NetSuite non ancora collegato) e perche'.

**Se l'utente chiede un Google Doc invece di un file .md**: non limitarti a convertire il testo, costruisci un HTML ben formattato (h1/h2/h3, `<b>` per i punti chiave, `<table>` per le tabelle di confronto) e usa il tool Drive `create_file` con `contentMimeType: "text/html"` e titolo pulito — Drive lo converte automaticamente in un vero Google Doc (`application/vnd.google-apps.document`) con formattazione preservata. Verificato 2026-07-09.

**Narrativa parlata (discorsiva, non a bullet) e confronto col mese precedente**: se l'utente chiede la "narrativa del mese" oltre al contenuto delle slide, scrivila in paragrafi discorsivi pensati per essere letti/parafrasati a voce (non bullet da slide) — priorita' al Brain App per il contesto reale dietro i numeri (vedi sopra). Se chiede anche il confronto col mese precedente e quel mese usava una baseline diversa (es. BP'26 invece di FC3): **prima di rifare una query DWH**, controlla se il vault ha gia' un bridge di quel mese verificato sulla baseline corretta (es. `data-fc3-baseline-2026.md` contiene un bridge maggio 2026 vs FC3 gia' quadrato, riusabile senza ricalcolo) — spesso il lavoro e' gia' stato fatto in un ciclo precedente e va solo riletto, non ripetuto.

---

## Stile visivo (brand Stuart, per replicare il PDF di riferimento)

Fonte: `docs/doc-stuart-design-system.md`. Il deck segue questo sistema con alcune eccezioni deliberate.

**Colori — due livelli distinti, non confonderli:**
- *Fill* (barre, dot grandi, chip, sfondi): dark blue `#00249c`, Stuart blue `#0192ff`, Stuart green `#27e2a5`, rosso `#e8384f` (eccezione deliberata al brand generale, che evita il rosso — questo deck finance lo usa per i miss), light blue `#87eaff`, yellow `#ffcc36`.
- *Testo* per cifre positive/negative (delta, percentuali): deve essere PIU' scuro/saturato dei fill sopra, altrimenti a dimensione testo il verde/rosso brand risultano slavati e illeggibili. Usa `#0a8f5c` per il testo positivo, `#c8253f` per il negativo. Non renderizzare mai un numero positivo/negativo nel verde/rosso brand grezzo — quelli sono solo per i fill.
- Sfondo slide: non bianco piatto ne' grigio piatto — un neutro molto chiaro con leggera dominante blu (`#f4f6fb`). Le card sopra restano bianco puro `#ffffff`.
- Bordi: hairline 1px, grigio-blu chiaro (`#dde3f0`), mai un bordo pesante o grigio scuro. Ombre soft cool-toned, mai drop-shadow nero generico.

**Tipografia:** GT Walsheim (fallback Poppins, e' il fallback ufficiale Stuart, usabile direttamente). Titoli Black/Bold, sentence case, tracking leggermente stretto. Numeri in tabelle/KPI sempre tabulari (monospaced-digit) per allineamento verticale — dettaglio che da solo separa un deck "professionale" da uno generico.

**Formattazione numeri (convenzione del deck, applicala sempre):**
- Volume, Gross Revenue, GM (valori assoluti e delta): abbreviati al migliaio con suffisso "k", arrotondati (no decimali), tranne dove serve un decimale esplicito (es. "−€6.5k"). Mai il numero completo con virgole, mai in milioni.
- RPO e CPO (€/del o £/del): SEMPRE per intero con 2 decimali (es. "€6.27", "£4.68") — mai abbreviati a k. Questa e' l'unica eccezione alla regola del "k".
- Percentuali come date.

**Grafici waterfall/bridge — regole di costruzione (fondamentali, causa piu' comune di risultati "piatti" o con spazio vuoto):**
- La barra baseline (FC3/Subtotal) deve essere l'elemento piu' alto e occupare circa il 55-60% dell'altezza disponibile del grafico — non di piu': se domina "quasi tutta" l'altezza, gli scostamenti piccoli diventano invisibili (overcorrection verificata: barre baseline troppo dominanti schiacciano i delta a fili illeggibili). Dai a ogni barra di scostamento un'altezza minima visibile (~28-36px) anche quando il valore reale e' piccolissimo (es. −€6k) — priorita' alla leggibilita' di ogni barra, non alla proporzione matematica esatta.
- **Ordina le barre di scostamento dal piu' negativo al migliore (piu' positivo)**, non nell'ordine "naturale" del mapping cliente/segmento — verificato che questo ordinamento (invece di quello per segmento) rende il grafico piu' leggibile e in linea con quanto richiesto in pratica. Ricalcola la sequenza cumulativa nel nuovo ordine (la somma totale dei delta non cambia, cambia solo il percorso a gradini).
- **Se anche dopo le due regole sopra gli scostamenti restano visivamente schiacciati** (tipico quando baseline e delta sono di ordini di grandezza molto diversi, es. bridge YTD con baseline ~€25.000k e delta di poche decine di k): tronca l'asse verticale, facendolo partire non da zero ma da un valore vicino al range effettivo dei dati (es. per un bridge YTD Revenue con range 25.035-25.942k, asse da ~24.500k a ~26.200k), con un simbolo di "asse spezzato" (es. "//") alla base per segnalarlo — convenzione standard nei bridge chart finance quando la baseline e' molto piu' grande degli scostamenti. Non serve per i bridge del solo mese (baseline e delta gia' vicini in scala), ma quasi sempre serve per i bridge YTD.
- Tra ogni barra e la successiva, disegna una linea di connessione tratteggiata sottile (color `#a9bbe0`) dal top della barra corrente al punto di partenza della successiva (nel nuovo ordine, se riordinato) — presente nel PDF, e' il dettaglio che fa leggere il grafico come "vero bridge chart" invece di un bar chart generico. E' obbligatoria su ogni bridge chart del deck.
- Per posizionare correttamente ogni barra, calcola la sequenza cumulativa (partendo dal valore baseline, applicando ogni delta in ordine) — ogni barra copre lo spazio tra due valori consecutivi di questa sequenza. Non posizionare le barre "a occhio". Scrivi sempre la sequenza numerica esplicita nel prompt (non lasciare che il tool la calcoli da solo) — e' la causa piu' comune di bridge chart con gradini sbagliati.
- Larghezza barre generosa (non colonnine sottili) — sia baseline sia scostamenti.
- Barre con un piccolo bordo arrotondato (3-4px) solo sul lato esterno, non completamente a pillola.
- Etichette valore sopra/sotto ogni barra, bold, colore testo-sicuro (vedi sopra), abbastanza grandi da leggersi da fondo sala (min ~16-18px).
- **Testo scritto dentro/sopra le barre blu scure (es. "FC3", "Actual", "Actual YTD") deve essere bianco**, mai un colore scuro che si confonde col fill — se l'etichetta e' lunga (es. "Actual YTD"), valuta di andarla a capo su due righe per restare leggibile.
- **Layout diverso a seconda che la slide abbia uno o due grafici**: la slide con un solo bridge chart (mese corrente) usa due colonne affiancate — grafico a sinistra (~60-65% larghezza), box narrativo tratteggiato a destra (~30-35%). La slide con due bridge chart affiancati (YTD, Revenue+GM) impila invece il box narrativo a piena larghezza SOTTO i due grafici, non a fianco. Non applicare lo stesso pattern a entrambe.

**Nessuno spazio vuoto non stilizzato:** un elemento (slide, card, grafico) con piu' del ~15% della sua area come spazio vuoto non e' accettabile — va corretto aumentando scala/font/spaziatura interna, mai lasciando il vuoto. Le card si dimensionano al contenuto (righe impilate con spaziatura consistente ~16-24px), non a un'altezza fissa scelta a priori.

**Rifiniture verificate causa piu' comune di un secondo giro di correzioni:**
- Slide overview (KPI + card paese): i numeri di scostamento (es. "Δ −90k") devono essere quasi alla pari, per dimensione, col valore principale accanto (es. "471k") — non un dettaglio piccolo a fianco di un numero grande. Riduci anche lo spazio vuoto tra il banner titolo e la barra KPI sottostante, e tra il fondo delle card paese e il bordo inferiore della slide (le card si allargano/distribuiscono il contenuto per riempire, non lasciano un margine bianco residuo).
- Slide con due box bianchi affiancati (es. weekly pacing: commentary a sinistra + tabella a destra): i due box devono finire alla stessa altezza, allineati al contenuto del box piu' "naturale" (tipicamente la tabella) — non stirati fino al bordo inferiore della slide ne' di altezze diverse tra loro.

**Evita i segnali tipici di "AI-generated design"**: gradienti viola-blu, tutto centrato, `rounded-lg` uniforme ovunque, emoji come marker di bullet (le bandiere paese vanno bene, sono dati), barra-accento-su-card ripetuta ovunque, foto stock, texture.

---

## Prompt per generare le slide (Claude Design o altro tool AI)

Quando il contenuto e' pronto, costruisci un prompt **completamente autosufficiente** (ogni numero e ogni frase scritti direttamente nel prompt, nessun riferimento a link/file/artifact esterni che il tool di destinazione non vedrebbe) che includa:

1. Un'istruzione esplicita in apertura: costruire una **presentazione vera** con slide native (titoli, forme, tabelle, grafici come elementi nativi) — non una pagina web, non un mockup HTML, non un documento che scorre. Questo perche' molti tool "AI design" tendono a produrre HTML/canvas anche quando l'output finale e' presentato come slide: l'istruzione deve essere inequivocabile.
2. Le regole di CANVAS (16:9 full-bleed, contenuto che riempie tutta l'altezza, mai raggiunto stirando spazio vuoto ma dimensionando il contenuto stesso).
3. La convenzione di formattazione numeri (sezione sopra).
4. Lo stile brand completo (sezione sopra) — colori fill vs testo, tipografia, bordi/ombre, regole specifiche sui bridge chart con linee di connessione e sequenza cumulativa per il posizionamento barre.
5. Slide per slide, tutto il contenuto (testo delle card, numeri delle tabelle, bullet della narrativa) scritto per intero — non "vedi sopra" o riferimenti a sezioni precedenti del documento.
6. Un self-check finale esplicito da eseguire prima di consegnare: nessuno spazio vuoto >15%, tutte le linee di connessione presenti sui bridge chart, entrambi i grafici della slide YTD presenti (non solo uno), tutti i paragrafi di narrativa mostrati per intero (non troncati), numeri conformi alla convenzione k/decimali, barre di scostamento ordinate dal piu' negativo al migliore con sequenza cumulativa scritta esplicitamente, layout a due colonne per la slide a un solo bridge chart vs narrativa-sotto per quella a due bridge chart, testo bianco leggibile su ogni barra blu scura.

Se il primo output dal tool AI risulta ancora "piatto" o simile a una pagina web: le due cose piu' efficaci da segnalare in un messaggio di follow-up sono (a) "deve essere una slide deck nativa, non una webpage" e (b) "i numeri positivi/negativi sono troppo chiari/slavati, usa le tonalita' testo-sicure indicate, non il colore brand grezzo".

Aspettativa realistica: anche un prompt ottimo porta a una bozza solida on-brand, non a una replica pixel-perfect del PDF al primo tentativo — soprattutto sui bridge chart e sulla tabella settimanale densa. **Prevedi 2-4 giri di correzione via chat nel tool di destinazione** (verificato su un ciclo reale 2026-07-08/11): tipicamente servono, in quest'ordine, (1) un giro sulla logica di posizionamento cumulativo delle barre se il primo tentativo le disegna "a occhio" invece che a gradini, (2) un giro sulla leggibilita' degli scostamenti (altezza minima barre, eventuale asse troncato sui bridge YTD), (3) un giro sulle rifiniture (spazio vuoto residuo, allineamento box, dimensione dei delta vs numero principale). Da' un messaggio di correzione alla volta, verifica lo screenshot/PDF risultante prima di dare il successivo — combinare troppe correzioni in un solo messaggio rende piu' difficile capire quale fix non ha funzionato.

---

## Caveat noti

- **Google Drive**: alcuni file (es. la presentazione stessa) possono restituire l'errore "ineligible for generative AI contexts" per una sensitivity label — non e' un problema di permessi account (altri file Drive restano accessibili normalmente). In quel caso chiedi il PDF.
- **Export FC3 completo**: e' la fonte primaria per i dati mensili di dettaglio cliente; i file del vault (`data-fc3-baseline-2026.md`, `data-fc3-2026-mensile.md`) sono solo una cache parziale (maggio a livello cliente + GM mensile aggregato per paese/globale). Non bastano da soli per un mese diverso da maggio a livello di dettaglio cliente.
- **OPS Tracker**: leggere l'intero file via Drive connector e' inefficiente in token — sempre preferire il parsing locale di un export Excel scaricato dall'utente su tab specifici. Il nome del file puo' cambiare da un mese all'altro.
- **PL AmRest/JET**: GR e GM negli actuals DWH divergono dalla dashboard per additional RPO (scarto variabile, non fisso, vedi `concetto-additional-rpo.md`). Si usano sempre i valori DWH; la barra PL Top assorbe lo scostamento. Lo scarto puo' essere eccezionalmente ampio in certi mesi (visto: gennaio) — non assumere che sia sempre piccolo.
- **YTD e freeze FC3**: non includere mai gen-feb (o i mesi pre-freeze del forecast in uso) nel calcolo della varianza YTD senza prima verificare che il loro delta sia effettivamente ~0 barra per barra. Vedi sezione dedicata sopra.
- **Baseline switch**: lo stesso identico deck puo' passare da BP'26 a FC3 (o viceversa) tra un ciclo e l'altro dell'MBR. Non assumere la baseline dal titolo della slide precedente senza chiedere conferma.
- **Weekly pacing vs mese chiuso**: sono due periodi diversi (vedi Regole generali). Non riusare per errore i dati del mese chiuso sulla slide weekly, o viceversa.
