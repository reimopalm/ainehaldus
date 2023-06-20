with open("failid.txt", encoding="utf8") as f:
    sisuread = f.read().splitlines()
sisuread.sort()
        
with open("parandamine.txt", "w") as g:
    for nr, rida in enumerate(sisuread, start=1):
        nimi, muu = rida.split(".")
        g.write(f"* {nimi}\n\n2. (/18) (a)\n\n(b)\n\nR    14.04    {nr}\n\n")
    
    g.write(("-" * 72) + "\n\n")

    for nr, rida in enumerate(sisuread, start=1):
        nimi, muu = rida.split(".")
        g.write(f"* {nimi}\n\n3. (/20)\n\nR    14.04    {nr}\n\n")
        