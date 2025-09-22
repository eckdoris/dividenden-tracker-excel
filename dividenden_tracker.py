import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titel
st.title("📊 Dividenden Tracker")

# Excel laden
@st.cache_data
def load_data():
    return pd.read_excel("portfolio.xlsx")

df = load_data()

# Dividenden berechnen (pro Jahr und pro Monat)
df["Jahresdividende"] = df["Stückzahl"] * df["Dividende je Aktie"]

# Monatsauszahlungen vorbereiten
monate = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun",
          "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]

monat_data = {m: 0 for m in monate}
for _, row in df.iterrows():
    for monat in str(row["Monat"]).split(","):
        monat = monat.strip()
        if monat in monate:
            monat_data[monat] += row["Jahresdividende"] / len(str(row["Monat"]).split(","))

# ---------------- Diagramme ----------------

st.subheader("Kuchendiagramm: Verteilung nach Aktien")
fig1, ax1 = plt.subplots()
ax1.pie(df["Jahresdividende"], labels=df["Aktie"], autopct="%.1f%%")
st.pyplot(fig1)

st.subheader("Kuchendiagramm: Verteilung nach Monaten")
fig2, ax2 = plt.subplots()
ax2.pie(monat_data.values(), labels=monat_data.keys(), autopct="%.1f%%")
st.pyplot(fig2)

st.subheader("Balkendiagramm: Monatliche Dividenden (12 Monate)")
fig3, ax3 = plt.subplots()
ax3.bar(monat_data.keys(), monat_data.values())
ax3.set_ylabel("Dividende (€)")
st.pyplot(fig3)

st.subheader("Balkendiagramm: Jahresdividende pro Aktie")
fig4, ax4 = plt.subplots()
ax4.bar(df["Aktie"], df["Jahresdividende"])
ax4.set_ylabel("Dividende (€)")
plt.xticks(rotation=45)
st.pyplot(fig4)

# Tabelle anzeigen
st.subheader("📑 Übersicht Portfolio")
st.dataframe(df)
