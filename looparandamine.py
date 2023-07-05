import re, os, datetime

PARANDAMISEFAILINIMI = "parandamine.txt"

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

def loe_nimed(failinimi):
    """
    Loeb failist nimed. Mittesobiva info püüab vahele jätta.
    """
    try:
        with open(failinimi) as f:
            nimed = []
            nime_otsing = re.compile(r'^\W*([^\W\d]+[.]?(?:[ -][^\W\d]+[.]?)+)[\W\d]*$')
            for rida in f:
                m = re.search(nime_otsing, rida)
                if m:
                    nimed.append(m.group(1))
            return nimed
    except:
        print(f"Faili {failinimi} ei saa avada.")
        return []

def loo_parandamine(nimed, punktid):
    """
    Loob etteantud nimede põhjal parandamise faili. Kui nimi on juba failis olemas,
    siis tõstab olemasoleva info ümber.

    Parameetrid:
        nimed (list): Esitajate nimede järjend
        punktid (list): Ülesannete punktide arvude järjend
    """
    nimi, laiend = os.path.splitext(PARANDAMISEFAILINIMI)
    abifailinimi = f"{nimi}2{laiend}"
    try:
        abifail = open(abifailinimi, "w")
    except:
        print("Ei saa avada abifaili")
        return

    # Kopeerida ümber senine info
    olemasolevad = {}
    if os.path.isfile(PARANDAMISEFAILINIMI):
        try:
            parandamisefail = open(PARANDAMISEFAILINIMI)
        except:
            print("Ei saa avada parandamise faili")
            return
        nime_otsing = re.compile(r'^#\s*(?:[\s-][^\W\d]+[.]?){2,}(?:\s+\d+)?')
        info_otsing = re.compile(r'^[ETKNRLP]\s+\d{1,2}[.]\d{1,2}\s\d{1,2}:\d{2}(?:\s+\d+){1,}')
        nimi = None
        olemas = False
        for rida in parandamisefail:
            m = re.search(nime_otsing, rida)
            if m:
                uus_nimi = re.sub(r'^\W+|[\W\d]+$', '', m.group(0))
                osad = re.sub(r'[-.]', ' ', uus_nimi).split()
                if len(osad) >= 2 and sum(len(s) > 1 for s in osad) > 1 and all(s.istitle() for s in osad):
                    nimi = uus_nimi
                    olemas = nimi in nimed
                    if olemas:
                        olemasolevad[nimi] = []
                        rida = re.sub(nime_otsing, '# <--{nimi}-->', rida)
            elif olemas and re.search(info_otsing, rida):
                rida = re.sub(info_otsing, '<--{info}-->', rida)
            if olemas:
                olemasolevad[nimi].append(rida)
            else:
                abifail.write(rida)
        parandamisefail.close()

    # Lisada uus info
    praegu = datetime.datetime.now()
    for nr, nimi in enumerate(nimed, start=1):
        inforida = f"{'ETKNRLP'[praegu.weekday()]}    {praegu.day}.{praegu.month:02d} " \
                   f"{praegu.hour}:{praegu.minute:02d}    {nr}"
        if nimi in olemasolevad:
            abifail.write(''.join(olemasolevad[nimi]).replace('<--{nimi}-->', nimi)
                          .replace('<--{info}-->', inforida))
        else:
            abifail.write(f"# {nimi}\n\n")
            if len(punktid) > 1:
                for ülnr, ülpun in enumerate(punktid, start=1):
                    abifail.write(f"{ülnr}. (/{ülpun})\n\n")
            else:
                abifail.write(f"(/{punktid[0]})\n\n")
            abifail.write(f"{inforida}\n\n")
    abifail.close()

    # Vormistada lõpptulemus
    if os.path.isfile(abifailinimi):
        if os.path.isfile(PARANDAMISEFAILINIMI):
            os.remove(PARANDAMISEFAILINIMI)
        os.rename(abifailinimi, PARANDAMISEFAILINIMI)


def main():
    """
    Küsib kasutajalt nimede faili nime ja punkte ning loob parandamise faili.
    """
    failinimi = küsi_failinimi("Sisesta nimede faili nimi:", ".*nimed.*[.]txt")
    if not failinimi:
        return

    punktid = küsi_punktid()
    if not punktid:
        return

    nimed = loe_nimed(failinimi)
    if not nimed:
        return

    loo_parandamine(nimed, punktid)


if __name__ == "__main__":
    main()
