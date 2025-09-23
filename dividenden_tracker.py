import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# GitHub-Rohlink zur Excel-Datei
GITHUB_URL = "https://raw.githubusercontent.com/eckdoris/dividenden_tracker/main/portfolio.xlsx"

# -------------------------------
# Daten laden
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_excel(GITHUB_URL)

df = load_data()

# Jahresdividende berechnen
df["Jahresdividende"] = df["Stückzahl"] * df["Dividende je Aktie"]

# -------------------------------
# Streamlit App
# -------------------------------
st.set_page_config(page_title="Dividenden Tracker", layout="wide")

st.title("📊 Dividenden Tracker")
st.write("Portfolio wird automatisch aus GitHub geladen.")

# Rohdaten anzeigen
st.subheader("Dein Portfolio")
st.dataframe(df)

# -------------------------------
# Gesamtdaten
# -------------------------------
gesamt_dividende = df["Jahresdividende"].sum()
st.metric("Gesamte Jahresdividende", f"{gesamt_dividende:.2f} €")

# -------------------------------
# Kuchendiagramm – Verteilung nach Aktien
# -------------------------------
st.subheader("Kuchendiagramm: Verteilung nach Aktien")
fig1, ax1 = plt.subplots()
ax1.pie(df["Jahresdividende"], labels=df["Name"], autopct='%1.1f%%')
st.pyplot(fig1)

# -------------------------------
# Monatliche Dividendenberechnung
# -------------------------------
st.subheader("Monatliche Dividenden")
# Monatsdaten berechnen
monats_dividenden = {i: 0 for i in range(1, 13)}

for _, row in df.iterrows():
    monate = str(row["Monate"]).split(",")
    betrag = row["Jahresdividende"] / row["Zahlungen pro Jahr"]
    for m in monate:
        m = m.strip()
        if m.isdigit():
            monats_dividenden[int(m)] += betrag

# DataFrame für Monate
monats_df = pd.DataFrame(list(monats_dividenden.items()), columns=["Monat", "Dividende"])

# Diagramm
fig2, ax2 = plt.subplots()
ax2.bar(monats_df["Monat"], monats_df["Dividende"])
ax2.set_xticks(range(1, 13))
ax2.set_xlabel("Monat")
ax2.set_ylabel("Dividende (€)")
st.pyplot(fig2)

# Tabelle
st.dataframe(monats_df)
