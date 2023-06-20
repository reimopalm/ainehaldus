import subprocess, os, zipfile, csv, re

# Pöörab näidatud leheküljed ümber. Ette antakse failinimi ja pööratavate
# lehekülgede järjend.
def pööra_ümber(pdffailinimi, lehed):
    puhasnimi, puhaslaiend = os.path.splitext(str(pdffailinimi))
    uusnimi = f"{puhasnimi}2{puhaslaiend}"
    lkarg = [str(leht) + "down" for leht in lehed]
    arg = ['pdftk', pdffailinimi, 'rotate', *lkarg, 'output', uusnimi]
    subprocess.run(arg)
    if os.path.isfile(uusnimi) and os.path.getsize(uusnimi) > 0:
        os.remove(pdffailinimi)
        os.rename(uusnimi, pdffailinimi)
        
        
# Tükeldab pdf-faili eraldi failideks. Ette antakse piiride järjend,
# kus on kirjas algus ja failinimi, ning kaustanimi, kuhu tulemusfailid
# paigutada.
def jaga_failid(pdfsisud, kaustanimi):
    os.makedirs(kaustanimi, exist_ok=True)
    for pdfsisu in pdfsisud:
        pdfsisuread = pdfsisu.split('\n')
        pdffailinimi = pdfsisuread[0]
        for i in range(1, len(pdfsisuread)):
            nr, nimi = pdfsisuread[i].split(maxsplit=1)
            uusnimi = nimi.strip() + ".pdf"
            vahemik = nr.strip().strip(",") + "-"
            if i < len(pdfsisuread)-1:
                nr, _ = pdfsisuread[i+1].split(maxsplit=1)
                vahemik += str(int(nr.strip(","))-1)
            else:
                vahemik += "end"
            arg = ['pdftk', pdffailinimi, 'cat', vahemik,
                   'output', os.path.join(kaustanimi, uusnimi)]
            subprocess.run(arg)
                    
# Kogub kaustast failid kokku ja moodustab ühe zip-faili, mille saab
# Moodle'i ülesande vahendisse tagasisidena üles laadida. Ette antakse
# kaustanimi ja hindamisfaili nimi, viimane on Moodle'ist alla laaditud
# csv-fail, kus on kirjas alamkaustade nimedes vajalikud koodid.
def kogu_failid(kaustanimi, hindamisfailinimi):
    koodid = {}
    with open(hindamisfailinimi, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        for row in csv_reader:
            nimi = row[1]
            kood = re.findall("[0-9]+$", row[0])[0]
            koodid[nimi] = kood
        
    with zipfile.ZipFile(kaustanimi + ".zip", mode='w') as z:
        for root, dirs, files in os.walk(kaustanimi):
            files.sort()
            for file in files:
                isikunimi, _ = os.path.splitext(str(file))
                if isikunimi not in koodid:
                    print(f"Nime '{isikunimi}' ei leia")
                    continue
                alamkaustanimi = \
                   f"{isikunimi}_{koodid[isikunimi]}_assignsubmission_file_"                
                filepath = os.path.join(root, file)
                arcname = os.path.join(alamkaustanimi, file)
                z.write(filepath, arcname)
            files = [os.path.join(root, file) for file in files]
            arg = ['pdftk', *files, 'cat', 'output', kaustanimi + ".pdf"]
            subprocess.run(arg)
            