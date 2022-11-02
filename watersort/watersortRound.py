import json

class WatersortRound:
    def __init__(self, round_name):
        round_file = open('watersort/rounds/{}.json'.format(round_name), 'r')
        jsonObj = json.loads(round_file.read())
        self.num_of_glasses = jsonObj['num_of_glasses']
        self.board = jsonObj['board']
    
    def getBoard(self):
        return self.board