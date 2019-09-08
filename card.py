# -*- coding: utf-8 -*-
"""
Created on Sun Mar 31 10:17:27 2019

@author: Gerry
"""

from random import shuffle
#import time
class Card:
    def __init__(self):
        self.card = [
            {"name" : "3D",  "value" : 1,  "number": 3,  "image": "D"},
            {"name" : "3C",  "value" : 2,  "number": 3,  "image": "C"},
            {"name" : "3H",  "value" : 3,  "number": 3,  "image": "H"},
            {"name" : "3S",  "value" : 4,  "number": 3,  "image": "S"},

            {"name" : "4D",  "value" : 5,  "number": 4,  "image": "D"},
            {"name" : "4C",  "value" : 6,  "number": 4,  "image": "C"},
            {"name" : "4H",  "value" : 7,  "number": 4,  "image": "H"},
            {"name" : "4S",  "value" : 8,  "number": 4,  "image": "S"},

            {"name" : "5D",  "value" : 9,  "number": 5,  "image": "D"},
            {"name" : "5C",  "value" : 10, "number": 5,  "image": "C"},
            {"name" : "5H",  "value" : 11, "number": 5,  "image": "H"},
            {"name" : "5S",  "value" : 12, "number": 5,  "image": "S"},

            {"name" : "6D",  "value" : 13, "number": 6,  "image": "D"},
            {"name" : "6C",  "value" : 14, "number": 6,  "image": "C"},
            {"name" : "6H",  "value" : 15, "number": 6,  "image": "H"},
            {"name" : "6S",  "value" : 16, "number": 6,  "image": "S"},

            {"name" : "7D",  "value" : 17, "number": 7,  "image": "D"},
            {"name" : "7C",  "value" : 18, "number": 7,  "image": "C"},
            {"name" : "7H",  "value" : 19, "number": 7,  "image": "H"},
            {"name" : "7S",  "value" : 20, "number": 7,  "image": "S"},

            {"name" : "8D",  "value" : 21, "number": 8,  "image": "D"},
            {"name" : "8C",  "value" : 22, "number": 8,  "image": "C"},
            {"name" : "8H",  "value" : 23, "number": 8,  "image": "H"},
            {"name" : "8S",  "value" : 24, "number": 8,  "image": "S"},

            {"name" : "9D",  "value" : 25, "number": 9,  "image": "D"},
            {"name" : "9C",  "value" : 26, "number": 9,  "image": "C"},
            {"name" : "9H",  "value" : 27, "number": 9,  "image": "H"},
            {"name" : "9S",  "value" : 28, "number": 9,  "image": "S"},

            {"name" : "10D", "value" : 29, "number": 10, "image": "D"},
            {"name" : "10C", "value" : 30, "number": 10, "image": "C"},
            {"name" : "10H", "value" : 31, "number": 10, "image": "H"},
            {"name" : "10S", "value" : 32, "number": 10, "image": "S"},

            {"name" : "JD",  "value" : 33, "number": 11,  "image": "D"},
            {"name" : "JC",  "value" : 34, "number": 11,  "image": "C"},
            {"name" : "JH",  "value" : 35, "number": 11,  "image": "H"},
            {"name" : "JS",  "value" : 36, "number": 11,  "image": "S"},

            {"name" : "QD",  "value" : 37, "number": 12,  "image": "D"},
            {"name" : "QC",  "value" : 38, "number": 12,  "image": "C"},
            {"name" : "QH",  "value" : 39, "number": 12,  "image": "H"},
            {"name" : "QS",  "value" : 40, "number": 12,  "image": "S"},

            {"name" : "KD",  "value" : 41, "number": 13,  "image": "D"},
            {"name" : "KC",  "value" : 42, "number": 13,  "image": "C"},
            {"name" : "KH",  "value" : 43, "number": 13,  "image": "H"},
            {"name" : "KS",  "value" : 44, "number": 13,  "image": "S"},

            {"name" : "AD",  "value" : 45, "number": 14,  "image": "D"},
            {"name" : "AC",  "value" : 46, "number": 14,  "image": "C"},
            {"name" : "AH",  "value" : 47, "number": 14,  "image": "H"},
            {"name" : "AS",  "value" : 48, "number": 14,  "image": "S"},

            {"name" : "2D",  "value" : 49, "number": 15,  "image": "D"},
            {"name" : "2C",  "value" : 50, "number": 15,  "image": "C"},
            {"name" : "2H",  "value" : 51, "number": 15,  "image": "H"},
            {"name" : "2S",  "value" : 52, "number": 15,  "image": "S"}]


    def shuffleDeck(self):
        deck = [i+1 for i in range (52)]
        shuffle(deck)
        deck = self.getCardNames(deck)
        return deck


    def getCardNames(self, values):
        names = []
        for i in range (len(values)):
            cardname = list(filter (lambda x : x['value'] == values[i], self.card))[0]['name']
            names.append(cardname)
        return names
    
    
    def getCardValues(self, cardnames):
        values = []
        for i in range (len(cardnames)):
            cardvalue = list(filter (lambda x : x['name'] == cardnames[i], self.card))[0]['value']
            values.append(cardvalue)
        return values
    
    
    def getCardNumbers(self, cardnames):
        numbers = []
        for i in range (len(cardnames)):
            cardnumb = list(filter (lambda x : x['name'] == cardnames[i], self.card))[0]['number']
            numbers.append(cardnumb)
        return numbers
    
    
    def getCardImage(self, cardnames):
        images = []
        for i in range (len(cardnames)):
            cardimg = list(filter (lambda x : x['name'] == cardnames[i], self.card))[0]['image']
            images.append(cardimg)
        return images
    
    
    def sortingCards(self, cardnames):
        values = self.getCardValues(cardnames)
        values.sort()
        cardName = self.getCardNames(values)
        return cardName
        
    
    def sortingPairs(self, pairs):
        tempPair = pairs
        sortedPair = []
        for i in range(len(pairs)):
            scorePair = [self.getPairScore(x) for x in tempPair]
            index = scorePair.index(min(scorePair))
            lowestPair = tempPair[index]
            sortedPair.append(lowestPair)
            tempPair = tempPair[:index] + tempPair[index+1:]
        return sortedPair
    
    
    def isSingle(self, card):
        return len(card) == 1
    
    
    def isPair(self, cardnames):
        if len(cardnames) == 2:
            values = self.getCardNumbers(cardnames)
            if len(set(values)) == 1: return True
        return False


    def isTris(self, cardnames):
        if len(cardnames) == 3:
            values = self.getCardNumbers(cardnames)
            if len(set(values)) == 1: return True
        return False


    def isFours(self, cardnames):
        if len(cardnames) == 4:
            values = self.getCardNumbers(cardnames)
            if len(set(values)) == 1: return True
        return False


    def isStraight(self, cardnames):
        if len(cardnames) == 5:
            sortedCards = self.sortingCards(cardnames)
            cardNumbers = self.getCardNumbers(sortedCards)
            x = cardNumbers
            if (x[0] == 11 and x[1] == 12 and x[2] == 13 and x[3] == 14 and x[4] == 15): return False
            if (x[0] == 3 and x[1] == 4 and x[2] == 5 and x[3] == 6 and x[4] == 15): return True
            if (x[0] == 3 and x[1] == 4 and x[2] == 5 and x[3] == 14 and x[4] == 15): return True
            return (x[0]+1 == x[1] and x[1]+1 == x[2] and x[2]+1 == x[3] and x[3]+1 == x[4])
        return False
        
    
    def isFlush(self, cardnames):
        if len(cardnames) == 5:
            cardImages = self.getCardImage(cardnames)
            if len(set(cardImages)) == 1: return True
        return False
    
    
    def isFullHouse(self, cardnames):
        if len(cardnames) == 5:
            sortedCards = self.sortingCards(cardnames)
            array1 = sortedCards[0:3]
            array2 = sortedCards[3:5]
            if (self.isTris(array1) and self.isPair(array2)): return True
            
            array1 = sortedCards[0:2]
            array2 = sortedCards[2:5]
            if (self.isTris(array2) and self.isPair(array1)): return True
        return False
        
    
    def isFourCards(self, cardnames):
        if len(cardnames) == 5:
            sortedCards = self.sortingCards(cardnames)
            array1 = sortedCards[0:4]
            array2 = sortedCards[1:5]
            if (self.isFours(array1) or self.isFours(array2)): return True
        return False
    
    
    def isStraightFlush(self, cardnames):
        return (self.isStraight(cardnames) and self.isFlush(cardnames))
    
    
    def isCombo(self, cardnames):
        return (self.isStraight(cardnames) or self.isFlush(cardnames) or
                self.isFullHouse(cardnames) or self.isFourCards(cardnames) or 
                self.isStraightFlush(cardnames))
    
    
    def getPair(self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        pair = []
        tris = self.getTris(sortedCards)
        four = self.getFourCards(sortedCards)
        
        # dari 4 cards ambil pair
        if four:
            for i in four:
                for j in range(len(i)-1):
                    for k in range(j, len(i)-1):
                        pair.append((i[j], i[k+1]))
        
        # dari tris ambil pair
        if tris:
            for i in tris:
                for j in range(len(i)-1):
                    for k in range(j, len(i)-1):
                        pair.append((i[j], i[k+1]))
        
        # ambil pair
        for i in range (len(sortedCards) - 1):
            array = tuple(sortedCards[i:i+2])
            if self.isPair(array):
                pair.append(array)
                
        # ilangin duplicate
        pair = list(set(pair))
        for i in range(len(pair)):
            pair[i] = list(pair[i])
            
        if len(pair) > 0:
            return pair
        
        
    def getTris(self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        tris = []
        
        # dari 4 cards ambil tris
        four = self.getFourCards(sortedCards)
        if four:
            for i in four:
                for j in range(len(i)-2):
                    for k in range(j, len(i)-2):
                        for l in range(k, len(i)-2):
                            tris.append((i[j], i[k+1], i[l+2]))
        
        # ambil tris
        for i in range (len(sortedCards) - 2):
            array = tuple(sortedCards[i:i+3])
            if self.isTris(array):
                tris.append(array)
        
        #ilangin duplicate
        tris = list(set(tris))
        for i in range(len(tris)):
            tris[i] = list(tris[i])
            
        if len(tris) > 0:
            return tris
    
    
    def getFourCards (self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        four = []
        for i in range (len(sortedCards) - 3):
            array = sortedCards[i:i+4]
            if self.isFours(array):
                four.append(array)
        if len(four) >0:
            return four
    
    
    def getStraight(self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        straight = []
        if len(sortedCards) >=5:
            for i in range(len(sortedCards)-4):
                for j in range(i, len(sortedCards)-4):
                    for k in range(j, len(sortedCards)-4):
                        for l in range(k, len(sortedCards)-4):
                            for m in range(l, len(sortedCards)-4):
                                temp = (sortedCards[i], sortedCards[j+1], sortedCards[k+2], sortedCards[l+3], sortedCards[m+4])
                                if card.isStraight(list(temp)):
                                    if not(card.isStraightFlush(list(temp))):
                                        straight.append(list(temp))
        return straight
    
    
    def getFlush(self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        flush = []
        if len(sortedCards) >=5:
            for i in range(len(sortedCards)-4):
                for j in range(i, len(sortedCards)-4):
                    for k in range(j, len(sortedCards)-4):
                        for l in range(k, len(sortedCards)-4):
                            for m in range(l, len(sortedCards)-4):
                                temp = (sortedCards[i], sortedCards[j+1], sortedCards[k+2], sortedCards[l+3], sortedCards[m+4])
                                if card.isFlush(list(temp)):
                                    if not(card.isStraightFlush(list(temp))):
                                        flush.append(list(temp))
        return flush
    
    
    def getFullHouse(self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        fullhouse = []
        
#        start = time.time()
        if len(sortedCards) >=5:
            for i in range(len(sortedCards)-4):
                for j in range(i, len(sortedCards)-4):
                    for k in range(j, len(sortedCards)-4):
                        for l in range(k, len(sortedCards)-4):
                            for m in range(l, len(sortedCards)-4):
                                temp = (sortedCards[i], sortedCards[j+1], sortedCards[k+2], sortedCards[l+3], sortedCards[m+4])
                                if card.isFullHouse(list(temp)):
                                    fullhouse.append(list(temp))
#        end = time.time()
#        print(end-start)
        return fullhouse
        
#        start = time.time()
#        fourCards = self.getFourCards(sortedCards)
#        tris = self.getTris(sortedCards)
#        pairs = self.getPair(sortedCards)
#        
#        if len(pairs) > 1:
#            tempPair = pairs
#            sortedPair = []
#            for i in range(len(pairs)):
#                scorePair = [card.getPairScore(x) for x in tempPair]
#                index = scorePair.index(min(scorePair))
#                lowestPair = tempPair[index]
#                sortedPair.append(lowestPair)
#                tempPair = tempPair[:index] + tempPair[index+1:]
#            pairs = sortedPair
#            
#        if fourCards and tris:
#            tris = [x for x in tris if not(any(x[0] in y for y in fourCards))]
#            
#        if tris and pairs:
#            if fourCards:
#                pairs = [x for x in pairs if not(any(x[0] in y for y in tris)) and not(any(x[0] in z for z in fourCards))]
#            else:
#                pairs = [x for x in pairs if not(any(x[0] in y for y in tris))]
#        
#        
#        if tris and pairs:
#            if len(tris) > 0 and len(pairs) > 0:
#                if len(tris) <= len(pairs):
#                    for i in range(len(tris)):
#                        fullhouse.append(tris[i]+pairs[i])
#                else:
#                    for i in range(len(tris)):
#                        fullhouse.append(tris[i]+pairs[0])
#        end = time.time()
#        print(end-start)
#        return fullhouse

    
    def getFourCardsCombo(self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        fourcards = []
        if len(sortedCards) >=5:
            for i in range(len(sortedCards)-4):
                for j in range(i, len(sortedCards)-4):
                    for k in range(j, len(sortedCards)-4):
                        for l in range(k, len(sortedCards)-4):
                            for m in range(l, len(sortedCards)-4):
                                temp = (sortedCards[i], sortedCards[j+1], sortedCards[k+2], sortedCards[l+3], sortedCards[m+4])
                                if card.isFourCards(list(temp)):
                                    fourcards.append(list(temp))
        return fourcards
    
    
    def getStraightFlush(self, cardnames):
        sortedCards = self.sortingCards(cardnames)
        straightflush = []
        if len(sortedCards) >=5:
            for i in range(len(sortedCards)-4):
                for j in range(i, len(sortedCards)-4):
                    for k in range(j, len(sortedCards)-4):
                        for l in range(k, len(sortedCards)-4):
                            for m in range(l, len(sortedCards)-4):
                                temp = (sortedCards[i], sortedCards[j+1], sortedCards[k+2], sortedCards[l+3], sortedCards[m+4])
                                if card.isStraightFlush(list(temp)):
                                    straightflush.append(list(temp))
        return straightflush
    
    
    def getCombo(self, cardnames):
        comboLists= []
        if len(self.getStraight(cardnames)) > 0:
            [comboLists.append(x) for x in self.getStraight(cardnames)]
        
        if len(self.getFlush(cardnames)) > 0:
            [comboLists.append(x) for x in self.getFlush(cardnames)]
        
        if len(self.getFullHouse(cardnames)) > 0:
            [comboLists.append(x) for x in self.getFullHouse(cardnames)]
            
        if len(self.getFourCardsCombo(cardnames)) > 0:
            [comboLists.append(x) for x in self.getFourCardsCombo(cardnames)]
            
        if len(self.getStraightFlush(cardnames)) > 0:
            [comboLists.append(x) for x in self.getStraightFlush(cardnames)]
            
        return comboLists
    
    
    def getPairScore(self, cardnames):
        return max(self.getCardValues(cardnames))
    
    
    def getComboScore(self, cardnames):
        if(self.isStraightFlush(cardnames)):
            return (5000 + max(self.getCardValues(cardnames)))
        
        if(self.isFourCards(cardnames)):
            return (4000 + max(self.getCardValues(self.getFourCards(cardnames)[0])))
        
        if(self.isFullHouse(cardnames)):
            return (3000 + max(self.getCardValues(self.getTris(cardnames)[0])))
    
        if(self.isFlush(cardnames)):
            if(self.getCardImage(cardnames)[0] == "D"): return (2000 + max(self.getCardValues(cardnames)))
            if(self.getCardImage(cardnames)[0] == "C"): return (2250 + max(self.getCardValues(cardnames)))
            if(self.getCardImage(cardnames)[0] == "H"): return (2500 + max(self.getCardValues(cardnames)))
            if(self.getCardImage(cardnames)[0] == "S"): return (2750 + max(self.getCardValues(cardnames)))
    
        if(self.isStraight(cardnames)):
            if('2S' in cardnames or '2H' in cardnames or '2C' in cardnames or '2D' in cardnames):
                if('AS' in cardnames or 'AH' in cardnames or 'AC' in cardnames or 'AD' in cardnames):
                    sortedCards = self.sortingCards(cardnames)
                    removeTwo = sortedCards[:-2]
                    return (1000 + max(self.getCardValues(removeTwo)))
                else:
                    sortedCards = self.sortingCards(cardnames)
                    removeOne = sortedCards[:-1]
                    return (1000 + max(self.getCardValues(removeOne)))
                        
            return (1000 + max(self.getCardValues(cardnames)))
    
card = Card()
#card.shuffleDeck()
#card.getCardNames([1,2,4,5])
#card.getCardValues(['3D', '2D'])
#card.sortingCards(['3D', '2D', '10S'])
#card.sortingPairs([['QH','QS'],['8C','8H']])
#card.getCardNumbers(['3D', '2D', '10S'])
#card.getCardImage(['3D', '2D', '10S'])
#card.isSingle(['3D', '3S'])
#card.isPair(['3D', '3S'])
#card.isTris(['3D', '3S', '3H'])
#card.isFours(['3D', '3S', '3H', '3C'])
#card.isStraight(['JS','QD','KS','AH'])
#card.isFlush(['JS','QS','KS','AS', '3S'])
#card.isFullHouse(['JS','JH','AC','AS', 'AH'])
#card.isFourCards(['JS','JD','JC','AS', 'AH'])
#card.isStraightFlush(['10S','JS','QS','KS','AS'])
#card.isCombo(['10S','JS','QS','KS'])
#card.getPair(['4H', '4D', '4S', '6C', '6S', '7D', '10C', '10S', 'QC', 'KD', 'KC', '2D', '2C', '5D', '5C', '5H', '5S'])
#card.getTris(['4H', '4D', '4S', '6C', '6S', '7D', '10C', '10S', 'QC', 'KD', 'KC', '2D', '2C', '5D', '5C', '5H', '5S'])
#card.getFourCards(['4H', '4D', '4S', '6C', '6S', '7D', '10C', '10S', 'QC', 'KD', 'KC', '2D', '2C', '5D', '5H', '5S'])



#card.getStraight(['4H', '5D', '8S', '6C', '6S', '7D', 'KD', 'KC', '2D', '2C','10S','JS','QS','KS','AS'])
#card.getFlush(['4H', '5D', '6C', '7D', '10C', '10S', 'QC', 'KD', 'KC', '2D', '2C', '9S','JS','QS','KS','AS'])
#card.getFullHouse(['2D','2C','2H','4H', '5D', '8S', '6C', '6S','6H', '7D', '10C', '10S', 'QC', 'KD', 'KC', '3C', '10D', '10H'])
#card.getFullHouse(['3D','3C','3H','3S','4D','4H','5D','5C','5H','7H','7S','8C','8S','9H','9S','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C'])
#card.getFullHouse([d['name'] for d in card.card])
#card.getFourCardsCombo(['QC', 'KD', 'KC', '2D', '2C', '5D', '5C', '5H', '5S'])
#card.getStraightFlush(['2D', '2C', '5D', '5C', '5H', '9S','10S','JS','QS','KS','AS', 'KC'])


#card.getCombo(['10S','JS','QS','KS','AC', '9S'])


#card.getPairScore(['10S','KC'])
#card.getComboScore(['10S','JS','QS','KS','AS'])
#card.getComboScore(['10H','10D','10C','10S', 'KC'])
#card.getComboScore(['7H','7D','7C','KS', 'KC'])
#card.getComboScore(['9H','9D','9C','2S', '2D'])
#card.getComboScore(['10S','JH','QS','KS','AS'])
#card.getComboScore(['10S','4S','QS','KS','AS'])
#card.getComboScore(['2S','3D','4S','5S','AS'])