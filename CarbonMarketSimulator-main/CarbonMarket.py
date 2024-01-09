from mesa import Model, Agent

from mesa.datacollection import DataCollector
from mesa.visualization.ModularVisualization import ModularServer
import numpy as np 
import matplotlib.pyplot as plt 
import math

class CustomModel(Model):
    """
    A class used to represent an agent-based carbon simulation model

    Attributes
    ----------
    participants : list
        a list of objects of the Participant class agent type
    regulators : list
        a list of objects of the Regulator class agent type
    nSteps : int
        number that chronologically identifies the current step of the model
    initialEmissions : int
        initial value in tonnes of CO2 emited by the system
"""
    
    def __str__(self):
        """Prints information about the model and its agents"""
        
        string = "\n*--------------------------------------*\nModel with: \n" + str(len(self.participants)) + " Participant(s)\n" + str(len(self.regulators)) + " Regulator(s)\n"
        for regulator in self.regulators:
            participantsList = []
            for participant in regulator.myParticipants:
                participantsList.append(participant.unique_id)
            participantsList = [str(int) for int in participantsList]
            string += "Regulator " + str(regulator.unique_id) + " regulates participants " + ', '.join(participantsList) + ".\n"

        for participant in self.participantsCorporations:
            string += "Corporation " + str(participant.unique_id) + " has " + str(participant.Credits) + " credits, emits " + str(participant.Emissions) + " tonnes of CO2 and produces " + str(participant.Production) + " units of goods.\n"
            
        string += "*--------------------------------------*\n"
        return string

    def __init__(self):
        """Model constructor"""
        
        self.participants = []
        self.participantsIndividuals = []
        self.participantsCorporations = []
        self.regulators = []
        self.nSteps = 0
        self.initialEmissions = 0
        self.server = None
        self.datacollector = None 
        
    def step(self):  
        """	Advances the model by one step"""
        if self.nSteps == 0:
            self.initialEmissions = 0
            for participant in self.participantsCorporations:
                self.initialEmissions += participant.Emissions
            
            self.topFiftyPolluters = []
            self.topFiftyMoreEfficient= []
            self.middleList = []
            
            tempList = sorted(self.participantsCorporations, key=lambda x: x.EmissionsPerProduct, reverse=True)
            newTempList = []
            for entry in tempList:
                newTempList.append(entry.unique_id)
            
            middle = len(self.participantsCorporations) / 2
            init = int(round(middle - 25))
            end = int(round(middle + 25))
            self.topFiftyPolluters = newTempList[:50]
            self.topFiftyMoreEfficient = newTempList[-50:]
            self.middleList = newTempList[init:end]
        
        self.nSteps += 1
        for regulator in self.regulators:
            regulator.run(self.nSteps)  
            
        self.datacollector.collect(self)
            
    def addVisualization(self, elementList, modelName, modelParameters):
        self.server = ModularServer(self, elementList, modelName, modelParameters)
        
    def addDataCollector(self, datacollector):
        self.datacollector = datacollector
    
    def launchVisualization(self):
        self.server.launch()
    # add Participant agent to model
    # +participantProperties = "Type", "Price Reasoning", "Initial Price"
    # +attributes: custom variables
    def addParticipant(self, participantProperties, attributes):
        """Adds a Participant agent to model according to a set of properties and attributes"""
        
        count = len(self.participants) + 100
        participant = Participant(self, count, participantProperties, attributes)
        self.participants.append(participant)
        
        if participant.type == "Corporation":
            self.participantsCorporations.append(participant)
        elif participant.type == "Individual":
            self.participantsIndividuals.append(participant)
        else:
            raise Exception("Wrong participant type.")
            
    
    # add Participant agent to model
    # receives Participant agent object
    def addParticipantObject(self, participantObject):
        """Adds a Participant agent object to model"""
        
        count = len(self.participants) + 100
        participantObject.unique_id = count
        self.participants.append(participantObject)
        
        if participantObject.type == "Corporation":
            self.participantsCorporations.append(participantObject)
        elif participantObject.type == "Individual":
            self.participantsIndividuals.append(participantObject)
        else:
            raise Exception("Wrong participant type.")
        
        
    # add multiple Participant agents to model
    # receives +list of participantProperties and +list of attributes
    def addMultipleParticipants(self, participantsPropertiesList, attributesList):
        """Adds multiple Participant agents to model according to a set of properties and attributes"""
        
        for count, participantProperties in enumerate(participantsPropertiesList):
            self.addParticipant(participantProperties,attributesList[count])
    
    def addMultipleParticipantsObject(self, participantsObjectList):
        """Adds multiple Participant agent objects to model"""
        
        for participantObject in participantsObjectList:
            self.addParticipantObject(participantObject)
    
    # add Regulator agent to model
    # +regulatorProperties = 
    # +whoRegulates = "All" or list of Participant agents id
    def addRegulator(self, regulatorProperties, whoRegulates = "All"):
        """Adds a Regulator agent to model according to a set of properties"""
        
        count = len(self.regulators) + 1
        regulator = Regulator(count, regulatorProperties, self)
        self.regulators.append(regulator)
        
        listToRegulate = []
        if whoRegulates == "All":
            listToRegulate = self.participants
        else:
            for participant in self.participants:
                if participant.unique_id in whoRegulates:
                    listToRegulate.append(participant)
            
        for participant in listToRegulate:
            self.addParticipantRegulatorRelationship(participant.unique_id, regulator.unique_id)
            
        self.regulators.sort(key=lambda x: x.priority)
        
    # add Participant agent to model
    # receives Participant agent object
    def addRegulatorObject(self, regulatorObject, whoRegulates = "All"):
        """Adds a Regulator agent object to model"""
        
        count = len(self.regulators) + 1
        regulator = regulatorObject
        regulatorObject.unique_id = count
        self.regulators.append(regulator)
        
        listToRegulate = []
        if whoRegulates == "All":
            listToRegulate = self.participants
        else:
            for participant in self.participants:
                if participant.unique_id in whoRegulates:
                    listToRegulate.append(participant)
            
        for participant in listToRegulate:
            self.addParticipantRegulatorRelationship(participant.unique_id, regulator.unique_id)
            
        self.regulators.sort(key=lambda x: x.priority)
        
        
    # adds regulatory relationship
    # receives +Participant agent id and +Regulator agent id
    def addParticipantRegulatorRelationship(self, participantID, regulatorID):        
        """Establishes a regulatory relationship between a Participant agent and a Regulator agent"""
        
        for participant in self.participants:
            if participant.unique_id == participantID:
                myParticipant = participant
                break
        for regulator in self.regulators:
            if regulator.unique_id == regulatorID:
                myRegulator = regulator
                break
        try:
            participant.addRegulator(myRegulator)
            regulator.addParticipant(myParticipant)
        except:
            print("ERROR: Wrong relationships.")
        
        
    # adds CoordinationMechanism to Regulator agent
    # receives +Regulator agent id, +sequence number by which it will be run and +mechanismProperties
    # mechanismProperties = "Mechanism Type"           
    def addMechanismToRegulator(self, regulatorID, mechanismProperties, sequence):
        """Assigns a CoordinationMechanism to a Regulator agent according to a set of mechanism properties"""
        
        for regulator in self.regulators:
            if regulator.unique_id == regulatorID:
                mechanism = CoordinationMechanism(mechanismProperties, sequence)
                mechanism.addRegulator(regulator)
                regulator.addMechanism(mechanism)
    
    # adds CoordinationMechanism object to Regulator agent
    # receives CoordinationMechanism object
    def addMechanismObjectToRegulator(self, regulatorID, mechanismObject):
        """Assigns a custom CoordinationMechanism object to a Regulator agent"""
        
        for regulator in self.regulators:
            if regulator.unique_id == regulatorID:
                regulator.addMechanism(mechanismObject)
        
    # adds DirectRegulation to Regulator agent
    # receives: +Regulator agent id
    # +condition that Participant agents have to comply with to receive an +directRegulation
    # +condition["Frequency"] = "First Time" or "Every Time" (the directRegulation is run every step or only during the initial step?)
    # +condition["Type"] = "By Periodicity" or "By Value" (the directRegulation is run periodically, or only if the agents fulfill a certain condition?)
    # +condition["Attribute Name"] = Attribute name of the agent to be compared in the condition 
    # +condition["Comparator"] = "More Than" or "Less Than"
    # +condition["Reference Value"] = Value that the attribute will be compared with
    # +incentive can be either positive or negative
    # +incentive["Attribute"] = Attribute name
    # +incentive["Value"] = Positive or negative value to increment to designated attribute
    # +order = "Before" or "After" mechanism stage
    def addDirectRegulationToRegulator(self, regulatorID, condition, incentive, order = "Before"):
        """Assigns a DirectRegulation to a Regulator agent according to a set of rules"""
        
        directRegulation = DirectRegulation(condition, incentive, order)
        for regulator in self.regulators:
            if regulator.unique_id == regulatorID:
                regulator.addDirectRegulation(directRegulation)
        
    def addDirectRegulationObjectToRegulator(self, regulatorID, directRegulationObject, order = "Before"):
        """Assigns a custom DirectRegulation object to a Regulator agent"""

        for regulator in self.regulators:
            if regulator.unique_id == regulatorID:
                regulator.addDirectRegulation(directRegulationObject)                    
                                
