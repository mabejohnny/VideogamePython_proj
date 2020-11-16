class Publisher:
    def __init__(self, name):
        self.name = name
        self.sales = 0
        self.platforms = []
        self.games = []

    @staticmethod
    def publisher_decoder(name):
        return Publisher(name)