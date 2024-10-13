import random
from individual import Individual
from predator import Predator
from food import Food


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class World:
    def __init__(self,indiPop,predPop,foodCount,mutationChance,width,height,predSpeed,indiSpeed,foodSize,predSize,indiSize,indiVisionRange,predVisionRange):
        self.indiPop = indiPop
        self.predPop = predPop
        self.foodCount = foodCount
        self.mutationChance = mutationChance
        self.width = width
        self.height = height
        self.predSpeed = predSpeed
        self.indiSpeed = indiSpeed
        self.foodSize = foodSize
        self.predSize = predSize
        self.indiSize = indiSize
        self.indiVisionRange = indiVisionRange
        self.predVisionRange = predVisionRange
    
    def spawn(self,indiPop,predPop,foodCount):
        self.indiPop = indiPop
        self.predPop = predPop
        self.foodCount = foodCount
        # self,hp,vision,speed,mateSelectionProb,color,visionRadius,width,height,size
        indis = [Individual(100,random.randint(10,self.indiVisionRange),self.indiSpeed,0.5,GREEN,self.width,self.height,self.indiSize,self.indiVisionRange) for i in range(self.indiPop)]
        # self,hp,vision,speed,mateSelectionProb,color,width,height,predSize,maxVision
        preds = [Predator(150,random.randint(10,self.predVisionRange),self.predSpeed,0.5,RED,self.width,self.height,self.predSize,self.predVisionRange) for i in range(self.predPop)]
        food = [Food(100,random.randint(0,self.width),random.randint(0,self.height),self.foodSize) for i in range(self.foodCount)]
        self.indis = indis
        self.preds = preds
        self.food = food


    def endGeneration(self):
        # TODO : Randomly select one individual and one predator, compare they're stats and kill accordlingly

        indis = []
        for i in self.indis:
            if i.hp>0 and i.generation<2:
                indis.append(i)
        self.indis = indis
        self.indiPop = len(indis)

        preds = []
        for i in self.preds:
            if i.hp > 0 and i.generation<2:
                i.incerementGeneration()
                preds.append(i)
        self.preds = preds
        self.predPop = len(preds)

        #---- Preprocessing for biased random as we don't need to precompute this again and again ----#
        fitnessSum_indi = 0
        for i in self.indis:
            fitnessSum_indi += i.getFitness()
        individual_probs_indi = [i.getFitness()/fitnessSum_indi for i in self.indis]
        cumulative_probs_indi = []
        cumulativeSum_indi = 0
        for i in range(self.indiPop):
            cumulativeSum_indi += individual_probs_indi[i]
            cumulative_probs_indi.append(cumulativeSum_indi)
        self.probs_indi = cumulative_probs_indi


        fitnessSum_pred = 0
        for i in self.preds:
            fitnessSum_pred += i.getFitness()
        predvidual_probs_pred = [i.getFitness()/fitnessSum_pred for i in self.preds]
        cumulative_probs_pred = []
        cumulativeSum_pred = 0
        for i in range(self.predPop):
            cumulativeSum_pred += predvidual_probs_pred[i]
            cumulative_probs_pred.append(cumulativeSum_pred)
        self.probs_pred = cumulative_probs_pred
    
    def selectParents(self,indiOrpred):
        if indiOrpred == 'indi':
            indi1 = self.indis[random.randint(0,self.indiPop-1)]
            if random.random() < indi1.mateSelectionProb:
                indi2 = self.tournamentSelection(indiOrpred)
            else:
                indi2 = self.biasedRandomSelection(indi1,indiOrpred)
            return indi1,indi2
        else:
            pred1 = self.preds[random.randint(0,self.predPop-1)]
            if random.random() < pred1.mateSelectionProb:
                pred2 = self.tournamentSelection(indiOrpred)
            else:
                pred2 = self.biasedRandomSelection(pred1,indiOrpred)
            return pred1,pred2
    
    def tournamentSelection(self,indiOrpred):
        if indiOrpred == 'indi':
            indi2 = self.indis[random.randint(0,self.indiPop-1)]
            indi3 = self.indis[random.randint(0,self.indiPop-1)]
            while indi2 == indi3:
                indi3 = self.indis[random.randint(0,self.indiPop-1)]
            if indi2.getFitness() > indi3.getFitness():
                return indi2
            else:
                return indi3
        else:
            pred2 = self.preds[random.randint(0,self.predPop-1)]
            pred3 = self.preds[random.randint(0,self.predPop-1)]
            while pred2 == pred3:
                pred3 = self.preds[random.randint(0,self.predPop-1)]
            if pred2.getFitness() > pred3.getFitness():
                return pred2
            else:
                return pred3

    def biasedRandomSelection(self,creature,indiOrpred):
        if indiOrpred == 'indi':
            hasGotPair = False
            while hasGotPair == False:
                selectedValue = random.random()
                for i in range(self.indiPop):
                    if selectedValue <= self.probs_indi[i]:
                        if self.indis[i] != creature:
                            return self.indis[i]
                        break
        else:
            hasGotPair = False
            while hasGotPair == False:
                selectedValue = random.random()
                for i in range(self.predPop):
                    if selectedValue <= self.probs_pred[i]:
                        if self.preds[i] != creature:
                            return self.preds[i]
                        break
    
    def crossover(self,creature1,creature2,indiOrPred):
        parents =[creature1,creature2]

        hp1 = parents[random.randint(0,1)].hp
        vision1 = parents[random.randint(0,1)].vision
        speed1 = parents[random.randint(0,1)].speed
        mateSelectionProb1 = parents[random.randint(0,1)].mateSelectionProb

        hp2 = parents[0 if hp1==1 else 1].hp
        vision2 = parents[0 if vision1==1 else 1].vision
        speed2 = parents[0 if speed1==1 else 1].speed
        mateSelectionProb2 = parents[0 if mateSelectionProb1==1 else 1].mateSelectionProb
        if indiOrPred == 'indi':

            child1 = Individual(hp1,vision1,speed1,mateSelectionProb1,parents[0].color,self.width,self.height,parents[0].indiSize,parents[0].maxVision)
            child1 = self.mutate(child1)
            child2 = Individual(hp2,vision2,speed2,mateSelectionProb2,parents[0].color,self.width,self.height,parents[0].indiSize,parents[0].maxVision)
            child2 = self.mutate(child2)
            return child1,child2
        else:
            child1 = Predator(hp1,vision1,speed1,mateSelectionProb1,parents[0].color,self.width,self.height,parents[0].predSize,parents[0].maxVision)
            child1 = self.mutate(child1)
            child2 = Predator(hp2,vision2,speed2,mateSelectionProb2,parents[0].color,self.width,self.height,parents[0].predSize,parents[0].maxVision)
            child2 = self.mutate(child2)
            return child1,child2
        

    def mutate(self,creature):
        if random.random() < self.mutationChance:
            newVision = min(creature.vision + random.randint(-10,10),creature.maxVision)
            newSpeed = creature.speed + random.uniform(0.1,0.1)
            newHp = creature.hp + random.randint(-10,10)
            newMateSelectionProb = creature.mateSelectionProb + random.randint(-10,10)/100

            creature.vision = newVision
            creature.speed = newSpeed
            creature.hp = newHp
            creature.mateSelectionProb = newMateSelectionProb
            return creature
        return creature

    def newGeneration(self):
        self.endGeneration()
        indis = []
        for i in range(self.indiPop//2):
            parent1 , parent2 = self.selectParents('indi')
            child1 , child2 = self.crossover(parent1,parent2,'indi')
            indis.append(child1)
            indis.append(child2)
            indis.append(parent1)
            indis.append(parent2)
        self.indis = indis
        self.indiPop = len(indis)
        
        preds = []
        for i in range(self.predPop//2):
            parent1 , parent2 = self.selectParents('pred')
            child1 , child2 = self.crossover(parent1,parent2,'pred')
            preds.append(child1)
            preds.append(child2)
            preds.append(parent1)
            preds.append(parent2)
        self.preds = preds
        self.predPop = len(preds)
        
        self.food = [Food(10,random.randint(0,self.width),random.randint(0,self.height),self.foodSize) for i in range(self.foodCount)]

        # self.preds = [Predator(100,random.randint(10,self.predVisionRange),self.predSpeed,0.5,RED,self.width,self.height,self.predSize,self.predVisionRange) for i in range(self.predPop)]

    def getBestIndi(self):
        bestFitness = -float('inf')
        bestIndi = None
        for i in self.indis:
            fitness = i.getFitness()
            if fitness > bestFitness:
                bestFitness = fitness
                bestIndi = i
        return bestIndi

    def getStats(self,gen):
        vision_indi = []
        mateSelectionProb_indi = []
        speed_indi = []
        for i in self.indis:
            vision_indi.append(i.vision)
            mateSelectionProb_indi.append(i.mateSelectionProb)
            speed_indi.append(i.speed)
        
        vision_pred = []
        mateSelectionProb_pred = []
        speed_pred = []
        for i in self.preds:
            vision_pred.append(i.vision)
            mateSelectionProb_pred.append(i.mateSelectionProb)
            speed_pred.append(i.speed)
        
        stats = {
            "gen" : gen,
            "max_speed_indi" : max(speed_indi),
            "max_matSelectionProb_indi" : max(mateSelectionProb_indi),
            "max_vision_indi" : max(vision_indi),
            "avg_speed_indi" : sum(speed_indi)/len(speed_indi),
            "avg_matSelectionProb_indi" : sum(mateSelectionProb_indi)/len(mateSelectionProb_indi),
            "avg_vision_indi" : sum(vision_indi)/len(vision_indi),
            "population_indi" : len(self.indis),

            "max_speed_pred" : max(speed_pred),
            "max_matSelectionProb_pred" : max(mateSelectionProb_pred),
            "max_vision_pred" : max(vision_pred),
            "avg_speed_pred" : sum(speed_pred)/len(speed_pred),
            "avg_matSelectionProb_pred" : sum(mateSelectionProb_pred)/len(mateSelectionProb_pred),
            "avg_vision_pred" : sum(vision_pred)/len(vision_pred),
            "population_pred" : len(self.preds),
        }
        return stats


    
        