class Participant(Agent):
    """
    A class used to represent a participant agent in a carbon market model.

    Attributes
    ----------
    myRegulators : list
        a list of objects of the Regulator class agent type that regulate the agent
    type : str
        type of the agent
    priceReasoning : str
        logic by which the agent will define its price for a certain tradable token. Can either be "Fixed Price" or "Price Function"
    myPrice : int 
        current price of an unit of a tradable token in the conception of the agent
    hasDecision : bool
        defines if the agent has to perform a decision before the CoordinationMechanism stage or not
    """ 
      
    def __init__(self, model, participantID, participantProperties, initialAttributes):
        """Participant agent constructor"""
        
        super().__init__(participantID, model)   
        self.myRegulators = []
        self.type = participantProperties["Type"]
        
        if self.type == "Corporation":
            self.priceReasoning = participantProperties["Price Reasoning"]
            self.myPrice = participantProperties["Initial Price"] #fixed price or initial price
            self.hasDecision = participantProperties["Decision"]
                        
        for attributeName in initialAttributes:
            setattr(self, attributeName, initialAttributes[attributeName])
        
    def addRegulator(self, regulator):
        """Defines a regulator to the Participant agent"""
        self.myRegulators.append(regulator)
            
    #virtual method
    def priceFunction(self):
        """Results in a price for a unit of tradable token (Virtual method)"""
        raise NotImplementedError()
        
    def decision(self):
        """Method to be implemented if the agents has to perform a certain action before the CoordinationMechanism stage (Virtual method)"""
        raise NotImplementedError()
            
    def getBid(self, auctionType):
        """Results in an auction bid"""
        price = self.getBidPrice(auctionType)
        volume = math.ceil(self.getBidVolume(auctionType))
        bid = {'buyerId': self, 'bidPrice': price, 'bidVolume': volume}
        return bid
        
    def getBidPrice(self, auctionType):
        """Returns the price of an unit in an auction bid according to the designated price logic in the constructor"""
        
        if self.priceReasoning == "Fixed Price":
            return self.myPrice
        elif self.priceReasoning == "Price Function":
            return self.priceFunction(auctionType) 
        else:
            print("ERROR: Wrong price reasoning.")
            return False
        
    def getBidVolume(self, auctionType):
        """Returns the quantity that the agent is willing to trade"""
        raise NotImplementedError()
        
    def isBuyingCredits(self):
        """Tells if the agent is willing to buy credits"""
        
        return (self.Emissions > self.Credits)
    
    def isSellingCredits(self):
        """Tells if the agent is willing to sell credits"""
        
        return (self.Credits > self.Emissions)
                
    def changeAttribute(self, attributeName, value):
        """Increments or decrements a custom attribute by a certain value"""
        
        newValue = getattr(self, attributeName) + value
        setattr(self, attributeName, newValue)
    
    def receiveCredits(self, numberOfCredits, price):
        self.Credits += numberOfCredits
        
    def surrendAllCreditsToAggregator(self):
        myCredits = self.Credits
        self.Credits = 0
        return myCredits
    
    def individualAction(self):
        self.Credits += 900
               
        
                
                
