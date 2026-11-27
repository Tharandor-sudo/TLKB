"""
Haushalts-Navigator 2032 – Modelle rechnen und in den Navigator einsetzen.

Aufruf (im Hauptordner des Repositorys):
    python modell/trainieren.py

Was das Skript macht:
1. Liest die Testwelle (daten/TLKB_Datensatz2_Testwelle.csv).
2. Rechnet die Steuerschätzung (lineare Regression, wie Musterlösung 4)
   und die Terminchance (logistische Regression, nach den Entscheidungen in CLAUDE.md).
3. Speichert die Werte in modell/parameter.json.
4. Schreibt die Demo-Datei daten/demo_testhaushalte.csv (die 30 % Testhaushalte, ohne Ergebnis).
5. Setzt Werte und Demo-Daten in index.html ein.
6. Zeigt die Kontrollwerte. Weichen sie ab, stimmt etwas nicht.

Benötigt: pandas, numpy, scikit-learn
"""
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent.parent
DATEN = ROOT / "daten" / "TLKB_Datensatz2_Testwelle.csv"
DEMO = ROOT / "daten" / "demo_testhaushalte.csv"
PARAM = ROOT / "modell" / "parameter.json"
SEITE = ROOT / "index.html"
ZUFALL = 42

d = pd.read_csv(DATEN)
ja = (d.beratung_abgeschlossen == "ja").astype(int)
konk = (d.zivilstand.str.strip().str.lower() == "konkubinat").astype(int)
Z = pd.DataFrame({
    "lohn": d.lohn_total_monat / 1000,
    "rente": d.renten_total_monat / 1000,
    "anteil": d.anteil_tieferes_einkommen,
    "kinder": d.anzahl_kinder,
    "alter": d.alter_mittel,
})

# 1) Steuerschätzung: wie Musterlösung 4 (70/30, Zufall 42, nicht standardisiert)
tr_r, te_r = train_test_split(d.index, test_size=0.3, random_state=ZUFALL)
reg = LinearRegression().fit(Z.loc[tr_r], d.steuer_delta_chf_jahr[tr_r])
fehler = d.steuer_delta_chf_jahr[te_r] - reg.predict(Z.loc[te_r])

# 2) Terminchance: Kanal, Konkubinat, Lohn, Rente, Anteil, Kinder, Alter.
#    Bewusst NICHT: Beraterkontakte, Hypothek, Depot, Haushaltstyp (siehe CLAUDE.md).
SPALTEN = ["eb", "tel", "konkubinat", "lohn", "rente", "anteil", "kinder", "alter"]
X = pd.DataFrame({
    "eb": (d.kontaktkanal == "E-Banking").astype(float),
    "tel": (d.kontaktkanal == "Telefon").astype(float),
    "konkubinat": konk,
}).join(Z)[SPALTEN]
tr, te = train_test_split(d.index, test_size=0.3, random_state=ZUFALL, stratify=ja)
skal = StandardScaler().fit(X.loc[tr])
klass = LogisticRegression(max_iter=3000).fit(skal.transform(X.loc[tr]), ja[tr])

param = {
    "reg": {
        "intercept": float(reg.intercept_),
        "coef": dict(zip(Z.columns, map(float, reg.coef_))),
        "mae": float(fehler.abs().mean()),
        "p10": float(fehler.quantile(0.1)),
        "p90": float(fehler.quantile(0.9)),
    },
    "clf": {
        "intercept": float(klass.intercept_[0]),
        "coef": dict(zip(SPALTEN, map(float, klass.coef_[0]))),
        "mean": dict(zip(SPALTEN, map(float, skal.mean_))),
        "scale": dict(zip(SPALTEN, map(float, skal.scale_))),
    },
}
PARAM.write_text(json.dumps(param, indent=2), encoding="utf-8")

# 3) Demo-Datei: die Testhaushalte, nur Daten, die die Bank vorher kennt
demo_spalten = ["haushalt_id", "zivilstand", "alter_mittel", "lohn_total_monat", "renten_total_monat",
                "anteil_tieferes_einkommen", "anzahl_kinder", "hypothek_saldo", "depotwert", "beraterkontakte_12m"]
demo = d.loc[te, demo_spalten].sort_values("haushalt_id")
demo.to_csv(DEMO, index=False)

# 4) In index.html einsetzen
seite = SEITE.read_text(encoding="utf-8")
seite, n1 = re.subn(r"const PARAMS = \{.*?\};\n", lambda m: "const PARAMS = " + json.dumps(param) + ";\n", seite, count=1, flags=re.S)
seite, n2 = re.subn(r'(<script type="text/plain" id="demo-csv">).*?(</script>)',
                    lambda m: m.group(1) + DEMO.read_text(encoding="utf-8").strip() + m.group(2), seite, count=1, flags=re.S)
if n1 != 1 or n2 != 1:
    raise SystemExit("index.html: Stelle für Werte oder Demo-Daten nicht gefunden – nichts geändert.")
SEITE.write_text(seite, encoding="utf-8")

# 5) Kontrollwerte: gleiche Rechnung wie im Navigator
Xt = X.loc[te].copy()
Xt["eb"], Xt["tel"] = 0.0, 1.0
chance = klass.predict_proba(skal.transform(Xt))[:, 1]
delta = reg.predict(Z.loc[te])
t = pd.DataFrame({"id": d.haushalt_id[te].values, "chance": chance, "delta": delta, "konk": konk[te].values})
liste = t[(t.konk == 0) & (t.delta >= 500)].copy()
liste["punkte"] = liste.chance * liste.delta
liste = liste.sort_values(["punkte", "id"], ascending=[False, True])
marke = int(np.argmax(liste.chance.cumsum().values >= 60)) + 1

print("Kontrollwerte (erwartet in Klammern):")
print(f"  Steuer je 1'000 CHF Lohn:   {reg.coef_[0]:.1f}   (145.4)")
print(f"  Mittlerer Fehler:           {fehler.abs().mean():.0f}   (583)")
print(f"  Fehlerband 8 von 10:        {fehler.quantile(0.1):.0f} bis {fehler.quantile(0.9):.0f}   (-918 bis 900)")
print(f"  Anrufliste / Information:   {len(liste)} / {((t.konk == 0) & (t.delta <= -500)).sum()}   (215 / 391)")
print(f"  Marke bei 60 Terminen:      Rang {marke}   (115, entspricht {round(marke * 3000 / 900)} pro Monat; erwartet 383)")
print("index.html, modell/parameter.json und daten/demo_testhaushalte.csv sind aktualisiert.")
