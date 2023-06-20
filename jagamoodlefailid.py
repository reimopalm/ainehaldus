import os, re, zipfile, time, datetime


lähtekaust = "j:/"
sihtkaust = "k:/Ained/"
nimedefail = "admin/nimed.txt"
parandamisefail = "parandamine.txt"


def loo_töökaust(ainenimi, kaustanimi):
    """
    Moodustab vajalikud alamkaustad ja muudab viimase kausta aktiivseks.
    
    Parameetrid:
        ainenimi (str): Aine nimi
        kaustanimi (str): Alamkaustade tee, eraldajaks "\\" või "/"
        
    Tagastab:
        str: Tee viimase kaustani
    """
    
    if not os.path.exists(sihtkaust):
        print(f"Kausta '{sihtkaust} ' ei leia.")
        return
    
    os.chdir(sihtkaust)
    
    if not os.path.exists(ainenimi):
        print(f"Ainenime '{ainenimi}' ei leia.")
        return
    
    töökaust = os.path.join(sihtkaust, ainenimi, 'materjal', 'tööd',
                            *kaustanimi.replace("\\", "/").split("/"))
    os.makedirs(töökaust, exist_ok=True)
    os.chdir(töökaust)
    
    return töökaust

            
def loenimedefail(ainenimi):
    """
    Loeb kõigi osalejate nimede standardkujud aine nimede failist.

    Parameetrid:
        ainenimi (str): Aine nimi

    Tagastab:
        set: Nimede hulk
        
    Näide:
        loenimedefail("aine")  # Tagastab: {'Nimi1', 'Nimi2', 'Nimi3'}
                
    """
    
    nimedefailinimi = os.path.normpath(os.path.join(
                sihtkaust, ainenimi, nimedefail))
    try:
        with open(nimedefailinimi) as f:
            return {nimi.strip() for nimi in f}
    except:
        print(f"Ei leia aine '{ainenimi}' nimede faili.")
        return set()
    

def kõik_esinevad(sõnehulk, sõne):
    """
    Kontrollib, kas kõik antud sõnede hulga sõned esinevad antud sõnes.
    
    Parameetrid:
        sõnehulk (set): Sõnede hulk
        sõne (str): Kontrollitav sõne
        
    Tagastab:
        bool: `True`, kui kõik hulga sõned esinevad sõnes, muidu `False`
        
    Näide:
        kõik_esinevad({"Aa", "Cc"}, "Aa Bb Cc")  # Tagastab: True
        
    """
    return all(s in sõne for s in sõnehulk)
            
            
def asendaunicodetäpid(s):
    """
    Asendab sõnes Unicode'i tähed vastavate ASCII tähtedega.

    Parameetrid:
        s (str): Sõne, mille Unicode'i tähed asendatakse.

    Tagastab:
        str: Muudetud sõne.

    Näide:
        asendaunicodetäpid("ář")  # Tagastab: "ar"

    """
    s = s.strip()
    asendus = {'á': 'a', 'ř': 'r'}
    s = ''.join(asendus.get(c, c) for c in s)
    return s


def asendatäpid(s):
    """
    Asendab sõnes täpitähed täppideta tähtedega.

    Parameetrid:
        s (str): Sõne, milles täpitähed asendatakse.

    Tagastab:
        str: Muudetud sõne, kus täpitähed on asendatud täppideta tähtedega.

    """
    s = s.strip()
    asendus = {'õ': 'o', 'ä': 'a', 'ö': 'o', 'ü': 'u', 'š': 's', 'ž': 'z',
               'Õ': 'O', 'Ä': 'A', 'Ö': 'O', 'Ü': 'U', 'Š': 'S', 'Ž': 'Z',
               '_': ''}    
    s = ''.join(asendus.get(c, c) for c in s)
    s = asendaunicodetäpid(s)
    return s


def leiaesitajanimi(nimekaustaosa, nimed):
    """
    Leiab faili kaustaosast esitaja nime, mis kuulub nimede hulka.

    Parameetrid:
        nimekaustaosa (str): Faili kaustaosa
        nimed (list): Nimede hulk, kust sobivat nime otsitakse

    Tagastab:
        str: Faili kaustaosast eraldatud nimi.
             Kui sobivat nime ei leia, siis tagastab tühisõne "".

    """
    for nimi in nimed:
        nimehulk = nimi.split()
        if kõik_esinevad(nimehulk, nimekaustaosa) or \
           kõik_esinevad(nimehulk, asendatäpid(nimekaustaosa)) or \
           kõik_esinevad(asendatäpid(nimi).split(), nimekaustaosa):
            return nimi
    return ""
      

