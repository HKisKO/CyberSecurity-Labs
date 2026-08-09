services = {
    22 : "SSH",
    80 : "HTTP",
    443 : "HTTPS"
}

#Fonction d affichage de service 
def afficher_services():
    print("===== SERVICES ===== \n")
    for port,service in services.items():
        print(f"{port} : {service}\n")


#recherche de service par port
def rechercher_par_port():
    while True:
        try:

            choix=int(input("Entrer un port : "))
            if choix in services.keys():
                print("Service : ", services[choix]) 
                return #je pense pas besoin 
            else:
                print("Aucun service trouvé pour ce port.") 
                return  
        except ValueError:
            print("Un port est un entier reessayer !!")

#rechercher un port par service 
def rechercher_par_service():
    trouve=False
    service_demandé = input("Entrez un service : ").upper()
    for port, service in services.items():
        if service_demandé == service:
            print("Port : " , port)
            trouve = True

    if not trouve:
        print("service indisponible")   
        
#ajout de service avec contrainte 
def ajout_de_services():

    while True:
        try:
            port_nouveau_service=int(input("Entrer le numero de port "))
       
            if port_nouveau_service in services.keys():
                print("Numero de port deja existant!!")
                return

            else:
                service_associe=input("entrer son service associé ").upper()
                if service_associe in services.values():
                    print("Ce service est deja associé a un autre port!!!  REESAYER!")
                    return
                else:
                    services[port_nouveau_service]= service_associe
                    print(f"Service {service_associe} ajouté sur le port {port_nouveau_service}.")
                    return
        except ValueError:
            print("un numero de port est un entier")

#supprimer un service
def delete_service():
    while True:
        try:

            port_to_delete= int(input("Entrer le port à supprimer "))  
            if port_to_delete in services:
                service_of_port= services[port_to_delete]
                services.pop(port_to_delete)  
                print(f"Vous avez supprimer le port {port_to_delete} dont le service est : {service_of_port}")  
                return 
            else:
                print("Ce port n'existe pas")  
                return
        except ValueError:
            print("entrer un numero de port !") 


def menu():
    while True:

        try:
            choix = int(input(
                "========== SERVICE MANAGER ==========\n"
                "\n"
                "1 - Afficher tous les services\n"
                "2 - Rechercher un service par port\n"
                "3 - Rechercher un port par service\n"
                "4 - Ajouter un service\n"
                "5 - Supprimer un service\n"
                "6 - Quitter\n"
                "\n"
                "Votre choix : \n"
            ))
            return choix
        
        except ValueError:
            print("ERREUR: VEUILLEZ INSERER UN NOMBRE !")


while True:

    choix = menu()
    
    if choix == 1:
        print("Vous avez choisi : 1")
        afficher_services()

    elif choix == 2:
        print("Vous avez choisi : 2")
        rechercher_par_port()

    elif choix == 3:
        print("Vous avez choisi : 3")
        rechercher_par_service()

    elif choix == 4:
        print("Vous avez choisi : 4")
        ajout_de_services()


    elif choix == 5:
        print("Vous avez choisi : 5\n")
        delete_service()

    elif choix == 6:
        print("Au revoir !\n")
        break

    else:
        print("Choix invalide.\n"
              "Reessayez!!!\n")