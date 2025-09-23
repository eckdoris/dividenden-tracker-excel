import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# Excel-Daten laden
# ==============================
@st.cache_data
def load_data():
    df = pd.read_excel("portfolio.xlsx")

    # Nur Aktien mit Stückzahl > 0 behalten
    df = df[df["Stückzahl"] > 0]

    return df

# ==============================
# Dividenden-Berechnung
# ==============================
def calculate_dividends(df):
    monthly_dividends = {i: 0 for i in range(1, 13)}

    for _, row in df.iterrows():
        name = row["Name"]
        stueckzahl = row["Stückzahl"]
        div_pro_aktie = row["Dividende je Aktie"]
        payments = row["Zahlungen pro Jahr"]
        monate = str(row["Monate"]).split(",")

        # Jahresdividende = Stückzahl * Dividende je Aktie
        jahres_dividende = stueckzahl * div_pro_aktie

        # Anteil pro Zahlung
        if payments > 0:
            betrag_pro_zahlung = jahres_dividende / payments
        else:
            betrag_pro_zahlung = 0

        # Auf die Monate verteilen
        for m in monate:
            try:
                monat = int(m.strip())
                if monat in monthly_dividends:
                    monthly_dividends[monat] += betrag_pro_zahlung
            except:
                continue

    return monthly_dividends

# ==============================
# Streamlit App
# ==============================
def main():
    st.title("📊 Mein Dividenden Tracker")

    df = load_data()

    st.subheader("📑 Meine Rohdaten")
    st.dataframe(df)

    # Dividenden berechnen
    monthly_dividends = calculate_dividends(df)

    st.subheader("📅 Monatliche Dividendensumme")
    monat_df = pd.DataFrame({
        "Monat": list(monthly_dividends.keys()),
        "Dividende (€)": list(monthly_dividends.values())
    })

    st.dataframe(monat_df)

    # Gesamtsumme
    gesamt = sum(monthly_dividends.values())
    st.markdown(f"💰 **Gesamtsumme Dividenden: {gesamt:.2f} €**")

    # Balkendiagramm
    fig, ax = plt.subplots()
    ax.bar(monat_df["Monat"], monat_df["Dividende (€)"])
    ax.set_xlabel("Monat")
    ax.set_ylabel("Dividende (€)")
    ax.set_title("Monatliche Dividenden")
    st.pyplot(fig)


if __name__ == "__main__":
    main()
