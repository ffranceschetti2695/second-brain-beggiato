---
title: "FC3 2026 - Mensile per Paese (Stuart)"
summary: "FC3 March 2026 export: Volume e GM mensili 2026 a livello cliente, aggregati per paese (UK/FR/PL) e globale. Riconciliato contro la riga TOTAL del file."
tags: [data, type/reference, stuart, fc3]
status: active
created: 2026-06-26
updated: 2026-06-26
related: ["[[data-fc3-baseline-2026]]", "[[entity-stuart]]", "[[concetto-rpo-cpo-slo]]", "[[progetto-ops-dashboard]]"]
---

# FC3 2026 - Mensile per Paese

Dati estratti dal file **`Revenue to GM - FC3 - March 2026 - Export to DWH`** (export marzo 2026, tutti i 12 mesi 2026, livello cliente/segmento/pipeline per paese). Questa nota congela i mensili a livello **paese e globale**; il dettaglio cliente di maggio sta in [[data-fc3-baseline-2026]].

## Come si costruisce l'aggregato (validato)

1. **Paese** = somma di tutti i suoi **clienti + segmenti (MM/SMB) + pipeline del paese**. La pipeline nel file è split per paese (UK/FR/PL deep dive) e risomma alla Global Pipeline.
2. **Globale** = somma dei tre paesi.
3. **Quadratura**: il GM globale deve coincidere con la riga **TOTAL** del file.

## Test di riconciliazione (GM)

- **Maggio: €1.069.958 calcolato vs €1.069.957 TOTAL** → match (±€1). Coincide col valore già nel vault.
- **Volume maggio globale: 756.105** = identico al baseline esistente.
- **11 mesi su 12 riconciliano a ±€3** contro TOTAL.
- **Gennaio**: residuo €15.116 (calcolato €574.878 vs TOTAL €589.994). Ogni cliente di gennaio torna incrociando GM-del × Volume del file → il residuo è nella riga TOTAL della fonte, non nei dati cliente. Da chiarire con la fonte.

## GM mensile per paese (€)

| Mese | UK | FR | PL | Globale | TOTAL file |
|---|---|---|---|---|---|
| Gen | 249.812 | 241.131 | 83.935 | 574.878 | 589.994 ⚠️ |
| Feb | 305.707 | 207.886 | 99.239 | 612.832 | 612.830 |
| Mar | 457.847 | 265.550 | 137.919 | 861.316 | 861.317 |
| Apr | 561.391 | 271.747 | 122.068 | 955.206 | 955.206 |
| Mag | 608.425 | 313.548 | 147.985 | 1.069.958 | 1.069.957 |
| Giu | 576.172 | 321.702 | 141.013 | 1.038.887 | 1.038.889 |
| Lug | 535.234 | 337.884 | 150.073 | 1.023.191 | 1.023.191 |
| Ago | 518.414 | 216.692 | 148.599 | 883.705 | 883.705 |
| Set | 187.627 | 319.574 | 97.836 | 605.037 | 605.039 |
| Ott | 139.744 | 334.021 | 40.630 | 514.395 | 514.396 |
| Nov | -47.029 | 313.183 | 43.084 | 309.238 | 309.241 |
| Dic | -106.354 | 320.672 | -18.195 | 196.123 | 196.123 |

## Volume mensile per paese (ordini)

| Mese | UK | FR | PL | Globale |
|---|---|---|---|---|
| Gen | 528.023 | 76.084 | 109.136 | 713.243 |
| Feb | 503.276 | 66.951 | 93.847 | 664.074 |
| Mar | 530.136 | 75.268 | 105.219 | 710.623 |
| Apr | 528.640 | 77.854 | 102.905 | 709.399 |
| Mag | 563.289 | 82.787 | 110.029 | 756.105 |
| Giu | 560.884 | 86.408 | 105.481 | 752.773 |
| Lug | 561.040 | 90.616 | 106.935 | 758.591 |
| Ago | 567.315 | 64.289 | 105.843 | 737.447 |
| Set | 557.508 | 95.799 | 109.128 | 762.435 |
| Ott | 587.349 | 102.062 | 111.328 | 800.739 |
| Nov | 579.113 | 106.046 | 112.388 | 797.547 |
| Dic | 603.265 | 112.716 | 104.928 | 820.909 |

## GM mensile per cliente (€) — fonte del roll-up

Pipeline = pipeline del paese (deep dive). Valori verificati incrociando GM-del × Volume del file.

