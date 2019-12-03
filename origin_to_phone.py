PATH_BASE = 'C:\\Users\\Toccato.000\\Dropbox\\Toccato\\Pythons\\hackathon\\database\\base.txt'
PATH_AZIMUT = 'C:\\Users\\Toccato.000\\Dropbox\\Toccato\\Pythons\\hackathon\\database\\azimut.txt'


class IdentifyOriginPhone:
    DATA_BASE_ORIGIN: str
    AZIMUT_ORIGIN: str

    def __init__(self, code):
        self.code = code
        self.DB: dict = {}
        self.AZIMUT: dict = {}

    def __repr__(self):
        return self.run()

    def run(self):
        self.__open_azimut()
        self.__open_data_base()
        self.find_code()
        self.find_azimut()
        self.validate_code()
        return self.DB[self.code] #+ ' [' + self.AZIMUT[self.code] + ']'

    def validate_code(self):
        self.code = ''.join(map(str, list(map(int, ''.join(c for c in self.code.strip() if c.isdigit())))[2:4]))

    def __open_data_base(self):
        with open(PATH_BASE, 'r') as file:
            self.DATA_BASE_ORIGIN = file.read()

    def __open_azimut(self):
        with open(PATH_AZIMUT, 'r') as file:
            self.AZIMUT_ORIGIN = file.read()

    def find_code(self):
        list_code = []
        n = self.DATA_BASE_ORIGIN.split('\n')
        for i in n:
            list_code.append(i.split('\n')[0])

        for i in list_code:
            A = i.split('-')[0].strip()
            B = i.split('-')[1].strip()
            self.DB[A] = B

    def find_azimut(self):
        for i in self.AZIMUT_ORIGIN.split('\n'):
            A = i.split('=')[0].strip()
            B = i.split('=')[1].strip()
            self.AZIMUT[A] = B

