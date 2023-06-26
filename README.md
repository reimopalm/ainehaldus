# Ainete haldamise tööriistad

Pythoni programmid ülikooli õppeainete läbiviimisel sagedamini ettetulevate tegevuste sooritamiseks, peamiselt Moodle'ist saadud andmete töötlemiseks.

## jagamoodletestid.py

Koondab Moodle'i testikatsete vastused ja punktide arvud ühte Exceli tabelisse, kus neid saab ülevaatlikult analüüsida.

### Kasutamine

1. Laadida alla kaks faili, hinnete alt punktide tabel ja vastuste alt vastuste tabel, mõlemad csv-vormingus, ning tõsta sobivasse kausta.
2. Selles kaustas olles käivitada programm `jagamoodletestid`.
3. Kui programm emba-kumba sisendfaili automaatselt üles ei leia, siis küsib selle nime.

Tulemuseks tekib Exceli tabel, kus iga küsimuse kohta on üks leht. Igal lehel on kirjas kõigi testisooritajate kõik vastused loetaval kujul. Vastused on järjestatud punktide arvu kahanemise järjekorras.

Veerus EP asub kahekohaline kood, mille esimene number näitab, kas see katse oli vastava lahendaja jaoks esimene, ja teine number, kas see katse oli parim. Küsimuse numbri määrab  küsimusevariantide arvu järgi. Punktide arvu teisendab skaalale 0-1. Veergu Uus võib kirjutada uue punktide arvu.

## jagamoodlefailid.py

Jagab Moodle'ist allalaaditud esituste zip-failis olevad tööd esitajate järgi alamkaustadesse. Niimoodi saab kõik tööd ühekorraga alla laadida ja vaadata need läbi oma arvutis.

* Toimib nii Moodle'i ülesande kui ka VPL-harjutuse vahendist saadud failidega.
* Eemaldab Moodle'i lisatud tehnilise info, jättes alles ainult õppija esitatud failid.
* Lisaks moodustab parandamise tekstifaili kõigi esitajate nimedega ajalises järjekorras.
* Toetab korduvat käivitamist: uuest failist pakib lahti ainult need esitused, kus on midagi muutnud.

### Kasutamine

1. Ülesande või VPL-harjutuse vahendist allalaaditud fail tõsta sobivasse kausta.
2. Selles kaustas olles käivitada programm `jagamoodlefailid`.
3. Programm püüab sisendfaili ise üles leida. Kui ta seda ei suuda, siis küsib failinime.
4. Sisestada ülesannete maksimaalsed punktide arvud ühes reas. Mitme arvu puhul eraldada need üksteisest koma, semikooloni või tühikuga.

Tulemuseks tekib iga õppija kohta alamkaust, mille sisuks kõik tema esitatud failid. Lisaks moodustatakse parandamise jaoks fail `parandamine.txt`, kuhu võib kirjutada ülesannete punktid ja tagasiside.

Muutunud esituse kirjutab uude alamkausta, mille nime lõpus on järjekorranumber, samuti lisab uue kirje parandamise faili lõppu. Olemasolevaid andmeid üle ei kirjuta.

## jagapdf.py

Võimaldab teha pdf-failidega mitmesuguseid tegevusi. Mõeldud esmajoones pabertööde sisseskannimisel saadud pdf-failide töötlemiseks, aga enamikku tegevustest saab teha ükskõik milliste pdf-failidega.

### Kasutamine

1. Kõik töödeldavad pdf-failid tõsta sobivasse kausta.
2. Käivitada programm `jagapdf` ja sisestada tegevuse number.
3. Vajadusel sisestada tegevuse sooritamiseks vajalikud muud andmed.

Programmiga saab teha järgmisi tegevusi.
* 1 - Jaga failid. Tükeldab pdf-failid eraldi pdf-failideks. Kõik saadud failid kirjutab ühte tulemuskausta. Tükeldamise piirid antakse ette failis `algused.txt`, kus on eraldi ridadel kirjas failinimi ja seejärel iga tüki alguslehe number ja nimi, näiteks 
```
esimene_tükeldatav_fail.pdf
1 Esimene Nimi
5 Teine Nimi
9 Kolmas Nimi
teine_tükeldatav_fail.pdf
1 Neljas Nimi
3 Viies Nimi
```

