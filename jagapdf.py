import os, re, zipfile, csv, datetime
from pypdf import PdfReader, PdfWriter

PDFKAUSTANIMI = "pdf"
PARANDAMISEFAILINIMI = "parandamine.txt"
PDFKOGUFAILINIMI = "pdfkogu.pdf"

def küsi_failinimi(küsimus, muster = ""):
    """
    Küsib kasutajalt failinime või võtab selle etteantud mustri järgi ise, kui leiab.
    """
    if muster:
        failinimed = [failinimi for failinimi in os.listdir() if re.search(muster, failinimi)]
        if len(failinimed) == 0:
            print("Jooksvast kaustast sobivaid faile ei leidnud.")
        elif len(failinimed) == 1:
            print(f"Leidsin faili '{failinimed[0]}'.")
            return failinimed[0]
        else:
            print(f"Leidsin {len(failinimed)} sobivat faili:")
            print("\n".join(failinimed))

    while True:
        failinimi = input(küsimus.rstrip()+" ").strip()
        if not failinimi:
            return
        if os.path.exists(failinimi):
            return failinimi
        print("Sellist faili pole.")

def küsi_punktid():
    """
    Küsib kasutajalt ülesannete maksimaalseid punktide arve.
    Sisestada ühe reana, eraldajaks tühik, koma või semikoolon.
    """
    while True:
        sisestus = input("Sisesta maksimumpunktid: ")
        if not sisestus.strip():
            return
        punktid = re.findall(r'[^ ,;]+', sisestus)
        kõik_sobivad = True
        for i, p in enumerate(punktid):
            try:
                punktid[i] = int(p)
            except:
                try:
                    punktid[i] = float(p)
                except:
                    print(f"Punktide arv '{p}' ei sobi.")
                    kõik_sobivad = False
        if kõik_sobivad:
            return punktid

def küsi_lehenumbrid(küsimus):
    """
    Küsib kasutajalt lehenumbreid.
    Sisestada ühe reana, eraldajaks tühik, koma või semikoolon.
    """
    while True:
        sisestus = input(küsimus.rstrip()+" ")
        if not sisestus.strip():
            return
        arvud = re.findall(r'[^ ,;]+', sisestus)
        kõik_sobivad = True
        for i, p in enumerate(arvud):
            try:
                arvud[i] = int(p)
                if arvud[i] < 1:
                    raise
            except:
                print(f"Lehenumber '{p}' ei sobi.")
                kõik_sobivad = False
        if kõik_sobivad:
            return arvud

