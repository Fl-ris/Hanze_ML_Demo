----------------------------------------------
-- Sqlite3 database voor de enquete vragen  --
-- Autheur: Floris Menninga                 --
-- Datum: 01-08-2025                        --
-- Versie: 0.1                              --
----------------------------------------------


create table IF NOT EXISTS vragenlijst_data(
id integer primary key,
social_media boolean,  -- Vraag 1: Maak je gebruik van Snapchat of Tiktok?
mp3_speler boolean, -- Vraag 2: Heb je ooit een Sony Walkman / discman gekocht?
krant boolean, -- Vraag 3: Lees je regelmatig de krant?
telefoon int, -- Vraag 4: Wat lijkt het meest op je eerste mobiele telefoon?
bellen_of_email boolean, -- Vraag 5: Geef je de voorkeur aan bellen of emailen / Whatsapp etc.?
smileys boolean, -- Vraag 6: Gebruik je bij het sturen van digitale berichten geregeld smileys zoals "😂"
werkelijke_leeftijd int -- Klopt de voorspelling (bevestigd door het persoon zelf).
voorspelde_generatie int, -- Hier zal de voorspeling voor dit persoon opgeslagen worden.
);

-- Test trainings data. --
insert into vragenlijst_data(social_media, mp3_speler, krant, telefoon, bellen_of_email, smileys) values(0,1,1,1,1,0,55);
insert into vragenlijst_data(social_media, mp3_speler, krant, telefoon, bellen_of_email, smileys) values(0,1,1,4,1,1, 40);
insert into vragenlijst_data(social_media, mp3_speler, krant, telefoon, bellen_of_email, smileys) values(0,1,1,2,1,1, 60);
insert into vragenlijst_data(social_media, mp3_speler, krant, telefoon, bellen_of_email, smileys) values(0,1,1,2,1,1, 60);