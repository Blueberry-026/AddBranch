import sys
import os
import glob
from typing import List

gedRep = "e:\Genealogie\Datas"
gedFile = "EricGhis.ged"
outFile = "branches.ged"

def SosaToGp(sosa):
    s=sosa
    Sortir=False
    gp = 0; #"x"

    if s < 8:
        Sortir = True
    while (not Sortir):
        if (s % 2) == 1:
            s=s-1
        s = int(s/2)
        if s<8 :
            Sortir=True

    if s == 4:
        gp = 0; #"M"
    elif s == 5:
        gp = 1; #"N"
    elif s == 6:
        gp = 2; #"C"
    elif s == 7:
        gp = 3; #"G"

    return gp


try:
    f_IN = open(gedRep + "\\"+gedFile, 'r', encoding='utf8', errors="ignore")
    f_OUT = open(gedRep + "\\"+outFile, 'w', encoding='utf8', errors="ignore")
    ged=f_IN.readlines()
    sosaTab: List[int] = 20*[0];
    sosaPtr = 0;
    for line in ged:  # Using 'for ... in' on file object
        print("<"+line+">");
        part=line.split(" ");
        if (part[0] == "0") :
            # On arrive sur une nouvelle déclaration
            if sosaPtr>0 :
                res=list("----");
                f_OUT.write("1 _BRCH ");
                for i in range(sosaPtr):
                    so = SosaToGp(sosaTab[i]);
                    if so==0:
                        res[so]='M';
                    if so==1:
                        res[so]='N';
                    if so==2:
                        res[so]='C';
                    if so==3:
                        res[so]='G';
                #f_OUT.write(res + "\n")
                for i in range(len(res)):
                    f_OUT.write(res[i])
                f_OUT.write("\n")
            sosaPtr = 0;

            if part[1] == "TRLR":
                print("<" + line + ">");

            if (len(part)>=3) :
                if (len(part[2])>4) and (part[2][:4] == "INDI"):
                    # On arrive sur une déclaration d'individu
                    for sosaPtr in range(len(sosaTab)):
                        sosaTab[sosaPtr]=0;
                    sosaPtr = 0;
        if (part[0] == "1") and (part[1] == "_SOSADABOVILLE"):
            br = part[2].split("-")
            sosa = int(br[0])
            sosaTab[sosaPtr] = sosa;
            sosaPtr = sosaPtr + 1;
            f_OUT.write (line)
        else:
            if (part[0] == "1") and (part[1] == "_BRCH"):
                print ("sauté")
            else:
                f_OUT.write (line)
    f_IN.close()
    f_OUT.close()

except IOError:
   type, value, traceback = sys.exc_info()
   print >> sys.stderr, "Error saving file:", value
