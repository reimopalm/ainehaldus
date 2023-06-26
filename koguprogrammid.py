import re, os

VÄLJUNDFAILINIMI = "programmid.py"

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

def küsi_alamkaustad():
    """
    Küsib kasutajalt alamkaustade nimesid, kust programme otsida.
    Kaustanimede eraldajaks võib olla tühik, koma või semikoolon.
    """
    while True:
        sisestus = input("Sisesta alamkaustade nimed: ")
        if not sisestus.strip():
            return
        alamkaustad = re.findall(r'[^ ,;]+', sisestus)
        kõik_olemas = True
        for alamkaust in alamkaustad:
            if not os.path.isdir(alamkaust):
                print(f"Ei leia alamkausta '{alamkaust}'")
                kõik_olemas = False
        if kõik_olemas:
            return alamkaustad

def loe_nimed(failinimi):
    """
    Loeb failist nimed. Püüab mittesobiva info vahele jätta.
    """
    try:
        with open(failinimi) as f:
            nimed = []
            for rida in f:
                rida = re.sub(r'\d', '.', rida)
                m = re.search(r"^[^\w]*(\w\w[ \w]*)[^\w]*$", rida)
                if m:
                    nimed.append(m.group(1))
            return nimed
    except:
        print(f"Faili {failinimi} ei saa avada.")
        return []


def kogu_üks(isikunimi, alamkaustanimed):
    """
    Kogub alamkaustadest kokku ühe esitaja programmid.
    Nummerdatud kaustade olemasolul arvestab kõige suurema numbriga kausta.
    """
    sisu = ""
    for alamkaust in alamkaustanimed:
        järgmine_kaust = os.path.join(alamkaust, isikunimi)
        if os.path.isdir(järgmine_kaust):
            n = 1
            while os.path.isdir(järgmine_kaust):
                n += 1
                kaust = järgmine_kaust
                järgmine_kaust = os.path.join(alamkaust, isikunimi + str(n))
            for failinimi in os.listdir(kaust):
                if failinimi.endswith(".py"):
                    sisu += f"# {alamkaust} - {failinimi}\n\n"
                    with open(os.path.join(kaust, failinimi)) as f:
                        sisu += f.read().rstrip()
                    sisu += "\n\n"
    return sisu

def kogu_kõik(isikunimed, alamkaustanimed):
    """
    Kogub alamkaustadest kokku kõigi esitajate programmid ja kirjutab faili.
    """
    with open(VÄLJUNDFAILINIMI, 'a', encoding="UTF-8") as f:
        for isikunimi in isikunimed:
            if f.tell() != 0:
                f.write("\n# " + "-" * 70 + "\n")
            f.write(f"## {isikunimi}\n\n")
            sisu = kogu_üks(isikunimi, alamkaustanimed)
            f.write(sisu)

def main():
    """
    Küsib kasutajalt nimede faili nime ja alamkaustu, kogub kokku kõigi
    esitajate programmid ning moodustab ühe väljundfaili.
    """
    failinimi = küsi_failinimi("Sisesta nimede faili nimi:", ".*nimed.*[.]txt")
    if not failinimi:
        return

    alamkaustanimed = küsi_alamkaustad()
    if not alamkaustanimed:
        return

    nimed = loe_nimed(failinimi)
    if not nimed:
        return

    kogu_kõik(nimed, alamkaustanimed)

if __name__ == "__main__":
    main()
