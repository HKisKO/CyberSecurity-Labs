
#ouverture d'un file auth.log et afficher son contenue 

def afficher_logs():
    try:
        with open("auth.log" ,"r") as fichier :
                for ligne in fichier:
                    print(ligne, end="")

    except FileNotFoundError as erreur:
        print(f"ERREUR : fichier {erreur.filename}  introuvable.")





#Compter le nombre de connexion echouées et reussites
def compter_connexion():

    compteur_echec=0
    compteur_reussi=0
    try:
        with open("auth.log","r") as fichier :
            for ligne in fichier :
                if "Failed password" in ligne:
                    compteur_echec+= 1
                elif "Accepted password" in ligne:
                    compteur_reussi+=1


        print("Nombre de connexion echoués : " ,compteur_echec )
        print("le nombre de connexions reusiites: " , compteur_reussi) 

    except FileNotFoundError as erreur:
        print(f"ERREUR : fichier {erreur.filename}  introuvable.")



#afficher les adresses Ip "Failed Password"
def afficher_ip_echecs():
    try:
        with open("auth.log" , "r") as fichier :
            for ligne in fichier :
                if "Failed password" in ligne :
                    mots = ligne.split()
                    print(mots[-1])

    except FileNotFoundError as erreur:
        print(f"ERREUR : fichier {erreur.filename}  introuvable.")





#les adresse ip suspectes et qui ont echoué a se connecter

def compter_echecs_par_ip():
    echecs_par_ip = {}
    try:
        with open("auth.log" , "r") as fichier :
            for ligne in fichier :
                if "Failed password" in ligne :
                    mots = ligne.split()
                    ip_adress=mots[-1]
                    if ip_adress in echecs_par_ip:
                        echecs_par_ip[ip_adress]+= 1
                    else:
                        echecs_par_ip[ip_adress] = 1
                    
        print("===== ECHECS PAR IP =====")
        for adress,nombre_echec in echecs_par_ip.items():
            print( f"{adress} : {nombre_echec} échec(s)" ) 
        
        #Ceci peut etre fait dans une seule boucle . C est juste pour l'affichage que j ai mis une deuxieme boucle 
        print("\n===== IP SUSPECTES =====")
        for adresse, nombre_echec in echecs_par_ip.items():
            if nombre_echec >= 3:
                print(f"{adresse} : {nombre_echec} tentatives échouées")

    except FileNotFoundError as erreur:
        print(f"ERREUR : fichier {erreur.filename}  introuvable.")




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
                    "5 -Quitter\n"
                    "\n"
                    "Votre choix : "
                ))
            return choix
        except ValueError:
            print("Entrée invalide !")

while True:

    choix = menu()

    if choix == 1:
       afficher_logs()

    elif choix == 2:
        compter_connexion()

    elif choix == 3:
        afficher_ip_echecs()

    elif choix == 4:
        compter_echecs_par_ip()

    elif choix == 5:
        print("AU revoir !\n")
        break
    else:
        print("Choix invalide.\n"
              "Reessayez!!!\n")
    

