import streamlit as st
import mysql.connector
from mysql.connector import Error

# Fonction pour se connecter à la base MySQL
def get_connection():
    # Remplacez '12345' par votre mot de passe MySQL root
    # Assurez-vous que 'HotelDB' est bien le nom de votre base de données
 return mysql.connector.connect(
    host='localhost',
    user='root',
    password='yoga',
    database='HotelDB'
)


# Afficher la liste des clients
def afficher_clients():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_client, nom_complet, ville, email FROM Client")
        clients = cursor.fetchall()
        st.write("### Liste des Clients")
        if clients:
            for c in clients:
                st.write(f"ID: {c[0]} - {c[1]} - Ville: {c[2]} - Email: {c[3]}")
        else:
            st.info("Aucun client trouvé.")
    except Error as e:
        st.error(f"Erreur lors de l'affichage des clients: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Afficher la liste des réservations avec nom client et ville hôtel
def afficher_reservations():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT R.id_chambre, R.date_debut, R.date_fin, C.nom_complet, H.ville
            FROM Reservation R
            JOIN Client C ON R.id_client = C.id_client
            JOIN Chambre Ch ON R.id_chambre = Ch.id_chambre
            JOIN Hotel H ON Ch.id_hotel = H.id_hotel
            ORDER BY R.date_debut
        """
        cursor.execute(query)
        reservations = cursor.fetchall()
        
        st.write("### Liste des Réservations")
        
        if reservations:
            for r in reservations:
                date_debut = r[1].strftime('%Y-%m-%d') if hasattr(r[1], 'strftime') else str(r[1])
                date_fin = r[2].strftime('%Y-%m-%d') if hasattr(r[2], 'strftime') else str(r[2])
                st.write(f"Chambre ID: {r[0]}, Du {date_debut} au {date_fin}, Client: {r[3]}, Hôtel (Ville): {r[4]}")
        else:
            st.info("Aucune réservation trouvée.")
    
    except Error as e:
        st.error(f"Erreur lors de l'affichage des réservations: {e}")
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Afficher chambres disponibles entre 2 dates
def afficher_chambres_disponibles(date_debut, date_fin):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT Ch.id_chambre, Ch.numero, Ch.etage, H.ville, T.nom_type AS nom_type_chambre
            FROM Chambre Ch
            JOIN Hotel H ON Ch.id_hotel = H.id_hotel
            JOIN TypeChambre T ON Ch.id_type = T.id_type
            WHERE Ch.id_chambre NOT IN (
                SELECT id_chambre FROM Reservation
                WHERE NOT (date_fin < %s OR date_debut > %s)
            )
        """
        cursor.execute(query, (date_debut, date_fin))
        chambres = cursor.fetchall()
        st.write(f"### Chambres disponibles du {date_debut} au {date_fin}")
        if chambres:
            for ch in chambres:
                st.write(f"ID: {ch[0]}, Numéro: {ch[1]}, Étage: {ch[2]}, Ville: {ch[3]}, Type: {ch[4]}")
        else:
            st.info("Aucune chambre disponible pour ces dates.")
    except Error as e:
        st.error(f"Erreur lors de la recherche de chambres disponibles: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Ajouter un client
def ajouter_client(nom, adresse, ville, code_postal, email, telephone):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(id_client), 0) + 1 FROM Client")
        new_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO Client (id_client, adresse, ville, code_postal, email, telephone, nom_complet) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (new_id, adresse, ville, code_postal, email, telephone, nom)
        )
        conn.commit()
        st.success(f"Client '{nom}' ajouté avec l'ID {new_id}")
    except Error as e:
        st.error(f"Erreur lors de l'ajout du client: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Ajouter une réservation
def ajouter_reservation(id_chambre, date_debut, date_fin, id_client):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM Reservation
            WHERE id_chambre = %s AND NOT (date_fin < %s OR date_debut > %s)
        """, (id_chambre, date_debut, date_fin))
        dispo_count = cursor.fetchone()[0]
        if dispo_count > 0:
            st.error("La chambre n'est pas disponible pour cette période.")
            return
        cursor.execute(
            "INSERT INTO Reservation (id_chambre, date_debut, date_fin, id_client) VALUES (%s,%s,%s,%s)",
            (id_chambre, date_debut, date_fin, id_client)
        )
        conn.commit()
        st.success(f"Réservation ajoutée avec succès pour la chambre ID {id_chambre}.")
    except Error as e:
        st.error(f"Erreur lors de l'ajout de la réservation: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Interface Streamlit
st.title("Gestion Hôtel")

menu_options = ["Afficher Clients", "Afficher Réservations", "Chambres Disponibles", "Ajouter Client", "Ajouter Réservation"]
menu = st.sidebar.selectbox("Menu", menu_options)

if menu == "Afficher Clients":
    afficher_clients()

elif menu == "Afficher Réservations":
    afficher_reservations()

elif menu == "Chambres Disponibles":
    st.subheader("Rechercher des Chambres Disponibles")
    date_debut_dispo = st.date_input("Date début disponibilité")
    date_fin_dispo = st.date_input("Date fin disponibilité")
    if st.button("Rechercher Chambres"):
        if date_debut_dispo > date_fin_dispo:
            st.error("La date de début doit être avant ou égale à la date de fin.")
        else:
            afficher_chambres_disponibles(date_debut_dispo, date_fin_dispo)

elif menu == "Ajouter Client":
    st.subheader("Ajouter un Nouveau Client")
    with st.form("form_ajouter_client"):
        nom = st.text_input("Nom complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.text_input("Code postal")
        email = st.text_input("Email")
        telephone = st.text_input("Téléphone")
        submitted_client = st.form_submit_button("Ajouter Client")
        if submitted_client:
            if nom and adresse and ville and code_postal and email and telephone:
                ajouter_client(nom, adresse, ville, code_postal, email, telephone)
            else:
                st.error("Veuillez remplir tous les champs.")

elif menu == "Ajouter Réservation":
    st.subheader("Ajouter une Nouvelle Réservation")
    conn_ui = None
    cursor_ui = None
    try:
        conn_ui = get_connection()
        cursor_ui = conn_ui.cursor(dictionary=True)

        cursor_ui.execute("SELECT id_client, nom_complet FROM Client ORDER BY nom_complet")
        clients = cursor_ui.fetchall()
        client_options = {f"{c['nom_complet']} (ID: {c['id_client']})": c['id_client'] for c in clients}

        cursor_ui.execute("""
            SELECT Ch.id_chambre, Ch.numero, H.ville AS nom_hotel
            FROM Chambre Ch
            JOIN Hotel H ON Ch.id_hotel = H.id_hotel
            ORDER BY H.ville, Ch.numero

        """)
        chambres = cursor_ui.fetchall()
        chambre_options = {f"Chambre {c['numero']} (Hôtel: {c['nom_hotel']}, ID: {c['id_chambre']})": c['id_chambre'] for c in chambres}

        if not client_options:
            st.warning("Aucun client trouvé. Veuillez d'abord ajouter un client.")
        if not chambre_options:
            st.warning("Aucune chambre trouvée. Vérifiez la configuration des chambres.")

        if client_options and chambre_options:
            with st.form("form_ajouter_reservation"):
                client_display_sel = st.selectbox("Client", list(client_options.keys()))
                chambre_display_sel = st.selectbox("Chambre", list(chambre_options.keys()))
                date_debut_res = st.date_input("Date début réservation")
                date_fin_res = st.date_input("Date fin réservation")
                submitted_reservation = st.form_submit_button("Ajouter Réservation")

                if submitted_reservation:
                    if not client_display_sel or not chambre_display_sel:
                        st.error("Veuillez sélectionner un client et une chambre.")
                    elif date_debut_res >= date_fin_res:
                        st.error("La date de fin doit être après la date de début.")
                    else:
                        selected_client_id = client_options[client_display_sel]
                        selected_chambre_id = chambre_options[chambre_display_sel]
                        ajouter_reservation(selected_chambre_id, date_debut_res, date_fin_res, selected_client_id)
        
    except Error as e:
        st.error(f"Erreur lors du chargement des données pour la réservation: {e}")
    finally:
        if cursor_ui:
            cursor_ui.close()
        if conn_ui:
            conn_ui.close()
