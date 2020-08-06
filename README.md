# AddBranch
Outil de généalogie : ajoute une clé "_BRCH" à un GEDCOM pour indiquer la branche à laquelle un individu est rattaché

<br><b>Préambule :</b>
<br>1/ Le fichier traité doit etre conforme à la norme GEDCOM 5.5.x
<br>2/ Il doit doit contenir une numérotation SOSA (labels "_SOSA" ou "_SOSADABOVILLE")

<br><b>Principe : </b>
<br>1/ balaye le fichier GEDCOM pour identifier les 4 grands parents et recuperer l'initiale de leurs noms
<br>2/ ajoute à chaque INDI trouvé dans le GEDCOM et ayant un label SOSA un label _BRCH sous la forme de 4 lettres. Si l'INDI découle de la lignée du grand père maternel apr exemple, _BRCH contiendra "--X-" avec "X" etant l'initiale du grand père maternel. 
Le format de _BRCH est le suivant :
<br>&emsp;&emsp;      "ABCD" :  A : initiale du nom du grand père paternel
<br>&emsp;&emsp;&emsp;                B : initiale du nom de la grand mère paternel
<br>&emsp;&emsp;&emsp;                C : initiale du nom du grand père maternel
<br>&emsp;&emsp;&emsp;                D : initiale du nom de la grand mère maternel
&emsp;
<br>Un INDI peut avoir plusieurs SOSA donc la chaine peut avoir plusieurs lettres renseignées, par ex "-X-Y"
<br>3/ le fichier généré après analyse est un "branche.ged". A vérifier avant de le renommer avec votre nom.

<br><b>Nota:</b>
<br>1/ un INDI peut avoir plusieurs etiquettes "_SOSA" ou "_SOSADABOVILLE" selon le logiciel de généalogie utilisé
<br>2/ outil "quick and dirty", réalisé juste pour mon usage et publié pour information qui marche bien pour moi mais 
<br>    à utiliser avec précaution
<br>3/ je n'utilise pas les librairies de manipultation GEDCOM dispos pour Python donc pas de besoin autre que le fichier

<br>Dans mon cas, j'utilise l'excellent ANCESTRIS, non testé avec les GEDCOM utilisés/générés par d'autres outils mais
ca ne devrait pas avoir d'impact sur les fonctions utilisés
