import os, re, zipfile, time, datetime

PARANDAMISEFAILINIMI = "parandamine.txt"

TÜÜP_ÜLESANNE = 1
TÜÜP_VPLHARJUTUS = 2

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

def faili_tüüp(failinimi):
    """
    Määrab faili tüübi: ülesanne või VPL-harjutus.
    """
    if os.path.exists(failinimi):
        if re.search(r'-[0-9]+( [(][0-9]+[)])?[.]zip', failinimi):
            return TÜÜP_ÜLESANNE
        with zipfile.ZipFile(failinimi, 'r') as z:
            if 'Report.txt' in z.namelist():
                return TÜÜP_VPLHARJUTUS

def loo_parandamine(esitajad, punktid):
    """
    Loob parandamise abifaili.

    Parameetrid:
        esitajad (dict): Esitajate andmeid sisaldav sõnastik
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
        nimed = set(re.sub(r'[\W\d]+$', '', nimi) for nimi in esitajad.keys())
        nime_otsing = re.compile(r'^#\s*(?:[\s-][^\W\d]+[.]?){2,}(?:\s+\d+)?')
        info_otsing = re.compile(r'^[ETKNRLP]\s+\d{1,2}[.]\d{1,2}\s\d{1,2}:\d{2}(?:\s+\d+){1,}')
        nimi = None
        olemas = False
        for rida in parandamisefail:
            m = re.search(nime_otsing, rida)
            if m:
                uus_nimi = re.sub(r'^\W+|[\W\d]+$', '', m.group(0))
                osad = re.sub(r'[-.]', ' ', uus_nimi).split()
                if len(osad) >= 2 and sum(len(s)>1 for s in osad)>1 and all(s.istitle() for s in osad):
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
    jär_esitajad = sorted(esitajad.items(), key=lambda kv: kv[1]['kuupäev'])
    for nr, esitaja in enumerate(jär_esitajad, start=1):
        kp = esitaja[1]['kuupäev']
        inforida = "ETKNRLP"[datetime.date(kp[0], kp[1], kp[2]).weekday()]
        inforida += f"    {kp[2]}.{kp[1]:02d} {kp[3]}:{kp[4]:02d}"
        inforida += f"    {esitaja[1]['esitustearv']} {nr}"
        kaust = esitaja[1]['kaust']
        nimi = re.sub(r'[\W\d]+$', '', kaust)
        if nimi in olemasolevad:
            abifail.write(''.join(olemasolevad[nimi]).replace('<--{nimi}-->', kaust)
                          .replace('<--{info}-->', inforida))
        else:
            abifail.write(f"# {kaust}\n\n")
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


def on_tehniline_fail(info, ziptüüp):
    """
    Kontrollib, kas fail on süsteemi tehniline fail.
    """
    if info.is_dir():
        return True
    if ziptüüp == TÜÜP_ÜLESANNE and \
            info.filename.endswith("onlinetext_veebitekst.html") and info.file_size == 76:
        return True
    if ziptüüp == TÜÜP_VPLHARJUTUS and \
            (re.search(r'/\d{4}(-\d{2}){5}[.]ceg/', info.filename) or info.filename == 'Report.txt'):
        return True
    return False

def eralda_esitajanimi(info, ziptüüp):
    """
    Eraldab faili andmetest esitaja nime vastavalt zip-faili tüübile.
    """
    if ziptüüp == TÜÜP_ÜLESANNE:
        m = re.match('(.*?)_', info.filename)
        if m:
            return m.group(1)
    elif ziptüüp == TÜÜP_VPLHARJUTUS:
        nimekaustaosa = os.path.dirname(info.filename)
        m = re.match('(.*?) [0-9]+', nimekaustaosa)
        if m:
            return m.group(1)
    return ""

def eralda_kuupäev(info, ziptüüp):
    """
    Eraldab faili andmetest faili kuupäeva.
    """
    if ziptüüp == TÜÜP_ÜLESANNE:
        if not info.filename.endswith("veebitekst.html"):
            return info.date_time
    if ziptüüp == TÜÜP_VPLHARJUTUS:
        nimekaustaosa = os.path.dirname(info.filename)
        kp = re.search(r'/(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})', nimekaustaosa)
        if kp:
            return tuple(int(kp.group(i)) for i in range(1, 7))
    return (datetime.datetime.now().year, 1, 1, 0, 0, 0)

def eralda_failinimi(info, ziptüüp):
    """
    Eraldab faili andmetest faili õige nime.
    """
    if ziptüüp == TÜÜP_ÜLESANNE:
        m = re.search('(_file_|_onlinetext_)(.*)$', info.filename)
        if m:
            return m.group(2)
    if ziptüüp == TÜÜP_VPLHARJUTUS:
        return os.path.basename(info.filename)
    return info.filename

def leia_esitajad(failinimi):
    """
    Otsib antud nimega zip-failist üles kõik esitajad, kellel on kohaliku kausta
    senise seisuga võrreldes uusi faile. Arvestab ainult kõige viimast esitust.
    Määrab lahtipakkimiseks kaustade nimed, vajadusel lisades lõppu järjekorranumbri.

    Tagastab:
      dict: Sõnastik, mille sisuks on esitajate andmed järgmise struktuuriga:
          {
            esitaja_nimi_1: {
                'kuupäev': viimase_esituse_kuupäev,
                'kaust': sihtkausta_nimi,
                'esitustearv': esituste_arv
            },
            esitaja_nimi_2: {
                'kuupäev': viimase_esituse_kuupäev,
                'kaust': sihtkausta_nimi,
                'esitustearv': esituste_arv
            },
            ...
          }
          viimase_esituse_kuupäev - Viimase esituse kuupäev ja kellaaeg
          sihtkausta_nimi - Esitaja kausta nimi, kuhu failid salvestatakse,
                            vajadusel numbriga, kui on olemas varasem kaust
          esituste_arv - Selle esitaja esituste koguarv

    """
    esitajad = {}
    kuupäevad = {}
    ziptüüp = faili_tüüp(failinimi)

    with zipfile.ZipFile(failinimi, 'r') as z:
        for info in z.infolist():
            if on_tehniline_fail(info, ziptüüp):
                continue

            esitaja_nimi = eralda_esitajanimi(info, ziptüüp)
            if not esitaja_nimi:
                print(f"Ei leidnud esitaja nime failist {info.filename}")
                continue

            # Uue kuupäeva arvestamine
            lähtefaili_kuup_aeg = eralda_kuupäev(info, ziptüüp)
            if esitaja_nimi not in kuupäevad:
                kuupäevad[esitaja_nimi] = set()
            kuupäevad[esitaja_nimi].add(lähtefaili_kuup_aeg)
            if lähtefaili_kuup_aeg < max(kuupäevad[esitaja_nimi]):
                continue
            if esitaja_nimi in esitajad:
                assert lähtefaili_kuup_aeg >= esitajad[esitaja_nimi]['kuupäev']
                if lähtefaili_kuup_aeg == esitajad[esitaja_nimi]['kuupäev']:
                    continue
                else:
                    del esitajad[esitaja_nimi]

            # Kontroll, kas fail on uus
            uus_kaust = esitaja_nimi
            if os.path.exists(uus_kaust):
                # Leia suurim olemasolev kaust
                n = 1
                while os.path.exists(uus_kaust):
                    suurim_kaust = uus_kaust
                    n += 1
                    uus_kaust = f"{esitaja_nimi} {n}"
                # Kas fail leidub seal
                lähtefaili_nimi = eralda_failinimi(info, ziptüüp)
                sihtfaili_nimi = os.path.join(suurim_kaust, lähtefaili_nimi)
                if os.path.exists(sihtfaili_nimi):
                    # Võrdle kuupäevi
                    aeg = time.localtime(os.path.getmtime(sihtfaili_nimi))
                    sihtfaili_kuup_aeg = (aeg.tm_year, aeg.tm_mon, aeg.tm_mday,
                                          aeg.tm_hour, aeg.tm_min, aeg.tm_sec)
                    if lähtefaili_kuup_aeg <= sihtfaili_kuup_aeg:
                        continue

            # Lisa esitaja info sõnastikku
            esitajad[esitaja_nimi] = {
                'kuupäev': lähtefaili_kuup_aeg,
                'kaust': uus_kaust
            }

    # Lisa esituste arvud
    for esitaja_nimi in esitajad:
        esitajad[esitaja_nimi]['esitustearv'] = len(kuupäevad[esitaja_nimi])

    return esitajad

    
def paki_lahti(failinimi, esitajad):
    """
    Pakib zip-failist lahti esitajate sõnastikuga määratud esitused.

    Parameetrid:
        failinimi (str): Moodle'ist allalaaditud esituste faili nimi
        esitajad (dict): Leitud uute failide esitajate nimed ja kuupäevad

    """
    ziptüüp = faili_tüüp(failinimi)
    
    with zipfile.ZipFile(failinimi, 'r') as z:
        for info in z.infolist():

            if on_tehniline_fail(info, ziptüüp):
                continue

            esitaja_nimi = eralda_esitajanimi(info, ziptüüp)
            if esitaja_nimi not in esitajad:
                continue

            kuup_aeg = eralda_kuupäev(info, ziptüüp)
            if ziptüüp == TÜÜP_VPLHARJUTUS and kuup_aeg < esitajad[esitaja_nimi]['kuupäev']:
                continue

            # Paki fail lahti õige nimega
            kaust = esitajad[esitaja_nimi]['kaust']
            if not os.path.exists(kaust):
                os.mkdir(kaust)
            info.filename = eralda_failinimi(info, ziptüüp)
            z.extract(info, kaust)
            
            # Kuupäev ja kellaaeg õigeks
            kuup_aeg = time.mktime(kuup_aeg + (0, 0, -1))
            os.utime(os.path.join(kaust, info.filename), (kuup_aeg, kuup_aeg))

def main():
    """
    Küsib kasutajalt failinime ja ülesannete punkte ning pakib faili lahti.
    """
    failinimi = küsi_failinimi("Sisesta failinimi:", ".*[.]zip")
    if not failinimi:
        return

    if not zipfile.is_zipfile(failinimi):
        print("See ei ole zip-fail.")
        return

    if not faili_tüüp(failinimi):
        print("See fail on tundmatut tüüpi.")
        return

    punktid = küsi_punktid()
    esitajad = leia_esitajad(failinimi)
    paki_lahti(failinimi, esitajad)
    loo_parandamine(esitajad, punktid)

if __name__ == "__main__":
    main()