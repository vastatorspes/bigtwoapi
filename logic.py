# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 07:42:51 2019

@author: Gerry
"""

from card import Card

card = Card()

class Logic:
    
    # card1 = hand
    # card2 = field
    
    def higherSingle(self, card1, card2):
        return (card.getCardValues(card1)[0] - card.getCardValues(card2)[0]) > 0
    
    
    def higherPair(self, cards1, cards2):
        return (card.getPairScore(cards1) - card.getPairScore(cards2)) > 0
    
    
    def higherCombo(self, cards1, cards2):
        return (card.getComboScore(cards1) - card.getComboScore(cards2)) > 0
    
    
    def legalCard(self, cards):
        return (card.isSingle(cards) or card.isPair(cards) or card.isCombo(cards))
    
    
    def legalFirstMove(self, cards):
        if (self.legalCard(cards)):
            hand = card.sortingCards(cards)
            return hand[0] == '3D'
        return False
    
    def legalMove(self, cards, field):
        if (self.legalCard(cards) and self.legalCard(field)):
            if (card.isSingle(cards) and card.isSingle(field)):
                return self.higherSingle(cards, field)
            
            if (card.isPair(cards) and card.isPair(field)):
                return self.higherPair(cards, field)
    
            if (card.isCombo(cards) and card.isCombo(field)):
                return self.higherCombo(cards, field)


    def possibleMoves(self, hand, field, control, turn):
        moveLists = []
        
        if control == True:
            [moveLists.append([x]) for x in hand]
            
            pairLists = card.getPair(hand)
            if pairLists:
                [moveLists.append(x) for x in pairLists]
            
            comboLists = card.getCombo(hand)
            if comboLists:
                [moveLists.append(x) for x in comboLists]
                
            if turn == 0:
                moveLists = [x for x in moveLists if '3D' in x]
                
            return moveLists
        
        
        if len(field) == 1:
            for _ in hand:
                single = [_]
                if self.higherSingle(single, field):
                    moveLists.append(single)
            
        if len(field) == 2:
            pairLists = card.getPair(hand)
            if pairLists:
                if len(pairLists) > 0:
                    for _ in pairLists:
                        if self.higherPair(_, field):
                            moveLists.append(_)
        
        if len(field) == 5:
            comboLists = card.getCombo(hand)
            if comboLists:
                if len(comboLists) > 0:
                    for _ in comboLists:
                        if self.higherCombo(_,field):
                            moveLists.append(_)
            
        moveLists.append([])
        return moveLists

logic = Logic()
logic.higherSingle(['3D'], ['5D'])
#logic.higherPair(['3D', '3H'], ['2D', '2S'])
#logic.higherCombo(['2D', '2S', '2H', '2C', '5H'], ['3D', '3H', '3S', '4H', '4S'])
#logic.legalFirstMove(['3D', '3S', '4S', '4H', '4D'])

#logic.legalMove(['3D'],['3S'])
#logic.legalMove(['2D', '2H'],['3D', '3S'])
#logic.legalMove(['3D', '4D', '5D', '6D', '7D'],['2D', '2S', '2H', '2C', '5H'])

#card = Card()
#hand = card.shuffleDeck()[0:13]
#hand = card.sortingCards(hand)

#hand = ['3D', '4D', '4S', '6C', '6S', '7D', '10C', '10S', 'QC', 'KD', 'KC', '2D', '2C']
##hand = ['3D','4S']
#field = ['4D', '4H']
#logic.possibleMoves(hand, field, True, 1)










