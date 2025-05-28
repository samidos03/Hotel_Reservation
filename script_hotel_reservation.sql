CREATE DATABASE IF NOT EXISTS HotelDB;
USE HotelDB;

CREATE TABLE Hotel (
  id_hotel INT PRIMARY KEY,
  ville VARCHAR(100),
  pays VARCHAR(100),
  code_postal VARCHAR(10)
);

CREATE TABLE Client (
  id_client INT PRIMARY KEY,
  adresse VARCHAR(255),
  ville VARCHAR(100),
  code_postal VARCHAR(10),
  email VARCHAR(100),
  telephone VARCHAR(20),
  nom_complet VARCHAR(100)
);

CREATE TABLE Prestation (
  id_prestation INT PRIMARY KEY,
  prix DECIMAL(7,2),
  description VARCHAR(255)
);

CREATE TABLE TypeChambre (
  id_type INT PRIMARY KEY,
  nom_type VARCHAR(50),
  prix DECIMAL(7,2)
);

CREATE TABLE Chambre (
  id_chambre INT PRIMARY KEY,
  numero INT,
  etage INT,
  balcon BOOLEAN,
  id_hotel INT,
  id_type INT,
  FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel),
  FOREIGN KEY (id_type) REFERENCES TypeChambre(id_type)
);

CREATE TABLE Reservation (
  id_chambre INT,
  date_debut DATE,
  date_fin DATE,
  id_client INT,
  PRIMARY KEY (id_chambre, date_debut),
  FOREIGN KEY (id_chambre) REFERENCES Chambre(id_chambre),
  FOREIGN KEY (id_client) REFERENCES Client(id_client)
);

CREATE TABLE Evaluation (
  id_client INT,
  date_evaluation DATE,
  note INT,
  commentaire TEXT,
  id_hotel INT,
  PRIMARY KEY (id_client, date_evaluation),
  FOREIGN KEY (id_client) REFERENCES Client(id_client),
  FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel)
);


INSERT INTO Hotel VALUES
(1, 'Paris', 'France', '75001'),
(2, 'Lyon', 'France', '69002');

INSERT INTO Client VALUES
(1, '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
(2, '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
(3, '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
(4, '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
(5, '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012', 'Emma Giraud');

INSERT INTO Prestation VALUES
(1, 15, 'Petit-déjeuner'),
(2, 30, 'Navette aéroport'),
(3, 0, 'Wi-Fi gratuit'),
(4, 50, 'Spa et bien-être'),
(5, 20, 'Parking sécurisé');

INSERT INTO TypeChambre VALUES
(1, 'Simple', 80),
(2, 'Double', 120);

INSERT INTO Chambre VALUES
(1, 201, 2, 0, 1, 1),
(2, 502, 5, 1, 1, 2),
(3, 305, 3, 0, 2, 1),
(4, 410, 4, 0, 2, 2),
(5, 104, 1, 1, 2, 2),
(6, 202, 2, 0, 1, 1),
(7, 307, 3, 1, 1, 2),
(8, 101, 1, 0, 1, 1);

INSERT INTO Reservation VALUES
(1, '2025-06-15', '2025-06-18', 1),
(2, '2025-07-01', '2025-07-05', 2),
(7, '2025-11-12', '2025-11-14', 2),
(10, '2026-02-01', '2026-02-05', 2), 
(3, '2025-08-10', '2025-08-14', 3),
(4, '2025-09-05', '2025-09-07', 4),
(9, '2026-01-15', '2026-01-18', 4), 
(5, '2025-09-20', '2025-09-25', 5);

INSERT INTO Evaluation VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
(5, '2025-09-20', 4, 'Très bon séjour.', 5);
