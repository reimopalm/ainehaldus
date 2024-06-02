import datetime, locale
import os, re, csv

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

def loe_andmed(failinimi):
    """
    Loeb etteantud nimega csv-failist vastused sisse.

    Tagastab:
        küsimused (list): erinevate küsimuste järjend
        tabel (list): kõik vastused tabelina
    """
    try:
        f = open(failinimi, newline='', encoding="UTF-8")
    except:
        print(f"Tagasisidefaili '{failinimi}' ei saa avada.")
        return

    küsimused = []
    tabel = []

    lugeja = csv.reader(f)
    päiserida = next(lugeja)
    algus = 3 if re.search('[nN]imi|[nN]ame', päiserida[0]) else 1

    for küsimus in päiserida[algus:]:
        if küsimus not in küsimused:
            küsimused.append(küsimus)
    küsimuste_arv = len(küsimused)
    if (len(päiserida)-algus) % küsimuste_arv != 0:
        print(f"Päiserea struktuur pole ühtlane: {len(päiserida)-algus} küsimust ja {len(küsimused)} erinevat.")
        return

    for k in range(küsimuste_arv):
        for j in range(algus+k+küsimuste_arv, len(päiserida), küsimuste_arv):
            if päiserida[algus+k] != päiserida[j]:
                print(f"Küsimusteplokid pole ühesugused.")
                print(f"1. ploki {k+1}. küsimus on '{päiserida[algus+k]}'")
                print(f"{(j-algus-k)//küsimuste_arv+1}. ploki {k+1}. küsimus on '{päiserida[j]}'")
                return

    for rida in lugeja:
        rida = list(map(str.strip, rida))
        if algus == 3:
            m = re.search('(?:Projekt|Rühm|Project|Group) (\w+)', rida[1])
            rida[1] = m.group(1) if m else ""
        else:
            rida[1:1] = ["", ""]
        tabel.append(rida)
    f.close()

    assert len(set(len(rida) for rida in tabel)) == 1

    return küsimused, tabel

def kirjuta_tulemused(küsimused, sõnastik, failinimi):
    """
    Moodustab tulemusfaili. Ette antakse küsimuste järjend ja korrastatud vastuste sõnastik.
    """
    try:
        f = open(failinimi, 'a', encoding="UTF-8")
    except:
        print(f"Ei saa avada faili {failinimi}.")
        return

    proj_kaupa = isinstance(list(sõnastik.keys())[0], str)

    # Üldpäis
    if proj_kaupa:
        pealkiri = os.path.basename(failinimi)
        pealkiri = os.path.splitext(pealkiri)[0]
        f.write(f'<h1 style="text-align: center;">{pealkiri}</h1>')
        locale.setlocale(locale.LC_TIME, '')
        kuupäev = datetime.datetime.today()
        pealkiri = kuupäev.strftime("%d. %B %Y")
        f.write(f'<h2 style="text-align: center;">{pealkiri}</h2>')

    # Jaotise pealkiri
    pealkiri = '(a) Projektide' if proj_kaupa else '(b) Hindajate'
    f.write(f'<h1>{pealkiri} kaupa</h1>\n<h2>Vastuste arvud</h2>')
    for i, küsimus in enumerate(küsimused, start=1):
        f.write(f'Küs {i}. {küsimus}<br>')
    f.write('<p></p>\n')

    nimed = sorted(sõnastik.keys())

    # Kokkuvõtlik tabel
    f.write('<table>\n')
    f.write('<tr><th style="text-align: center;">Nr</th>'
            '<th style="text-align: left;">Nimi</th>')
    if not proj_kaupa:
        f.write('<th style="text-align: center;">Rühm</th>')
    for i in range(len(küsimused)):
        f.write(f'<th style="text-align: center;">Küs {i+1}</th>')
    f.write('</tr>\n')

    for i, nimi in enumerate(nimed, start=1):
        f.write(f'<tr><td style="text-align: center;">{i}.</td>')
        if proj_kaupa:
            f.write(f'<td>{nimi}</td>')
        else:
            f.write(f'<td>{nimi[1]}</td>'
                    f'<td style="text-align: center;">{nimi[0]}</td>')
        for vastused in sõnastik[nimi]:
            if isinstance(vastused, list):
                f.write(f'<td style="text-align: center;">{len(vastused)}</td>')
            elif isinstance(vastused, dict):
                f.write(f'<td style="text-align: center;">{sum(vastused.values())}</td>')
        f.write('</tr>\n')
    f.write('</table>\n')

    # Kõik vastused
    for nimi in nimed:
        pealkiri = nimi if proj_kaupa else nimi[1]
        f.write(f'<h2>{pealkiri}</h2>\n')

        for k, küsimus in enumerate(küsimused):
            f.write(f'<p><b>{küsimus}</b></p>\n')
            vastused = sõnastik[nimi][k]
            if k == 0:
                f.write(f'<p>Vastuste arv {sum(vastused.values())}</p>')
                continue
            if isinstance(vastused, list):
                f.write('<ul>\n')
                for vastus in vastused:
                    vastus = vastus.replace('\n', '<br>').replace('&amp;', '&')
                    f.write(f'<li>{vastus}</li>\n')
                f.write('</ul>\n')
            elif isinstance(vastused, dict):
                f.write('<table>')
                for vastus, arv in sorted(vastused.items()):
                    vastus = vastus.rstrip('.').replace('\n', '<br>').replace('&amp;', '&')
                    f.write(f'<tr><td>{vastus}</td><td width=20px></td><td>{arv}</td>'
                            f'<td style="color: #666666;">{"&#9608;"*arv}</td></tr>')
                f.write('</table>')


