from random import uniform

class Simulator(object):
    def __init__(self,*args):
        self.alpha = input("Alpha : ")
        self.gamma = input("Gamma : ")
        self.cycle = input("Cycle : ") 
        self.difficulty = input("Difficulty : ")

        self.public_chain   = []  #list of  block of the official Blockchain 
        self.private_chain  = []  # list of block of the Selfish Miner Blockchain 
        
      
        #OUTPUT 
        self.honnest_orphan     = 0   # nb of unpublished block of the honest miner 
        self.selfish_orphan     = 0   # nb of unpublished block of the selfish miner
        self.selfish_blocks     = 0 
        self.honnest_blocks     = 0 
        self.honnest_bis_blocks = 0 
        self.total_blocks       = 0 

    @property
    def alpha(self):
        return self.__alpha
    @alpha.setter
    def alpha(self,value):
        if not isinstance (value,float):
            try : 
                value = float(value)
            except Exception as e :    
                raise TypeError("Alpha's value must be a float")
        else : 
            self.__alpha=value  

    @property
    def gamma(self):
        return self.__gamma
    @gamma.setter
    def gamma(self,value):
        if not isinstance (value,float):
            try : 
                value = float(value)
            except Exception as e :               
                raise TypeError("Gamma's value must be a float")
        else : 
            self.__gamma=value         


    @property
    def cycle(self):
        return self.__cycle
    @cycle.setter
    def cycle(self,value):
        if not isinstance (value,int):
            try : 
                value = int(value)
            except Exception as e : 
                raise TypeError("Cycle's value must be a integer")
        else : 
            self.__cycle = value  

 # Simulate awarding a Bitcoin block
 #  a => Percent of the total network owned by the selfish mining pool
 #  g => If two branches are competing, g (gamma) is the percent of the
 #       honest miners which join the selfish mining pool in mining on
 #       top of the selfish block
    
    def getFirstMiner(self,a,g) : 
        rnd = uniform(0,1)

        if rnd >a and rnd <= (a+(1-a)*g) : 
            #HM found a block on top of the selfish blockchain
            return 1 
        
        if rnd > (a + (1-a) * g) :
            # HM found a block first on the official Blockchain
            return 0 

        else : 
            # SM found a block 
            return -1 
        
    def override(self) :
        self.public_chain = []
        for private_block in self.private_chain : 
            self.public_chain.append(private_block)

    def fork(self):
        self.private_chain = []
        for public_block in self.public_chain :
            self.private_chain.append(public_block)

    def show_public_chain(self):
        res = "PUBLIC BLOCKS : "
        for block in self.public_chain : 
            res += str(block) + " , " 
        print(res)

    def show_private_chain(self):
        res = "PRIVATE BLOCKS : "
        for block in self.private_chain : 
            res += str(block) + " , " 
        print(res)

    def cycle_attack(self): 
        attack = True 
        selfish_blocks = 0 
        while attack :
            delta = len(self.private_chain) - len(self.public_chain)
            #Initial
            if delta == 0 :
                #print("Delta == 0 ")
                if selfish_blocks == 1 : 
                    res = self.getFirstMiner(self.alpha,self.gamma)
                    if res == 0 : 
                        #print("HM found a block first")
                        #print("End of attack : SM abandon")
                        self.public_chain.append(0)
                        attack = False 
                    if res == 1 : 
                        #print("SM found a block first on PRIVATE CHAIN")
                        #print("End attack : override official Blockchain")
                        self.private_chain.append(1)
                        self.override()
                        attack = False   
                    if res == -1 : 
                       # print("SM found a block first")
                       # print("End attack : override official Blockchain ")    
                        self.private_chain.append(-1)
                        selfish_blocks   += 1
                        self.override()
                        attack = False 
                else : # initial 
                    res = self.getFirstMiner(self.alpha,0)
                    if res == 0 :
                        #print("HM found a block first")
                        self.public_chain.append(0)
                    if res == -1 : 
                        #print("SM found a block first")
                        selfish_blocks += 1
                        self.private_chain.append(-1) 
            if delta == 1 : 
                #print("delta == 1 ")
                res = self.getFirstMiner(self.alpha,self.gamma)
                if res == 0 : 
                   # print("HM found a block first on PUBLIC chain")
                    self.public_chain.append(0)
                if res == 1 : 
                   # print("SM found a block first on PRIVATE CHAIN")
                   # print("end attack : override official Blockchain")
                    self.private_chain.append(1)
                    self.override()
                    attack = False 
                if res == -1 : 
                   # print("SM found a block first")
                    selfish_blocks += 1 
                    self.private_chain.append(-1)
                    self.override()
                    attack = False 
                   # print("end attack : override official Blockchain ")
            if delta == -1 :
                # print("Delta == -1 ")
                res = self.getFirstMiner(self.alpha,0)
                if res == 0 : 
                    #print("HM found a block first")
                    self.public_chain.append(0)
                    attack = False 
                    #print("end attack : SM abandon") 
                if res == -1 : 
                    #print("SM found a block first")
                    selfish_blocks +=1 
                    self.private_chain.append(-1) 
        selfish_blocks = 0 
        self.fork()

    def runSimulation(self): 
        print("runSimulation methode")
        i = 0 
        while i<self.cycle :
            i+=1         
            if len(self.private_chain) != len(self.public_chain) : 
                raise TypeError (" DELTA != 0 ")
            else : 
                self.cycle_attack()
        

    def annalizeBlocks(self): 
        for block in self.public_chain :
            if block ==  1 :
                self.honnest_bis_blocks += 1
            if block ==  0 :
                self.honnest_blocks += 1 
            if block == -1: 
                self.selfish_blocks += 1
            self.total_blocks +=1 

    def getResult(self):
        self.runSimulation()
        self.annalizeBlocks()
        print("o     Blocks in the public chain   : " + str(self.total_blocks))
        print("o     Blocks mined by the SM pools : " + str(self.selfish_blocks))
        print("o     Blocks mined by the HM pools : " + str(self.total_blocks - self.selfish_blocks))
        print("       -> Mined on top of HM chain : " + str(self.honnest_blocks))
        print("       -> Mined on top of SM chain : " + str(self.honnest_bis_blocks))
        



def main(): 
    simule = Simulator()
    simule.getResult()
#simule.cycle_attack()
    #simule.test()

main()