### UK
| Cliente | Gen | Feb | Mar | Apr | Mag | Giu | Lug | Ago | Set | Ott | Nov | Dic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Tesco | 156.736 | 205.957 | 337.518 | 349.355 | 366.313 | 343.135 | 294.943 | 284.099 | 19.040 | 8.867 | -128.392 | -148.407 |
| Zapp | 54.521 | 50.051 | 66.063 | 127.258 | 145.819 | 134.815 | 132.803 | 113.279 | 61.274 | 30.777 | 10.890 | -8.271 |
| Pizza Hut | 1.831 | 1.758 | 4.236 | 5.752 | 8.760 | 10.172 | 11.886 | 13.153 | 8.964 | 9.322 | 6.208 | 3.979 |
| Iceland | -4.065 | 11.356 | 12.610 | 20.223 | 23.666 | 22.523 | 21.949 | 23.914 | 16.127 | 14.508 | 5.853 | -212 |
| TradeKart | 190 | 104 | 457 | 1.380 | 1.435 | 1.390 | 1.390 | 1.345 | 911 | 896 | 606 | 446 |
| UK Existing MM | 30.535 | 28.287 | 25.287 | 35.628 | 37.128 | 35.931 | 35.971 | 34.814 | 23.611 | 23.241 | 15.771 | 11.668 |
| UK New MM | 1.618 | 1.784 | 1.886 | 2.567 | 2.676 | 2.590 | 2.593 | 2.510 | 1.705 | 1.678 | 1.142 | 847 |
| UK Existing SMB | 7.058 | 5.388 | 5.635 | 7.684 | 7.992 | 7.734 | 7.741 | 6.741 | 5.061 | 4.979 | 3.360 | 2.468 |
| UK New SMB | 1.388 | 1.022 | 2.435 | 3.323 | 3.453 | 3.341 | 3.344 | 2.911 | 2.182 | 2.145 | 1.443 | 1.056 |
| UK Pipeline | 0 | 0 | 1.720 | 8.221 | 11.183 | 14.541 | 22.614 | 35.648 | 48.752 | 43.331 | 36.090 | 30.072 |

### FR
| Cliente | Gen | Feb | Mar | Apr | Mag | Giu | Lug | Ago | Set | Ott | Nov | Dic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Carrefour | 26.563 | 23.976 | 35.806 | 37.023 | 46.022 | 47.002 | 49.492 | 43.634 | 41.267 | 42.565 | 37.047 | 38.608 |
| Sushi Shop | 25.039 | 19.194 | 19.918 | 20.291 | 29.483 | 32.176 | 32.686 | 29.741 | 27.430 | 27.602 | 25.849 | 27.989 |
| Côté Sushi | 604 | 387 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Franprix | 4.667 | 5.464 | 3.840 | 4.250 | 6.750 | 8.250 | 11.120 | 7.100 | 13.100 | 14.630 | 14.520 | 14.460 |
| SYSTEME-U | 888 | 289 | 250 | 65 | 279 | 465 | 680 | 450 | 210 | -405 | -5.995 | -7.770 |
| FR Existing MM | 58.273 | 50.543 | 59.590 | 61.820 | 69.592 | 70.789 | 71.738 | 37.826 | 66.906 | 69.208 | 69.214 | 68.006 |
| FR New MM | 1.265 | 477 | 1.752 | 1.696 | 1.932 | 1.912 | 2.001 | 1.027 | 1.829 | 1.975 | 1.861 | 1.915 |
| FR Existing SMB | 103.636 | 88.489 | 99.568 | 99.524 | 106.115 | 103.484 | 107.424 | 43.363 | 101.900 | 106.606 | 101.575 | 104.789 |
| FR New SMB | 20.196 | 19.067 | 23.194 | 21.092 | 22.495 | 21.930 | 22.762 | 9.185 | 21.576 | 22.528 | 21.380 | 22.025 |
| FR Pipeline | 0 | 0 | 21.632 | 25.986 | 30.880 | 35.694 | 39.981 | 44.366 | 45.356 | 49.312 | 47.732 | 50.650 |