class Regulator(Agent):
    """
    A class used to represent a regulator agent in a carbon market simulation model.

    Attributes
    ----------
    priority : int
        a value that establishes the order by which Regulator agent actions will be executed
    myParticipants : list
        list of Participant agents being regulated by this agent
    myMechanisms : list
        list of CoordinationMechanism to be executed by this agent
    myDirectRegulationsBefore : list
        list of Incenive to be executed before the CoordinationMechanism stage
    myDirectRegulationsAfter : list
        list of Incenive to be executed after the CoordinationMechanism stage
    """
            
    def __init__(self, regulatorID, regulatorProperties, model):
        """Regulator agent constructor"""
        
        super().__init__(regulatorID, model)
        self.priority = regulatorProperties["Priority"]
        self.aggregator = regulatorProperties["Aggregator"]
        self.myParticipants = []
        self.myParticipantsCorporations = []
        self.myParticipantsIndividuals = []
        self.myMechanisms = []
        self.myDirectRegulationsBefore = []
        self.myDirectRegulationsAfter = []
        
    def addParticipant(self, participant):
        """Defines a regulatory relationship with a Participant agent"""
        
        self.myParticipants.append(participant)
        if participant.type == "Corporation":
            self.myParticipantsCorporations.append(participant)
        elif participant.type == "Individual":
            self.myParticipantsIndividuals.append(participant)
        else:
            raise Exception("Wrong participant type.")
            
        
    def addMechanism(self, mechanism):
        """Adds a CoordinationMechanism to be executed by this agent"""
        
        self.myMechanisms.append(mechanism)
        self.myMechanisms.sort(key=lambda x: x.sequence)
        
    #directRegulations can be given either before or after the coordination mechanism phase        
    def addDirectRegulation(self, directRegulation):
        """Adds a DirectRegulation to be executed by this agent"""
        
        if directRegulation.order == "Before":
            self.myDirectRegulationsBefore.append(directRegulation)
        elif directRegulation.order == "After":
            self.myDirectRegulationsAfter.append(directRegulation)
        else:
            print("ERROR: Wrong directRegulation order.")
            
    def getSellingVolume(self):
        """Determines the quantity of tradable tokens to be sold during a single step by the Regulator"""
        if self.aggregator:
            sellingVolume = 0
            for participant in self.myParticipantsIndividuals:
                sellingVolume += participant.surrendAllCreditsToAggregator()
            return sellingVolume
        else:
            return self.model.initialEmissions * 0.9
        
    def run(self, step):
        """Executes DirectRegulation(s), Participant agents' decisions and CoordinationMechanism(s) that are related ONLY with its own Partipant(s)   """
        
        for directRegulation in self.myDirectRegulationsBefore:
                for participant in self.myParticipantsCorporations:
                    if directRegulation.checkCondition(participant, step):
                        participant.changeAttribute(directRegulation.getAttribute(), directRegulation.getValue(participant))
        
        for participant in self.myParticipantsIndividuals:
            participant.individualAction()
            
        shuffledList = self.model.random.sample(self.myParticipantsCorporations, len(self.myParticipantsCorporations))    
          
        for participant in shuffledList:
            if participant.hasDecision:
                participant.decision()
    
        for mechanism in self.myMechanisms:
            mechanism.run(shuffledList)
            
        for directRegulation in self.myDirectRegulationsAfter:
                for participant in self.myParticipantsCorporations:
                    if directRegulation.checkCondition(participant, step):
                        participant.changeAttribute(directRegulation.getAttribute(), directRegulation.getValue(participant))
                
                
