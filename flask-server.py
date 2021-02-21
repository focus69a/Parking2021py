#region importy i inicjalizacja Flaska oraz MongoDB

#uslugi
#https://cloud.mongodb.com/v2/5e5180442f8b4e74c2ed0fc2#security/network/accessList   skladuje dane w NON SQL
#https://leafletjs.com/reference-1.7.1.html                             rysuje mape 
#RESTlink = 'https://nominatim.openstreetmap.org/?addressdetails=1&q='  zamienia adres na GEO


from flask import Flask   # podstawowe funckcje flask
from flask import redirect, url_for  # przekierowanie routingu to innego url np. /admin (2)
from flask import render_template  # to pozwala wyswietlac pliki html
from flask import request # to pozwala rozpoznawac czy przyszlo POST czy GET przyklad 6 - login
import sys #pozwala drukowac na konsole komunikaty i tylko po to
from flask import session # to pozwala przechowywac dane sesji  przyklad index7
# from flask.ext.MongoEngine import MongoEngine   
import dns # to jest po to żeby zadziałał protokół łączenia do mongo w AWS 
import mongoengine  # a to jest wraper dla mongo i pymongo z budowaniem modeli danych

import secrets  #ponizsze 3 linijki służą do generowania tokenu do trzymania sesji z userem
secret = secrets.token_urlsafe(32)

from datetime import timedelta #to nie jest konieczne ale jak chcemy dlugosc sesji pilnowac to potrzeba
import requests     #potrzebne żeby robić REST API pytania do szukania adresu
import json         #potrzebne żeby czytać jsony z adresami

app = Flask(__name__, template_folder= '.')
app.secret_key = secret    #ustawienie szyfrowania parametru session
app.permanent_session_lifetime=timedelta(minutes=5)  #przez tyle minut bedzie trzymana sesja dodac pozniej w route session.permanent = True

app.config["MONGODB_DB"] = 'baza1'
db = mongoengine # ???
db.connect(
       db='baza1',
       username='fafikuser',
       password='fafikuser',
       host='mongodb+srv://fafikuser:fafikuser@cluster0.86xtb.mongodb.net/baza1?retryWrites=true&w=majority'
)
# client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.86xtb.mongodb.net/<dbname>?retryWrites=true&w=majority")
# db = client.test
#db.init_app(app)

#endregion
# =============================================================================
#region  przyklady z kursu

# @app.route("/")
# def home():
#     # return render_template("index.html", content="Testing")
#     return "Hej to jest flask <h1>Tytul </h1>"


@app.route("/<p1>")  #to trick jak przekazac parametr fo flaska z przegladarki - robimy to w nawiasach
def user(p1):
    return f"Hej to jest parametr {p1}"

@app.route("/admin")  #przyklad przekierowania z admin do glownego katalogu
def admin():
    return redirect(url_for("home"))   #tu podajemy nazwe funkcji do wywolania z innego routa

@app.route("/render1")  #przyklad przekazania parametru do strony na 2 sposoby
def render1():
    name = "to_to_jest_content"
    return render_template("index.html", content=name, r=2)   #tu podajemy nazwe funkcji do wywolania z innego routa

@app.route("/render2")  #przyklad przekierowania z admin do glownego katalogu
def render2():
    name = "to_to_jest_content"
    return render_template("index2.html", content=name, r=2)   #tu podajemy nazwe funkcji do wywolania z innego routa

@app.route("/render3")  #przyklad przekierowania z admin do glownego katalogu
def render3():
    name = "przekazanie_listy"
    return render_template("index3.html", content=name, lista=["poz1","poz2","poz3"])   #tu podajemy nazwe funkcji do wywolania z innego routa

@app.route("/bloki1")  #przyklad budowania strony z blokow
def bloki1():
    return render_template("index4.html")   #tu podajemy nazwe funkcji do wywolania z innego routa

