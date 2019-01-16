
from random import uniform
import time 


def main() : 
#    compteur d'un clycle 
    q = float(input(" Enter the Relative Hashrate of the Selfish Miner : "))
    n = int(input(" Enter the Number of cycle's attacks : "))
    win= simulate(n,q)

    #print("win : ",win)
#transition : avec des randoms p & q 

## Decorate - Time to exceute the simulation 
def dec(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        print("--- T = %s seconds ---" % (time.time() - start_time))
    return wrapper 

@dec
def simulate(n,q): 
    i = 0         # Honest Miner au stade 0 
    j = 0         # Selfish Mier au stade 0 
    
    M = 0         # nb of block Blockchain Official 
    R = 0         # nb of official blocks mined by the attacker in the 
    H = 0         # nb of honest blocks mines by the honest miners after n attack cycles

    i_block = 0  
    j_block = 0 

    i_orphan = 0  # orphan honest miner blocks 
    j_orphan = 0  # orphan selfish miner blocks 
    
    # faire la variable aleatoire sur  q 
   
    attack = 1   

    
   # faire un 
    while ( attack < n): 
        p = uniform(0,1)
        #si p > alpha ( puissance  de calcul des s)
        print(" \n attack n°",attack, "\np :", p, "q:",q)
        if p < q : 
            print("Selfish Miner found a block ")
            # SM found a block first 
            j_block  += 1 #nb of block on the fork 
            i_orphan += 1
            
            if wait(i,j_block): 
                attack + 1 
                print("The Selfish Miner continue his attack ")
            
            if abandon(i,j_block):
                print ("The Selfish Miner abandon his attack")
                j = i 
                #return False 
            
            if override(i,j_block): 
                j += j_block
                i_orphan +=1 
                i = j 
                print("The selfish Miner win and override the official Blockchain, the official Blockchain is now containing ",i,"blocks with",j_block,"blocks commit from the attacker")
                return True 
        else :
            attack   += 1 
            i_block  += 1
            j_orphan += 1 
            i = i_block   #le bloc est publie sur la blockchain   
            print(" An Honest miner found a block, the official blockchain is now ",i)
    
        print( "(",i,",", j_block,")") 
        print("Nb of block on the selfish miner fork ",j_block )
    print( "Ophan RATIO : " )
    print("") 

   #  O = (i_orphan + j_orphan ) / M * 100 # % of orphan block 
    # hasrate = R/M # Long terme apparent has

  
    
def override(i,j):
    if i > 0  and j ==  i+1 : 
        return True  
    else : 
        return False 

def wait(i,j) :
    if i == j or i == 0 :
        return True 
    else :
         return False  
    #return j > i +1 

def abandon(i,j):
    if i == j+1 :
        return True  
    else : 
        return False 


#j * fonction indicatrice 

#  INPUT : n =nb of attack cycle 
#          q = relative hasrate 
#          gama = 

#  OUTPUT :  nb of official block mined in the official blockchain  at the end of n attack cycles 
#            nb of block mined by the attacker in the official blockchain after n attack cycles 
#            Probality Ratio 2/1 ( honnest and attackant)

main()