* 2 - Jaga failid ja loo parandamine. Tükeldab pdf-failid eraldi pdf-failideks ja lisaks moodustab parandamise abifaili `parandamine.txt`. Parandamise faili jaoks sisestada ülesannete maksimumpunktide arvud ühes reas, eraldatult koma, semikooloni või tühikuga. Nimedeks võetakse alguste failis kirjasolevad nimed.

* 3 - Kogu failid. Kogub tulemuskaustast pdf-failid kokku üheks suureks pdf-failiks `pdfkogu.pdf`.

* 4 - Moodusta tagasiside. Koostab tulemuskaustas olevate pdf-failide põhjal tagasisidefaili, mille saab Moodle'i ülesande vahendis kõigile korraga tagasisidena üles laadida. Tagasisidefaili koostamiseks vajab sellesama ülesande esitatud tööde alt allalaaditud hindamise töölehte (csv-faili).

* 5 - Asenda lehed. Asendab pdf-failis näidatud lehed teise pdf-faili näidatud lehtedega. Ette antakse pdf-faili nimi, asendatatavate lehtede numbrid, teise pdf-faili nimi, teise pdf-faili lehtede numbrid. Lehenumbrite järjendid peavad olema sama pikkusega.

* 6 - Muuda lehtede järjestust. Järjestab pdf-failis lehed ümber. Ette antakse pdf-faili nimi ja kaks sama pikka lehenumbrite järjendit. Tulemusena asendatakse esimeses järjendis nimetatud lehed teises järjendis nimetatud lehtedega.

* 7 - Pööra lehed ümber. Pöörab pdf-failis näidatud lehti 180 kraadi. Ette antakse pdf-faili nimi ja pööratavate lehtede numbrid.

* 8 - Kustuta lehed. Kustutab pdf-failis näidatud lehed. Ette antakse pdf-faili nimi ja kustutatavate lehtede numbrid.

## looparandamine.py

Loob parandamise abifaili `parandamine.txt`.

### Kasutamine

* Luua fail `nimed.txt`, kus on kirjas õppijate nimed soovitavas järjekorras.
* Käivitada programm `looparandamine`.
* Sisestada ülesannete maksimumpunktide arvud ühes reas, eraldajaks koma, semikoolon või tühik.

Tulemuseks on fail `parandamine.txt`, kuhu võib kirjutada iga õppija tagasiside ja ülesannete punktide arvud.

## koguprogrammid.py

Kogub näidatud osalejate Pythoni programmid programmid alamkaustadest kokku üheks failiks `programmid.py`. Sobib näiteks siis, kui on vaja koondada kokku ühe osaleja kõik programmid või kui on vaja kiiresti võrrelda paljude osalejejate Thonny logifailide sisu tegelikult esitatud programmidega.

### Kasutamine

1. Luua fail `nimed.txt`, kus on kirjas õppijate nimed soovitavas järjekorras.
2. Käivitada programm `koguprogrammid`.
3. Sisestada kaustade nimed, millest osalejaid otsitakse, eraldajaks koma, semikoolon või tühik.

Eeldab, et iga töö jaoks on oma kaust, mille all on omakorda õppijate failide kaustad. Ette antakse tööde kaustad, programm otsib nende seest õppijate kaustu.

Tulemuseks moodustatakse fail `programmid.py`, kus on järjest kirjas kõik leitud programmid koos osalejate nimede ja programmide nimedega.

## projektitagasiside.py

Kogub projektide hindamise küsitlusest kokku vastused ja grupeerib need projektide ning hindajate järgi. 

### Kasutamine

1. Laadida Moodle'ist alla projektide hindamise küsitluse vastuste fail csv-vormingus.
2. Käivitada programm `projektitagasiside`.
3. Kui programm vastuste faili automaatselt üles ei leia, siis küsib selle nime.

Tulemuseks on html-fail, kus on kirjas igale projekti saadud tagasiside ja iga hindaja antud tagasiside.

Eeldab, et küsitlus koosneb samade küsimuste plokkidest, kus iga ploki esimene küsimus on hinnatava projekti nimi. Püüab ise kindlaks teha, kas küsimus oli tekstivastusega või valitava vastusega. Mittesisukad vastused ja projekti autori poolt omaenda projektile antud valikvastused jätab vahele.