@app.route("/bootstrap")  #przyklad budowania strony z blokow
def bootstrap1():
    return render_template("index5.html")   # zeby dzialal bootstrap we wszystkich stronach np. navbar to trzeba ten blok dodawac jako {% extends ...html %}

@app.route("/login", methods=["GET", "POST"])  # metody GET i POST oraz przekazzywanie danych z formularza
def login():
    if request.method == "POST":
        adres_email = request.form["exampleInputEmail1"]
        password = request.form["exampleInputPassword1"]
        checkbox = request.form.get("exampleCheck1")
        print(adres_email, password, checkbox, file=sys.stdout, flush=True) 
        return render_template("index6.html")  
    else:
        print('to byl GET', file=sys.stdout, flush=True)
        return render_template("index6.html")   

@app.route("/login1", methods=["GET", "POST"])  # jak dziala utrzymanie sesji - /session 1 przekazuje i zapamietuje user email i pwd a /session2 wyswietli tego usera
def login1():
    if request.method == "POST":
        adres_email = request.form["exampleInputEmail1"]
        password = request.form["exampleInputPassword1"]
        checkbox = request.form.get("exampleCheck1")

        session["adres_usera"] = adres_email
        session.permanent = True     # to mowi ze sesja ma byc utrzymana tyle czasu ile podane na gorze
    
        print(adres_email, file=sys.stdout, flush=True) 
        return f"<h1>wywolaj teraz sciezkę /session2 </h1>"  
    else:
        print('to byl GET', file=sys.stdout, flush=True)
        return render_template("index7.html")  

@app.route("/session1", methods=["GET", "POST"])  # metody GET i POST
def session1():
    if "adres_usera" in session:
        adres_email = session["adres_usera"]
        return f"<p> pamiętam z poprzedniego zapytania usera {adres_email}</p>"  
    else:
        return f"<p>nie pamietam usera, najpierw wywolaj /login1 </p>"  

@app.route("/logout1")
def logout1():
    session.pop("adres_usera", None)  # usuwa dane klienta z sesji
    return redirect(url_for("login1"))  #wraca nas do strony logowania

# zabawa z mongo
#endregion
#region model daych
class collection1(db.Document):  # definicja danych miejsca parkingowego
    sms = db.StringField()
    nr = db.StringField()
    lat = db.StringField()
    lon = db.StringField()
    status = db.StringField()
    link4nav = db.StringField()

class Users(db.Document):  # definicja danych miejsca parkingowego
    userID = 	db.DecimalField()   #1...m
    sms = db.StringField()
    carPlate = 	db.StringField()
    grupa =	db.ListField(db.StringField())


class Spaces(db.Document):  # definicja danych miejsca parkingowego
    spaceID =	db.StringField()   #1...n
    #spaceID =	db.DecimalField()   #1...n
    sms = 	db.StringField()   #+48 123456789
    location = db.PointField()
    opis =	db.StringField()
    status = db.StringField()  # ’free’, ’busy’, carPlate ‚’OOO’ 
    rezerwacjaDo = db.ComplexDateTimeField()
    link4nav = db.StringField()
    picture = db.StringField()
    grupa = db.ListField(db.StringField())

class WaitingLists(db.Document): 
    spaceID = db.StringField() #1..n
    waitingUsersID= db.ListField(db.StringField())
#endregion
#region ładowanie inicjalne daych
@app.route("/loadUsers") #inicjalne ładowanie danych o uzytkownikach 4 szt
def loadUsers():
    record = Users(sms = "601000001") 
    record.userID = 1
    record.carPlate ="WE111111"
    record.grupa = ['public', 'ibm', 'zus']
    record.save()
    
    record = Users(sms = "601000002")
    record.userID = 2
    record.carPlat ="WE222222"
    record.grupa = ['public', 'ibm', 'zus']
    record.save()

    record = Users(sms = "601000003")
    record.userID = 3
    record.carPlat ="WE333333"
    record.grupa = ['public', 'ibm', 'zus']
    record.save()

    record = Users(sms = "601000004")
    record.userID = 4
    record.carPlat ="WE444444"
    record.grupa = ['public', 'ibm', 'zus']
    record.save()
    return f"<p> dane uzytkownikow załadowane </p>"