TÜÜP_ÜLESANNE = 1
TÜÜP_VPLHARJUTUS = 2


def failitüüp(failinimi):
    """
    Määrab failinime järgi töö tüübi: ülesanne või VPL-harjutus.

    Parameetrid:
        failinimi (str): Failinimi, mille põhjal tuleb määrata töö tüüp

    Tagastab:
        int: Töö tüüp, kas TÜÜP_ÜLESANNE või TÜÜP_VPLHARJUTUS

    """
    if re.search(r'-[0-9]+( [(][0-9]+[)])?[.]zip', failinimi):
        return TÜÜP_ÜLESANNE
    else:
        return TÜÜP_VPLHARJUTUS


def leiavplkuupäev(failinimi):
    """
    Leiab VPL-harjutuse kaustanimest kuupäeva.
    
    Parameetrid:
        failinimi (str): VPL-harjutuse kaustanimi
      
    Tagastab:
        tuple: Kuupäeva ennik kujul (aasta, kuu, päev, tund, minut, sekund).

    """
    m = re.search(r'/(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})',
                  failinimi)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3)),
            int(m.group(4)), int(m.group(5)), int(m.group(6)))


def loeülpäised():
    """
    Küsib kasutajalt ülesannete numbrid ja punktide arvud.

    Tagastab:
        list: Ülesannete päiseid kirjeldavate sõnastike järjend.
              Igas sõnastikus on kirjas ülesande number ja punktide arv.

    """
    päiseread = []
    while True:
        ül = input("Sisesta ülesande number: ").strip()
        if not ül:
            break
        while True:
            p_str = input("Sisesta punktide arv: ").strip()
            try:
                float(p_str)
                break
            except:
                print("Pole arv")
        sõn = {"ülnr": ül, "punarv": p_str}
        päiseread.append(sõn)
    return päiseread


def looparandamine(esitajad, ülpäised, töökaust):
    """
    Loob parandamise abifaili.

    Parameetrid:
        esitajad (dict): Sõnastik, mis sisaldab esitajate andmeid
        ülpäised (list): Sõnastike järjend, kus on kirjas ülesannete numbrid
                         ja punktide arvud
        töökaust (str): Kaust, mille alamkaustadesse esitused salvestatakse

    Tagastab:
        None

    """
    nädalapäevad = ["E", "T", "K", "N", "R", "L", "P"]
    
    try:
        failinimi = os.path.join(töökaust, parandamisefail)
        f = open(failinimi, "a")
    except:
        print("Parandamise faili ei saa avada")
        return
    
    järj_esitajad = sorted(esitajad.items(), key=lambda kv: kv[1]['kuupäev'])
    
    for nr, r in enumerate(järj_esitajad, start=1):
        if f.tell() != 0:
            f.write("\n\n")
        
        # Nimi
        f.write(f"* {asendaunicodetäpid(r[1]['kuvatav'])}\n\n")
        
        # Ülesannete päised
        for s in ülpäised:
            if s["ülnr"].strip() != "-":
                f.write(f"{s['ülnr']}. ")
            f.write(f"(/{s['punarv']})\n\n")
            
        # Kellaaeg ja esituste arv
        kp = r[1]['kuupäev']  # r[1] on ajahetke ennik
        f.write(nädalapäevad[datetime.date(kp[0], kp[1], kp[2]).weekday()])
        f.write("    ")
        f.write(f"{kp[2]}.{kp[1]:02d} {kp[3]}:{kp[4]:02d}    ")
        f.write(f"{r[1]['esitustearv']} {nr}")
    f.close()


