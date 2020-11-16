class Game:
    def __init__(self, _id, rank, name, platform, year, genre, publisher, naSales, euSales, jpSales, otherSales, globalSales, __v):
        self._id = _id
        self.rank = rank
        self.name = name
        self.platform = platform
        self.year = year
        self.genre = genre
        self.publisher = publisher
        self.naSales = naSales
        self.euSales = euSales
        self.jpSales = jpSales
        self.otherSales = otherSales
        self.globalSales = globalSales
        self.__v = __v

    @staticmethod
    def game_decoder(obj):
        return Game(obj['_id'], obj['rank'], obj['name'], obj['platform'], obj['year'] , obj['genre'], obj['publisher'], obj['naSales'], obj['euSales'], obj['jpSales'], obj['otherSales'], obj['globalSales'], obj['__v'])

