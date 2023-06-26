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

    praegu = datetime.datetime.now()

    try:
        f = open(PARANDAMISEFAILINIMI, "a")
    except:
        print("Parandamise faili ei saa avada")
        return

    for i, nimi in enumerate(nimed, start=1):
        if f.tell() != 0:
            f.write("\n\n")

        # Nimi
        f.write(f"* {nimi}\n\n")

        # Ülesannete päised
        if len(punktid) > 1:
            for ülnr, ülpun in enumerate(punktid, start=1):
                f.write(f"{ülnr}. (/{ülpun})\n\n")
        else:
            f.write(f"(/{punktid[0]})\n\n")

        # Kuupäev ja kellaaeg
        f.write(f"{'ETKNRLP'[praegu.weekday()]}    {praegu.day}.{praegu.month:02d} "
                f"{praegu.hour}:{praegu.minute:02d}    {i}")

    f.close()

if __name__ == "__main__":
    main()