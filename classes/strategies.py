from classes.portfolio import Portfolio


class Strategy():
    def __init__(self):
        self.type = ""

    def to_json(self):
        return {}

    @staticmethod
    def from_json(json):
        if json['type'] == "ALLIN":
            return StrategyALLIN(assets=json['assets'])
        elif json['type'] == "DCA":
            return StrategyDCA(assets=json['assets'], freq=json['freq'])
        else:
            return Strategy()



class StrategyALLIN(Strategy):
    type = "ALLIN"

    def __init__(self, assets=""):
        self.assets = assets

    def to_json(self):
        return {
            "type": self.type,
            "assets": self.assets,
        }
    
    # def apply(self, portfolio: Portfolio):





class StrategyDCA(Strategy):
    type = "DCA"

    def __init__(self, assets="", freq=""):
        self.assets = assets
        self.freq = freq

    def to_json(self):
        return {
            "type": self.type,
            "assets": self.assets,
            "freq": self.freq
        }