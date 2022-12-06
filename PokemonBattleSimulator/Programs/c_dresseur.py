class Dresseur :
    """ Un dresseur de pokemon. """
    def __init__(self, nom : str, pokemon) :
        self.__nom = nom
        self.__pokemon = pokemon

    # Getters
    def get_nom_dresseur(self) :
        """ Retourne le nom du dresseur. """
        return self.__nom

    def get_pokemon(self) :
        """ Retourne le pokemon combattant. """
        return self.__pokemon

    def get_nom_pokemon(self) :
        """ Retourne le nom du pokemon. """
        return self.__pokemon.get_nom()

    # Setters
    def set_pokemon(self, pokemon) :
        """ Remplace le pokemon du dresseur. """
        self.__pokemon = pokemon

