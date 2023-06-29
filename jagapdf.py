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
    Sisestada ühe reana, eraldajaks tühikud, komad või semikoolonid.
    """
    while True:
        sisestus = input(küsimus.rstrip()+" ")
        if not sisestus.strip():
            return

        arvud = re.findall(r'[^ ,;]+', sisestus)
        paarid = []

        for i, el in enumerate(arvud):
            el = el.strip()

            if re.search(r'^\d+$', el):
                x1 = x2 = int(el)
            elif re.search(r'^\d+\s*-\s*\d+$', el):
                x1, x2 = map(int, re.split(r'-', el))
            elif re.search(r'-\s*\d+', el):
                x1, x2 = 1, int(el[1:])
            elif re.search(r'\d+\s*-', el):
                x1, x2 = int(el[:-1]), 10**6
            else:
                print(f"Element '{el}' on sobimatul kujul.")
                break

            if x1 == 0:
                print(f"Lehenumber ei või olla null: '{el}'.")
                break
            if x1 > x2:
                print(f"Vahemiku '{el}' algus on suurem kui lõpp.")
                break
            ind = next((j for j, (y1, y2) in enumerate(paarid[:i]) if x1 <= y2 and y1 <= x2), -1)
            if ind != -1:
                print(f"Lehed {arvud[ind]} ja {el} kattuvad.")
                break
            paarid.append((x1-1, x2-1))
        else:
            return paarid

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

def töötle_lehti(tegevus):
    """
    Rakendab pdf-faili lehtedele etteantud tegevust.
    """
    pdffailinimi = küsi_failinimi("Sisesta pdf-faili nimi:", "[.]pdf")
    if not pdffailinimi:
        return
    pdf_lugeja1 = PdfReader(pdffailinimi)
    X = len(pdf_lugeja1.pages)

    lehenumbrid = küsi_lehenumbrid("Sisesta lehenumbrid:")
    if not lehenumbrid:
        return

    if tegevus == "asenda_lehed":
        teisepdffailinimi = küsi_failinimi("Sisesta uute lehtede pdf-faili nimi:", "[.]pdf")
        if not pdffailinimi:
            return
        pdf_lugeja2 = PdfReader(teisepdffailinimi)
        Y = len(pdf_lugeja2.pages)

    if tegevus in ["asenda_lehed", "muuda_järjestust"]:
        teiselehenumbrid = küsi_lehenumbrid("Sisesta uued lehenumbrid:")
        if not lehenumbrid:
            return
        if len(lehenumbrid) != len(teiselehenumbrid):
            print(f"Lehenumbrite järjendid pole sama pikkusega.")
            return

    pdf_kirjutaja = PdfWriter()

    i, x = 0, 0
    x1, x2 = lehenumbrid[0]
    while x < X:
        if x < x1:
            leht = pdf_lugeja1.pages[x]
            pdf_kirjutaja.add_page(leht)
            x += 1
        else:
            if tegevus == "asenda_lehed":
                y1, y2 = teiselehenumbrid[i]
                for y in range(min(y1, Y), min(y2+1, Y)):
                    leht = pdf_lugeja2.pages[y]
                    pdf_kirjutaja.add_page(leht)
            elif tegevus == "muuda_järjestust":
                y1, y2 = teiselehenumbrid[i]
                for y in range(min(y1, X), min(y2+1, X)):
                    leht = pdf_lugeja1.pages[y]
                    pdf_kirjutaja.add_page(leht)
            elif tegevus == "pööra_ümber":
                for y in range(min(x1, X), min(x2+1, X)):
                    leht = pdf_lugeja1.pages[y]
                    leht.rotate(180)
                    pdf_kirjutaja.add_page(leht)
            x = x2 + 1
            i += 1
            x1, x2 = lehenumbrid[i] if i < len(lehenumbrid) else (X, X)
    pdf_kirjutaja.write(pdffailinimi)

def main():
    """
    Põhimenüü tegevuste sooritamiseks.
    """
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
            töötle_lehti("asenda_lehed")
        elif sisestus == "6":
            töötle_lehti("muuda_järjestust")
        elif sisestus == "7":
            töötle_lehti("pööra_ümber")
        elif sisestus == "8":
            töötle_lehti("kustuta")
        elif sisestus == "0" or sisestus == "":
            break
        print()

if __name__ == "__main__":
    main()