@app.route("/loadSpaces")  #inicjalne ładowanie danych o miejscach parkingowych 10szt
def loadSpaces():
    record = Spaces(spaceID = 1) 
    record.sms = "+486020000001"
   # record.location = [21.012097, 52.220061]
    record.location = {
    "type": "Point",
    "coordinates": [ 21.012097, 52.220061 ]}
    record.opis = "miejsce 1 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.2261204,21.0033269,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'ibm', 'zus']
    record.save()

    record = Spaces(spaceID = 2) 
    record.sms = "+486020000002"
   # record.location = [21.012197, 52.220161]
    record.location = {
    "type": "Point",
    "coordinates": [ 21.012197, 52.220161 ]}
    record.opis = "miejsce 2 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.220161,21.012197,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'ibm', 'zus']
    record.save()

    record = Spaces(spaceID = 3) 
    record.sms = "+486020000003"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 21.012297, 52.220261 ]}
    record.opis = "miejsce 3 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.220261,21.012297,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    record = Spaces(spaceID = 4) 
    record.sms = "+486020000004"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 20.980266056565338, 52.235995405273464 ]}
    record.opis = "miejsce 4 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.235995405273464,20.980266056565338,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    record = Spaces(spaceID = 5) 
    record.sms = "+486020000005"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 20.980379802989102, 52.23571241358325 ]}
    record.opis = "miejsce 5 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.23571241358325, 20.980379802989102,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    record = Spaces(spaceID = 6) 
    record.sms = "+486020000006"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 20.981958010958547, 52.23529444558823 ]}
    record.opis = "miejsce 6 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.23529444558823, 20.981958010958547,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    record = Spaces(spaceID = 7) 
    record.sms = "+486020000007"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 20.977466267998945, 52.23288713563373 ]}
    record.opis = "miejsce 7 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.23288713563373, 20.977466267998945,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    record = Spaces(spaceID = 8) 
    record.sms = "+486020000008"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 20.97809558313284, 52.234410789177645 ]}
    record.opis = "miejsce 8 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.234410789177645, 20.97809558313284,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    record = Spaces(spaceID = 9) 
    record.sms = "+486020000009"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 20.976822375866345, 52.23442872418827 ]}
    record.opis = "miejsce 9 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.23442872418827, 20.976822375866345,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    record = Spaces(spaceID = 10) 
    record.sms = "+486020000010"
   # record.location = [21.012297, 52.220261]
    record.location = {
    "type": "Point",
    "coordinates": [ 20.977012625596835, 52.23446457439213 ]}
    record.opis = "miejsce 10 kolo przystanku"
    record.status = "free"
    record.rezerwacjaDo = '2021,01,18,19,48,00,000000' #"YYYY,MM,DD,HH,MM,SS,NNNNNN"
    record.link4nav = "https://www.google.pl/maps/@52.23446457439213, 20.977012625596835,15.51z"
    record.picture = "../pic/m1"
    record.grupa =  ['public', 'pw']
    record.save()

    return f"<p> Spaces załadowane inicjalnie - 10 szt Wawa </p>"
#endregion
#region endpointy testowe /findSpace /ile1 /rezerwacja1
@app.route("/findSpace")
def findSpace():
    y = 300   #zasieg w jakim szukamy miejsca
    x = Spaces.objects( location__near = [ 20.977012625596835, 52.23446457439213 ], location__max_distance = y ).count()
    return f"<p> Znalazlem { x } miejsc w zasiegu { y } m </p>"   #zwraca ile znalaz obiektow w zasiegu


