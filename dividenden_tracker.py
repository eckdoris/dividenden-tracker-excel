import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Hilfsfunktionen
# -----------------------------
@st.cache_data
def load_data():
    # Lokale Excel-Datei laden
    df = pd.read_excel("portfolio.xlsx")

    # Berechnung: Gesamtdividende pro Jahr
    df["Dividende Gesamt"] = df["Stückzahl"] * df["Dividende je Aktie"]

    return df


def prepare_monthly_dividends(df):
    # Leeres Dictionary für Monate
    monthly = {i: 0 for i in range(1, 13)}

    for _, row in df.iterrows():
        # Welche Monate sind eingetragen? (z. B. "3,6,9,12")
        monate = str(row["Monate"]).split(",")

        # Dividende pro Zahlung
        if row["Zahlungen pro Jahr"] > 0:
            div_pro_zahlung = row["Dividende Gesamt"] / row["Zahlungen pro Jahr"]
        else:
            div_pro_zahlung = 0

        for m in monate:
            try:
                monat = int(m)
                if 1 <= monat <= 12:
                    monthly[monat] += div_pro_zahlung
            except:
                continue

    # In DataFrame umwandeln mit deutschen Monatsnamen
    monthly_df = pd.DataFrame.from_dict(monthly, orient="index", columns=["Dividende"])
    monthly_df.index = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]
    return monthly_df


# -----------------------------
# Streamlit App
# -----------------------------
st.set_page_config(page_title="📊 Dividenden Tracker", layout="wide")
st.title("📊 Mein Dividenden Tracker")

# Daten laden
df = load_data()

# Rohdaten anzeigen
st.subheader("📑 Meine Rohdaten")
st.dataframe(df)

# Monatsauswertung
st.subheader("📅 Monatliche Dividendensumme")
monthly_dividends = prepare_monthly_dividends(df)

st.bar_chart(monthly_dividends)

# Gesamtsumme
st.write(f"💰 Gesamtsumme Dividenden: **{monthly_dividends['Dividende'].sum():.2f} €**")
