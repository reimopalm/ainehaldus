import os

VÄLJUNDFAILINIMI = "programmid.py"

def kogu_üks(isikunimi, ülnimed):
    """
    Collects the content of Python files in subdirectories of the specified names.
    
    Args:
        isikunimi (str): Name of the person.
        ülnimed (list): List of subdirectory names.
    
    Returns:
        str: Concatenated content of Python files.
    """
    sisu = ""
    for ülnimi in ülnimed:
        alamkaust = os.path.join(ülnimi, isikunimi)
        for failinimi in os.listdir(alamkaust):
            if failinimi.endswith(".py"):
                sisu += f"# {failinimi}\n\n"
                with open(os.path.join(alamkaust, failinimi)) as f:
                    sisu += f.read().rstrip()                    
                sisu += "\n\n"
    return sisu

def kogu_kõik(isikunimed, ülnimed):
    """
    Collects and writes the content of Python files for multiple individuals.
    
    Args:
        isikunimed (list): List of individual names.
        ülnimed (list): List of subdirectory names.
    """
    f = open(VÄLJUNDFAILINIMI, 'w', encoding="utf8")
    esim = True
    for isikunimi in isikunimed:
        if esim:
            esim = False
        else:
            f.write("\n# " + "-" * 70 + "\n\n")
        f.write(f"# * {isikunimi}\n\n")
        sisu = kogu_üks(isikunimi, ülnimed)
        f.write(sisu)
    f.close()

isikunimed = [
    "Eesnimi Perekonnanimi",
    "Eesnimi Perekonnanimi",
    "Eesnimi Perekonnanimi",
]
ülnimed = ["1", "2"]
kogu_kõik(isikunimed, ülnimed)