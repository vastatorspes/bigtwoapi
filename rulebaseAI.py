# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:57:58 2019

@author: Gerry
"""

from logic import Logic
from card import Card
import time

logic = Logic()
card = Card()

# check kemungkinan kartu yang bisa dikeluarin lawan
def enemyProbably(hand, field_history):
    allcards = [d['name'] for d in card.card]
    unseen = list(set(allcards).difference(set(hand).union(set(field_history))))
    enemyLists = []
    # Single
    [enemyLists.append([x]) for x in unseen]
    # Pair
    pairLists = card.getPair(unseen)
    if pairLists:
        [enemyLists.append(x) for x in pairLists]

    # Combo (cuma diambil dari 15 kartu tertinggi kalo masih ada lebih dari 15)
    if len(unseen) > 15:
        tempUnseen = card.sortingCards(unseen)
        tempUnseen = tempUnseen[-15:]
        comboLists = card.getCombo(tempUnseen)
    else:
        comboLists = card.getCombo(unseen)
    if comboLists:
        [enemyLists.append(x) for x in comboLists]
    return enemyLists

#hand = ['3D','4D','5H','6H','7C','8D','8H','8S','9C','JD','JH','KD','AS']
#field_history = ['3H','3S','4H','5D','5C','5S','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KC','KH','KS','AD','AC','AH','2C']
#field_history = []
#enemyLists = enemyProbably(hand, field_history)


def findMaxValue(hand):
    value = []
    for cards in hand:
        value.append(max(card.getCardValues(cards)))
    return max(value)

#findMaxValue([['KD', 'KH'], ['AH']])


# milih kombo yang tepat
def comboSelection(hand):
    tempCombo = card.getCombo(hand)
    comboCombination = []
    # Find other combo
    for combo in tempCombo:
        otherCombo = card.getCombo(list(set(hand).difference(set(combo))))
        # Find double combo
        if otherCombo:
            for oCombo in otherCombo:
                comboCombination.append([combo,oCombo])

    if len(comboCombination) == 0:
        comboCombination = tempCombo

    handLeft = []
    selectedCombo = []
    if len(comboCombination) > 0:
        for combo in comboCombination:
            # ini kalo combo nya ada 2 di tangan
            if len(combo) == 2:
                cardLeft = [x for x in hand if x not in combo[0] and x not in combo[1]]     # sisa kartu setelah dikurangin combo
                
                trisCard = card.getTris(cardLeft)                                           # cari sisa kartu yang tris
                # kalo belom ada selected combo (iterasi pertama)
                if len(selectedCombo) == 0:
                    if trisCard:
                        usedCard = []
                        for tris in trisCard:
                            handLeft.append(tris)                               # kalo ada tris, simpen di handLeft
                            for _ in tris:
                                usedCard.append(_)                              # kalo tris ada, trisnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]

                    pairCard = card.getPair(cardLeft)              # cari pair card dari sisa kartu setelah cek tris
                    if pairCard:
                        usedCard = []
                        for pair in pairCard:
                            handLeft.append(pair)                               # kalo ada pair, simpen di handleft
                            for _ in pair:
                                usedCard.append(_)                              # kalo pair ada, pairnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]


                    for _ in cardLeft:
                        handLeft.append([_])

                    selectedCombo = combo


                # kalo udah ada selected combo nya
                elif len(selectedCombo) > 0:
                    tempHandLeft = []
                    if trisCard:
                        usedCard = []
                        for tris in trisCard:
                            tempHandLeft.append(tris)                           # kalo ada tris, simpen di tempHandLeft
                            for _ in tris:
                                usedCard.append(_)                              # kalo tris ada, trisnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]

                    pairCard = card.getPair([x for x in cardLeft])              # cari pair card dari sisa kartu setelah cek tris
                    if pairCard:
                        usedCard = []
                        for pair in pairCard:
                            tempHandLeft.append(pair)                           # kalo ada pair, simpen di handleft
                            for _ in pair:
                                usedCard.append(_)                              # kalo pair ada, pairnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]

                    for _ in cardLeft:
                        tempHandLeft.append([_])

                    # bandingin sisa kartu dari kombinasi combo sekarang sama sebelumnya
                    tempHandLeftScore = 0 if tempHandLeft == [] else findMaxValue(tempHandLeft)
                    handLeftScore = 0 if handLeft == [] else findMaxValue(handLeft)     
                    
                    selectedComboScore = [card.getComboScore(selectedCombo[0]), card.getComboScore(selectedCombo[1])]
                    tempComboScore = [card.getComboScore(combo[0]), card.getComboScore(combo[1])]
                    
                    if handLeftScore < tempHandLeftScore:
#                        print('combo ini \n', selectedCombo, '\n diganti ini \n', combo)
                        handLeft = tempHandLeft
                        selectedCombo = combo

                    elif handLeftScore == tempHandLeftScore:
                        if len(handLeft) > len(tempHandLeft):
#                            print(len(handLeft), len(tempHandLeft))
#                            print('ksesini')
#                            print('combo ini \n', selectedCombo, '\n diganti ini \n', combo)
                            handLeft = tempHandLeft
                            selectedCombo = combo
                        
                        elif len(handLeft) == len(tempHandLeft):
                            if max(selectedComboScore)+250 < max(tempComboScore):                   # kalo beda combonya
                                handLeft = tempHandLeft
                                selectedCombo = combo

            
            # kalo combonya cuma 1 di tangan
            elif len(combo) == 5:
                cardLeft = [x for x in hand if x not in combo]
                fourCard = card.getFourCards(cardLeft)
                
                # kalo belom ada selected combo (iterasi pertama)
                if len(selectedCombo) == 0:
                    if fourCard:
                        usedCard = []
                        for four in fourCard:
                            handLeft.append(four)                               # kalo ada four cards, simpen di handLeft
                            for _ in four:
                                usedCard.append(_)                              # kalo four cards ada, trisnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]
                    
                    trisCard = card.getTris(cardLeft)                           # cari sisa kartu yang tris
                    if trisCard:
                        usedCard = []
                        for tris in trisCard:
                            handLeft.append(tris)                               # kalo ada tris, simpen di handLeft
                            for _ in tris:
                                usedCard.append(_)                              # kalo tris ada, trisnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]

                    pairCard = card.getPair(cardLeft)              # cari pair card dari sisa kartu setelah cek tris
                    if pairCard:
                        usedCard = []
                        for pair in pairCard:
                            handLeft.append(pair)                               # kalo ada pair, simpen di handleft
                            for _ in pair:
                                usedCard.append(_)                              # kalo pair ada, pairnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]

                    for _ in cardLeft:
                        handLeft.append([_])

                    selectedCombo = [combo]
                
                elif len(selectedCombo) > 0:
                    tempHandLeft = []
                    if fourCard:
                        usedCard = []
                        for four in fourCard:
                            tempHandLeft.append(four)                               # kalo ada four cards, simpen di handLeft
                            for _ in four:
                                usedCard.append(_)                              # kalo four cards ada, trisnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]
                    
                    trisCard = card.getTris(cardLeft)                           # cari sisa kartu yang tris
                    if trisCard:
                        usedCard = []
                        for tris in trisCard:
                            tempHandLeft.append(tris)                           # kalo ada tris, simpen di tempHandLeft
                            for _ in tris:
                                usedCard.append(_)                              # kalo tris ada, trisnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]

                    pairCard = card.getPair([x for x in cardLeft])              # cari pair card dari sisa kartu setelah cek tris
                    if pairCard:
                        usedCard = []
                        for pair in pairCard:
                            tempHandLeft.append(pair)                           # kalo ada pair, simpen di handleft
                            for _ in pair:
                                usedCard.append(_)                              # kalo pair ada, pairnya simpen di used card

                        cardLeft = [x for x in cardLeft if x not in usedCard]

                    for _ in cardLeft:
                        tempHandLeft.append([_])
                        
                    # bandingin sisa kartu dari kombinasi combo sekarang sama sebelumnya
                    tempHandLeftScore = 0 if tempHandLeft == [] else findMaxValue(tempHandLeft)
                    handLeftScore = 0 if handLeft == [] else findMaxValue(handLeft)     
                        
                    selectedComboScore = card.getComboScore(selectedCombo[0])
                    tempComboScore = card.getComboScore(combo)
                    
                    if handLeftScore < tempHandLeftScore:
                        handLeft = tempHandLeft
                        selectedCombo = [combo]

                    elif handLeftScore == tempHandLeftScore:
                        if len(handLeft) > len(tempHandLeft):
#                            print(len(handLeft), len(tempHandLeft))
#                            print('ksesini')
#                            print('combo ini \n', selectedCombo, '\n diganti ini \n', combo)
                            handLeft = tempHandLeft
                            selectedCombo = [combo]
                        
                        elif len(handLeft) == len(tempHandLeft):
                            if selectedComboScore+250 < tempComboScore:                   # kalo beda combonya
                                handLeft = tempHandLeft
                                selectedCombo = [combo]
                                
                            
#    print(handLeft)
    return selectedCombo

#hand = ['3H','4D','4H','4S','5S','6D','7D','8D','8H','10H', 'QH']
#comboSelection(hand)

#hand = ['4H','5C','5S','6D','7H','8C','8S','9D','10D','JD','JC','QS','KD']
#hand = ['4H','5C','KS','6D','7H','8C','8S','9D','10D','JD','KC','QS','KD', 'AS','AD']
#hand = ['3H','4H','4D','4S','5D','5S','5H','6D','6H','7D','7H','8H','2H']                   # tes 2 combo 1 straight 1 flush
#hand = ['6D','6C','6S','KD','KH','AD','AC','AH']
#hand = ['6D','6C','6S','KD','KH','AD','AC','AH','2C']
#hand = ['5D','5S','5H','7D','7H','7C','7S']
#comboSelection(hand)

#hand = ['3S','4C','5H','6D','6C','6S','8D','10D','KD','KH','AD','AC','AH']
#comboSelection(hand)

#hand = ['5H','5C','5S','6D','7H','8C','8S']
#comboSelection(hand)

#hand = ['3D','3S','3H','5S','5D','JC','JS','2H']
#comboSelection(hand)

#hand = ['4H', '5C', '6D', '7H', '8C', '8S', '9D', '10D', 'JD', 'QS']
#comboSelection(hand)

#klasifikasi kelas
def cardClassifier(hand, field_history, min_hand):
    probCards = enemyProbably(hand, field_history)
    probSingle = []
    probPair = []
    probCombo = []
    classASP = []
    classA = []
    classB = []
    classC = []
    classD = []
    for i in probCards:
        if len(i) == 1:
            probSingle.append(i[0])
        if len(i) == 2:
            probPair.append(i)
        if len(i) == 5:
            probCombo.append(i)

    # find max and min single
    probSingle = card.sortingCards(probSingle)
    maxSingle = max(card.getCardValues(probSingle))
    minSingle = min(card.getCardValues(probSingle))
    divSingleIndex = int(len(probSingle) * 0.8)
    divSingle = card.getCardValues(probSingle)[divSingleIndex]

    # find max and min pair
    if len(probPair) > 0:
        sortedPair = card.sortingPairs(probPair)
        pairScore = [card.getPairScore(x) for x in sortedPair]
        maxPair = max(pairScore)
        minPair = min(pairScore)
        divPairIndex = int(len(sortedPair) * 0.7)
        divPair = card.getPairScore(sortedPair[divPairIndex])

    # find max and min combo
    if len(probCombo) > 0:
        allcards = [d['name'] for d in card.card]
        unseen = list(set(allcards).difference(set(hand).union(set(field_history))))
        if len(unseen) > 15:
            maxCombo = 3034
            minCombo = 1029
            divCombo = 2500
        else:
            tempCombo = probCombo
            sortedCombo = []
            for i in range(len(probCombo)):
                scoreCombo = [card.getComboScore(x) for x in tempCombo]
                index = scoreCombo.index(min(scoreCombo))
                lowestCombo = tempCombo[index]
                sortedCombo.append(lowestCombo)
                tempCombo = tempCombo[:index] + tempCombo[index+1:]

            comboScore = [card.getComboScore(x) for x in sortedCombo]
            maxCombo = max(comboScore)
            minCombo = min(comboScore)
            divComboIndex = int(len(sortedCombo) * 0.7)
            divCombo = card.getComboScore(sortedCombo[divComboIndex])

    # ASP = A single or A pair
    # klasifikasi single
    for i in hand:
        value = card.getCardValues([i])[0]
        # find classA single
        if value > maxSingle:
            classA.append([i])
            classASP.append(i)
        # find classB single
        if value > divSingle and value < maxSingle:
            classB.append([i])
        # find classC single
        if value <= divSingle and value > minSingle:
            classC.append([i])
        #find classD single
        if value < minSingle:
            classD.append([i])


    # klasifikasi pair
    pairs = []
    pairLists = card.getPair(hand)
    if pairLists:
        [pairs.append(x) for x in pairLists]
        pairs = card.sortingPairs(pairs)

    if len(probPair) > 0:
        for i in pairs:
            value = card.getPairScore(i)
            # find classA pair
            if value > maxPair:
                classA.append(i)
                classASP.append(i[0])
                classASP.append(i[1])
            # find classB pair
            if value > divPair and value < maxPair:
                classB.append(i)
            # find classC pair
            if value <= divPair and value > minPair:
                classC.append(i)
            # find classD pair
            if value < minPair:
                classD.append(i)
    elif len(probPair) == 0:
        for i in pairs:
            classA.append(i)
            classASP.append(i[0])
            classASP.append(i[1])


    # klasifikasi combo
    classASP = list(set(classASP))
    combos = []
    
    comboHand = list(set(hand) - set(classASP)) if min_hand >= 5 else hand

    if len(hand) > 6:
        tempComboLists1 = comboSelection(comboHand)
        tempComboLists2 = comboSelection(hand)
        comboLists = tempComboLists2 if len(tempComboLists2) > len(tempComboLists1) else tempComboLists1
    else:
        comboLists = comboSelection(hand)

    if comboLists:
        [combos.append(x) for x in comboLists]

    if len(probCombo) > 0:
        for i in combos:
            value = card.getComboScore(i)
            # find classA combo
            if value > maxCombo:
                classA.append(i)
            # find classB combo
            if value > divCombo and value < maxCombo:
                classB.append(i)
            # find classC combo
            if value <= divCombo and value > minCombo:
                classC.append(i)
            # find classD pair
            if value < minCombo:
                classD.append(i)
    elif len(probCombo) == 0:
        for i in combos:
            classA.append(i)

    return {'classA':classA,
            'classB':classB,
            'classC':classC,
            'classD':classD}

#hand = ['4D', '4H', '4S', '10H', 'JH', 'QC', 'KS', 'AS', '2H', '2S']
#field_history = ['3D', '5C', '6H', '7C', '8S', '9C', 'AD', 'AC', '6D', '6C', 'JD', 'JC', 'QD', 'QH', 'KC', 'KH', '5H', '5S', '9D', '9H', '3C', '3S', '5D', 'JS', 'AH', '2C', '7S']
#min_hand = 2
#cardClassifier(hand, field_history, min_hand)

#hand = ['4D', '4C', '6H', '7D', '7S', '8C', '9C', '10C', 'QC', 'AD', '2D', '2C', '2S']
#field_history = ['3D', '4H', '5C', '6S', '7C', '3C', '3H', '3S', '5D', '5S']
#min_hand = 8
#cardClassifier(hand, field_history, min_hand)

#hand = ['6D','JD','JH','JS','2D','2S']
#field_history = ['4C', 'KD', '3H', '3D', '2C', 'AD', '8D', '5H', '10S', 'QS', '7D', 'AH', '5S', '8C', 'AS', '7C', 'KS', 'QD', '6H', '5C', '8H', 'QC', '3S', 'JC', 'KC', '4D', '7H', '6C', '6S', '4H', 'AC', '9S']
#cardClassifier(hand, field_history)

# Two cards left
def twoCard(hand, classA, enemy1, enemy2, enemy3):
    # Check pair
    handPair = card.getPair(hand)
    if handPair:
        return handPair[0]
    elif classA or (1 in [enemy1, enemy2, enemy3]):
        return [hand[1]]
    return [hand[0]]

# Three cards left
def threeCard(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3):
    # Check pair
    handPair = card.getPair(hand)
    if handPair:
        filterSingle = [[x] for x in hand if not(any(x in Pair for Pair in handPair))]
        if classA:
            # 1 pair in class A
            if handPair[0] in classA:
                return handPair[0]     
            # single cards in class A
            elif filterSingle[0] in classA:
                return filterSingle[0]
        # If enemy single, play pair
        elif 1 in [enemy1, enemy2, enemy3]:
            return handPair[0]
        # If enemy 2 cards, play single
        elif 2 in [enemy1, enemy2, enemy3]:
            return filterSingle[0]
        else:
            if classD: return classD[0]
            if classC: return classC[0]
            if classB: return classB[0]
            if classA: return classA[0] 
    # All single cards
    else:
        if 1 in [enemy1, enemy2, enemy3]:
            if classA:
                if hand[2] in classA:
                    return [hand[1]]
                return [hand[2]]
            return [hand[2]]
        elif classA:
            if hand[2] in classA:
                return [hand[1]]
            return [hand[0]]
        return [hand[0]]

# Four cards left
def fourCard(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3):
    # Check pair
    handPair = card.getPair(hand)
    if handPair:
        # Double pairs
        if len(handPair) == 2:
            sortedPair = card.sortingPairs(handPair)
            if classA:
                if sortedPair[1] in classA:
                    return sortedPair[1]
                return sortedPair[0]
            elif 2 in [enemy1, enemy2, enemy3]:
                return sortedPair[1]
            return sortedPair[0]
        # One pair
        elif len(handPair) == 1:
            filterSingle = [[x] for x in hand if not(any(x in Pair for Pair in handPair))]
            if classA:
                # single cards in class A
                if filterSingle[1] in classA:
                    return filterSingle[0]
                # If enemy single, play pair
                elif 1 in [enemy1, enemy2, enemy3]:
                    return handPair[0]
                # If enemy 2 cards, play single
                elif 2 in [enemy1, enemy2, enemy3]:
                    return filterSingle[0]
                return filterSingle[1]
            else:
                if classD: return classD[0]
                if classC: return classC[0]
                if classB: return classB[0]
                if classA: return classA[0]
    # All single cards
    else:
        if classA:
            return [hand[1]]
        elif 1 in [enemy1, enemy2, enemy3]:
            return [hand[3]]
        return [hand[0]]

# Cards left <= 4
def underFour(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3):
    if len(hand) == 2:
        return twoCard(hand, classA, enemy1, enemy2, enemy3)
    elif len(hand) == 3:
        return threeCard(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3)
    elif len(hand) == 4:
        return fourCard(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3)
    return [hand[0]]

# Cards left > 4
def overFour(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3):
    comboCard = findComboInClass(classD) + findComboInClass(classC) + findComboInClass(classB) + findComboInClass(classA)
    pairCard = findPairInClass(classD) + findPairInClass(classC) + findPairInClass(classB) + findPairInClass(classA)
    singleCard = findSingleInClass(classD) + findSingleInClass(classC) + findSingleInClass(classB) + findSingleInClass(classA)
    if 1 in [enemy1, enemy2, enemy3]:
        if comboCard:
            return comboCard[0]
        elif pairCard:
            return pairCard[0]
        else:
            if classD: return classD[0]
            if classC: return classC[0]
            if classB: return classB[0]
            if classA: return classA[0]
    else:
        if (not comboCard) and (len(pairCard) > len(singleCard)):
            return pairCard[0]
        else:
            if classD: return classD[0]
            if classC: return classC[0]
            if classB: return classB[0]
            if classA: return classA[0]
                
def checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, classA, classB, classC, classD, selected_card):
    # Holdback Single
    if len(field) == 1:
        if len(hand) <= 2:
            return False
        if min(enemy1, enemy2, enemy3) <= 2 and selected_card == [hand[-1]]:
            return False
        if len(classA) < (len(classB) + len(classC) + len(classD)):
            if selected_card == [hand[-1]]:
                return True
        if min([len(hand), enemy1, enemy2, enemy3]) > 6:
            if selected_card == [hand[-1]]:
                return True
    # Holdback Pair
    if len(field) == 2:
        if len(hand) <= 3:
            return False
        if min([len(hand), enemy1, enemy2, enemy3]) > 2:
            if card.getPairScore(selected_card) >= 50:
                return True
    # Holdback Combo
    if len(field) == 5:
        if len(hand) == 5:
            return False
        if min([len(hand), enemy1, enemy2, enemy3]) > 6 and turn <= 4:
            # Check any enemy pass
            if 1 in pass_turn.values():
                # Check any combo from card left
                cardLeft = list(set(hand).difference(set(selected_card)))
                tempCombo = card.getCombo(cardLeft)
                if len(tempCombo) > 0 and (selected_card in classA or selected_card in classB):
                    return True
    return False

## Test Holdback Single
#hand = ['3D','4D','5H','6H','7C','8D','8H','8S','9C','JD','JH','KD','AS']
#field = ['4H']
#enemy1 = 8
#enemy2 = 7
#enemy3 = 9
#turn = 4
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#cardClass = {"classA" : [['KD'],['AH']],
#                  "classB" : [['JD','JH'],['AD','AS']],
#                  "classC" : [[]],
#                  "classD" : [[]]}
#selected_card = ['AS']
#checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, cardClass, selected_card)

## Test holdback single 2
#hand = ['5D','6S','7D','2S']
#field = ['JC']
#enemy1 = 7
#enemy2 = 3
#enemy3 = 8
#turn = 28
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#classA = [['2S']]
#classB = []
#classC = [['5D'], ['6S'], ['7D']]
#classD = []
#selected_card = ['2S']
#checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, classA, classB, classC, classD, selected_card)

## Test Holdback Pair
#hand = ['3D','4D','5H','6H','7C','8D','8H','8S','9C','JD','JH','AD','AS']
#field = ['4H','4S']
#enemy1 = 3
#enemy2 = 3
#enemy3 = 4
#turn = 4
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#cardClass = {"classA" : [],
#                  "classB" : [['JD','JH'],['AD','AS']],
#                  "classC" : [[]],
#                  "classD" : [[]]}
#selected_card = ['AD', 'AS']
#checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, cardClass, selected_card)
#
#
## Test Holdback Combo
#hand = ['3D','4D','5H','6H','7C','8D','8H','8S','9C','JD','JH','AD','AS']
#field = ['4C','4H','4S','6D','6C']
#enemy1 = 8
#enemy2 = 13
#enemy3 = 8
#turn = 4
#pass_turn = {0:0, 1:0, 2:1, 3:0}
#cardClass = {"classA" : [['AD','AS']],
#                  "classB" : [['JD','JH'],['8D','8H','8S','JD','JH']],
#                  "classC" : [[]],
#                  "classD" : [['3D','4D','5H','6H','7C']]}
#selected_card = ['8D','8H','8S','JD','JH']
#checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, cardClass, selected_card)

def findSingleInClass(className):
    return [x for x in className if len(x) == 1]
def findPairInClass(className):
    return [x for x in className if len(x) == 2]
def findComboInClass(className):
    return [x for x in className if len(x) == 5]

def splitTrisToSingleAndPair(className):
    splitedPair = []
    splitedSingle = []
    pairCards = []
    trisCards = []
    pairs = findPairInClass(className)
    if pairs:
        for pair in pairs:
            pairCards.append(pair[0])
            pairCards.append(pair[1])
        pairCards = card.sortingCards(list(set(pairCards)))
        
        trisInClass = card.getTris(pairCards)
        if trisInClass:
            for tris in trisInClass:
                trisCards.append(tris[0])
                trisCards.append(tris[1])
                trisCards.append(tris[2])
                splitedPair.append(tris[0:2]) 
                splitedSingle.append([tris[2]]) 
            
            pairFromTris = card.getPair(trisCards)
            classResult = [x for x in className if x not in pairFromTris]
            for x in splitedPair: classResult.append(x)
            for x in splitedSingle: classResult.append(x)
            return classResult
    return className

#splitTrisToSingleAndPair([['10H', 'JH', 'QH', 'KH', 'AH'], ['10S', 'JS', 'QS', 'KS', 'AS'], ['2D', '2H'], ['2D','2S']])


# buat advance strategy
def maxPairInCombo(comboCard):
    # Pair in two combo
    if (card.isFourCards(comboCard[0]) or card.isFullHouse(comboCard[0])) and (card.isFourCards(comboCard[1]) or card.isFullHouse(comboCard[1])):
        tempCard1 = comboCard[0]
        tempPair1 = card.getPair(tempCard1)
        tempCombo1 = [card.getPairScore(x) for x in tempPair1]
        tempCard2 = comboCard[1]
        tempPair2 = card.getPair(tempCard2)
        tempCombo2 = [card.getPairScore(x) for x in tempPair2]
        if max(tempCombo1) > max(tempCombo2):
            return [comboCard[0]]
        return [comboCard[1]]
    # Pair only in one combo
    else:
        if card.isFourCards(comboCard[0]) or card.isFullHouse(comboCard[0]):
            return [comboCard[0]]
        return [comboCard[1]]

#comboCard = [['8D','8H','8S','AH','AS'],['10D','10C','10H','10S','AS']]
#maxPairInCombo(comboCard)
    
#comboCard = [['9H', '9S', '2D', '2H', '2S'], ['6C', '7S', '8C', '9D', '10H']]
#maxPairInCombo(comboCard)

def splitComboToPair(comboCard):
    splitResult = []
    # Four cards
    if card.isFourCards(comboCard[0]):
        fourInCombo = card.getFourCards(comboCard[0])
        for x in fourInCombo:
            splitResult.append(x[0:2])
            splitResult.append(x[2:4])
    # Full house
    elif card.isFullHouse(comboCard[0]):
        trisInCombo = card.getTris(comboCard[0])
        splitResult.append([x for x in comboCard[0] if x not in trisInCombo[0]])
        for x in trisInCombo:
            splitResult.append(x[0:2])
        splitResult = card.sortingPairs(splitResult)
    # Straight, Flush, and Straight Flush
    else:
        splitResult = []
    return splitResult

#comboCard = [['10D','10C','10H','10S','AS']]
#comboCard = [['10D','10H','10S','AH','AS']]
#comboCard = [['3H','5H','7H','8H','10H']]
#splitComboToPair(comboCard)


def pairInCombo(comboCard, moveLists, enemy1, enemy2, enemy3):
    # Double combo
    if len(comboCard) == 2:
        if (card.isFourCards(comboCard[0]) or card.isFullHouse(comboCard[0])) or (card.isFourCards(comboCard[1]) or card.isFullHouse(comboCard[1])):
            comboCard = maxPairInCombo(comboCard)
            splitResult = splitComboToPair(comboCard)
            if 2 in [enemy1, enemy2, enemy3]:
                for cards in reversed(splitResult):
                    if cards in moveLists: return cards
                return []
            else:
                for cards in splitResult:
                    if cards in moveLists: return cards
                return []
        return []
    # Single combo
    if len(comboCard) == 1:
        if (card.isFourCards(comboCard[0]) or card.isFullHouse(comboCard[0])):
            comboCard = [comboCard[0]]
            splitResult = splitComboToPair(comboCard)
            if 2 in [enemy1, enemy2, enemy3]:
                for cards in reversed(splitResult):
                    if cards in moveLists: return cards
                return []
            else:
                for cards in splitResult:
                    if cards in moveLists: return cards
                return []
        return []

def maxSingleInCombo(comboCard):
    tempCombo1 = [card.getCardValues([x]) for x in comboCard[0]]
    tempCombo2 = [card.getCardValues([x]) for x in comboCard[1]]    
    if max(tempCombo1) > max(tempCombo2):
        return [comboCard[0]]
    return [comboCard[1]]

#comboCard = [['3H','5H','7H','8H','10H'], ['10D','10C','10H','10S','AS']]
#maxSingleInCombo(comboCard)

def splitComboToSingle(comboCard):
    return [[x] for x in comboCard[0]]

#comboCard = [['10D','10C','10H','10S','AS']]
#comboCard = [['10D','10H','10S','AH','AS']]
#comboCard = [['3H','5H','7H','8H','10H']]
#splitComboToSingle(comboCard)

def singleInCombo(comboCard, moveLists, enemy1, enemy2, enemy3):
    if len(comboCard) == 2:
        comboCard = maxSingleInCombo(comboCard)
    splitResult = splitComboToSingle(comboCard)
    if 1 in [enemy1, enemy2, enemy3]:
        for cards in reversed(splitResult):
            if cards in moveLists: return cards
        return []
    else:
        for cards in splitResult:
            if cards in moveLists: return cards
        return []

def splitPairToSingle(pairCard):
    return [[x] for x in pairCard[-1]]

#pairCard = [['2D','2H'], ['2D','2S']]
#splitPairToSingle(pairCard)

def splitMove(field, moveLists, comboCard, pairCard, singleCard, enemy1, enemy2, enemy3):
    # # Field combo
    if len(field) == 5:
        if comboCard:
            for cards in comboCard:
                if cards in moveLists: return cards
            return []
        return []
    # Field pair
    if len(field) == 2:
        if pairCard:
            if 2 in [enemy1, enemy2, enemy3]:
                for cards in reversed(pairCard):
                    if cards in moveLists: return cards
                else:
                    # Split combo
                    if comboCard:
                        return pairInCombo(comboCard, moveLists, enemy1, enemy2, enemy3)
                    return [] 
            else:
                for cards in pairCard:
                    if cards in moveLists: return cards
                else:
                    # Split combo
                    if comboCard:
                        return pairInCombo(comboCard, moveLists, enemy1, enemy2, enemy3)
                    return [] 
        else:
            # Split combo
            if comboCard:
                return pairInCombo(comboCard, moveLists, enemy1, enemy2, enemy3)
            return [] 
    # Field single
    if len(field) == 1:
        if singleCard:
            for cards in reversed(singleCard):
                if cards in moveLists: return cards
            else:
                # Split pair
                if pairCard:
                    splitResult = splitPairToSingle(pairCard)
                    for cards in splitResult:
                        if cards in moveLists: return cards
                    else:
                        # Split combo
                        if comboCard:
                            return singleInCombo(comboCard, moveLists, enemy1, enemy2, enemy3)
                        return []
                # Split combo
                if comboCard:
                    return singleInCombo(comboCard, moveLists, enemy1, enemy2, enemy3)
                return []
        else:                
            # Split pair
            if pairCard:
                splitResult = splitPairToSingle(pairCard)
                for cards in splitResult:
                    if cards in moveLists: return cards
                else:
                    # Split combo
                    if comboCard:
                        return singleInCombo(comboCard, moveLists, enemy1, enemy2, enemy3)
                    return []
            # Split combo
            if comboCard:
                return singleInCombo(comboCard, moveLists, enemy1, enemy2, enemy3)
            return []

# Not control move for advance strategy
def notControlMove(field, moveLists, comboCard, pairCard, singleCard, enemy1, enemy2, enemy3):
    # Field Combo
    if len(field) == 5:
        if comboCard:
            for cards in comboCard:
                if cards in moveLists: return cards
            return []
        return []
    # Field pair
    if len(field) == 2:
        if pairCard:
            if 2 in [enemy1, enemy2, enemy3]:
                for cards in reversed(pairCard):
                    if cards in moveLists: return cards
                return []
            else:
                for cards in pairCard:
                    if cards in moveLists: return cards
                return []
        return [] 
    # Field single
    if len(field) == 1:
        if singleCard:
            for cards in reversed(singleCard):
                if cards in moveLists: return cards
            return []
        return []
                
def advanceStrategy(hand, field, moveLists, pass_turn, classA, classB, classC, classD, enemy1, enemy2, enemy3, control, moveLen):
    print('masuk as')
    classASingle = findSingleInClass(classA)
    classAPair = findPairInClass(classA)
    classACombo = findComboInClass(classA)

    classBSingle = findSingleInClass(classB)
    classBPair = findPairInClass(classB)
    classBCombo = findComboInClass(classB)

    classCSingle = findSingleInClass(classC)
    classCPair = findPairInClass(classC)
    classCCombo = findComboInClass(classC)

    classDSingle = findSingleInClass(classD)
    classDPair = findPairInClass(classD)
    classDCombo = findComboInClass(classD)

    comboCard = classDCombo + classCCombo + classBCombo + classACombo
    pairCard = classDPair + classCPair + classBPair + classAPair
    singleCard = classDSingle + classCSingle + classBSingle + classASingle
    
    if moveLen <= 2:
        if control:
            if len(classA) > 0:                                                 # classAnya lebih dari 1
                return classA[0]
            else:
                if comboCard:
                    return comboCard[0]
                if pairCard:                                      # kalo gaada combo pasti ada poir
                    if 2 in [enemy1, enemy2, enemy3]:
                        return pairCard[-1]
                    return pairCard[0]
                if singleCard:
                    return singleCard[-1]
                return []

        if not control:
            if min(enemy1, enemy2, enemy3) <= 2:
                return splitMove(field, moveLists, comboCard, pairCard, singleCard, enemy1, enemy2, enemy3)
            # Enemy cards > 2
            else:
                return notControlMove(field, moveLists, comboCard, pairCard, singleCard, enemy1, enemy2, enemy3)
            
    if moveLen == 3:
        if control:
            if len(classA) > 1:                                                 # classAnya lebih dari 1
                return classA[0]
            else:
                if comboCard:
                    return comboCard[0]
                if pairCard:                                      # kalo gaada combo pasti ada poir
                    if 2 in [enemy1, enemy2, enemy3]:
                        return pairCard[-1]
                    return pairCard[0]
                if singleCard:
                    return singleCard[-1]
                return []

        if not control:
            if min(enemy1, enemy2, enemy3) <= 2:
                return splitMove(field, moveLists, comboCard, pairCard, singleCard, enemy1, enemy2, enemy3)
            # Enemy cards > 2
            else:
                return notControlMove(field, moveLists, comboCard, pairCard, singleCard, enemy1, enemy2, enemy3)

def moveSelection(hand, field, turn, pass_turn, classA, classB, classC, classD, enemy1, enemy2, enemy3, control, cardClass):
    classAlen = len(classA)
    classBlen = len(classB)
    classClen = len(classC)
    classDlen = len(classD)
    
    tempClassA = classA
    tempClassB = classB
    tempClassC = classC
    tempClassD = classD

    moveLists = logic.possibleMoves(hand, field, control, turn)
    moveLen = classAlen + classBlen + classClen + classDlen
    if moveLen <= 3 and len(hand) > 4:
        return advanceStrategy(hand, field, moveLists, pass_turn, classA, classB, classC, classD, enemy1, enemy2, enemy3, control, moveLen)

    # Start game must play 3D
    if turn == 0:
        classA = [x for x in classA if x in moveLists]
        classB = [x for x in classB if x in moveLists]
        classC = [x for x in classC if x in moveLists]
        classD = [x for x in classD if x in moveLists]
        if classD: return classD[0]
        if classC: return classC[0]
        if classB: return classB[0]
        if classA: return classA[0]

    if classAlen > (classClen + classDlen + classBlen) and classAlen > 0:
        classA = [x for x in classA if x in moveLists]
        if classA: return classA[0]
            
    if control:
        if len(hand) <= 4:
            selected_card = underFour(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3)
            return selected_card
        else:
            selected_card = overFour(hand, classA, classB, classC, classD, enemy1, enemy2, enemy3)
            return selected_card

    if not control:
        # Field single
        if len(field) == 1:
            # Split bigPair
            bigPair = findPairInClass(classA)
            if bigPair:
                bigSingle = bigPair[-1]
                classA.append([bigSingle[0]])
                classA.append([bigSingle[1]])
        
        classA = [x for x in classA if x in moveLists]
        classB = [x for x in classB if x in moveLists]
        classC = [x for x in classC if x in moveLists]
        classD = [x for x in classD if x in moveLists]

        if classD:
            for selected_card in classD:
                if not checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, tempClassA, tempClassB, tempClassC, tempClassD, selected_card):
                    return selected_card
        if classC:
            for selected_card in classC:
                if not checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, tempClassA, tempClassB, tempClassC, tempClassD, selected_card):
                    return selected_card
        if classB:
            for selected_card in classB:
                if not checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, tempClassA, tempClassB, tempClassC, tempClassD, selected_card):
                    return selected_card
        if classA:
            for selected_card in classA:
                if not checkHoldback(hand, field, enemy1, enemy2, enemy3, turn, pass_turn, tempClassA, tempClassB, tempClassC, tempClassD, selected_card):
                    return selected_card
        if 1 in [enemy1, enemy2, enemy3]:
            comboCard = findComboInClass(classD) + findComboInClass(classC) + findComboInClass(classB) + findComboInClass(classA)
            pairCard = findPairInClass(classD) + findPairInClass(classC) + findPairInClass(classB) + findPairInClass(classA)
            singleCard = findSingleInClass(classD) + findSingleInClass(classC) + findSingleInClass(classB) + findSingleInClass(classA)
            return splitMove(field, moveLists, comboCard, pairCard, singleCard, enemy1, enemy2, enemy3)
        return []

def predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn):
    if type(hand) != list:
        hand = hand.translate({ord('"'):None})
        hand = hand.translate({ord(']'):None})
        hand = hand.translate({ord('['):None})
        hand = hand.translate({ord("'"):None})
        hand = hand.translate({ord(' '):None})
        hand = hand.split(",")

    if type(field) != list:
        if field == "[',']":
            field = []
        else:
            field = field.translate({ord('"'):None})
            field = field.translate({ord(']'):None})
            field = field.translate({ord('['):None})
            field = field.translate({ord("'"):None})
            field = field.translate({ord(' '):None})
            field = field.split(",")

    if type(field_history) != list:
        if field_history == "[',']":
            field_history = []
        else:
            field_history = field_history.translate({ord('"'):None})
            field_history = field_history.translate({ord(']'):None})
            field_history = field_history.translate({ord('['):None})
            field_history = field_history.translate({ord("'"):None})
            field_history = field_history.translate({ord(' '):None})
            field_history = field_history.split(",")

    if type(pass_turn) != list and type(pass_turn) != dict:
        pass_turn = pass_turn.translate({ord('"'):None})
        pass_turn = pass_turn.translate({ord(']'):None})
        pass_turn = pass_turn.translate({ord('['):None})
        pass_turn = pass_turn.translate({ord("'"):None})
        pass_turn = pass_turn.translate({ord(' '):None})
        pass_turn = pass_turn.split(",")
        pass_turn = {0:int(pass_turn[0]),
                     1:int(pass_turn[1]),
                     2:int(pass_turn[2]),
                     3:int(pass_turn[3])}

    if control == "true" or control == "True":
        control = True
    elif control == "false" or control == "False":
        control = False
        
    moveLists = logic.possibleMoves(hand, field, control, turn)
    if len(moveLists) == 0:
        return []
    min_enemy = min([enemy1, enemy2, enemy3])
    cardClass = cardClassifier(hand, field_history, min_enemy)
    classA = cardClass['classA']
    classB = cardClass['classB']
    classC = cardClass['classC']
    classD = cardClass['classD']

    filterClassA = [x for x in classA]
    filterClassB = [x for x in classB]
    filterClassC = [x for x in classC]
    filterClassD = [x for x in classD]

    classASingle = findSingleInClass(filterClassA)
    classAPair = findPairInClass(filterClassA)
    classACombo = findComboInClass(filterClassA)
    
    classBSingle = findSingleInClass(filterClassB)
    classBPair = findPairInClass(filterClassB)
    classBCombo = findComboInClass(filterClassB)
    
    classCSingle = findSingleInClass(filterClassC)
    classCPair = findPairInClass(filterClassC)
    classCCombo = findComboInClass(filterClassC)
    
    classDSingle = findSingleInClass(filterClassD)
    classDPair = findPairInClass(filterClassD)
    classDCombo = findComboInClass(filterClassD)
    
    # All play single
    if len(classASingle) >= (len(classCSingle) + len(classDSingle)) and len(classASingle) >= len(classBSingle) and (len(filterClassB) + len(filterClassC) + len(filterClassD))>0 and (len(filterClassB) + len(filterClassC) + len(filterClassD)) < len(filterClassA):
        filterClassA = classASingle
        filterClassB = classBSingle
        filterClassC = classCSingle
        filterClassD = classDSingle
    
    else:
        # Tidak pecah combo atau pair
        if len(hand) >= 4:
            classAPair = [x for x in classAPair if not(any(x[0] in Combo for Combo in classDCombo)) and not(any(x[1] in Combo for Combo in classDCombo))
                                               and not(any(x[0] in Combo for Combo in classCCombo)) and not(any(x[1] in Combo for Combo in classCCombo))
                                               and not(any(x[0] in Combo for Combo in classBCombo)) and not(any(x[1] in Combo for Combo in classBCombo))
                                               and not(any(x[0] in Combo for Combo in classACombo)) and not(any(x[1] in Combo for Combo in classACombo))]
            
            classBPair = [x for x in classBPair if not(any(x[0] in Combo for Combo in classDCombo)) and not(any(x[1] in Combo for Combo in classDCombo))
                                               and not(any(x[0] in Combo for Combo in classCCombo)) and not(any(x[1] in Combo for Combo in classCCombo))
                                               and not(any(x[0] in Combo for Combo in classBCombo)) and not(any(x[1] in Combo for Combo in classBCombo))
                                               and not(any(x[0] in Combo for Combo in classACombo)) and not(any(x[1] in Combo for Combo in classACombo))]
        
            classCPair = [x for x in classCPair if not(any(x[0] in Combo for Combo in classDCombo)) and not(any(x[1] in Combo for Combo in classDCombo))
                                               and not(any(x[0] in Combo for Combo in classCCombo)) and not(any(x[1] in Combo for Combo in classCCombo))
                                               and not(any(x[0] in Combo for Combo in classBCombo)) and not(any(x[1] in Combo for Combo in classBCombo))
                                               and not(any(x[0] in Combo for Combo in classACombo)) and not(any(x[1] in Combo for Combo in classACombo))]
        
            classDPair = [x for x in classDPair if not(any(x[0] in Combo for Combo in classDCombo)) and not(any(x[1] in Combo for Combo in classDCombo))
                                               and not(any(x[0] in Combo for Combo in classCCombo)) and not(any(x[1] in Combo for Combo in classCCombo))
                                               and not(any(x[0] in Combo for Combo in classBCombo)) and not(any(x[1] in Combo for Combo in classBCombo))
                                               and not(any(x[0] in Combo for Combo in classACombo)) and not(any(x[1] in Combo for Combo in classACombo))]
            
            classASingle = [x for x in classASingle if not(any(x[0] in Pair for Pair in classDPair)) and not(any(x[0] in Combo for Combo in classDCombo))
                                                   and not(any(x[0] in Pair for Pair in classCPair)) and not(any(x[0] in Combo for Combo in classCCombo))
                                                   and not(any(x[0] in Pair for Pair in classBPair)) and not(any(x[0] in Combo for Combo in classBCombo))
                                                   and not(any(x[0] in Pair for Pair in classAPair)) and not(any(x[0] in Combo for Combo in classACombo))]
            
            classBSingle = [x for x in classBSingle if not(any(x[0] in Pair for Pair in classDPair)) and not(any(x[0] in Combo for Combo in classDCombo))
                                                   and not(any(x[0] in Pair for Pair in classCPair)) and not(any(x[0] in Combo for Combo in classCCombo))
                                                   and not(any(x[0] in Pair for Pair in classBPair)) and not(any(x[0] in Combo for Combo in classBCombo))
                                                   and not(any(x[0] in Pair for Pair in classAPair)) and not(any(x[0] in Combo for Combo in classACombo))]
        
            classCSingle = [x for x in classCSingle if not(any(x[0] in Pair for Pair in classDPair)) and not(any(x[0] in Combo for Combo in classDCombo))
                                                   and not(any(x[0] in Pair for Pair in classCPair)) and not(any(x[0] in Combo for Combo in classCCombo))
                                                   and not(any(x[0] in Pair for Pair in classBPair)) and not(any(x[0] in Combo for Combo in classBCombo))
                                                   and not(any(x[0] in Pair for Pair in classAPair)) and not(any(x[0] in Combo for Combo in classACombo))]
        
            classDSingle = [x for x in classDSingle if not(any(x[0] in Pair for Pair in classDPair)) and not(any(x[0] in Combo for Combo in classDCombo))
                                                   and not(any(x[0] in Pair for Pair in classCPair)) and not(any(x[0] in Combo for Combo in classCCombo))
                                                   and not(any(x[0] in Pair for Pair in classBPair)) and not(any(x[0] in Combo for Combo in classBCombo))
                                                   and not(any(x[0] in Pair for Pair in classAPair)) and not(any(x[0] in Combo for Combo in classACombo))]
            
            filterClassA = classACombo + classAPair + classASingle
            filterClassB = classBCombo + classBPair + classBSingle
            filterClassC = classCCombo + classCPair + classCSingle
            filterClassD = classDCombo + classDPair + classDSingle    
        # Di bawah 4 cards bisa main pair atau single
        else:
            filterClassA = classACombo + classAPair + classASingle
            filterClassB = classBCombo + classBPair + classBSingle
            filterClassC = classCCombo + classCPair + classCSingle
            filterClassD = classDCombo + classDPair + classDSingle
    
    
    classA = splitTrisToSingleAndPair(filterClassA)
    classB = splitTrisToSingleAndPair(filterClassB)
    classC = splitTrisToSingleAndPair(filterClassC)
    classD = splitTrisToSingleAndPair(filterClassD)
    
    print(' Class A \n', classA)
    print(' Class B \n', classB)
    print(' Class C \n', classC)
    print(' Class D \n', classD)

    return moveSelection(hand, field, turn, pass_turn, classA, classB, classC, classD, enemy1, enemy2, enemy3, control, cardClass)

#allcards = [d['name'] for d in card.card]
#list(set(allcards).difference(set(['4D','4S','6D','2D'])))


## Test pair
#hand = ['6C','7S','8C','9D','9H','9S','10H','2D','2H','2S']
#field = ['8D','8H']
#control = False
#field_history = ['3D', '5C', '6H', '7C', '8S', '9C', 'AD', 'AC', '6D', '6C', 'JD', 'JC', 'QD', 'QH', 'KC', 'KH', '5H', '5S', '9D', '9S', '3C', '3S', '5D', 'JS', 'AH', '2C', '7S', '10S', '2D', '3H', '9H', 'QS', '2H']
#turn = 53
#enemy1 = 2
#enemy2 = 6
#enemy3 = 6
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test double combo
#hand = ['4C', '7D', '8D', '8C', '8H', '10D', '10C']
#field = ['2H']
#control = False
#field_history = ['3D', '5C', '6H', '7C', '8S', '9C', 'AD', 'AC', '6D', '6C', 'JD', 'JC', 'QD', 'QH', 'KC', 'KH', '5H', '5S', '9D', '9S', '3C', '3S', '5D', 'JS', 'AH', '2C', '7S', '10S', '2D', '3H', '9H', 'QS', '2H']
#turn = 53
#enemy1 = 1
#enemy2 = 9
#enemy3 = 2
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test double combo
#hand = ['4D', '4H', '4S', '10H', 'JH', 'QC', 'KS', 'AS', '2H', '2S']
#field = ['QS']
#control = False
#field_history = ['3D', '5C', '6H', '7C', '8S', '9C', 'AD', 'AC', '6D', '6C', 'JD', 'JC', 'QD', 'QH', 'KC', 'KH', '5H', '5S', '9D', '9H', '3C', '3S', '5D', 'JS', 'AH', '2C', '7S', '10S', '2D', '3H', '9S', 'QS']
#turn = 53
#enemy1 = 2
#enemy2 = 7
#enemy3 = 1
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test single advanced strategy
#hand = ['3C', '3H', '4D', '4C', '5C', '8D', '8H', '8S', 'AD', 'AC', 'AS']
#field = ['2S']
#control = False
#field_history = ['3D', '4H', '5D', '6C', '2D', '3S', 'QD', 'QC', 'QH', 'QS', '9D', '9C', 'JD', 'JS', 'KD', 'KH', '2C', '2H', '6H', '6S', '10H', '10S', '5S', '7D', '9H', '9S', 'JH', 'KS', 'AH', '7C', '7H', '10D', 'JC', '2S']
#turn = 39
#enemy1 = 4
#enemy2 = 11
#enemy3 = 1
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test double combo
#hand = ['3S', '4H', '4S', '5C', '6D', '7S', '9D', '9S', 'AC', 'AH', 'AS']
#field = ['8D', '8H', '8S', 'JH', 'JS']
#control = False
#field_history = ['3D', '3H', '5H', '5S', '7D', '7C', '10C', '10S', '4D', '4C', '5D', '8C', '9H', '10H', 'JD', 'QH', 'QS', 'KH', 'AD', '2D', '2C', '2H', '6H', '7H', '10D', 'JC', 'QC', 'KD', 'KC', '2S', '8D', '8H', '8S', 'JH', 'JS']
#turn = 47
#enemy1 = 1
#enemy2 = 2
#enemy3 = 3
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test double combo
#hand = ['3S', '4H', '4S', '5C', '6D', '7S', '9D', '9S', 'AC', 'AH', 'AS']
#field = ['AD']
#control = False
#field_history = ['3D', '3C', '10C', '10S', '5H', '5S', '7D', '7C', 'KC', 'KS', '4D', '4C', '5D', '8C', '9H', '10H', 'JD', 'QH', 'QS', 'KH', 'AD']
#turn = 47
#enemy1 = 4
#enemy2 = 10
#enemy3 = 6
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
    
## Test underfour
#hand = ['10D', '10S', '2S']
#field = []
#control = True
#field_history = ['3D', '9D', '9H', 'JD', 'JS', 'QD', 'KS', 'AD', '5C', '5S', '8H', '8S', 'JC', 'JH', 'AC', 'AS', '2D', '2H', '4D', '4C', '4H', '7D', '7S']
#turn = 25
#enemy1 = 9
#enemy2 = 11
#enemy3 = 6
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test pecah tris 2
#hand = ['6H', '7D', '8D', '2D', '2C', '2S']
#field = ['8C']
#control = False
#field_history = ['3D', '3C', '3H', 'KD', 'KC', '6D', '6C', '6S', '7H', '7S', '3S', '4D', '4S', '5S', 'QS', 'KS', 'AC', 'AS', '4C', '4H', '9D', '9H', '9C', '9S', 'QD', 'QH', '7C', '8C']
#turn = 28
#enemy1 = 6
#enemy2 = 4
#enemy3 = 8
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test holdback single 2
#hand = ['5D', '6D', 'AS', '2S']
#field = ['JC']
#control = False
#field_history = ['3D', '4C', '6D', 'QS', 'KD', 'KH', 'AS', '7C', '9C', 'QC', 'KC', 'AC', '4S', '7S', '8S', 'JS', '3C', '3S', '5C', '5H', '5S', '7H', '9H', '9S', '10D', '10S', '4H', '8D', '9D', 'JC', '2D','2C','2H']
#turn = 28
#enemy1 = 7
#enemy2 = 3
#enemy3 = 8
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test pair 2
#hand = ['5D', '2D', '2S']
#field = ['JC']
#control = False
#field_history = ['3D', '4C', '6D', 'QS', 'KD', 'KH', 'AS', '7C', '9C', 'QC', 'KC', 'AC', '4S', '6S', '7S', '8S', 'JS', '3C', '3S', '5C', '5H', '5S', '7D', '7H', '9H', '9S', '10D', '10S', '4H', '8D', '9D', 'JC']
#cardClassifier(hand, field_history)
#turn = 28
#enemy1 = 6
#enemy2 = 3
#enemy3 = 8
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test findMaxValue
#hand = ['4H', '5C', '6D', '7H', '8C', '8S', '9D', '10D', 'JD', 'QS']
#field = ['2D']
#control = False
#field_history = ['3D', '5S', '6D', '7S', '8D', 'JC', 'QS', 'AS', '2S', '10D', '10C', 'JC', 'JS', 'AD', 'AH', '3S', '5C', '6C', 'KD', 'KC', 'KH', '2D']
#cardClassifier(hand, field_history)
#turn = 29
#enemy1 = 4
#enemy2 = 9
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test pecah Pair
#hand = ['JD', '2D', '2C']
#field = ['QH']
#control = False
#field_history = ['3D', '4H', '5C', 'AH', '2H', '4C', '4S', '8D', '8C', '8H', '7D', '7S', 'JC', 'JH', 'JS', '3S', '9C', 'QD', 'KH', '2S', '3H', '4D', '5S', 'QC', 'KD', 'KS', '6C', '7C', 'QS', 'AD', 'AC', '5D', '7H', '8S', 'KC', '9S', '10S', 'AS', '10H', 'QH', '9H']
#cardClassifier(hand, field_history)
#turn = 11
#enemy1 = 1
#enemy2 = 6
#enemy3 = 2
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test double combo
#hand = ['4D', '5D', '9S', '10H', 'JD', 'QS', 'KC', 'KH', 'AD', 'AC', 'AS', '2D', '2C']
#field = ['QD']
#control = False
#field_history = ['3D', '4H', '5C', 'AH', '2H', '4C', '4S', '8D', '8C', '8H', '7D', '7S', 'JC', 'JH', 'JS', '3S', '9C', 'QD']
#cardClassifier(hand, field_history)
#turn = 11
#enemy1 = 7
#enemy2 = 7
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##hand = ['3H','4H','4D','4S','5D','5S','5H','6D','6H','7D','7H','8H','2H']
#hand = ['5D','5S','5H','6D','6H','7D','7H']
#field = []
#control = True
#field_history = []
#turn = 1
#enemy1 = 13
#enemy2 = 13
#enemy3 = 13
#pass_turn = {0:0, 1:0, 2:0, 3:0}
##start = time.time()
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
##end = time.time()
##print(end-start)

##Test full house Ace
#hand = ['3S','4C','5H','6D','6C','6S','8D','10D','KD','KH','AD','AC','AH']
#field = ['3C','3H','QD','QC','QH']
#control = False
#field_history = ['3D','3C','3H','QD','QC','QH']
#turn = 7
#enemy1 = 8
#enemy2 = 10
#enemy3 = 10
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##Test single
#hand = ['4H','5C','5S','6D','7H','8C','8S','9D','10D','JD','JC','QS','KD']
#field = ['8D']
#control = False
#field_history = ['3D','3H','4D','4C','6C','6H','AC','AS','5D','7C','8D']
#turn = 7
#enemy1 = 8
#enemy2 = 10
#enemy3 = 10
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##Test pair
#hand = ['4D','4S','JH','JS','2S']
#field = []
#control = True
#turn = 30
#field_history = ['6D','2H','4C', 'KD', '2C','AD', '8D', '5H', '10S', 'QS', '7D', '5S', '8C', '7C', 'KS', 'QD','6H','5C','8H','QC', '3S','JC','KC','7H','6C','2D','6S','4H','AC','9S','5D','10H','KH','3C','9H','JD','7S']
#enemy1 = 2
#enemy2 = 4
#enemy3 = 3
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##Test pair Ace
#hand = ['3S','4S','6D','6H','8S','9H','10H','JC','AD','AS','2H','2S']
#field = ['4C','4H']
#control = False
#turn = 30
#field_history = ['3D','4D','4C','4H','5C','5H','6D','6C','6S','7D','7H','7S','8C','8H','9D','9S','10C','JS','QH','QS','KD','KC','KH','KS','2C']
#enemy1 = 8
#enemy2 = 6
#enemy3 = 2
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test pair 2
#hand = ['3D','3C','2S']
#field = []
#control = True
#turn = 41
#field_history = ['3H','3S','4D','4C','4H','4S','5D','5C','5H','5S','6D','6C','6H','6S','7D','7C','7H','8S','9D','9C','9H','9S','10D','10C','10H','10S','JC','JH','JS','QD','QH','QS','KD','KC','KH','KS','AD','AC','AH','AS','2C','2H']
#enemy1 = 3
#enemy2 = 2
#enemy3 = 1
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

#hand = ['3D','3S','3H','5S','5D','JC','JS','2H']
#field = []
#control = True
#turn = 1
#field_history = ['4H','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','QD','QS','KS','KH','KC','AD','AC','AH','2S']
#enemy1 = 7
#enemy2 = 7
#enemy3 = 9
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

## Test hold full house
#hand = ['6D','6S','8H','8S','JD','JC','JS','2H']
#field = ['5S', '5D']
#control = False
#turn = 6
#field_history = ['4H','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','QD','QS','KS','KH','KC','AD','AC','AH','2S']
#enemy1 = 7
#enemy2 = 7
#enemy3 = 8
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

#
#hand = ['3D','4S','5H','5S','6D','6C','6S','7D','7C','8H','JH','QC','2H']
#field = []
#control = True
#turn = 1
#field_history = []
#enemy1 = 13
#enemy2 = 13
#enemy3 = 13
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

#Test underFour
#hand = ['4D','8H','AS']
#field = []
#control = True
#turn = 8
#field_history = ['3D','3H','3S','4H','5D','5C','5S','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

#Test single
#hand = ['3C','4D','5H','6H','7C','8D','8H','8S','9C','JD','JH','KD','AS']
#field = []
#control = True
#turn = 8
#field_history = ['3D','3H','3S','4H','5D','5C','5S','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
#
##Test Pair
#hand = ['4D','4S','AS']
#field = []
#control = True
#turn = 8
#field_history = ['3D','3H','3S','4H','5D','5C','5S','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
#
##Test Straight
#hand = ['6H','6S','7D','7C','9D','9C','10C','JD','JH','KD','QC','QH','AS']
#field = []
#control = True
#turn = 4
#field_history = ['3D','3C','3H','3S','4D','4H','5D','5C','5H','7H','7S','8C','8S','9H','9S','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##Test Combo Full House
#hand = ['6H','6S','7D','7C','7S','8D','8H','8S','9C','JD','JH','KD','AS']
#field = []
#control = True
#turn = 8
#field_history = ['3D','3C','3H','3S','4D','4H','5D','5C','5H','7H','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
#
#
##Test underFour
#hand = ['4D','8H','AS']
#field = ['2H']
#control = False
#turn = 8
#field_history = ['3D','3H','3S','4H','5D','5C','5S','7D','7H','7S','8C','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
#
##Test single
#hand = ['3C','4D','5H','6H','7C','8D','8H','8S','9C','JD','JH','KD','AS']
#field = []
#control = False
#turn = 8
#field_history = ['3D','3H','3S','4H','5D','5C','5S','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
#
##Test Pair
#hand = ['4D','4S','AS']
#field = ['3C']
#control = False
#turn = 8
#field_history = ['3D','3H','3S','4H','5D','5C','5S','7D','7H','7S','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
#
##Test Straight
#hand = ['6H','6S','7D','7C','9D','9C','10C','JD','JH','KD','QC','QH','AS']
#field = []
#control = False
#turn = 4
#field_history = ['3D','3C','3H','3S','4D','4H','5D','5C','5H','7H','7S','8C','8S','9H','9S','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)
#
##Test Combo Full House
#hand = ['6H','6S','7D','7C','7S','8D','8H','8S','9C','JD','JH','KD','AS']
#field = []
#control = False
#turn = 8
#field_history = ['3D','3C','3H','3S','4D','4H','5D','5C','5H','7H','8C','9D','9H','9S','10C','10H','10S','JC','JS','QD','QS','KS','KH','KC','AD','AC','AH','2C']
#enemy1 = 5
#enemy2 = 4
#enemy3 = 7
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##Test Combo Full House
#hand = ['3D','3C','3S','4D','4S','8D','8H','9D','9C','JD','JH','KD','AS']
#field = []
#control = True
#turn = 0
#field_history = []
#enemy1 = 13
#enemy2 = 13
#enemy3 = 13
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##Test Combo Full House
#hand = ['6D','7D','7H','7S','2D','2S']
#field = []
#control = True
#turn = 40
#field_history = ['3D','3H','3S','4C','5C','5H','5S','6S','7C','8D','8H','9C','9H','9S','10D','10S','JD','JH','JS','QD','QC','QH','QS','KD','KC','KH','KS','AD','AC','AH','AS','2C','2H']
#enemy1 = 8
#enemy2 = 2
#enemy3 = 6
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)

##Test single underFour
#hand = ['4D','4S','6H','2S']
#field = []
#control = True
#turn = 30
#field_history = ['3D','4C','4H','5C','5H','6D','6C','6S','7D','7H','7S','8C','8H','9D','9S','10C','JS','QH','QS','KD','KC','KH','KS','2C','2H']
#enemy1 = 2
#enemy2 = 5
#enemy3 = 4
#pass_turn = {0:0, 1:0, 2:0, 3:0}
#predictedMove(hand, field, control, turn, field_history, enemy1, enemy2, enemy3, pass_turn)