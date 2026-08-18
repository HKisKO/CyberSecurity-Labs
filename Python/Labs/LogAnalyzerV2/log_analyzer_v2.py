#le mode de sortie (affichage sur terminal ou exporter resultats)
def choisir_sortie():
    while True:
        try:
            choix=int(input("        ===== MODE DE SORTIE =====     \n"
        "1 - Afficher uniquement dans le terminal \n"
        "2 - Exporter aussi dans un fichier texte \n"
        ))

            if choix==1:
                return "terminal"
            elif choix==2:
                return "fichier"
            else:
                print("choisissez 1 ou 2 !!!")

        except ValueError:
            print("Entrer un entier 1 ou 2")

#choix si mode = exporter un fichier
def choisir_mode_fichier():
    while True:
        try:
            choix = int(input(
                "===== MODE D'ÉCRITURE =====\n"
                "1 - Créer/remplacer le rapport\n"
                "2 - Ajouter au rapport existant\n"
                "3 - Créer uniquement s'il n'existe pas\n"
                "4 - Annuler\n"
                "Votre choix : "
            ))

            if choix== 1:
                return "w"
            elif choix== 2:
                return "a"
            elif choix== 3:
                return "x"
            elif choix==4:
                return None
            else:
                print("choisissez entre 1 et 4")
        except ValueError:
            print("Entrez un entier entre 1 et 4.")



#eviter de repeter le controle dexception 
def lire_fichier():
    while True:  
        nom_fichier = input("Nom de fichier à analyser : ")
        try:
            with open(nom_fichier, "r") as fichier:
                lignes = fichier.readlines()
                return nom_fichier,lignes

        except FileNotFoundError as erreur:
            print(f"ERREUR : fichier {erreur.filename} introuvable.")

#demander (le nom de fechier sois a entrer sois a maj sois rajouter du contenue dedan selon mode)
def exporter_fichier(mode):
    while True:
        nom_rapport = input("Nom du fichier de rapport : ")
        try:
            with open(nom_rapport, mode) as fichier:
                fichier.write("===== RAPPORT LOG ANALYZER =====\n")

            print(f"votre rapport est enregistré dans : {nom_rapport}")
            return nom_rapport
        
        except FileExistsError:
            print(f"ERREUR : le fichier {nom_rapport} existe déjà.")



#afficher le contenue du fichier
def afficher_logs(lignes,mode_sortie,nom_rapport):
    
    if mode_sortie =="terminal" :
        if not lignes:
            print("fichier vide")
            return
        for ligne in lignes:
            print(ligne, end="")
    elif mode_sortie == "fichier":
        if not lignes:
            print(f"fichier vide y a rien a ecrire sur {nom_rapport}")
            return
        with open(nom_rapport,'a') as fichier :
            fichier.write("\n===== LOGS =====\n")
            for ligne in lignes:
                fichier.write(ligne)



#Compter le nombre de connexion echouées et reussites
def compter_connexion(lignes,mode_sortie,nom_rapport):

    compteur_echec=0
    compteur_reussi=0

    if not lignes:
            print("fichier vide")
            return 
    
    for ligne in lignes :
                if "Failed password" in ligne:
                    compteur_echec+= 1
                elif "Accepted password" in ligne:
                    compteur_reussi+=1

    if mode_sortie == "terminal":  
        print("Nombre de connexion echoués : " ,compteur_echec )
        print("le nombre de connexions reusiites: " , compteur_reussi) 

    elif mode_sortie == "fichier" :
        with open(nom_rapport,"a") as fichier :
            fichier.write("Le nombre de connexion echouées et reussites \n")
            fichier.write(f"nombre de connexion echoués : {compteur_echec} \n ")
            fichier.write(f"nombre de connexions reusiites : {compteur_reussi}  \n")
   


#afficher les adresses Ip "Failed Password"
def afficher_ip_echecs(lignes,mode_sortie,nom_rapport):

    if not lignes:
        print("fichier vide")
        return
    
    ip_echecs =[]

    for ligne in lignes:
        if "Failed password" in ligne :
            mots = ligne.split()
            ip_echecs.append(mots[-1])

    if mode_sortie=="terminal":
        for adresses in ip_echecs:
            print(adresses)

    elif mode_sortie=="fichier":
        with open(nom_rapport,"a") as fichier :
            fichier.write("\n les adresses ip avec mauvais password sont : \n")
            for adresses in ip_echecs:
                fichier.write(f"{adresses} \n")


#les adresse ip suspectes et qui ont echoué a se connecter