class DirectRegulation():
    """
    A class used to represent an DirectRegulation policy in a carbon market simulation model.

    Attributes
    ----------
    condition : dict(str)
        condition that has to be fulfilled for the directRegulation to be applied. condition["Frequency"] can either be "Every Time" or "First Time" (the directRegulation is run every step or only during the initial step?). condition["Type"] can either be "By Periodicity" or "By Value" (the directRegulation is run periodically, or only if the agents fulfill a certain condition?).     # +condition["Attribute Name"] = Attribute name of the agent to be compared in the condition. condition["Comparator"] can either be "More Than" or "Less Than". condition["Reference Value"] is the value that the attribute will be compared with
    directRegulation : dict(str|int)
        directRegulation to be given if the condition is fulfilled. directRegulation["Attribute"] is the name of the agent's attribute to be changed. directRegulation["Value"] is the positive or negative value to be incremented or decremented to the attribute.
    order : str
        tells if the directRegulation is to be run before or after the CoordinationMechanism stage.
"""
    
    def __init__(self, condition = None, directRegulation = None, order = "Before"):  
        """DirectRegulation constructor"""
        
        self.condition = condition
        self.directRegulation = directRegulation
        self.order = order
    
    def checkCondition(self, participant, step):
        """Checks if a certain participant fulfills the defined condition """
        
        if self.condition["Frequency"] == "First Time":
            if step != 1:
                return False
        elif self.condition["Frequency"] != "Every Time":
            print("ERROR: Wrong condition frequency.")
            return False
        
        if self.condition["Type"] == "By Periodicity":
            return True
        elif self.condition["Type"] == "By Value":
            try:
                attributeValue = getattr(participant, self.condition["Attribute Name"])
            except:
                print("ERROR: Wrong condition attribute.")
                return False
            if self.condition["Comparator"] == "More Than":
                return (attributeValue >= self.condition["Reference Value"])
            elif self.condition["Comparator"] == "Less Than":
                return (attributeValue < self.condition["Reference Value"])
        else:
            print("ERROR: Wrong condition type.")
            return False
        
    def getValue(self, participant):
        return self.directRegulation["Value"]
        
    def getAttribute(self):
        return self.directRegulation["Attribute"]
                    
                
class CoordinationMechanism():
    """
    A class used to represent a Coordination Mechanism in a carbon market simulation model.

    Attributes
    ----------
    regulatorParent : object
        regulator of this mechanism
    type: str
        type of the CoordinationMechanism. Can either be an "Auction", a "Market" or a "Collective Choice"
    sequence : int
        order by which the CoordinationMechanism should be run in relation with other CoordinationMechanisms
        """
        
    def __str__(self):
        return self.name
    
    def __init__(self, mechanismProperties, sequence):
        """CoordinationMechanism constructor"""
        
        self.type = mechanismProperties["Mechanism Type"]
        self.name = mechanismProperties["Mechanism Name"]
        self.sequence = sequence
        
        if self.type == "Auction":
            self.auctionType = mechanismProperties["Auction Type"]
            if self.auctionType == "Double Auction":
                self.doubleAuctionType = mechanismProperties["Double Auction Type"]
        elif self.type == "Market":
            self.marketType = mechanismProperties["Market Type"]
            self.demand = self.demandFunction()
            pass
        elif self.type == "Collective Choice":
            pass
        else:
            print("ERROR: Wrong Mechanism Type.")
            
    def addRegulator(self, regulator):
        self.regulatorParent = regulator
        
    def run(self, participants):
        """Executes the CoordinationMechanism, involving a set of Participant agents"""

        if self.type == "Auction" and self.auctionType != "Double Auction":
            
                
            bids = []   
            successfulBids = []
                
            for participant in participants:
                if (participant.isBuyingCredits()):
                    bids.append(participant.getBid("Regulator Auction"))
            bids.sort(reverse=True, key=self.orderByBidPrice)
                
            sellingVolume = self.regulatorParent.getSellingVolume()
            unitsSold = 0
            clearingPrice = 0
            for bid in bids:
                unitsSold += bid['bidVolume']
                if unitsSold >= sellingVolume:
                    bid['bidVolume'] = bid['bidVolume'] - (unitsSold - sellingVolume)
                    clearingPrice = bid['bidPrice']
                    successfulBids.append(bid)
                    break
                successfulBids.append(bid)
                clearingPrice = bid['bidPrice']
            
            if self.auctionType == "Uniform Price":    
                for bid in successfulBids:
                    bid['buyerId'].receiveCredits(bid['bidVolume'], clearingPrice)
                            
                for participant in participants:
                    participant.setClearingPrice(clearingPrice)
                self.regulatorParent.clearingPrice = clearingPrice
            
            elif self.auctionType == "Discriminatory Price":
                for bid in successfulBids:
                    bid['buyerId'].receiveCredits(bid['bidVolume'], bid['bidPrice'])
            
                for participant in participants:
                    participant.setClearingPrice(clearingPrice)
                self.regulatorParent.clearingPrice = clearingPrice
                    
            elif self.auctionType == "Second Price":
                for i, bid in enumerate(successfulBids):
                    bid['buyerId'].receiveCredits(bid['bidVolume'], bids[i+1]['bidPrice'])
                    newClearingPrice = bids[i+1]['bidPrice']
                    
                for participant in participants:
                    participant.setClearingPrice(newClearingPrice)
                self.regulatorParent.clearingPrice = newClearingPrice
                
            else:
                raise Exception("Wrong Auction Type.")
                
        elif self.type == "Auction" and self.auctionType == "Double Auction":
            
            buyBids = []
            buyBidsExtended = []
            sellBids = []
            sellBidsExtended = []
            
            for participant in participants:
                if (participant.isBuyingCredits()):
                    buyBids.append(participant.getBid("Double Auction"))
            buyBids.sort(reverse=True, key=self.orderByBidPrice)
                
            for participant in participants:
                if (participant.isSellingCredits()):
                    sellBids.append(participant.getBid("Double Auction"))
            sellBids.sort(key=self.orderByBidPrice)