def leiaesitajad(failinimi, nimed, töökaust):
    """
    Otsib antud nimega failist üles kõik esitajad, kellel on töökausta senise
    seisuga võrreldes uusi faile. Arvestab ainult kõige viimast esitust.

    Parameetrid:
      failinimi (str): Moodle'ist allalaaditud esituste faili nimi
      nimed (set): Aines osalejate nimede hulk
      töökaust (str): Kaust, mille alamkaustadesse esitused salvestatakse

    Tagastab:
      dict: Sõnastik, mis sisaldab esitajate andmeid, järgmise struktuuriga:
          {
            esitaja_nimi_1: {
                'kuupäev': viimase_esituse_kuupäev,
                'kuvatav': sihtkausta_nimi,
                'esitustearv': esituste_arv
            },
            esitaja_nimi_2: {
                'kuupäev': viimase_esituse_kuupäev,
                'kuvatav': sihtkausta_nimi,
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
    ziptüüp = failitüüp(failinimi)        
    os.chdir(lähtekaust)
    
    with zipfile.ZipFile(failinimi, 'r') as z:
        for info in z.infolist():
            
            # Jäta vahele kaustad ja spetsiaalsed failid
            if info.is_dir():
                continue
            elif ziptüüp == TÜÜP_ÜLESANNE and \
                 info.filename.endswith("onlinetext_veebitekst.html") and \
                 info.file_size == 76:
                continue
            elif ziptüüp == TÜÜP_VPLHARJUTUS and \
                 os.path.basename(info.filename) in \
                 ['Report.txt', 'compilation.txt', 'execution.txt',
                  'grade.txt', 'gradecomments.txt']:
                continue
            
            # Eralda faili nime kaustaosast esitaja nimi
            if ziptüüp == TÜÜP_ÜLESANNE:
                m = re.match('(.*)_', info.filename)
                nimekaustaosa = m.group(1)
            elif ziptüüp == TÜÜP_VPLHARJUTUS:
                nimekaustaosa = os.path.dirname(info.filename)
            esitajanimi = leiaesitajanimi(nimekaustaosa, nimed)
            if esitajanimi == "":
                print("Ei leidnud esitaja nime failinimest: " + info.filename)
                continue
            
            # Leia kopeeritava faili kuupäev
            if ziptüüp == TÜÜP_ÜLESANNE:
                if info.filename.endswith("veebitekst.html"):
                    lähtefaili_kuup_aeg = (datetime.datetime.now().year,
                                           1, 1, 0, 0, 0)
                else:
                    lähtefaili_kuup_aeg = info.date_time                    
            elif ziptüüp == TÜÜP_VPLHARJUTUS:
                lähtefaili_kuup_aeg = leiavplkuupäev(nimekaustaosa)
            
            # Uue kuupäeva arvestamine
            if esitajanimi not in kuupäevad:
                kuupäevad[esitajanimi] = set()
            kuupäevad[esitajanimi].add(lähtefaili_kuup_aeg)
            if lähtefaili_kuup_aeg < max(kuupäevad[esitajanimi]):
                continue
            if esitajanimi in esitajad:
                assert lähtefaili_kuup_aeg >= esitajad[esitajanimi]['kuupäev']
                if lähtefaili_kuup_aeg == esitajad[esitajanimi]['kuupäev']:
                    continue
                else:
                    del esitajad[esitajanimi]
                
            # Leia kopeeritava faili nimi
            if ziptüüp == TÜÜP_ÜLESANNE:
                m = re.search('(_file_|_onlinetext_)(.*)$', info.filename)
                kopeeritavnimi = m.group(2) if m else info.filename
            elif ziptüüp == TÜÜP_VPLHARJUTUS:
                kopeeritavnimi = os.path.basename(info.filename)
                                    
            # Kontroll, kas fail on uus
            nimekaust = os.path.join(töökaust, esitajanimi)
            if os.path.exists(nimekaust):
                # Leia suurim olemasolev kaust
                n = 1
                uuskaust = nimekaust
                while os.path.exists(uuskaust):
                    suurimkaust = uuskaust
                    n += 1
                    uuskaust = os.path.join(töökaust, f"{esitajanimi} {n}")
                # Kas fail leidub seal
                sihtfailinimi = os.path.join(suurimkaust, kopeeritavnimi)
                if os.path.exists(sihtfailinimi):
                    # Võrdle kuupäevi
                    aeg = time.localtime(os.path.getmtime(sihtfailinimi))
                    sihtfaili_kuup_aeg = (aeg.tm_year, aeg.tm_mon, aeg.tm_mday,
                                      aeg.tm_hour, aeg.tm_min, aeg.tm_sec)
                    if lähtefaili_kuup_aeg <= sihtfaili_kuup_aeg:
                        continue
            else:
                uuskaust = nimekaust
                    
            # Lisa esitaja info sõnastikku
            esitajad[esitajanimi] = {
                'kuupäev': lähtefaili_kuup_aeg,
                'kuvatav': os.path.basename(uuskaust)
            }

    # Lisa esituste arvud
    for esitajanimi in esitajad:
        esitajad[esitajanimi]['esitustearv'] = len(kuupäevad[esitajanimi])
        
    return esitajad

    
def pakilahti(failinimi, esitajad, nimed, töökaust):
    """
    Pakib zip-failist lahti esitajate sõnastikuga määratud esitused.

    Parameetrid:
        failinimi (str): Moodle'ist allalaaditud esituste faili nimi
        esitajad (dict): Lahtipakitavate failide esitajate nimed ja kuupäevad
        nimed (set): Aines osalejate nimede hulk
        töökaust (str): Kaust, mille alamkaustadesse esitused salvestatakse

    Tagastab:
        None
        
    """
    ziptüüp = failitüüp(failinimi)
    
    with zipfile.ZipFile(failinimi, 'r') as z:
        for info in z.infolist():
                        
            # Jäta vahele kaustad ja spetsiaalsed failid
            if info.is_dir():
                continue
            elif ziptüüp == TÜÜP_ÜLESANNE and \
                 info.filename.endswith("onlinetext_veebitekst.html") and \
                 info.file_size == 76:
                continue
            elif ziptüüp == TÜÜP_VPLHARJUTUS and \
                 os.path.basename(info.filename) in \
                 ['Report.txt', 'compilation.txt', 'execution.txt',
                  'grade.txt', 'gradecomments.txt']:
                continue
            
            # Eralda faili nimest esitaja nimi
            if ziptüüp == TÜÜP_ÜLESANNE:
                m = re.match('(.*)_', info.filename)
                nimekaustaosa = m.group(1)
            elif ziptüüp == TÜÜP_VPLHARJUTUS:
                nimekaustaosa = os.path.dirname(info.filename)
            esitajanimi = leiaesitajanimi(nimekaustaosa, nimed)
            if esitajanimi not in esitajad:
                continue
            
            # Leia kopeeritava faili kuupäev ja nimi
            if ziptüüp == TÜÜP_ÜLESANNE:
                kuup_aeg = info.date_time
                m = re.search('(_file_|_onlinetext_)(.*)$', info.filename)
                kopeeritavnimi = m.group(2) if m else info.filename
            elif ziptüüp == TÜÜP_VPLHARJUTUS:
                kuup_aeg = leiavplkuupäev(nimekaustaosa)
                if kuup_aeg < esitajad[esitajanimi]['kuupäev']:
                    continue
                kopeeritavnimi = os.path.basename(info.filename)
                
            # Paki fail lahti            
            nimekaust = os.path.join(töökaust, esitajad[esitajanimi]['kuvatav'])
            if not os.path.exists(nimekaust):
                os.mkdir(nimekaust)
            info.filename = kopeeritavnimi            # faili esialgne nimi
            z.extract(info, nimekaust)                # paki lahti
            
            # Kuupäev ja kellaaeg õigeks
            kuup_aeg = time.mktime(kuup_aeg + (0, 0, -1))
            os.utime(os.path.join(nimekaust, info.filename),
                     (kuup_aeg, kuup_aeg))
            
                        
def jaga(failinimi, ainenimi, kaustanimi, ülpäised):    
    """
    Jagab zip-failis olevad esitused kaustadesse ja loob parandamise faili.

    Parameetrid:    
        failinimi (str): Moodle'ist allalaaditud esituste faili nimi
        ainenimi (str): Aine nimi.
        kaustanimi (str): Kausta nimi, kuhu esitused lahti pakkida
        ülpäised (list): Sõnastike järjend, kus on kirjas ülesannete numbrid
                         ja punktide arvud.

    Tagastab:
        None
        
    """
    if not ainenimi.strip() or not kaustanimi.strip():
        return
    
    os.chdir(lähtekaust)    
    if not zipfile.is_zipfile(failinimi):
        print("See ei ole zip-fail.")
        return
    
    töökaust = loo_töökaust(ainenimi, kaustanimi)
    nimed = loenimedefail(ainenimi)
    if nimed != set(): 
        esitajad = leiaesitajad(failinimi, nimed, töökaust)    
        pakilahti(failinimi, esitajad, nimed, töökaust)    
        looparandamine(esitajad, ülpäised, töökaust)
    
    
for failinimi in os.listdir(lähtekaust):
    if failinimi.endswith(".zip"):
        
        # Esituste fail
        
        ziptüüp = failitüüp(failinimi)
        if ziptüüp == TÜÜP_ÜLESANNE:
            print("Ülesanne:", failinimi)
        elif ziptüüp == TÜÜP_VPLHARJUTUS:
            print("VPL-harjutus:", failinimi)
            
        ainenimi = input("Sisesta aine: ").strip()
        if not ainenimi:
            continue
        kaustanimi = input("Sisesta kaust: ").strip()
        print()
        
        # Ülesannete päised
        
        ülpäised = loeülpäised()
        
        jaga(failinimi, ainenimi, kaustanimi, ülpäised)
        
