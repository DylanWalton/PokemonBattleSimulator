class Pokemon :
    """" Un pokemon. """
    def __init__(self, nom : str, pv : int, attaque : int, defense : int, niveau : int) :
        self.__nom = nom
        self.__pv = int(((2*pv+16+21)*niveau)/100)+niveau+10
        self.__attaque = int(((2*attaque+16+21)*niveau)/100)+niveau+10
        self.__defense = int(((2*defense+16+21)*niveau)/100)+niveau+10
        self.__niveau = niveau
        self.__loboNum = 3   # Le nombre de fois que le pokemon pourra effectuer l'attaque speciale 'lobotimisation'.
        self.__lanceTableDeg = self.__pv//5   # Les degats a infliger a ce pokemon quand l'attaque speciale 'Lance de table' est effectuee.

    def set_degats(self, degats : int) :
        """" Soustrait degat de pv si degat et inferieur a pv, sinon, le pokemone 'meurt'. """
        if degats <= self.__pv :
            self.__pv -= degats
        else :
            self.__pv = 0

    # Getters
    def get_nom(self) :
        """ Retourne le nom du pokemon. """
        return self.__nom

    def get_pv(self) :
        """ Retourne le pv du pokemon. """
        return self.__pv

    def get_attaque(self) :
        """ Retourne l'attaque du pokemon. """
        return self.__attaque

    def get_defense(self) :
        """ Retourne la defense du pokemon. """
        return self.__defense

    def get_niveau(self) :
        """ Retourne le niveau du pokemon. """
        return self.__niveau

    def get_loboNum(self) :
        """ Retourne le nombre de fois restant dont le pokemon peut effectuer l'attaque speciale 'lobotimisation'. """
        return self.__loboNum

##    def get_extincteurNum(self) :
##        """ Retourne le nombre de fois restant dont le pokemon peut effectuer l'attaque speciale 'extincteur'. """
##        return self.__extincteurNum


    def attaquer(self, pokemon) :
        """ Inflige des degats a un pokemon. """
        from random import randint
        cm = randint(85, 100) / 100
        degats = ((self.__niveau*.4+2)*self.__attaque/(self.__defense*2)+2)*cm//1
        print(degats)
        pokemon.set_degats(degats)

    # Attaques Speciales
    def lobotimisation(self, pokemon) :
        if self.__loboNum > 0 :
            from random import randint
            cm = randint(85, 100) / 100
            degats = ((self.__niveau*.4+2)*self.__attaque/(self.__defense*2)+2)*cm//1
            pokemon.set_degats(degats * 1.7 // 1)
            self.__loboNum -= 1

    def extincteur(self, pokemon) :
        from random import randint
        cm = randint(85, 100) / 100
        degats = ((self.__niveau*.4+2)*self.__attaque/(self.__defense*2)+2)*cm//1
        pokemon.set_degats(degats * 1.2 // 1)
        self.__extincteurNum -= 1

    def lanceDeTable(self, pokemon) :
        self.set_degats(self.__lanceTableDeg)
        from random import randint
        cm = randint(85, 100) / 100
        degats = ((self.__niveau*.4+2)*self.__attaque/(self.__defense*2)+2)*cm//1
        pokemon.set_degats(degats * 1.4 // 1)




pikachu = Pokemon("Pikachu", 35, 55, 40, 10)
onix = Pokemon("Onix", 35, 45, 160, 10)