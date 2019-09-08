# -*- coding: utf-8 -*-
"""
Created on Tue May 28 02:07:31 2019

@author: Gerry
"""

from rulebaseAI import predictedMove
from flask import Flask
from flask_restful import Resource, Api
from os import environ

app.run(environ.get('PORT'))

app = Flask(__name__)
api = Api(app)

#class AI1(Resource):
#    def get(self, hand, field, control, turn):
#        if field == None:
#            field = [',']
#        print(hand, field, control, turn)
#        return {'move': randomAI(hand, field, control, turn)}
#    
#api.add_resource(AI1, '/AI1/<hand>+<field>+<control>+<int:turn>')


class RuleBased1(Resource):
    def get(self, hand, field, control, turn, field_history, e1hand, e2hand, e3hand, pass_turn):
        if field == None:
            field = [',']
        if field_history == None:
            field_history = [',']
        
#        print(hand, field, control, turn, field_history, e1hand, e2hand, e3hand, pass_turn)
        return {'move': predictedMove(hand, field, control, turn, field_history, e1hand, e2hand, e3hand, pass_turn)}
    
api.add_resource(RuleBased1, '/RuleBased1/<hand>+<field>+<control>+<int:turn>+<field_history>+<int:e1hand>+<int:e2hand>+<int:e3hand>+<pass_turn>')

app.run(environ.get('PORT'))


#hand = ['4H', '4D', '4S', '7D', '10C', '10S', 'QC', '2D', '2C']
#field = ['3H', '3S', '3D', '5S', '5D']
#predictedMove(hand, field, False, 1)