class Platform:
    def __init__(self, name):
        self.name = name
        self.sales = 0
        self.games = []

    @staticmethod
    def platform_decoder(name):
        return Platform(name)
