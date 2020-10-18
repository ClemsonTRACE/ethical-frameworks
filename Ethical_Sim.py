import random
import json
import sys

class Ethical_Sim:
    dilemmas = [] #Dilemmas that the player will tackle
    gifts = ["A Hat", "A Board Game", "A Sweater", "A Bike", "A Computer"]
    dilemmasDone = [] #Dilemma list the player traversed
    QUESTION_COUNT = None #Number of questions we want to ask
    modifierTypes = ("P_Number", "T_Number", "H_Percent", "M_Percent", "L_Percent", "Result", "Gift")
    relationOptions = ("Family Member(s)", "Friend(s)", "Stranger(s)")
    results = ["Dead", "In Pain"]
    #AGE Modifiers?

    def __init__(self, questionCount):
        json_array = json.load(open("Dilemna.json"))
        self.QUESTION_COUNT = questionCount

        #Load list of dilemmas into memory
        for item in json_array:
            self.dilemmas.append(item)

        #Generate initial node randomly
        self.makeNextDilemma(random.randint(0,len(self.dilemmas)-1), random.randint(0,1))

    #Make a decision on the current dilemma and pick the next one, this needs 
    #to be separate form the sending of a dilemma due to the first node being 
    #randomly generated
    def makeNextDilemma(self, currentDilemma, decision):
        nextDilemma = random.choice(self.dilemmas[currentDilemma]["target_"+str(decision)])
        node = self.dilemmas[nextDilemma].copy()
        for ind, mod in enumerate(node["Modifier_Types"]):
            print(mod)
            if mod == self.modifierTypes[0]: #People
                node["Modifiers"].append(random.randint(0, 10))
            elif mod == self.modifierTypes[1]: #Time (Days)
                node["Modifiers"].append(random.randint(1, 10))
            elif mod == self.modifierTypes[2]: #High Percent
                node["Modifiers"].append(random.randint(66,101)/100.0)
            elif mod == self.modifierTypes[3]: #Medium Percent
                node["Modifiers"].append(random.randint(33,66)/100.0)
            elif mod == self.modifierTypes[4]: #Low Percent
                node["Modifiers"].append(random.randint(0,33)/100.0)
            elif mod == self.modifierTypes[5]: #results
                node["Modifiers"].append(random.choice(self.results))
            elif mod == self.modifierTypes[6]: #Gift
                node["Modifiers"].append(random.choice(self.gifts))
            print(node["Modifiers"])
            node["Description"] = node["Description"].replace("[M"+str(ind)+"]", str(node["Modifiers"][-1]))
        
        for relation in range(0, node["Relation_Count"]):
            node["Relationships"].append(random.choice(self.relationOptions))
            node["Description"] = node["Description"].replace("[relation_"+str(relation)+"]", node["Relationships"][-1])

        self.dilemmasDone.append(node)

    #return the current dilemma the player is doing, which should be the last one
    def getCurrentDilemma(self):
        return self.dilemmas[-1]

    #Utilitarian reward, based on creating the most good, this is going to 
    #look at helping the most people.  Life or death is valued at a 1, pain is 
    #valued at a 0.5, the reward is calculated for how much good is made vs. 
    #how much total good is available
    def utilitarianReward(self, dilemma, decision):
        pass

    #The deontology reward is based on a strict act based deontology where 
    #hard rules are set and not broken. These are scored with 0 for break
    #and 1 for keep, these rules are:
    #Do not Deliberately Kill
    #Do not Deliberately Harm Others
    #Do not Deliberately Harm Yourself
    #Do not Steal
    #Do not Lie 
    #Act the way that is the maxum you can will as a universal 
    def deontologyReward(self, dilemma, decision):
        pass
    #1     2
    #10    5
    #10/10 5/10
    #young = 1
    #middle = 0.9
    #old = 0.8

    #Virtues ethics are based on common virtues that are seen in humans.  While 
    #this study does not focus on every virtue, this is designed to act as a 
    #representative base for what virtue ethics would look like.  Relavent Virtues 
    #scored with 0 for ignore or 1 for prioritize include:
    #Liberality - The virtue of charity
    #Friendliness - Be friendly to other
    #Loyalty - emphasise family and friends 
    #Courage - Aware of danger, but act
    #Truthfulness - virtue of honesty
    def virtueEthicsReward(self, dilemma, decision):
        pass
            
    
sim = Ethical_Sim(20)
print(sim.dilemmasDone[-1])
