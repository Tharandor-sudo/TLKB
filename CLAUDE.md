# Haushalts-Navigator 2032 – Projektgedächtnis für Claude Code

Diese Datei liest Claude Code bei jedem Start. Sie hält fest, was das Team entschieden hat und warum.
Wer eine Entscheidung ändert, trägt das hier ein (mit Datum), damit alle denselben Stand haben.

## Worum es geht

Projektarbeit (Leistungsnachweis 2, CAS AI in Product Management HS 26, Gruppe 1).
Fiktive Thurlindner Kantonalbank (TLKB). Die Individualbesteuerung gilt ab 1.1.2032.
Das Tool erstellt jeden Monat eine Anrufliste für die Kampagne «Fitness-Check 2032»:
14 Spezialisten, rund 200 Beratungen pro Monat, 3'000 Kandidaten pro Monat.
Pitch vor der Geschäftsleitung: 12.12.2026. Alle Daten sind frei erfunden.

## So arbeiten wir mit Claude

- Antworten auf Deutsch, in einfacher Sprache, ohne Fachjargon.
- Nichts über eine Datei behaupten, die nicht geöffnet wurde: zuerst nachschauen, dann antworten.
- Ist eine Anfrage mehrdeutig: nachfragen, statt die wahrscheinlichste Variante zu wählen.
- Zahlen nur aus Rechnungen auf den Daten, nicht aus dem Gedächtnis.
- Nach jeder Änderung an Modell oder Regeln: `python modell/trainieren.py` laufen lassen und die Kontrollwerte prüfen.

## Dateien

- `index.html` – der Navigator (eine Datei, läuft im Browser, Daten bleiben im Browser).
- `modell/trainieren.py` – rechnet beide Modelle und setzt Werte und Demo-Daten in `index.html` ein.
- `modell/parameter.json` – die gespeicherten Modellwerte.
- `daten/TLKB_Datensatz2_Testwelle.csv` – Testwelle, 3'000 Haushalte (Lerndaten).
- `daten/demo_testhaushalte.csv` – die 900 Testhaushalte ohne Ergebnis (Demo-Datei).

Die Werte in `index.html` (Zeile `const PARAMS = …`) und die Demo-Daten nie von Hand ändern,
immer über `modell/trainieren.py`.

## Entscheidungen (Stand 27.11.2026)

| Nr. | Thema | Entscheidung | Grund |
|---|---|---|---|
| 1 | Liste | Alle Kandidaten gerankt, Marke dort, wo das Ziel an Terminen erwartet erreicht ist; Ziel verschiebbar | 200 Beratungen brauchen rund 380 Anrufe, nicht 200 |
| 2 | Haushaltstyp | Entfällt im Tool | Die Bank hat die 13 Spalten für die Typen im Betrieb nicht; ohne Typ sortiert die Liste gleich gut |
| 2b | Gespräch | Richtet sich nach der Richtung des geschätzten Deltas | Ersetzt den Leitfaden pro Typ |
| 3 | Betroffenheit | Nur wer geschätzt ≥ +500 CHF mehr zahlt; Sortierung nach Chance × Delta | Auftrag: Beratung für die, die mehr zahlen |
| 4 | Weniger-Zahler | Rubrik «Information statt Beratung» (Delta ≤ −500), strikt getrennt von der Anrufliste | Rentner gewinnen, wollen aber kaum Beratung |
| 4b | Kaum Änderung | Zwischen −500 und +500: fallen heraus | Auftragsblatt |
| – | Konkubinat | Fällt heraus | Wird schon heute einzeln besteuert |
| 5 | Rückmeldung | Ergebnis-Spalte und Export im MVP; Vergleichsgruppe (zufälliger Anteil) als Antrag für den Pilot | MVP einfach halten, Wirkung im Pilot sauber messen |
| 6 | Form | Webseite, Rechnung im Browser | Datenschutz: Kundendaten verlassen den Computer nicht |
| 7 | Nutzen | Über besser eingesetzte Beratungszeit (nicht über eingesparte Kontakte) | Anrufzahl bleibt fast gleich; Gewinn: Beratungen landen bei den Richtigen |
| 8 | Hypothek, Depot | Nicht für die Sortierung; Anzeige: Hypothek ja/nein, Depot in Stufen (<50'000 / 50'000–250'000 / >250'000) | Bringen der Liste nichts; Vermögensdaten sparsam; «nicht nach Vermögen sortieren» |
| 9a | Unsicherheit | Delta mit Bandbreite gut sichtbar; dem Kunden nie eine geschätzte Zahl nennen | Schätzung liegt bei Einzelfällen auch in der Richtung falsch |
| 9b | Kanton | Nur Bundessteuer, klar beschriftet; Kanton als offener Punkt im Pitch | Kanton Thurlinden hat noch nicht entschieden |
| 10 | Kanal | Immer Telefon für die Anrufliste; Information per Brief oder E-Banking | Kanal in der Testwelle per Los zugeteilt: Telefon klar am besten |
| 11 | Beraterkontakte | Nicht für die Sortierung, nur Anzeige | Sonst werden Kunden ohne bisherigen Kontakt benachteiligt; Ursache/Wirkung unklar |
| 13 | Demo | Die 900 echten Testhaushalte; Modelle nur auf 70 % gelernt | Ehrliche Demo |
| – | Regressionszahlen | Die der Musterlösung 4 (nachrechenbar) | Auftragsblatt nennt abweichende Zahlen (165, 450/Kind, 620), die sich nicht nachrechnen lassen |
| – | Vergleich im Pitch | «Rund 380 Anrufe statt rund 1'130 Kontakte» (zufällig, gemischte Kanäle) | Teamentscheid; Reserve-Antwort: zufällig, alle per Telefon ≈ 870 |
| – | Block 2 und 3 | Namen, Deutungen und Sätze der Musterlösungen 2 und 3 gelten als unsere | Teamentscheid |

## Kennzahlen (geprüft)

- Steuer-Delta: Startwert −432; je 1'000 CHF Lohn +145; je 1'000 CHF Rente +102; je Prozentpunkt Anteil tieferes Einkommen −49; Kind −16; Alter −1. Mittlerer Fehler 583 CHF; 8 von 10 Fehlern zwischen −918 und +900.
- Anrufliste: rund 380 Anrufe für 200 Termine pro Monat (Spanne etwa 300–400 über 6 Aufteilungen), statt rund 1'130 Kontakte bei zufälliger Auswahl.
- Mit Liste gehen gut 9 von 10 Beratungen an Haushalte, die wirklich ≥ 500 CHF mehr zahlen, statt rund die Hälfte: 70–90 Beratungen pro Monat mehr bei den Richtigen.
- Nutzen-Szenarien (Annahme 120 CHF pro Stunde; 60 / 90 / 120 Minuten pro Beratung): ≈ 100'000–130'000 / 150'000–195'000 / 200'000–260'000 CHF pro Jahr an besser eingesetzter Beratungszeit. Keine Einsparung auf dem Konto.
- Demo (900 Haushalte): Anrufliste 215, Information 391, kaum Änderung 176, Konkubinat 118; Marke bei Rang 115 für 60 Termine.

## Offene Punkte

- Tabelle «Von der Analyse zum Tool» und Folien für den Pitch (Botschaften vom Team noch zu bestätigen).
- Pilot: gemeinsame Ablage der Ergebnisse für 14 Spezialisten (heute speichert jeder Browser für sich).
- Pilot: Vergleichsgruppe (z. B. 10 % zufällig gezogene Mehrzahler) beantragen.
- Kantons- und Gemeindesteuer nachziehen, sobald der Kanton entscheidet.
