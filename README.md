### Hanze Machine learning Demo voor Zpannend Zernike ###

Het machine learning model dat gedemonstreerd wordt met dit dashboard zal de leeftijd van de gebruiker proberen te bepalen 
aan de hand van de volgende vragen:
- Maak je gebruik van Snapchat of Tiktok?
- Heb je ooit een Sony Walkman / discman gekocht? 
- Lees je regelmatig de krant?
- Geef je de voorkeur aan bellen of emailen / Whatsapp etc.
- Gebruik je bij het sturen van digitale berichten geregeld smileys zoals "😂"

### Gebruik: ###

Python venv maken: (optioneel)

`python -m venv dashboard_venv`

venv gebruiken: (optioneel)

`source /pad/naar/venv/bin/activate`

Libraries installeren:

`pip install -r requirements.txt`

Dashboard starten:

`python app.py`

Navigeer in de webbrowser naar het volgende adres: http://127.0.0.1:8050/


### Database / model verwijderen ###
Verwijder DB/database.db en assets/model.joblib

>Op deze zelfde plek kan je ook een bestaand model zetten om te gebruiken. 