### PL
| Cliente | Gen | Feb | Mar | Apr | Mag | Giu | Lug | Ago | Set | Ott | Nov | Dic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| AmRest | 66.954 | 68.595 | 89.043 | 85.050 | 104.900 | 96.480 | 103.316 | 102.551 | 69.651 | 27.476 | 22.952 | -7.944 |
| Just Eat (JET) | 17.484 | 30.258 | 48.279 | 36.292 | 42.331 | 40.596 | 42.365 | 41.516 | 24.363 | 9.586 | 16.573 | -11.453 |
| PL Existing MM | -196 | -273 | 396 | 456 | 464 | 464 | 471 | 480 | 414 | 369 | 345 | 210 |
| PL Existing SMB | -288 | 578 | 186 | 246 | 264 | 254 | 285 | 285 | 172 | 124 | 92 | -100 |
| PL New SMB | -19 | 81 | 15 | 24 | 26 | 25 | 29 | 29 | 13 | 5 | 1 | -29 |
| PL Pipeline | 0 | 0 | 0 | 0 | 0 | 3.194 | 3.607 | 3.738 | 3.223 | 3.070 | 3.121 | 1.121 |

## Target mensili per paese — input per la ops-dashboard

GR per paese = Σ clienti + pipeline. RPO = GR/Volume; CPO = (GR − GM)/Volume (definizioni in [[concetto-rpo-cpo-slo]]). **Global GR maggio = €4.443.217 = identico al vault.** Questi (Volume sopra + RPO + CPO) sono l'input di `deriveWeeklyTargets`.

### Gross Revenue mensile per paese (€)
| Mese | UK | FR | PL | Globale |
|---|---|---|---|---|
| Gen | 3.104.209 | 761.416 | 513.886 | 4.379.511 |
| Feb | 2.975.946 | 661.213 | 435.729 | 4.072.888 |
| Mar | 3.162.605 | 788.917 | 484.480 | 4.436.002 |
| Apr | 2.900.794 | 809.261 | 463.091 | 4.173.146 |
| Mag | 3.089.877 | 858.457 | 494.883 | 4.443.217 |
| Giu | 3.073.739 | 887.787 | 475.703 | 4.437.229 |
| Lug | 3.093.855 | 933.849 | 481.824 | 4.509.528 |
| Ago | 3.142.125 | 629.087 | 476.746 | 4.247.958 |
| Set | 3.106.319 | 979.184 | 491.740 | 4.577.243 |
| Ott | 3.287.592 | 1.043.680 | 495.541 | 4.826.813 |
| Nov | 3.259.972 | 1.077.534 | 511.330 | 4.848.836 |
| Dic | 3.409.169 | 1.141.227 | 480.922 | 5.031.318 |

### RPO target mensile per paese (€/ordine)
| Mese | UK | FR | PL |
|---|---|---|---|
| Gen | 5.879 | 10.008 | 4.709 |
| Feb | 5.913 | 9.876 | 4.643 |
| Mar | 5.966 | 10.481 | 4.604 |
| Apr | 5.487 | 10.395 | 4.500 |
| Mag | 5.485 | 10.369 | 4.498 |
| Giu | 5.480 | 10.274 | 4.510 |
| Lug | 5.514 | 10.306 | 4.506 |
| Ago | 5.539 | 9.785 | 4.504 |
| Set | 5.572 | 10.221 | 4.506 |
| Ott | 5.597 | 10.226 | 4.451 |
| Nov | 5.629 | 10.161 | 4.550 |
| Dic | 5.651 | 10.125 | 4.583 |

### CPO target mensile per paese (€/ordine)
| Mese | UK | FR | PL |
|---|---|---|---|
| Gen | 5.406 | 6.838 | 3.940 |
| Feb | 5.306 | 6.771 | 3.586 |
| Mar | 5.102 | 6.953 | 3.294 |
| Apr | 4.425 | 6.904 | 3.314 |
| Mag | 4.405 | 6.582 | 3.153 |
| Giu | 4.453 | 6.551 | 3.173 |
| Lug | 4.560 | 6.577 | 3.102 |
| Ago | 4.625 | 6.415 | 3.100 |
| Set | 5.235 | 6.885 | 3.610 |
| Ott | 5.359 | 6.953 | 4.086 |
| Nov | 5.710 | 7.208 | 4.166 |
| Dic | 5.827 | 7.280 | 4.757 |

Nota: RPO/CPO mostrati a 3 decimali ma derivabili esatti da GR/GM/Volume sopra (più precisi). Il dettaglio GR per cliente sta nel file sorgente. Prossimo: dare questi mensili a `deriveWeeklyTargets` e caricare actuals reali + target nella ops-dashboard. Vedi [[progetto-ops-dashboard]].
