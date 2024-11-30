import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Configuration de la page
st.set_page_config(page_title="Diagramme de Gantt", layout="wide")

st.title("Diagramme de Gantt Dynamique")

# Fonction pour définir la couleur en fonction de l'avancement
def get_color(progress):
    if progress < 50:
        return "red"
    elif 50 <= progress < 100:
        return "yellow"
    else:
        return "green"

# Initialisation du DataFrame
if "gantt_data" not in st.session_state:
    st.session_state["gantt_data"] = pd.DataFrame(columns=["Phase", "Début", "Fin", "Avancement (%)"])

# Zone d'entrée pour ajouter des phases
st.sidebar.header("Ajouter une nouvelle phase")
phase_name = st.sidebar.text_input("Nom de la phase")
start_date = st.sidebar.date_input("Date de début", value=datetime.now())
end_date = st.sidebar.date_input("Date de fin", value=datetime.now() + timedelta(days=7))
progress = st.sidebar.slider("Avancement (%)", min_value=0, max_value=100, step=1)

if st.sidebar.button("Ajouter la phase"):
    new_data = {
        "Phase": phase_name,
        "Début": pd.to_datetime(start_date),
        "Fin": pd.to_datetime(end_date),
        "Avancement (%)": progress,
    }
    st.session_state["gantt_data"] = pd.concat(
        [st.session_state["gantt_data"], pd.DataFrame([new_data])], ignore_index=True
    )
    st.sidebar.success(f"La phase '{phase_name}' a été ajoutée.")

# Afficher les données ajoutées
st.subheader("Données du Projet")
st.dataframe(st.session_state["gantt_data"])

# Créer le diagramme de Gantt
st.subheader("Diagramme de Gantt")
if not st.session_state["gantt_data"].empty:
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, row in st.session_state["gantt_data"].iterrows():
        color = get_color(row["Avancement (%)"])
        ax.barh(
            row["Phase"],
            (row["Fin"] - row["Début"]).days,
            left=(row["Début"] - st.session_state["gantt_data"]["Début"].min()).days,
            color=color,
            edgecolor="black",
        )

    # Configuration des axes
    ax.set_xlabel("Jours")
    ax.set_ylabel("Phases")
    ax.set_title("Diagramme de Gantt")
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%b"))

    # Afficher le graphique
    st.pyplot(fig)
else:
    st.info("Ajoutez des phases pour générer le diagramme de Gantt.")
