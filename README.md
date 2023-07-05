# Ainete haldamise tööriistad

Pythoni programmid ülikooli õppeainete läbiviimisel sagedamini ettetulevate tegevuste sooritamiseks, peamiselt Moodle'ist saadud andmete töötlemiseks. Võite kasutada sellisena nagu on või kohandada oma vajaduste järgi.

## jagamoodletestid.py

Paigutab Moodle'i testi vastused ja punktide arvud ülevaatlikult Exceli tabelisse. Sobib näiteks testiküsimuste toimimise uurimiseks, samuti vastuste käsitsi ülevaatamiseks.

**Kasutamine**

1. Laadida alla kaks faili, testi hinnete alt punktide tabel ja testi vastuste alt vastuste tabel, mõlemad csv-vormingus, ning tõsta sobivasse kausta.
2. Selles kaustas olles käivitada programm `jagamoodletestid`.

Programm leiab sisendfailid jooksvast kaustast ise üles. Kui ta seda ei suuda, siis küsib failinime kasutajalt. Sisestada võib ka alamkaustas oleva faili koos otsimisteega.

Tulemusena luuakse Exceli tabel, kus iga küsimuse kohta on üks leht, millel on kirjas kõigi testisooritajate sellele küsimusele antud vastused loetaval kujul. Vastused on järjestatud punktide arvu kahanemise järjekorras. Tabelis saab vastuseid kõigi veergude järgi filtreerida.

Veerus EP asub kahekohaline kood, mille esimene number näitab, kas see katse oli vastaja jaoks esimene, ja teine number, kas see katse oli parim. Küsimuse number määratakse küsimuse variantide arvu järgi. Kui küsimus kasutab juhuslikkust ja vastuse osad seetõttu on juhuslikus järjekorras, siis sorteeritakse need tähestikuliselt. Punktide arv teisendatakse skaalale 0-1, püüdes tulemust mõistlikult ümardada. Veergu Uus võib kirjutada uue punktide arvu või muu oma kommentaari.

## jagamoodlefailid.py

Jagab Moodle'ist allalaaditud esituste zip-failis olevad tööd esitajate järgi alamkaustadesse. Niimoodi saab kõik tööd ühekorraga alla laadida ja tegeleda nendega oma arvutis.

* Toimib nii Moodle'i ülesande kui ka VPL-harjutuse vahendist saadud failidega.
* Eemaldab Moodle'i lisatud tehnilise info, jättes alles ainult õppija esitatud failid.
* Lisaks moodustab parandamise jaoks abifaili kõigi esitajate nimedega ajalises järjekorras.
* Toetab korduvat käivitamist: uuest failist pakib lahti ainult need esitused, kus on midagi muutnud.

**Kasutamine**

1. Ülesande või VPL-harjutuse vahendist allalaaditud fail tõsta sobivasse kausta.
2. Selles kaustas olles käivitada programm `jagamoodlefailid`.
3. Programm püüab sisendfaili ise üles leida. Kui ta seda ei suuda, siis küsib failinime.
4. Sisestada ülesannete maksimaalsed punktide arvud ühes reas. Mitme arvu puhul eraldada need üksteisest tühiku, koma või semikooloniga.

Tulemuseks tekib iga õppija kohta alamkaust, milles asuvad kõik tema esitatud failid. Lisaks moodustatakse parandamise jaoks fail `parandamine.txt`, kuhu võib kirjutada ülesannete punktid ja tagasiside.

Kui esitust on muudetud, siis paigutab selle uude alamkausta, mille nime lõpus on järjekorranumber. Olemasolevaid faile üle ei kirjuta. Parandamise failis tõstab vastava kirje koos tekstiga faili lõppu, seda võib seejärel muuta.

## jagapdf.py

Võimaldab teha pdf-failidega mitmesuguseid tegevusi. Mõeldud eeskätt pabertööde sisseskannimisel saadud pdf-failide töötlemiseks, aga enamikku tegevustest saab teha ükskõik milliste pdf-failidega.

**Kasutamine**

1. Kõik töödeldavad pdf-failid tõsta sobivasse kausta.
2. Käivitada selles kaustas olles programm `jagapdf` ja sisestada tegevuse number.
3. Vajadusel sisestada valitud tegevuse sooritamiseks vajalikud muud andmed.

Programmiga saab teha järgmisi tegevusi.
* 1 - Jaga failid. Tükeldab pdf-failid eraldi pdf-failideks. Saadud failid kirjutab kõik ühte tulemuskausta. Tükeldamise piirid antakse ette failis `algused.txt`, kus on eraldi ridadel kirjas failinimi ja seejärel iga tüki alguslehe number ja nimi. Tükeldatavaid faile võib olla mitu. Nimedeks võivad olla õppijate nimed, laiend lisatakse failile automaatselt. Näiteks: 
```
esimene_tükeldatav_fail.pdf
1 Esimene Nimi
5 Teine Nimi
9 Kolmas Nimi
teine_tükeldatav_fail.pdf
1 Neljas Nimi
3 Viies Nimi
```