def jaga_failid(parandamine=False):
    """
    Tükeldab pdf-faili eraldi failideks ja paneb need tulemuskausta.
    Vajadusel teeb lisaks parandamise abifaili.
    """
    algused = küsi_failinimi("Sisesta alguste faili nimi:", ".*algused.*[.]txt")
    if not algused:
        return

    if parandamine:
        punktid = küsi_punktid()
        if not punktid:
            return
        nimed = []

    pdfsisud = []
    with open(algused) as f:
        for rida in f:
            rida = rida.strip()
            if re.search(r'\d+\s\S', rida):
                pdfsisud[-1].append(rida)
            elif re.search(r'^.*[.]pdf$', rida):
                pdfsisud.append([rida])

    os.makedirs(PDFKAUSTANIMI, exist_ok=True)

    for pdfsisu in pdfsisud:
        pdffailinimi = pdfsisu[0]
        if os.path.isfile(pdffailinimi):
            print(pdffailinimi)
        else:
            print(f"Ei leia pdf-faili '{pdffailinimi}'")
            continue

        pdf_lugeja = PdfReader(pdffailinimi)

        for i in range(1, len(pdfsisu)):
            print(pdfsisu[i])
            alguslehenr, failinimi = pdfsisu[i].split(maxsplit=1)
            alguslehenr = int(alguslehenr.strip().strip("."))-1

            failinimi = failinimi.strip()
            if parandamine:
                nimed.append(failinimi)
            if not failinimi.endswith(".pdf"):
                failinimi = failinimi + ".pdf"
            failinimi = os.path.join(PDFKAUSTANIMI, failinimi)

            if i < len(pdfsisu)-1:
                nr, _ = pdfsisu[i+1].split(maxsplit=1)
                lõpulehenr = int(nr.strip().strip("."))-1
            else:
                lõpulehenr = len(pdf_lugeja.pages)

            pdf_kirjutaja = PdfWriter()

            for leht in pdf_lugeja.pages[alguslehenr:lõpulehenr]:
                pdf_kirjutaja.add_page(leht)

            pdf_kirjutaja.write(failinimi)

    if parandamine:
        try:
            f = open(PARANDAMISEFAILINIMI, "a")
        except:
            print(f"Parandamise faili '{PARANDAMISEFAILINIMI}' ei saa avada.")
            return
        praegu = datetime.datetime.now()
        for i, nimi in enumerate(nimed, start=1):
            if f.tell() != 0:
                f.write("\n\n")
            f.write(f"* {nimi}\n\n")
            if len(punktid) > 1:
                for ülnr, ülpun in enumerate(punktid, start=1):
                    f.write(f"{ülnr}. (/{ülpun})\n\n")
            else:
                f.write(f"(/{punktid[0]})\n\n")
            f.write(f"{'ETKNRLP'[praegu.weekday()]}    {praegu.day}.{praegu.month:02d} "
                    f"{praegu.hour}:{praegu.minute:02d}    {i}")
        f.close()

def kogu_failid():
    """
    Kogub pdfi kaustast failid kokku üheks pdf-failiks.
    """
    failinimed = [failinimi for failinimi in os.listdir(PDFKAUSTANIMI) if failinimi.endswith('.pdf')]
    failinimed.sort()
    pdf_kirjutaja = PdfWriter()
    for failinimi in failinimed:
        failitee = os.path.join(PDFKAUSTANIMI, failinimi)
        pdf_kirjutaja.append(failitee)
    pdf_kirjutaja.write(PDFKOGUFAILINIMI)

def moodusta_tagasiside():
    """
    Paneb kokku tagasisidefaili, mille saab Moodle'isse ülesande tagasisidena üles laadida.
    Osalejakoodid võtab Moodle'ist allalaaditud csv-failist.
    """
    hindamisfailinimi = küsi_failinimi("Sisesta koodide faili nimi:", ".*[.]csv")
    if not hindamisfailinimi:
        return
    koodid = {}
    with open(hindamisfailinimi, encoding="utf8") as csv_fail:
        csv_lugeja = csv.reader(csv_fail, delimiter=',')
        next(csv_lugeja)
        for rida in csv_lugeja:
            osaleja_nimi = rida[1]
            osaleja_kood = re.sub('[a-zA-Z]', '', rida[0])
            koodid[osaleja_nimi] = osaleja_kood
    zipnimi, _ = os.path.splitext(hindamisfailinimi)
    with zipfile.ZipFile(zipnimi + '.zip', mode='w') as z:
        failinimed = [failinimi for failinimi in os.listdir(PDFKAUSTANIMI) if failinimi.endswith('.pdf')]
        failinimed.sort()
        for failinimi in failinimed:
            osaleja_nimi, _ = os.path.splitext(failinimi)
            if osaleja_nimi not in koodid:
                print(f"Ei leia osalejat '{osaleja_nimi}'")
                continue
            failitee = os.path.join(PDFKAUSTANIMI, failinimi)
            zipkaustanimi = f"{osaleja_nimi}_{koodid[osaleja_nimi]}_assignsubmission_file_"
            zipkogunimi = os.path.join(zipkaustanimi, failinimi)
            z.write(failitee, zipkogunimi)

