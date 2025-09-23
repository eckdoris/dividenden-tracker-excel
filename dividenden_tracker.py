import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dividenden Tracker", layout="wide")

st.title("📊 Dividenden Tracker")

# ======================
# Daten laden
# ======================
uploaded_file = st.file_uploader("Lade dein Portfolio hoch (Excel-Datei)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Spalten-Namen prüfen (müssen exakt so heißen wie in deiner Excel-Tabelle)
    required_cols = ["Name", "Stückzahl", "Dividende je Aktie", "Zahlungen pro Jahr", "Monate"]
    for col in required_cols:
        if col not in df.columns:
            st.error(f"❌ Spalte fehlt in der Excel-Datei: {col}")
            st.stop()

    # ======================
    # Berechnungen
    # ======================
    df["Jahresdividende"] = df["Stückzahl"] * df["Dividende je Aktie"]

    # Monatsdividenden verteilen
    monats_dict = {i: 0 for i in range(1, 13)}

    for _, row in df.iterrows():
        betrag_pro_zahlung = row["Jahresdividende"] / row["Zahlungen pro Jahr"]

        # Monate auslesen (z. B. "3,6,9,12")
        monate = str(row["Monate"]).split(",")
        for monat in monate:
            monat = monat.strip()
            if monat.isdigit():
                monats_dict[int(monat)] += betrag_pro_zahlung

    monats_df = pd.DataFrame(list(monats_dict.items()), columns=["Monat", "Dividende"])
    monats_df.set_index("Monat", inplace=True)

    # ======================
    # Diagramme
    # ======================
    col1, col2 = st.columns(2)

    # 1. Kuchendiagramm: Verteilung nach Aktien
    with col1:
        st.subheader("Kuchendiagramm: Verteilung nach Aktien")
        fig1, ax1 = plt.subplots()
        ax1.pie(df["Jahresdividende"], labels=df["Name"], autopct='%1.1f%%', startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

    # 2. Kuchendiagramm: Verteilung nach Monaten
    with col2:
        st.subheader("Kuchendiagramm: Verteilung nach Monaten")
        fig2, ax2 = plt.subplots()
        ax2.pie(monats_df["Dividende"], labels=monats_df.index, autopct='%1.1f%%', startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)

    # 3. Balkendiagramm Monatsansicht
    st.subheader("📅 Balkendiagramm: Letzte 12 Monate")
    fig3, ax3 = plt.subplots()
    ax3.bar(monats_df.index, monats_df["Dividende"])
    ax3.set_xlabel("Monat")
    ax3.set_ylabel("Dividende (€)")
    st.pyplot(fig3)

    # 4. Balkendiagramm Jahresansicht
    st.subheader("📆 Balkendiagramm: Jahresübersicht")
    gesamt_dividende = df["Jahresdividende"].sum()
    fig4, ax4 = plt.subplots()
    ax4.bar(["Gesamt"], [gesamt_dividende])
    ax4.set_ylabel("Dividende (€)")
    st.pyplot(fig4)

    # ======================
    # Tabelle anzeigen
    # ======================
    st.subheader("📋 Portfolio Übersicht")
    st.dataframe(df)

else:
    st.info("⬆️ Lade zuerst deine Excel-Datei hoch.")