@app.route("/ile1")
def ile1():
    x = collection1.objects.count()
    print(x, file=sys.stdout, flush=True)  #mongo zwraca liczbe obiektow wszystkich w kolekcji
    yy = collection1.objects(status = 'free')    #zwara te ze statusem free
    for y in yy:
        print(y.sms, file=sys.stdout, flush=True)  # drukujemy dla tych wolnych wartosc pola .sms
    
    return f"<p> { x } { y.sms } </p>"  # i pokazuje na stronie liczbe obiektow w bazie i ostatni wolny

@app.route("/rezerwacja1")    
def rezerwacja1():
    nowa_rezerwacja = collection1.objects(nr='1').first()
    nowa_rezerwacja.update(status = 'WE0001AA')

    x = collection1.objects.count()
    print(x, file=sys.stdout, flush=True)  #mongo zwraca liczbe obiektow
    yy = collection1.objects()  # pobiera wszystkie z kolecji
    for y in yy:
        print(y.status, file=sys.stdout, flush=True)  #mongo zwraca liczbe obiektow
    
    return f"<p> { x } { y.status } </p>"  #wraca nas do strony logowania

#endregion

#========================APLIKACJA PARKING - BEGIN ============================================= 

@app.route("/")
@app.route("/parking_login", methods=["GET", "POST"])  # jak dziala utrzymanie sesji - /session 1 przekazuje i zapamietuje user email i pwd a /session2 wyswietli tego usera
def parking_login():
    if request.method == "POST":
        userID = request.form["userID"]
        pin = request.form["InputPIN"]

        session["userID"] = userID
        session.permanent = True     # to mowi ze sesja ma byc utrzymana tyle czasu ile podane na gorze
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++" + pin, file=sys.stdout, flush=True) 
        print("Zalogował się use nr: " + userID + ", PIN: " + pin, file=sys.stdout, flush=True) 
        
        #przygotowanietlenia do wyswietlenia rezerwacji
        if request.form["action"] == "Display":
            userID = userID
            spaceID = 7 
            adres = "Warszawa ul.Nowowiejska 7"
            rezerwacjaDo = '2021,01,18,19,48,00,000000'
            link4nav = "https://www.google.pl/maps/@52.23288713563373, 20.977466267998945,15.51z"
            picture = "/static/ParkingSpace1.jpg"
            grupa =  ['public', 'pw']
            opis ="miejsce 7 kolo przystanku"

            #return redirect(url_for("parking_display")) 
            #print('Msg-10-POST', file=sys.stdout, flush=True)
            return render_template("parking_display.html", p1=userID, p2=spaceID, p3=adres, p4=rezerwacjaDo, p5=link4nav, p6=picture, p7=grupa, p8=opis)   #tu podajemy nazwe funkcji do wywolania z innego routa
        elif request.form["action"] == "Search":
            #print('Msg-11-POST', file=sys.stdout, flush=True)
            return render_template("parking_search.html")  
        else: 
            #print('Msg-12-POST', file=sys.stdout, flush=True)
            return render_template("parking_login.html")  
    else:
        #print('Msg-2-GET-ladowanie pustego formularza', file=sys.stdout, flush=True)
        return render_template("parking_login.html")  

@app.route("/parking_display", methods=["GET", "POST"])  # metody GET i POST
def parking_display():
    if "userID" in session:
        nr_tel = session["userID"]
        print('wywolujemy Display z userID= '+ nr_tel, file=sys.stdout, flush=True)
        if request.form["action"] == "Open":
            p1 = nr_tel
            p2 = "Warszawa adres"
            p3 = "rezerwacja ważna do 15:35"
            p4 = "link to miejsca www/gogle.mapy.com/xrz.txer.ea"

            return f"<p> Otwieramy Gate </p>"
       
        elif request.form["action"] == "Cancel":
            return f"<p> Trzeba odwolac rezerwacje </p>"
       
        elif request.form["action"] == "Return":
            # return f"<p> chce wrocic do loginu </p>"
            # return redirect(url_for("parking_login"))
            return render_template("parking_login.html")   #tu podajemy nazwe funkcji do wywolania z innego routa

    else:
        return f"<p>nie pamietam usera, najpierw wywolaj /parking_login </p>"  
        return redirect(url_for("home"))