#{'buyerId': self.unique_id, 'bidPrice': price, 'bidVolume': volume}

            for buyBid in buyBids:
                for i in range(buyBid['bidVolume']):
                    buyBidsExtended.append({'buyerId': buyBid['buyerId'], 'bidPrice': buyBid['bidPrice']})
            
            for sellBid in sellBids:
                for i in range(sellBid['bidVolume']):
                    sellBidsExtended.append({'buyerId': sellBid['buyerId'], 'bidPrice': sellBid['bidPrice']})                
            
            lenBuy = len(buyBidsExtended)
            lenSell = len(sellBidsExtended)
            
            if lenBuy > lenSell:
                smallestLen = lenSell
            else:
                smallestLen = lenBuy
                
            breakeven = -1
            allFulfilled = False
            for i in range(smallestLen):
                if buyBidsExtended[i]['bidPrice'] >= sellBidsExtended[i]['bidPrice']:
#                    print(str(buyBidsExtended[i]['bidPrice']) + " - " + str(sellBidsExtended[i]['bidPrice']))
                    breakeven = i
                else:
                    break
            if breakeven + 1 == smallestLen:
                allFulfilled = True
            

           
            if breakeven != -1:
                if self.doubleAuctionType == "Average":
    
                    price = (buyBidsExtended[breakeven]['bidPrice'] + sellBidsExtended[breakeven]['bidPrice']) / 2
                    for n in range(breakeven):
                        buyBidsExtended[n]['buyerId'].receiveCredits(1,price)
                        sellBidsExtended[n]['buyerId'].sellCredits(1, price)
                    self.regulatorParent.clearingPriceDoubleAuction = price
                        
                elif self.doubleAuctionType == "McAfee":
                    if allFulfilled:
                        price = (buyBidsExtended[breakeven]['bidPrice'] + sellBidsExtended[breakeven]['bidPrice']) / 2
                    else:
                        price = (buyBidsExtended[breakeven + 1]['bidPrice'] + sellBidsExtended[breakeven + 1]['bidPrice']) / 2
                    
                    if buyBidsExtended[breakeven]['bidPrice'] >= price >= sellBidsExtended[breakeven]['bidPrice']:
                        for n in range(breakeven):
                            buyBidsExtended[n]['buyerId'].receiveCredits(1,price)
                            sellBidsExtended[n]['buyerId'].sellCredits(1, price)
                            self.regulatorParent.clearingPriceDoubleAuction = price
                    else:
                        for n in range(breakeven - 1):
                            buyBidsExtended[n]['buyerId'].receiveCredits(1,buyBidsExtended[breakeven]['bidPrice'])
                            sellBidsExtended[n]['buyerId'].sellCredits(1, sellBidsExtended[breakeven]['bidPrice'])   
                            self.regulatorParent.clearingPriceDoubleAuction = buyBidsExtended[breakeven]['bidPrice']
                            
                elif self.doubleAuctionType == "VCG":
                    for n in range(breakeven):
                        buyBidsExtended[n]['buyerId'].receiveCredits(1, sellBidsExtended[n]['bidPrice'])
                        sellBidsExtended[n]['buyerId'].sellCredits(1, buyBidsExtended[n]['bidPrice'])
                        self.regulatorParent.clearingPriceDoubleAuction = sellBidsExtended[n]['bidPrice']
                
#            for participant in participants:
#                participant.setClearingPrice(clearingPrice)
#            self.regulatorParent.clearingPrice = clearingPrice
                
        elif self.type == "Market":
            if self.marketType == "Goods Market":
                self.salesList = []
                demand = self.demandFunction()
                    
                for participant in participants:
                    if (participant.isMarketSelling()):
                        self.salesList.append(participant.getMarketOffer())
                            
                self.salesList.sort(key=self.orderBySellingPrice)
                                
                participants.sort(key=self.orderByUniqueId)
                    
                soldUntilNow = 0
                #lastPrice = 0
                for sellingOffer in self.salesList:
                    soldUntilNow += sellingOffer['saleVolume']
                    if (soldUntilNow >= demand):
                        saleVolume = sellingOffer['saleVolume'] - (demand - soldUntilNow)
                        participants[sellingOffer['sellerId'] - 100].sellItems(saleVolume, sellingOffer['salePrice'])
                        #lastPrice = sellingOffer['salePrice']
                        break
                    participants[sellingOffer['sellerId'] - 100].sellItems(sellingOffer['saleVolume'], sellingOffer['salePrice'])
                    #lastPrice = sellingOffer['salePrice']
                        
                for participant in participants:
                    if (soldUntilNow >= demand):
                        participant.wasLastDemandSatisfied = True
                    else:
                        participant.wasLastDemandSatisfied = False

                        
                        
        elif self.type == "Collective Choice":
            raise NotImplementedError()
                
    def orderByBidPrice(self, d):
        return d['bidPrice']
    
    def orderBySellingPrice(self, d):
        return d['salePrice']
    
    def orderByUniqueId(self, d):
        return d.unique_id
    
    def demandFunction(self):
        raise NotImplementedError()
    
    