def main():
    """
    Küsib kasutajalt tagasisidefaili nime ja loob html-faili, kus tagasiside on korrastatud
    projektide kaupa ja hindajate kaupa.

    Vastused korrastatakse järgmisele kujule:
      {
        nimi_1: [
          [K1_v1, K1_v2, K1_v3],
          {K2_v1: arv1, K2_v2: arv2, K3_v3, arv3}
          ...
        ],
        nimi_2: [
          [K1_v1, K1_v2, K1_v3],
          {K2_v1: arv1, K2_v2: arv2, K3_v3, arv3}
          ...
        ],
        ...
      }
      Tekstvastusega küsimuste vastused esitatakse järjendina, valikvastustega küsimuste vastused
      sõnastikuna, kus kirjed on kujul küsimus: vastuste_arv.
    """
    failinimi = küsi_failinimi("Sisesta failinimi:", r'.*([tT]agasiside|[fF]eedback).*[.]csv')
    if not failinimi:
        return

    küsimused, tabel = loe_andmed(failinimi)

    küsimuste_arv = len(küsimused)

    TEKSTVASTUS = 1
    VALIKVASTUS = 2

    # Määra küsimuste tüübid
    tüübid = [TEKSTVASTUS] * küsimuste_arv
    for k in range(küsimuste_arv):
        koguarv = 0
        kõikvastused = set()
        for rida in tabel:
            for j in range(3+k, len(rida), küsimuste_arv):
                if rida[j] not in {"", "0", "-"}:
                    koguarv += 1
                    kõikvastused.add(rida[j])
        if koguarv > 1.4 * len(kõikvastused):
            tüübid[k] = VALIKVASTUS

    # Kogu andmed kokku
    projektid = {}
    hindajad = {}
    for rida in tabel:
        rühm_nimi = (rida[1], rida[0])
        hindajad[rühm_nimi] = [[] if tüüp == TEKSTVASTUS else {} for tüüp in tüübid]
        for j in range(3, len(rida), küsimuste_arv):
            projekti_nimi = rida[j]
            if projekti_nimi == "":
                continue
            if projekti_nimi not in projektid:
                projektid[projekti_nimi] = [[] if tüüp == TEKSTVASTUS else {} for tüüp in tüübid]
            for k, tüüp in enumerate(tüübid):
                vastus = rida[j+k]
                if vastus not in {"", "0", "-"}:
                    if tüüp == TEKSTVASTUS:
                        projektid[projekti_nimi][k].append(vastus)
                        hindajad[rühm_nimi][k].append(vastus)
                    elif tüüp == VALIKVASTUS and \
                            (k == 0 or rühm_nimi[0] not in projekti_nimi.split(maxsplit=2)[0:2]):
                        projektid[projekti_nimi][k][vastus] = projektid[projekti_nimi][k].get(vastus, 0) + 1
                        hindajad[rühm_nimi][k][vastus] = hindajad[rühm_nimi][k].get(vastus, 0) + 1

    # Salvesta tulemused
    failinimi = os.path.splitext(failinimi)[0] + ".html"
    if os.path.isfile(failinimi):
        os.remove(failinimi)

    kirjuta_tulemused(küsimused, projektid, failinimi)
    kirjuta_tulemused(küsimused, hindajad, failinimi)

if __name__ == "__main__":
    main()