def zbuduj_liste_odpowiedzi(parsed):  #buduje liste potencjalnych celow podrozy do wyswietlenia do dokladnego wyboru

    #print(json.dumps(parsed, indent=4, sort_keys=True))

    #print('>>Zbuduj_liste_odpowiedzi<< -> Liczba znalezionych potencjalnych adresow docelowych 1a: ',  len(parsed), file=sys.stdout, flush=True)

    nowy_json = [] 
    nr_pos = 0
    for i in parsed:
        temp_lista = {}
        temp_lista['nr_pos'] = nr_pos
        temp_lista['lat']=i.get('lat')
        temp_lista['lon']=i.get('lon')
        temp_lista['address']=str(i.get('address').get('country')) + "," + str(i.get('address').get('state')) + "," + str(i.get('address').get('city')) + "," + str(i.get('address').get('suburb')) + "," + str(i.get('address').get('road')) + "," + str(i.get('address').get('house_number'))
        nowy_json.append(temp_lista)
        nr_pos = nr_pos+1 
    #print('>>Zbuduj_liste_odpowiedzi<< -> Odchudzone lista atrybutow potencjalnych adresow docelowych 1b: ',  len(nowy_json), file=sys.stdout, flush=True)
    return nowy_json

def findSpaces(lat, lon, range_min, range_max, status):    #szukamy miejsc wokol punktu docelowego w mongoDB
    r_min = range_min   #zasieg w jakim szukamy miejsca
    r_max = range_max
    lon = lon
    lat = lat
    status = status
    #print('>>findSpaces<< lon: ' + lon + ' lat: ' + lat , file=sys.stdout, flush=True)
    #pobieramy do x wszyskie obiekty w danym zasiegu
    #ile_wolnych = Spaces.objects( location__near = [ float(lon), float(lat) ], location__min_distance = r_min ,location__max_distance = r_max, status = 'free' ).count()
    lista = Spaces.objects( location__near = [ float(lon), float(lat) ], location__min_distance = r_min ,location__max_distance = r_max, status = status )

    print(" >>findSpace<< Znalazlem: " + str(len(lista)) + " o statusie " + status  + " miejsc parkingowych w zasiegu: " + str(r_min) + " - " + str(r_max)+ " m", file=sys.stdout, flush=True)

    print(" >>findSpace<< Lista wynikow z mongoDB: ", file=sys.stdout, flush=True)
    for x in lista:
        print(str(x.spaceID), x.status, x.location['coordinates'][0], x.location['coordinates'][1], file=sys.stdout, flush=True)  # drukujemy dla tych co zostaly zwrococe, takze wolne i zajete

    wynik_lista_json = [] 
    for x in lista:
        temp_lista = {}
        temp_lista['spaceID'] = x.spaceID
        temp_lista['status'] = x.status
        temp_lista['opis'] = x.opis
        temp_lista['lat'] = x.location['coordinates'][1]
        temp_lista['lon']=x.location['coordinates'][0]
        wynik_lista_json.append(temp_lista)
    
    return wynik_lista_json

