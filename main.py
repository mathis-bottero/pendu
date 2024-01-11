import random
import pygame
import sys
import matplotlib.pyplot as plt  # Importation de matplotlib.pyplot as plt pour pouvoir utiliser les couleur de manière plus facile



# Initialisation de Pygame
pygame.init()


# Définition des couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
ROUGE = "red"
BLEUE = "blue"
ROSE = "pink"




# Configuration de la fenêtre
largeur, hauteur = 1400, 700  # Modification de la taille de la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("HANGMAN GAME")


# Police d'écriture
font = pygame.font.Font(None, 36)

options = ["START A NEW GAME", "INSERT A NEW WORD IN THE FILE", "DISPLAY SCORES", "EXIT THE PROGRAMM"]

def afficher_menu():
    fenetre.fill(BLANC)
    titre = font.render("HANGMAN  MENU", True, ROUGE)
    fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 50))
    y = 150
    regions_rectangulaires = {}  # Dictionnaire pour stocker les régions rectangulaires associées à chaque option
    for option in options:
        texte = font.render(option, True, BLEUE)
        largeur_texte, hauteur_texte = texte.get_size()

        # Dessiner la boîte autour de l'option
        region_rectangulaire = pygame.Rect((largeur // 2 - 350, y, 700, 50))
        pygame.draw.rect(fenetre, (192, 192, 192), region_rectangulaire, 2)

        # Centrer le texte à l'intérieur de la boîte
        fenetre.blit(texte, (largeur // 2 - largeur_texte // 2, y + (50 - hauteur_texte) // 2))

        regions_rectangulaires[option] = region_rectangulaire
        y += 50 + 50  # Ajoute un espacement entre les options

    pygame.display.flip()

    return regions_rectangulaires



def choisir_mot_aleatoire(difficulte):
    with open("mots.txt", "r", encoding="utf-8") as fichier:
        mots = [mot.strip().lower() for mot in fichier.readlines() if difficulte[0] <= len(mot.strip()) <= difficulte[1]]
        
    mot_choisi = random.choice(mots)
    return mot_choisi



def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = " ".join([lettre if lettre in lettres_trouvees else "_" for lettre in mot])
    return mot_cache



def choose_difficulties():
    fenetre.fill(BLANC)
    titre = font.render("CHOOSE DIFFICULTY", True, ROUGE)
    fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 50))

    options_difficulte = ["EASY", "MEDIUM", "HARD", "BACK"]
    y = 150
    regions_difficulte = {}

    difficultes = {"EASY": (1, 4), "MEDIUM": (5, 6), "HARD": (7, 20) }

    for option_difficulte in options_difficulte:
        texte_difficulte = font.render(option_difficulte, True, BLEUE)
        largeur_texte_difficulte, hauteur_texte_difficulte = texte_difficulte.get_size()

        region_rectangulaire_difficulte = pygame.Rect((largeur // 2 - 250, y, 500, 50))
        pygame.draw.rect(fenetre, (192, 192, 192), region_rectangulaire_difficulte, 2)

        fenetre.blit(texte_difficulte, (largeur // 2 - largeur_texte_difficulte // 2, y + (50 - hauteur_texte_difficulte) // 2))

        regions_difficulte[option_difficulte] = region_rectangulaire_difficulte
        y += 50 + 50

    pygame.display.flip()

    choix_difficulte = None
    while choix_difficulte not in options_difficulte:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pygame.K_RETURN

                for option_difficulte, region_rectangulaire_difficulte in regions_difficulte.items():
                    if region_rectangulaire_difficulte.collidepoint(pos):
                        choix_difficulte = option_difficulte
            
            if choix_difficulte == "Back":
                return None  # Retourner None si l'option "Back" est choisie

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                choix_difficulte = "Back"  # Utiliser "Back" pour revenir en arrière

    return difficultes.get(choix_difficulte)  # Utiliser get pour renvoyer None si "Back" est choisi



def player_name():
    name = ""
    writing = True
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 52)

    while writing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    writing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        fenetre.fill(BLANC)
        titre = font.render("HANGMAN USER NAME", True, ROUGE)
        fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 100))

        prompt = font.render("Enter your name : {}".format(name), True, BLEUE)
        fenetre.blit(prompt, (largeur // 2 - prompt.get_width() // 2, 230))
        pygame.display.flip()
        clock.tick(60)

    return name  # Retourne le nom de l'utilisateur après la boucle while



def load_scores(filename="scores.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
    # Convertir les scores en une liste de dictionnaires {'nom': nom, 'score': score}
    scores = [line.strip().split(":") for line in lines]
    scores = [{'nom': score[0].strip(), 'score': int(score[1].strip())} for score in scores]
    return scores

def save_scores(player_name, erreurs_max, erreurs, filename="scores.txt"):
    score = erreurs_max - erreurs
    new_score = f"{player_name}:{score}"  

    # Enregistrer le nouveau score dans le fichier
    with open(filename, 'a') as file:
        file.write(new_score + "\n")

def display_scores():
    clock = pygame.time.Clock()
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False 

        fenetre.fill(BLANC)
        titre = font.render("HIGH BOARDSCORES", True, ROUGE)
        fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 50))

        scores = load_scores()

        if scores:
            y = 150
            for score in scores:
                score_text = font.render(f"{score['nom']} _ _ _ _ _  _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ {score['score']}", True, NOIR)
                fenetre.blit(score_text, (largeur // 2 - score_text.get_width() // 2, y))
                y += 40

        pygame.display.flip()
        clock.tick(60)



# La Boucle principale de mon jeu
def menu():
    name = ""  # Initialiser le nom ici
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Gestion de la touche "Back" avant de sélectionner une option
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                name = ""  # Réinitialiser le nom si la touche "Back" est enfoncée

        regions_rectangulaires = afficher_menu()

        choix = None
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                # Vérifie si les coordonnées du clic sont à l'intérieur de l'une des régions rectangulaires
                for option, region_rectangulaire in regions_rectangulaires.items():
                    if region_rectangulaire.collidepoint(pos):
                        choix = option
                        break
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                choix = "EXIT THE PROGRAMM"  # Revenir au menu si la touche Échap est enfoncée

        if choix == "START A NEW GAME":
            difficulte = choose_difficulties()
            if difficulte is None:
                continue  # Revenir au début de la boucle principale si l'option "Back" est choisie
            name = player_name()
            pendu(difficulte, name)  # Passer le nom du joueur à la fonction pendu
        elif choix == options[1]:
            inserer_mot()
        elif choix == "DISPLAY SCORES":
            display_scores()
        elif choix == "EXIT THE PROGRAMM":
            pygame.quit()
            sys.exit()




def inserer_mot():
    nouveau_mot = ""
    en_train_d_ecrire = True

    clock = pygame.time.Clock()

    while en_train_d_ecrire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    en_train_d_ecrire = False
                    # Ajouter le nouveau mot au fichier mots.txt
                    with open("mots.txt", "a", encoding="utf-8") as fichier:
                        fichier.write(f"{nouveau_mot} \n")
                elif event.key == pygame.K_BACKSPACE:
                    nouveau_mot = nouveau_mot[:-1]
                elif event.key in range(pygame.K_a, pygame.K_z + 1):
                    lettre = chr(event.key).lower()
                    nouveau_mot += lettre
                elif event.key == pygame.K_ESCAPE:
                    return  # Retourner au menu si la touche Échap est enfoncée

        fenetre.fill(BLANC)

        titre = font.render("ADD A NEW WORD", True, ROUGE)
        fenetre.blit(titre, (largeur // 2 - titre.get_width() // 2, 100))
        prompt = font.render("Enter a new word : {}".format(nouveau_mot), True, BLEUE)
        fenetre.blit(prompt, (largeur // 2 - prompt.get_width() // 2, 250))

        pygame.display.flip()
        clock.tick(60)


def dessiner_pendu(erreurs):
    if erreurs >= 1:
        pygame.draw.line(fenetre, NOIR, (100, 400), (100, 100), 5)  # Poteau
        pygame.draw.line(fenetre, NOIR, (50, 400), (350, 400), 5)  # Le potau de bas
        pygame.draw.line(fenetre, NOIR, (100, 100), (250, 100), 5)  # Le potau de haut
        pygame.draw.line(fenetre, NOIR, (100, 150), (200, 100), 5)  # Le potau penchant
        pygame.draw.line(fenetre, NOIR, (250, 180), (250, 100), 5)  # La corde
    if erreurs >= 2:
        pygame.draw.circle(fenetre, ROSE, (250, 210), 30, 5)  # Tête
    if erreurs >= 3:
        pygame.draw.line(fenetre, NOIR, (250, 235), (250, 335), 5)  # Corps
    if erreurs >= 4:
        pygame.draw.line(fenetre, NOIR, (250, 280), (315, 250), 5)  # Bras droit
    if erreurs >= 5:
        pygame.draw.line(fenetre, NOIR, (250, 280), (185, 250), 5)  # Bras gauche 
    if erreurs >= 6:
        pygame.draw.line(fenetre, NOIR, (250, 335), (200, 385), 5)  # Jambe droite
    if erreurs >= 7:
        pygame.draw.line(fenetre, NOIR, (250, 335), (300, 385), 5)  # Jambe gauche


def pendu(difficulte, name):
    mot_a_trouver = choisir_mot_aleatoire(difficulte)
    lettres_trouvees = set()
    erreurs_max = 7  # Le nombre de tentative pour deviner le mot
    erreurs = 0

    pygame.display.set_caption("Hangman Game - Guess the word!")

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Appuyer echap pour revenir au menu du jeu 
                    return
                elif event.key in range(pygame.K_a, pygame.K_z + 1):
                    lettre = chr(event.key).lower()
                    if lettre not in lettres_trouvees:
                        lettres_trouvees.add(lettre)
                        if lettre not in mot_a_trouver:
                            erreurs += 1

        fenetre.fill(BLANC)

        afficher_mot = afficher_mot_cache(mot_a_trouver, lettres_trouvees)
        mot_texte = font.render(afficher_mot, True, NOIR)
        fenetre.blit(mot_texte, (largeur // 2 - mot_texte.get_width() // 2, 200))

        lettres_essayed = " ".join(sorted(lettres_trouvees))
        lettres_essayed_texte = font.render(f"Attempts allowed : {lettres_essayed}", True, NOIR)
        fenetre.blit(lettres_essayed_texte, (largeur // 2 - lettres_essayed_texte.get_width() // 2, 90))

        erreurs_texte = font.render("Errors {}/{}".format(erreurs, erreurs_max), True, ROUGE)
        fenetre.blit(erreurs_texte, (largeur // 2 - erreurs_texte.get_width() // 2, 300))

        dessiner_pendu(erreurs)

        pygame.display.flip()
        clock.tick(60)

        if set(lettres_trouvees) >= set(mot_a_trouver):
            gagne_texte = font.render("Congratulations {}! You guessed the word '{}'.".format(name, mot_a_trouver), True, VERT)
            save_scores(name, (erreurs_max), erreurs)
            fenetre.blit(gagne_texte, (largeur // 2 - gagne_texte.get_width() // 2, 400))
            s_text = font.render("Your score has been saved successfully!", True, VERT)
            fenetre.blit(s_text, (largeur // 2 - gagne_texte.get_width() // 2, 450))
            pygame.display.flip()
            pygame.time.wait(5000)
            return

        # Ajoutez cette condition pour mettre à jour le dessin après chaque devinette de lettre
        if erreurs > 0 and erreurs < erreurs_max and set(lettres_trouvees) < set(mot_a_trouver):
            dessiner_pendu(erreurs)

        if erreurs == erreurs_max:
            perdu_texte = font.render("Failed, {} reached the maximum number of attempts. The word was :'{}'.".format(name, mot_a_trouver), True, ROUGE)
            fenetre.blit(perdu_texte, (largeur // 2 - perdu_texte.get_width() // 2, 530))
            pygame.display.flip()
            pygame.time.wait(5000)
            return



# Appeler la fonction menu à la fin du script
if __name__ == "__main__":
    menu()
