# ==============================================================
# --------------------------CALCULATRICE -----------------------
# ==============================================================

from tkinter import Tk, Label, Button, Entry, StringVar, Toplevel
from math import pi, sin, cos, tan, sqrt
from collections import deque

operations = ["+", "-", "*", "/"]
elements_speciaux = ["(", ")", "**2", "sqrt"]
touches = [
  "1", "2", "3", "sin", "4", "5", "6", "tan", "7", "8", "9", "cos", "0", ".",
  "pi"
]


class Calculatrice(Tk):

  def __init__(self):
    super().__init__()

    #L'entrée de l'utilisateur
    self.entree = StringVar()
    #Liste d'historique qui est une pile avec une taille max de 10
    self.historique = deque([], maxlen=10)

    #Titre et configuration de la fenetre
    self.title("Calculatrice")
    self.config(bg="white")
    self.create_widgets()

    #-----------------Dimensions et centrage-----------------
    """
    hauteur = 430
    largeur = 275
    ecran_x = self.winfo_screenwidth()
    ecran_y = self.winfo_screenheight()
    pos_x = (ecran_x - largeur) // 2
    pos_y = ecran_y // 2 - hauteur // 2
    self.geometry(f"{largeur}x{hauteur}+{pos_x}+{pos_y}")
    """

  def create_widgets(self):
    #-----------------Titre de la calculatrice-----------------
    Label(self, text="TI-99", fg="blue", bg="white",
          font=("Arial", 17)).grid(row=0,
                                   column=0,
                                   columnspan=5,
                                   padx=10,
                                   pady=10)

    #-----------------Buttons utiles-----------------
    # Clear
    Button(self,
           text="C",
           fg="red",
           bg="#FBF9BE",
           height=2,
           width=2,
           command=self.reset,
           font=("Arial", 14)).grid(row=1, column=4, padx=1, pady=1)
    # Delete
    Button(self,
           text="Del",
           fg="red",
           bg="#EFBFC8",
           height=2,
           width=2,
           command=self.delete,
           font=("Arial", 14)).grid(row=6, column=0, padx=1, pady=1)

    # Valider
    Button(self,
           text="=",
           fg="blue",
           bg="#00BDF2",
           height=2,
           width=2,
           command=lambda: self.calcul(self.entree.get()),
           font=("Arial", 14)).grid(row=5, column=0, padx=1, pady=1)

    # Historique
    Button(self,
           text="Historique",
           bg="#BEEF7E",
           fg="black",
           height=1,
           width=4,
           command=self.fenetre_historique,
           font=("Arial", 7)).grid(row=0, column=4, padx=0, pady=0)

    #-----------------Ecran-----------------
    Entry(self,
          fg="black",
          bg="white",
          textvariable=self.entree,
          width=21,
          borderwidth=10,
          font=("Arial", 11)).grid(row=1,
                                   column=0,
                                   columnspan=4,
                                   padx=5,
                                   pady=5)

    #-----------------Les touches de la calculatrice-----------------

    #-----Les touches 0 à 9/sin/cos/tan/pi/.-----
    #Initialisaton de colonnes et lignes
    num_col = 0
    num_row = 2
    for touche in touches:
      Button(self,
             text=f"{touche}",
             bg="#6666CD",
             height=2,
             width=2,
             command=lambda x=touche: self.button_click(x),
             font=("Arial", 14)).grid(row=num_row,
                                      column=num_col,
                                      padx=0,
                                      pady=0)
      #Incrémentation de nombre de colonne
      num_col += 1
      #Lorsque le numéro de colonne atteint 4, on l'initialise et on incrémente le numéro de ligne
      if num_col == 4:
        num_col = 0
        num_row += 1
        #Lorsque le numéro de ligne atteint 5, on commence par la colonne 1 au lieu de 0 pour avoir le 0 au milieu.
        if num_row == 5:
          num_col = 1

    #-----Les opérandes-----
    #Initialisaton de lignes
    num_row = 2
    for operande in operations:
      Button(self,
             text=f"{operande}",
             bg="#EEEE3B",
             height=2,
             width=2,
             command=lambda x=operande: self.button_click(x),
             font=("Arial", 14)).grid(row=num_row, column=4, padx=1, pady=1)
      #on incrémente le numero de ligne
      num_row += 1

    #-----Les éléments spéciaux-----
    num_col = 1
    for element in elements_speciaux:
      Button(self,
             text=f"{element}",
             bg="#F58220",
             height=2,
             width=2,
             command=lambda x=element: self.button_click(x),
             font=("Arial", 14)).grid(row=6, column=num_col, padx=1, pady=1)
      num_col += 1

  # -----------------Les fonctions-----------------
  def reset(self):
    self.entree.set("")

  #Traitement de touches pour les mettre sous forme d'une chaine de characteres en concaténation
  def button_click(self, element):
    #Vérifier que l'utilisateur ne tape pas deux fois sur l'opérande (sans mettre les parenthèses pour les signes)
    try:
      last_char = self.entree.get()[-1]
    except IndexError:
      last_char = ""

    if element in operations and last_char in operations:
      self.entree.set("ERREUR 2 opérandes, Tapez sur C")
    else:
      self.entree.set(self.entree.get() + f"{element}")

  #Utilisation de la fonction eval pour évaluer la chaîne en traitant les éventuelles erreurs
  def calcul(self, entree):
    try:
      resultat = str(eval(entree))
      self.entree.set(resultat)
      self.historique.appendleft(f"{entree} = {resultat}")
    except ZeroDivisionError:
      self.entree.set("ERREUR DIVISION PAR 0 Tapez sur C")
    except ValueError:
      self.entree.set("ERREUR DE VALEUR Tapez sur C")
    except SyntaxError:
      self.entree.set("ERREUR DE SYNTAXE Tapez sur C")
    except NameError:
      self.entree.set("ERREUR Tapez sur C")

  #Supprimer le dernier caractère de la chaîne
  def delete(self):
    self.entree.set(self.entree.get()[:-1])

  #Pour l'historique, nous affichons une fenêtre avec une liste d'historique qui est une pile avec une taille maximale de 10
  def fenetre_historique(self):
    fenetre_historique = Toplevel()
    fenetre_historique.title("Historique")
    fenetre_historique.config(width=300, height=200, bg="white")

    #Button pour quitter la fenetre historique
    Button(fenetre_historique,
           text="Quitter l'historique",
           command=fenetre_historique.destroy,
           font=("Arial", 12)).grid(row=0, column=0, padx=1, pady=1)
    num_row = 1

    #Si pas d'historique
    if len(self.historique) == 0:
      Label(fenetre_historique,
            text="Pas de historique",
            fg="red",
            bg="white",
            font=("Arial", 10)).grid(row=num_row, column=0)

    # Sinon on affiche les differentes operations
    for operation in self.historique:
      Label(fenetre_historique,
            text=f"{operation}",
            fg="blue",
            bg="white",
            font=("Arial", 10)).grid(row=num_row, column=0)
      num_row += 1


def main():
  calculatrice = Calculatrice()
  calculatrice.mainloop()


if __name__ == '__main__':
  main()