@app.route("/parking_search", methods=["GET", "POST"])  # metody GET i POST
def parking_search():
    if "userID" in session:
        userID = session["userID"]
        if request.form["action"] == "Search":
            p1 = request.form["Destination"]
            #print('>>/parking_search<< bedziemy szukac potencjalnych Destination= '+ p1, file=sys.stdout, flush=True)

            RESTlink = 'https://nominatim.openstreetmap.org/?addressdetails=1&q='
            RESTquery = p1 
            RESTparm = '&format=json&limit=20'
            query = RESTlink + RESTquery + RESTparm
            response = requests.get(query)
            struktura = response.json()
            #print('>>/parking_search<< ', response.json(), file=sys.stdout, flush=True)
            parsed = json.loads(response.text)
            
            wybrana_lista = zbuduj_liste_odpowiedzi(parsed)
            #print('>>/parking_search<< Liczba znalezionych potencjalnych adresow docelowych 1a: ',  len(wybrana_lista), file=sys.stdout, flush=True)
            #print ('>>/parking_search<<  Nowy krótki json: ', file=sys.stdout, flush=True)
            #print(json.dumps(wybrana_lista, indent=4, sort_keys=True), file=sys.stdout, flush=True)
            return render_template("parking_search.html", wybrana_lista = wybrana_lista) 


        # elif request.form["action"] == "xxx":
        #     return render_template("parking_select.html") 
            #return render_template("parking_cancel.html")
        elif request.form["action"] == "Return":
            return render_template("parking_login.html")   #tu podajemy nazwe funkcji do wywolania z innego routa

    else:
        return f"<p>nie pamietam usera, najpierw wywolaj /parking_login </p>"  
        return redirect(url_for("home"))

@app.route("/parking_select/<nr_pos>/<lat>/<lon>/<address>", methods=["GET", "POST"])  # metody GET i POST
def parking_select(nr_pos,lat,lon,address):
    if "userID" in session:
        userID = session["userID"]
        radius1 = 200
        radius2 = 500
        radius3 = 1000
        #print('>>/parking_select<< wybrane selection:  '+ nr_pos, file=sys.stdout, flush=True)
        lista_short_free = findSpaces(lat, lon, range_min=0, range_max=radius1, status="free")
        lista_short_busy = findSpaces(lat, lon, range_min=0, range_max=radius1, status="busy")
        lista_medium_free = findSpaces(lat, lon, range_min=radius1, range_max=radius2, status = "free")
        lista_medium_busy = findSpaces(lat, lon, range_min=radius1, range_max=radius2, status = "busy")
        lista_long_free = findSpaces(lat, lon, range_min=radius2, range_max=radius3, status = "free")
        lista_long_busy = findSpaces(lat, lon, range_min=radius2, range_max=radius3, status = "busy")
        #return f"<p> wybrano: {nr_pos}, {lat}, {lon}, {address}, a user= {userID} </p>"
        # return redirect(url_for("parking_login"))
        print(" >>parking_select<< Lista wynikow z mongoDB: ", file=sys.stdout, flush=True)
        for x in lista_medium_free:
            print(int(x.get('spaceID')),  x.get('status'), x.get('lat'), x.get('lon'), file=sys.stdout, flush=True)  # drukujemy dla tych co zostaly zwrococe, takze wolne i zajete

        print('>>/parking_select<<  Pozycje z listy_med: ',  len(lista_medium_free), file=sys.stdout, flush=True)
        #return render_template("parking_select.html", lat=lat, lon=lon, radius1=radius1, radius2=radius2, radius3=radius3, lista1=json.dumps(lista_short_distance), lista2=json.dumps(lista_medium_distance), lista3=json.dumps(lista_long_distance)) #bedzie wyswietlona okolica z pinezkami parkingow 
        return render_template("parking_select.html", lat=lat, lon=lon, radius1=radius1, radius2=radius2, radius3=radius3, lsf=json.dumps(lista_short_free), lsb=json.dumps(lista_short_busy), lmf=json.dumps(lista_medium_free), lmb=json.dumps(lista_medium_busy), llf=json.dumps(lista_long_free), llb=json.dumps(lista_long_busy)) #bedzie wyswietlona okolica z pinezkami parkingow 

    else:
        return f"<p>nie pamietam usera, najpierw wywolaj /parking_login </p>"  
        # return redirect(url_for("home"))

@app.route("/logout2")
def logout2():
    session.pop("adres_usera", None)  # usuwa dane klienta z sesji
    return redirect(url_for("login1"))  #wraca nas do strony logowania

#========================APLIKACJA PARKING - END ============================================= 

if __name__ == "__main__":
    app.run(debug=True)      # parametr ten pozwala nie przeladowywac za kazdym razem serwera po zmianach
