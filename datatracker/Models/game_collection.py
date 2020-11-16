class Game_Collection:
    def __init__(self, name):
        self.name = name
        self.games = []

    @staticmethod
    def gc_decoder(name):
        return Game_Collection(name)