def compter_echecs_par_ip(lignes,mode_sortie,nom_rapport):
    
    if not lignes:
        print("fichier vide")
        return

    
    echecs_par_ip = {}

    
    for ligne in lignes :
        if "Failed password" in ligne :
            mots = ligne.split()
            ip_adress=mots[-1]
            if ip_adress in echecs_par_ip:
                echecs_par_ip[ip_adress]+= 1
            else:
                echecs_par_ip[ip_adress] = 1


    classement = sorted(echecs_par_ip.items(),key=lambda element: element[1], reverse=True)  

    while True:
        try:
            seuil = int(input("Seuil de tentatives suspectes : "))
            if seuil <= 0:
                print("Le seuil doit être supérieur à 0.")
                continue
            
            break

        except ValueError:
            print("Entrée invalide ! Entrez un nombre entier.") 

    resultat = "\n===== ECHECS PAR IP =====\n"

    for adresse, nombre_echec in classement:
        resultat += f"{adresse} : {nombre_echec} échec(s)\n"

    resultat += "\n===== IP SUSPECTES =====\n"

    for adresse, nombre_echec in classement:
        if nombre_echec >= seuil:
            resultat += f"{adresse} : {nombre_echec} tentatives échouées\n"

    if mode_sortie == "terminal":
        print(resultat)

    elif mode_sortie == "fichier":
        with open(nom_rapport, "a") as fichier:
            fichier.write(resultat) 

'''
    if mode_sortie=="terminal":
        print("===== ECHECS PAR IP =====")
        for adress,nombre_echec in classement:
            print( f"{adress} : {nombre_echec} échec(s)" ) 
            
        print("\n===== IP SUSPECTES =====")
        for adresse, nombre_echec in classement:
            if nombre_echec >= seuil:
                print(f"{adresse} : {nombre_echec} tentatives échouées \n")

    elif mode_sortie== "fichier":
        with open(nom_rapport,"a") as fichier:
            fichier.write("===== ECHECS PAR IP ===== \n")
            for adress,nombre_echec in classement:
                fichier.write( f"{adress} : {nombre_echec} échec(s) \n" ) 

            fichier.write("\n===== IP SUSPECTES =====\n")
            for adresse, nombre_echec in classement:
                if nombre_echec >= seuil:
                    fichier.write(f"{adresse} : {nombre_echec} tentatives échouées")
'''

#fonction pour avoir le mode de sortie (fichier/terminal) et le nom du rapport 
def configurer_sortie():
    while True:
        mode_sortie = choisir_sortie()

        if mode_sortie == "terminal":
            return "terminal",None

        elif mode_sortie == "fichier":
            mode = choisir_mode_fichier()
            if mode is None:
                continue

            nom_rapport = exporter_fichier(mode)
            return "fichier", nom_rapport

def menu():

    while True:

        try:

            choix = int(input(
                "\n========== Log Analyzer ==========\n"
                    "\n"
                    "1 -Afficher les logs \n"
                    "2 -Afficher le nombre de connexion échouées et réussies\n"
                    "3 -Afficher les adresses Ip qui ont echoué a se connecter\n"
                    "4 -Afficher le nombre d'echec par adresse Ip et les adresses Ip suspectes \n"
                    "5 -Changer de fichier\n"
                    "6 -Quitter"
                    "\n"
                    "Votre choix : "
                ))
            return choix
        except ValueError:
            print("Entrée invalide !")



nom_fichier, lignes = lire_fichier()
mode_sortie, nom_rapport = configurer_sortie()

'''
while True:
    mode_sortie = choisir_sortie()

    if mode_sortie == "terminal":
        break

    elif mode_sortie == "fichier":
        mode = choisir_mode_fichier()
        if mode is None:
            continue
        nom_rapport = exporter_fichier(mode)

        break
'''

while True:

    choix = menu()

    if choix == 1:
       
       afficher_logs(lignes, mode_sortie, nom_rapport)

    elif choix == 2:
        compter_connexion(lignes,mode_sortie, nom_rapport)

    elif choix == 3:
        afficher_ip_echecs(lignes ,mode_sortie , nom_rapport)

    elif choix == 4:
        compter_echecs_par_ip(lignes, mode_sortie,nom_rapport)

    elif choix == 5:
        nom_fichier, lignes = lire_fichier()
        mode_sortie, nom_rapport = configurer_sortie()

    elif choix == 6:
        print("AU revoir !\n")
        break

    else:
        print("Choix invalide.\n"
              "Reessayez!!!\n")
    