* 2 - Jaga failid ja loo parandamine. Tükeldab pdf-failid eraldi pdf-failideks ning lisaks moodustab parandamise abifaili `parandamine.txt`. Nimedeks võetakse alguste failis kirjasolevad nimed. Lisaks tuleb sisestada sisestada parandatavate ülesannete maksimumpunktide arvud ühes reas, eraldatult tühiku, koma või semikooloniga. 

* 3 - Kogu failid. Kogub tulemuskaustast pdf-failid kokku üheks suureks pdf-failiks `pdfkogu.pdf`.

* 4 - Moodusta tagasiside. Paneb tulemuskaustas olevatest pdf-failidest kokku tagasisidefaili, mille saab Moodle'i ülesande vahendis kõigile korraga tagasisidena üles laadida. Vajab tööks selle ülesande hindamise töölehte (csv-faili), mille saab alla laadida Moodle'ist ülesande esituste vaatest.

* 5 - Asenda lehed. Asendab pdf-failis lehed teise pdf-faili lehtedega. Ette antakse pdf-faili nimi, asendatatavate lehtede numbrite loend, teise pdf-faili nimi, teise pdf-faili lehtede numbrite loend. Lehed võib ette anda üksiknumbrite või vahemikena, eraldajaks tühikud, komad või semikoolonid, näiteks 3, 5-7, 9. Loendid peavad koosnema samast arvust gruppidest.

* 6 - Muuda lehtede järjestust. Järjestab pdf-failis lehed ümber. Ette antakse pdf-faili nimi ja kaks sama pikka lehenumbrite loendit. Tulemusena asendatakse esimeses loendis nimetatud lehed teises loendis nimetatud lehtedega.

* 7 - Pööra lehed ümber. Pöörab pdf-failis lehti 180 kraadi. Ette antakse pdf-faili nimi ja pööratavate lehtede numbrid.

* 8 - Kustuta lehed. Kustutab pdf-failis näidatud lehed. Ette antakse pdf-faili nimi ja kustutatavate lehtede numbrid.

## looparandamine.py

Loob parandamise abifaili `parandamine.txt`.

**Kasutamine**

* Luua soovitavasse kausta fail `nimed.txt`, kuhu panna kirja õppijate nimed soovitavas järjekorras.
* Käivitada programm `looparandamine`.
* Sisestada ülesannete maksimumpunktide arvud ühe reana, eraldajaks tühikud, komad või semikoolonid.

Tulemuseks on fail `parandamine.txt`, kuhu võib kirjutada iga õppija tagasiside ja ülesannete eest saadud punktide arvud. Kui õppija nimi on parandamise failis juba olemas, siis tõstab vastava kirje koos tekstiga faili lõppu, seda võib seejärel muuta.

## koguprogrammid.py

Kogub osalejate Pythoni programmid alamkaustadest kokku üheks failiks `programmid.py`. Sobib näiteks siis, kui on vaja ühe osaleja kõik programmid ühte kohta koondada või kui on vaja kiiresti võrrelda paljude osalejejate Thonny logifailide sisu tegelikult esitatud programmidega.

**Kasutamine**

1. Luua põhikausta fail `nimed.txt`, kus on kirjas õppijate nimed soovitavas järjekorras.
2. Käivitada programm `koguprogrammid`.
3. Sisestada alamkaustade nimed, millest osalejaid otsitakse, eraldajaks koma, semikoolon või tühik.

Eeldab, et iga töö jaoks on oma alamkaust, mille all on omakorda õppijate failide kaustad. Ette antakse tööde kaustade nimed, nende seest otsib programm õppijate kaustu.

Tulemuseks moodustatakse fail `programmid.py`, kus on järjest kirjas kõik leitud programmid koos osalejate nimede ja programmide nimedega.

## projektitagasiside.py

Kogub projektide hindamise küsitlusest kokku vastused ja rühmitab need projektide ning hindajate järgi. 

**Kasutamine**

1. Laadida Moodle'ist alla projektide hindamise küsitluse vastuste fail csv-vormingus.
2. Käivitada programm `projektitagasiside`.

Kui programm vastuste faili automaatselt üles ei leia, siis küsib selle nime.

Tulemuseks on html-fail, kus on kirjas igale projekti saadud tagasiside ja iga hindaja antud tagasiside.

Eeldab, et küsitlus koosneb samasugustest küsimuste plokkidest, kus iga ploki esimene küsimus on hinnatava projekti nimi. Püüab ise kindlaks teha, kas küsimus oli tekstivastusega või valikvastusega. Mittesisukad vastused ja projekti autori poolt omaenda projektile antud valikvastused jätab vahele.