class CustomParticipant(Participant):
    
    def __init__(self, model, participantID, participantProperties, initialAttributes):
        super().__init__(model, participantID, participantProperties, initialAttributes)
        
        self.firstIteration = True
        
        self.biddingStrategy = -1
        self.propensityBiddingStrategy = [1,1,1]
        self.probabilityBiddingStrategy = [1/3, 1/3, 1/3]
        self.lastClearingPrice = -1
                
        self.creditsCost = 0
        self.Penalty = 0
        self.profit = 0
        self.sales = self.CostPerProduct * (self.ProfitRate + 1) * self.Production
        self.itemsSold = self.Production
        self.Emissions = self.Production * self.EmissionsPerProduct
        
        
        
    def calculateBiddingStrategy(self):
        if self.biddingStrategy == -1:
            return self.model.random.randint(1,4) 
        else:
            sum = 0
            EXPERIMENT = 0.1
            RECENCY = 0.2
            for idx, prop in enumerate(self.propensityBiddingStrategy):
                self.propensityBiddingStrategy[idx] = (1-RECENCY) * prop + self.gamma(idx, EXPERIMENT)
                sum += abs(self.propensityBiddingStrategy[idx])
                
            for idx, prob in enumerate(self.probabilityBiddingStrategy):
                self.probabilityBiddingStrategy[idx] = self.propensityBiddingStrategy[idx] / sum
            
            rand = self.model.random.uniform(0, 1)
            if (rand < self.probabilityBiddingStrategy[1]):
                return 1
            if (rand < (self.probabilityBiddingStrategy[1] + self.probabilityBiddingStrategy[2])):
                return 2
            return 3

    def gamma(self, strategy, EXPERIMENT):
        if (strategy == self.biddingStrategy):
            return (1 - EXPERIMENT) * self.profit
        else:
            return EXPERIMENT * self.profit / 2
        
    def calculateEmissions(self):
         return int(round(self.Production * self.EmissionsPerProduct))
     
    def calculateProfit(self):
        fabricationCost = self.CostPerProduct * self.Production
        profit = self.sales - fabricationCost - self.creditsCost - self.Penalty
