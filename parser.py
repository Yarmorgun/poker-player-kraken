__author__ = 'Artem Sliusar'


class Parser:

    def __init__(self):
        pass

    def parse_preflop(self, file_name):
        with open(file_name) as fo:
            lines = fo.readlines()

        probabilities = {}
        for line in lines:
            line_data = line.split("\t")
            hand = line_data[0]
            percentages = [float(percentage.replace("%", "").replace("\n", "")) for percentage in line_data[1:]]
            probabilities[hand] = percentages
        return probabilities