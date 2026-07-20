---
title: "Tone of Voice per i messaggi"
summary: "Come Francesco vuole che siano scritti i messaggi di lavoro (Slack, email): corti, naturali, diretti, senza accondiscendenza, senza giustificarsi, ne' em dash."
tags: [docs, comunicazione, stile]
status: active
created: 2026-06-30
updated: 2026-07-16
related: ["[[self-franceschetti]]", "[[entity-stuart]]"]
---

# Tone of Voice per i messaggi

Linee guida per quando si redige un messaggio di lavoro per conto di Francesco (Slack, email, commenti). Valgono per le comunicazioni verso colleghi, non per le note del vault.

## Passo obbligatorio: controllare sempre le DM col destinatario (aggiunto 2026-07-16)

Prima di scrivere qualsiasi bozza, leggere sempre lo storico DM (o il canale/thread pertinente) tra Francesco e la persona a cui si sta rispondendo — non solo quando esplicitamente richiesto. Serve per calibrare, non per copiare (vedi regola sotto "Mai lo stile del destinatario"):

- che rapporto c'e' (quanto e' confidenziale, quanto contesto pregresso condividono)
- cosa la persona gia' sa/si aspetta, per evitare di rispiegare l'ovvio
- eventuali tensioni o disaccordi recenti rilevanti al messaggio da scrivere
- il registro di formalita' che la relazione giustifica (es. con Mark e' molto informale, con altri interlocutori puo' essere diverso)

Questo e' un passo standing per qualsiasi bozza verso terzi, non solo per FC6/Mark.

## Regole

- **Corto.** Pochi paragrafi, niente preamboli. Dire la cosa e basta.
- **Poco esplicativo.** Non spiegare l'ovvio ne' giustificare troppo. Si assume che l'interlocutore abbia il contesto.
- **Non accondiscendente.** Niente complimenti di rito ("great breakdown", "super helpful"), niente assenso eccessivo. Un grazie asciutto va bene, l'adulazione no.
- **Naturale, non formale.** Tono colloquiale e umano. Il registro troppo formale suona fastidioso.
- **Diretto, con opinione.** Dare un parere e, quando serve, fare challenge delle assunzioni invece di limitarsi ad assecondare.
- **Niente em dash** (ne' `-` ne' `—`). Usare virgole, due punti o frasi separate.
- **Bullet point** quando si elencano piu' punti: si tengono, non si fondono in prosa.
- **Lingua.** In inglese quando il messaggio e' per colleghi Stuart.
- **Mai lo stile del destinatario.** Anche quando si controllano le DM con la persona per calibrare il tono, il registro da imitare e' quello di Francesco (frasi complete, misurato), non quello frammentato/informale dell'altra persona (es. i messaggi telegrafici di Mark Jones) — quello e' solo contesto, non il modello da copiare.

## Non giustificarsi (regola piu' importante, corretta il 2026-07-16)

Il difetto piu' frequente nelle bozze: suonare come se ci si stesse giustificando o difendendo da un'accusa implicita. Segnali da eliminare sempre:

- **Frasi con "ma" / "but" che contrastano un fatto con un'accusa non detta** — es. "we had to increase X, *but* it's grounded in actuals, *not just* numbers we inflated for the sake of it". Il "not just... for the sake of it" e' un'ammissione di colpa mascherata: implica che qualcuno potrebbe pensare che l'abbiamo gonfiato a caso, e lo sta negando invece di limitarsi a dire il motivo.
- **Negazioni difensive** ("not a new growth assumption", "not because we changed X out of nowhere") — stesso problema: si nega un'accusa che nessuno ha ancora fatto esplicitamente.
- **Domande retoriche che sfidano l'altro** ("why would this need to change?") suonano aggressive se usate per *concludere* un'affermazione gia' fatta. Una domanda finale va bene solo se e' genuinamente aperta e lascia che sia l'altra persona ad arrivarci da sola (vedi esempio sotto), non se e' la chiusura polemica di un ragionamento gia' deciso.

**Come si fa invece**: si elencano i fatti in sequenza, uno via l'altro, senza connettivi di contrasto. Prima la ragione di business (in modo neutro, senza scudo preventivo), poi il meccanismo tecnico specifico, poi l'assunzione di base che non e' cambiata. Si lascia che la conclusione emerga da sola dalla sequenza dei fatti, invece di dichiararla difendendola.

## Esempi del registro giusto

Dalla risposta a Ricardo (2026-06-30): "Thanks Ricardo, clear. The reactive payout seems to be what's hurting us on the non-BAU setups, so it makes sense to consider it at this stage." Corto, niente adulazione, parere diretto, nessun em dash.

Dalla bozza a Mark Jones su [[progetto-fc6-topline-proposal]] (2026-07-16, versione approvata dopo 3 round di correzioni): "Hello Mark, we had to review volume assumptions for certain accounts because of a request from our investor. With Tesco, this translated into lower volume for the second half of the year, and because of the pricing tier structure, this drove an increase in RPO. That said, if I'm not missing any part of the story, the current CPO level is based on the supply level we'll have (where we agreed to spend more than what's in the plan, to secure the right level of supply) and on us targeting 95% performance. Given that the RPO increased, I'd expect you to rework the CPO and increase it accordingly, but what would actually drive that increase if we're already targeting 95%?"

Perche' funziona: la ragione di business (richiesta dell'investitore) e' dichiarata senza scudo. Il meccanismo Tesco (volume giu' per zone exits, quindi tier diverso, quindi RPO su) e' una sequenza di fatti, non una difesa. La domanda finale e' genuina, non retorica: lascia a Mark lo spazio per portare un'informazione che magari manca.

## Vedi anche

[[self-franceschetti]] — [[entity-stuart]]