#        if self.Penalty > 0 and self.unique_id == 101:
#            print("PENALTY: " + str(self.Penalty))
        self.creditsCost = 0
        self.Credits = 0
        return profit
    
    def calculateNewOutput(self):
        difference = self.profit - self.previousProfit
        deltaProfit = 0.02 * abs(self.previousProfit)
        
        #if(self.unique_id == 102):
        #    print("EmissionsPerProduct: " + str(self.EmissionsPerProduct))
        #    print("Last Market Price: " + str(self.lastMarketPrice))
        #    print("Production: " + str(self.Production))
        #    print("Profit: " + str(self.profit))
        if ((difference > deltaProfit) and (self.profit > 0) and (difference > 0)) or ((self.profit >= 0) and (self.wasLastDemandSatisfied == False)):
            self.productionIncreased = True
            self.productionDecreased = False
        #    if(self.unique_id == 102):
        #        print("Production + \n")
            return self.Production * (1 + 0.01)
        elif (difference < -deltaProfit) or (self.itemsSold <= 0.80 * self.Production) or (self.profit <= 0):
            self.productionIncreased = False
            self.productionDecreased = True
        #    if(self.unique_id == 102):
        #        print("Production - \n")
            if(self.Production <= 50):
                return 0
            return self.Production * (1 - 0.01)
        else:
            self.productionIncreased = False
            self.productionDecreased = False
        #    if(self.unique_id == 102):
        #        print("Production 0 \n")
            return self.Production
        
    def calculateReservationPrice(self):
        if (self.Emissions == 0):
            return 0
        pv = (self.sales - self.CostPerProduct * self.Production) / self.Emissions
        #print("pv: " + str(pv))
        if pv > 0:
            return pv
        else:
            return 0

    def receiveCredits(self, numberOfCredits, price):
        self.Credits += numberOfCredits
        self.creditsCost = numberOfCredits * price
        
    def sellCredits(self, numberOfCredits, price):
        self.Credits -= numberOfCredits
        self.creditsCost = -abs(numberOfCredits * price)    
    
    def setClearingPrice(self, clearingPrice):
        self.lastClearingPrice = clearingPrice
    
    def decision(self):
        if self.firstIteration:
            self.previousProfit = self.calculateProfit()
        else:
            self.previousProfit = self.profit
        self.profit = self.calculateProfit()
                
        #decisão de produção
        if not self.firstIteration:
            self.oldProduction = self.Production
            self.Production = int(round(self.calculateNewOutput()))
        self.Emissions = self.calculateEmissions()
        
        self.biddingStrategy = self.calculateBiddingStrategy()
        self.reservationPrice = self.calculateReservationPrice()
        
        self.sales = 0
        self.itemsSold = 0
        self.firstIteration = False
        
    def priceFunction(self, auctionType):
        if auctionType == "Double Auction" and self.isSellingCredits():
            self.myPrice = self.lastClearingPrice * 1.10
            
        elif auctionType == "Double Auction" and self.isBuyingCredits() and self.lastClearingPrice != -1:
            self.myPrice = self.reservationPrice
        else:
            if (self.lastClearingPrice == -1):
                self.myPrice = self.model.random.uniform(0, self.reservationPrice + 1)
                return self.myPrice
            
            if (self.biddingStrategy == 1):
                prob = 3/4
            elif (self.biddingStrategy == 2):
                prob = 1/2
            elif (self.biddingStrategy == 3):
                prob = 1/4
            else:
                prob = 3/4
            
            self.myPrice = self.lastClearingPrice + prob * (self.reservationPrice - self.lastClearingPrice)
            
        return self.myPrice
    
    def getBidVolume(self, auctionType):
        if auctionType == "Regulator Auction" and self.Emissions > self.Credits:
            factor = 1.30
        else:
            factor = 1
        
        return abs(self.Emissions - self.Credits) * factor        
    
    def isMarketSelling(self):
        return self.Production > 0
    
    def getMarketOffer(self):
        price = self.getMarketPrice()
        volume = self.Production
        sale = {'sellerId': self.unique_id, 'salePrice': price, 'saleVolume': volume}
        return sale
    
    def getMarketPrice(self):
        value = self.CostPerProduct * (1 + self.ProfitRate) + (self.creditsCost / self.Production) 
        self.lastPenalty = self.Penalty
        self.Penalty = 0
        self.lastMarketPrice = value
        #print("Cost Per Product: " + str(self.CostPerProduct))
        #print("Emissions Per Product: " + str(self.EmissionsPerProduct))
        #print("Credits Cost: " + str(self.creditsCost))
        #print("Production: " + str(self.Production))
        #print(str(value))
        
        return value
        
    def sellItems(self, volume, price):
        self.itemsSold = volume
        self.sales = volume * price
        
class CreditsPenalty(DirectRegulation):
    
    def __init__(self, penaltyFactor, condition = None, directRegulation = None, order = "Before"):  
        super().__init__(condition, directRegulation, order)
        self.penaltyFactor = penaltyFactor
    
    def checkCondition(self, participant, step):
        return participant.Emissions > participant.Credits
    
    def getValue(self, participant):
        return self.penaltyFactor * participant.lastClearingPrice * (participant.Emissions - participant.Credits)
        
    def getAttribute(self):
        return "Penalty"
    
class CarbonTax(DirectRegulation):
    
    def __init__(self, carbonTax, condition = None, directRegulation = None, order = "Before"):  
        super().__init__(condition, directRegulation, order)
        self.carbonTax = carbonTax
    
    def checkCondition(self, participant, step):
        return True
    
    def getValue(self, participant):
        return self.carbonTax * participant.Emissions
    
    def getAttribute(self):
        return "Penalty"
    
class CustomMechanism(CoordinationMechanism):
    
    def demandFunction(self):
        
        return 1000 * 10000 #Number of Agents * Initial Production
    
    

            
        
def positiveNormal(mean, sigma):
    x = np.random.normal(mean,sigma)
    return(x if x>=0 else positiveNormal(mean,sigma))

def compute_emissions(model):
    sum = 0
    for participant in model.participantsCorporations:
        sum += participant.Emissions
    return sum

def compute_supply(model):
    sum = 0
    for participant in model.participantsCorporations:
        sum += participant.Production
    return sum

def compute_increased(model):
    sum = 0
    for participant in model.participantsCorporations:
        if participant.productionIncreased == True:
            sum += 1
    return sum

def compute_decreased(model):
    sum = 0
    for participant in model.participantsCorporations:
    
        if participant.productionDecreased == True:
            sum += 1
    return sum


def compute_creditsCost(model):
    sum = 0
    for participant in model.participantsCorporations:
        sum += participant.creditsCost
    return sum

def compute_clearingPrice(model):
    sum = 0
    for regulator in model.regulators:
        sum += regulator.clearingPrice
    return sum

def compute_clearingPriceDoubleAuction(model):
    sum = 0
    for regulator in model.regulators:
        sum += regulator.clearingPriceDoubleAuction
    return sum


def compute_topfiftypolluters(model):
    sum = 0
    for idx in model.topFiftyPolluters:
        sum += model.participants[idx - 100].Emissions
    return sum

def compute_topfiftyefficients(model):
    sum = 0
    for idx in model.topFiftyMoreEfficient:
        sum += model.participants[idx - 100].Emissions
    return sum

def compute_middleefficients(model):
    sum = 0
    for idx in model.middleList:
        sum += model.participants[idx - 100].Emissions

def compute_topfiftypolluterssupply(model):
    sum = 0
    for idx in model.topFiftyPolluters:
        sum += model.participants[idx - 100].Production
    return sum

