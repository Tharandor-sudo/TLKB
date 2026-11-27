# Haushalts-Navigator 2032

MVP der Gruppe 1 (CAS AI in Product Management HS 26) für die fiktive Thurlindner Kantonalbank:
eine monatliche Anrufliste für die Kampagne «Fitness-Check 2032». Alle Daten sind frei erfunden.

## Navigator öffnen

`index.html` im Browser öffnen (Doppelklick genügt). Dann «Testhaushalte laden» klicken
oder eine Kandidaten-Datei (CSV) hineinziehen. Die Datei wird nur im Browser gelesen.

Eine Kandidaten-Datei braucht diese Spalten:
`haushalt_id, zivilstand, lohn_total_monat, renten_total_monat, anteil_tieferes_einkommen, anzahl_kinder, alter_mittel`
Freiwillig (nur Anzeige): `hypothek_saldo, depotwert, beraterkontakte_12m`

## Gemeinsam arbeiten

1. Repository auf den eigenen Computer holen: `git clone <Adresse des Repositorys>`
2. Im Ordner Claude Code starten: `claude`
3. Für jede Änderung einen eigenen Zweig anlegen, danach einen Pull Request öffnen und von jemandem aus der Gruppe prüfen lassen.

Claude Code liest beim Start `CLAUDE.md`. Dort stehen alle Entscheidungen des Teams.
Wer eine Entscheidung ändert, trägt sie dort ein.

## Modelle neu rechnen

Nur nötig, wenn sich Regeln oder Merkmale ändern:

```
pip install -r requirements.txt
python modell/trainieren.py
```

Das Skript setzt die neuen Werte und die Demo-Daten direkt in `index.html` ein und zeigt Kontrollwerte.
Stimmen sie nicht mit den erwarteten Werten überein, die Änderung nicht übernehmen.

## Hinweis zum Link für den Pitch

Der auf claude.ai veröffentlichte Link aktualisiert sich nicht automatisch aus diesem Repository.
Vor dem Pitch eine Fassung festlegen und den Link bei Bedarf neu veröffentlichen.
