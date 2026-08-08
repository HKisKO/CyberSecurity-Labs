
#declaration dectionnaire
services = {
    22 : "SSH",
    80 : "HTTP",
    443 : "HTTPS"
}

#affichage globale :
#print(services)

#affichage des valeurs à droites :
#print(services.values())
#or
#for j in services.values():
#     print(j)


#affichage des valeurs à gauche :
#for i in services:
#   print(i)
#or
#print(services.keys())

#affichage port et son service :
#for port, service in services.items():
#   print(f"Port {port} => {service}")

#ajout d'un service 
#services[21] = "FTP" 
#print(services)

#Transformer http en http/1.1
#services[80] = "HTTP/1.1"
#print(services)

#supprimer le service ftp
#services.pop(21)
#print(services)

#recherche interaction avec user
#entrée = int (input( "quel port voulez vous check? "))

#if entrée in services.keys():
#    print(services[entrée])
#else:
#    print("port non existant")

#recherche avec http et trouve le numero du port 
#print(services)

#trouvé = False

#entrée = input("Quel service recherchez-vous ? ")

#for port, service in services.items():
#    if entrée == service:
#        print(f"{service} fonctionne sur le port {port}")
#        trouvé = True

#if not trouvé:
#    print("Service inexistant")


# afficher le nombre se service disponible
#print("les services disponibles : " ,len(services))

#trie et trie invers
print(sorted(services))
print(sorted(services,reverse=True))