def compute_topfiftyefficientssupply(model):
    sum = 0
    for idx in model.topFiftyMoreEfficient:
        sum += model.participants[idx - 100].Production
    return sum

def compute_middlesupply(model):
    sum = 0
    for idx in model.middleList:
        sum += model.participants[idx - 100].Production
    return sum

dc = DataCollector(model_reporters={ "Emissions": compute_emissions, "Supply": compute_supply, "Top Fifty Polluters Supply": compute_topfiftypolluterssupply, "Top Fifty Efficient Supply": compute_topfiftyefficientssupply, "Average Polluters Supply": compute_middlesupply, "Clearing Price": compute_clearingPrice, "Clearing Price Double Auction": compute_clearingPriceDoubleAuction})


myModel = CustomModel()
myModel.reset_randomizer(200)
myModel.addDataCollector(dc)

for i in range(1000):

    myCustomParticipant = CustomParticipant(myModel, i + 100, {"Type": "Corporation", "Price Reasoning": "Price Function", "Initial Price": 0, "Decision": True}, {"Credits":0, "Emissions":0, "Production": 10000, "EmissionsPerProduct": positiveNormal(0.1, 0.01), "CostPerProduct": 20, "ProfitRate": 0.1})
    myModel.addParticipantObject(myCustomParticipant)
    
#for i in range(1000):
#    myModel.addParticipant({"Type": "Individual"}, {"Credits": 0})

myModel.addRegulator({"Priority": 1, "Aggregator": False}, "All")


#myModel.addDirectRegulationToRegulator(1, {"Type": "By Periodicity", "Frequency": "Every Time"}, {"Attribute":"Credits", "Value": 1000 * 0.95}, order = "Before")




myModel.addMechanismToRegulator(1, {"Unit": "Credits",
                                    "Mechanism Name": "Carbon Auction",
                                    "Mechanism Type": "Auction",
                                    "Auction Type": "Uniform Price"}, 1)

myModel.addMechanismToRegulator(1, {"Unit": "Credits",
                                    "Mechanism Name": "Carbon Auction",
                                    "Mechanism Type": "Auction",
                                    "Auction Type": "Double Auction",
                                    "Double Auction Type": "Average"}, 2)

myCustomMechanismMarket = CustomMechanism({"Unit": "Goods",
                                    "Mechanism Name": "Goods Market",
                                    "Mechanism Type": "Market",
                                    "Market Type": "Goods Market"}, 3)

myModel.addMechanismObjectToRegulator(1, myCustomMechanismMarket)


myDirectRegulation1 = CreditsPenalty(5, order="After")
#myDirectRegulation2 = CarbonTax(16, order="After")

myModel.addDirectRegulationObjectToRegulator(1, myDirectRegulation1)
#myModel.addDirectRegulationObjectToRegulator(1, myDirectRegulation2)




#--- Visualização
#def participant_portrayal(participant):
#    if participant is None:
#        return
#    portrayal = {"Shape": "rect", "w":1, "h":1, "Filled": "true", "Layer":0}
#    
#    (x,y) = participant.get_position()
#    portrayal["x"] = x
#    portrayal["y"] = y

#myModel.addVisualization(elementList, "Carbon Market", None)

            
print(myModel)

for i in range(2500):
    print(i)
    #print(myModel)
    myModel.step()
    

df = myModel.datacollector.get_model_vars_dataframe()



plt.plot(df['Emissions'])
plt.title('Total Emissions')
plt.xlabel('N of Ticks')
plt.ylabel('Emissions (tCO2)')
plt.show()

df['Emissions Rolling'] = df['Emissions'].rolling(window=100).mean()
plt.plot(df['Emissions Rolling'])
plt.title('Total Emissions Rolling')
plt.xlabel('N of Ticks')
plt.ylabel('Emissions (tCO2)')
plt.show()


df['Supply Rolling'] = df['Supply'].rolling(window=100).mean()
df.plot(y=['Supply Rolling'])
plt.title('Supply Rolling')
plt.xlabel('N of Ticks')
plt.ylabel('N of Products')
plt.show()



df.plot(y=['Average Polluters Supply', 'Top Fifty Polluters Supply',  'Top Fifty Efficient Supply'])
plt.title('Top-50 Production')
plt.xlabel('N of Ticks')
plt.ylabel('N of Products')
plt.show()

plt.plot(df['Clearing Price'])
plt.title("Clearing Price")
plt.xlabel("N of Ticks")
plt.ylabel("Price (€)")
plt.show()

df['Clearing Price Rolling'] = df['Clearing Price'].rolling(window=100).mean()
plt.plot(df['Clearing Price Rolling'])
plt.title("Clearing Price Rolling")
plt.xlabel("N of Ticks")
plt.ylabel("Price (€)")
plt.show()

df['Clearing Price Double Auction Rolling'] = df['Clearing Price Double Auction'].rolling(window=100).mean()
plt.plot(df['Clearing Price Double Auction Rolling'])
plt.title("Clearing Price Double Auction Rolling")
plt.xlabel("N of Ticks")
plt.ylabel("Price (€)")
plt.show()

df.to_csv("Uniform_Price_Average.csv")
            


#TODO CLEARING PRICE DOS DOIS MECANISMOS
    