def asenda_lehed(teine_fail = False):
    """
    Asendab pdf-failis antud numbritega lehed samast või teisest failist võetud lehtedega.
    Lehenumbrid on täisarvud alatest 1st. Järjendid peavad olema sama pikkusega.
    """
    pdffailinimi = küsi_failinimi("Sisesta pdf-faili nimi:", "[.]pdf")
    if not pdffailinimi:
        return

    lehenumbrid = küsi_lehenumbrid("Sisesta asendatavad lehenumbrid:")
    if not lehenumbrid:
        return

    if teine_fail:
        teisepdffailinimi = küsi_failinimi("Sisesta uute lehtede pdf-faili nimi:", "[.]pdf")
        if not pdffailinimi:
            return

    teiselehenumbrid = küsi_lehenumbrid("Sisesta uued lehenumbrid:")
    if not lehenumbrid:
        return

    if len(lehenumbrid) != len(teiselehenumbrid):
        print(f"Lehenumbrite järjendid pole sama pikkusega: {lehenumbrid} ja {teiselehenumbrid}.")
        return

    pdf_lugeja1 = PdfReader(pdffailinimi)
    pdf_lugeja2 = PdfReader(teisepdffailinimi) if teine_fail else pdf_lugeja1
    pdf_kirjutaja = PdfWriter()
    for i, leht in enumerate(pdf_lugeja1.pages):
        if i+1 in lehenumbrid:
            j = teiselehenumbrid[lehenumbrid.index(i+1)]-1
            if j < len(pdf_lugeja2.pages):
                leht = pdf_lugeja2.pages[j]
        pdf_kirjutaja.add_page(leht)
    pdf_kirjutaja.write(pdffailinimi)

def töötle_lehti(tegevus):
    """
    Rakendab faili lehtedele nõutud tegevust.
    """

    pdffailinimi = küsi_failinimi("Sisesta pdf-faili nimi:", "[.]pdf")
    if not pdffailinimi:
        return

    lehenumbrid = küsi_lehenumbrid("Sisesta lehenumbrid:")
    if not lehenumbrid:
        return

    pdf_lugeja = PdfReader(pdffailinimi)
    pdf_kirjutaja = PdfWriter()
    for i, leht in enumerate(pdf_lugeja.pages):
        if i+1 in lehenumbrid:
            if tegevus == "pööra_ümber":
                leht.rotate(180)
                pdf_kirjutaja.add_page(leht)
        else:
            pdf_kirjutaja.add_page(leht)
    pdf_kirjutaja.write(pdffailinimi)


if __name__ == "__main__":

    failinimed = [failinimi for failinimi in os.listdir() if failinimi.endswith('.pdf')]
    if len(failinimed) == 0:
        print("Ei leidnud kaustast ühtegi pdf-faili.")
    else:
        print(f"Kaustas on fail{'id' if len(failinimed)>1 else ''}:")
        print("\n".join(failinimed))
    print()

    print("1 - Jaga failid")
    print("2 - Jaga failid ja loo parandamine")
    print("3 - Kogu failid")
    print("4 - Moodusta tagasiside")
    print("5 - Asenda lehed")
    print("6 - Muuda lehtede järjestust")
    print("7 - Pööra lehed ümber")
    print("8 - Kustuta lehed")
    print("0 - Lõpeta")

    print()

    while True:
        sisestus = input("Vali tegevus: ").strip()
        if sisestus == "1":
            jaga_failid()
        elif sisestus == "2":
            jaga_failid(True)
        elif sisestus == "3":
            kogu_failid()
        elif sisestus == "4":
            moodusta_tagasiside()
        elif sisestus == "5":
            asenda_lehed(True)
        elif sisestus == "6":
            asenda_lehed()
        elif sisestus == "7":
            töötle_lehti("pööra_ümber")
        elif sisestus == "8":
            töötle_lehti("kustuta")
        elif sisestus == "0" or sisestus == "":
            break
        print()