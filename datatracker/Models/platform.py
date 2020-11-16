class Platform:
    def __init__(self, name):
        self.name = name
        self.totalSales = 0
        self.games = []
        self.sales85_89 = 0
        self.sales90_94 = 0
        self.sales95_99 = 0
        self.sales00_04 = 0
        self.sales05_09 = 0
        self.sales10_14 = 0
        self.sales15_19 = 0
        self.publishers = []

    @staticmethod
    def platform_decoder(name):
        return Platform(name)
