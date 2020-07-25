import sys
import os
import glob
from typing import List

gedRep = "e:\Genealogie\Datas"
gedFile = "EricGhis.ged"
outFile = "branches.ged"

glbGPP = "4 G3"
glbGMP = "5 G3"
glbGPM = "6 G3"
glbGMM = "7 G3"

iGPP = "?"
iGMP = "?"
iGPM = "?"
iGMM = "?"


# ======================================================================'
# Function : lib_GetNomsGP()
# ======================================================================'
def lib_GetNomsGP():
    nom = "x"
    sd = "-"
    lg = 0

    global iGPP
    global iGMP
    global iGPM
    global iGMM

    for line in ged:  # Using 'for ... in' on file object
        part = line.split(" ")

        if (len(part) >= 2) and (part[0] == "2") and (part[1] == "SURN"):
            nom = part[2]

        if (len(part) >= 3):
            if (part[0] == "1") and (line[2:7] == "_SOSA"):
                lg = len(part[0]) + 1 + len(part[1]) + 1
                sd = line[lg:len(line) - 1]

                if sd == glbGPP:
                    iGPP = nom[0:1]
                elif sd == glbGMP:
                    iGMP = nom[0:1]
                elif sd == glbGPM:
                    iGPM = nom[0:1]
                elif sd == glbGMM:
                    iGMM = nom[0:1]
    return 1


# ======================================================================'
# Function : lib_SosaToGp(sosa)
# ======================================================================'
def lib_SosaToGp(sosa):
    s = sosa
    Sortir = False
    gp = 0  # "x"

    if s < 8:
        Sortir = True
    while (not Sortir):
        if (s % 2) == 1:
            s = s - 1
        s = int(s / 2)
        if s < 8:
            Sortir = True

    if s == 4:
        gp = 0  # "M"
    elif s == 5:
        gp = 1  # "N"
    elif s == 6:
        gp = 2  # "C"
    elif s == 7:
        gp = 3  # "G"

    return gp


# ======================================================================'
# Programme principal
# ======================================================================'
try:
    f_IN = open(gedRep + "\\" + gedFile, 'r', encoding='utf8', errors="ignore")
    f_OUT = open(gedRep + "\\" + outFile, 'w', encoding='utf8', errors="ignore")
    ged = f_IN.readlines()
    sosaTab: List[int] = 20 * [0]
    sosaPtr = 0

    lib_GetNomsGP()
    for line in ged:  # Parcours du GEDCOM
        part = line.split(" ")
        if (part[0] == "0"):
            #
            # On arrive sur une nouvelle déclaration (type "0")
            # Traiter l'INDI en cours avant de passer au nouveau. Ballayer le
            # tab sosaTab et cherche pour chaque num à quel GP ca renvoie.
            #
            if sosaPtr > 0:
                res = list("----")
                f_OUT.write("1 _BRCH ")
                for i in range(sosaPtr):
                    so = lib_SosaToGp(sosaTab[i])
                    if so == 0:
                        res[so] = iGPP  # 'M'
                    if so == 1:
                        res[so] = iGMP  # 'N'
                    if so == 2:
                        res[so] = iGPM  # 'C'
                    if so == 3:
                        res[so] = iGMM  # 'G'
                # f_OUT.write(res + "\n")
                for i in range(len(res)):
                    f_OUT.write(res[i])
                f_OUT.write("\n")
            sosaPtr = 0

            if part[1] == "TRLR":
                print("<" + line + ">")

            if (len(part) >= 3):
                if (len(part[2]) > 4) and (part[2][:4] == "INDI"):
                    # On arrive sur une déclaration d'individu
                    for sosaPtr in range(len(sosaTab)):
                        sosaTab[sosaPtr] = 0
                    sosaPtr = 0
        #
        # Garder dans un tableau toutes les valeurs SOSA présentes pour
        # un INDI (il peut y avoir plusieurs clés SOSA dans ANCESTRIS si on
        # a coché la case correspondante. Max=20.
        #
        if (part[0] == "1") and (part[1] == "_SOSADABOVILLE"):
            br = part[2].split("-")
            sosa = int(br[0])
            sosaTab[sosaPtr] = sosa
            if sosaPtr < len(sosaTab):
                sosaPtr = sosaPtr + 1
            else:
                print("ATTENTION: débordement du tableau sosaTab")

            f_OUT.write(line)
        else:
            if (part[0] == "1") and (part[1] == "_BRCH"):
                print("sauté")
            else:
                f_OUT.write(line)
    f_IN.close()
    f_OUT.close()

except IOError:
    type, value, traceback = sys.exc_info()
    print >> sys.stderr, "Error saving file:", value
