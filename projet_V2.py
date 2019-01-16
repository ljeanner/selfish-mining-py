#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import uniform 

def main() :
    q = float(input(" Enter the Relative Hashrate of the Selfish Miner : "))
    n = int(input(" Enter the Number of cycle's attacks : "))
    simulate(n,q)

def getTotalSMBlock(n_chain):
    selfish_block = 0 
    for block in n_chain : 
        if block == 0 : 
            selfish_block += 1 
    return selfish_block

def simulate(cylce_attack,sm_hashrate): 
    nb_attack = 0

    public_chain   = []  # nb of  block on the official Blockchain 
    private_chain  = []  # nb of block on the Selfish Miner Blockchain 
    selfish_branch = 0 

    honnest_orphan  = 0  # nb of unpublished block of the honest miner 
    selfish_orphan = 0   # nb of unpublished block of the selfish miner 


    while (nb_attack < cylce_attack):
        print("Cycle n° ",nb_attack )
        continue_cycle = True 
        while continue_cycle : 
            hm_hashrate = uniform(0,1) # relative hasrate of the honest miner
            gamma = uniform(0,1)
            delta = len(private_chain)-len(public_chain)
            if delta == 1 and selfish_branch == 1 : 
                gamma = uniform(0,1)
                print(gamma)
            else :
                gamma = 0 

            if hm_hashrate < sm_hashrate and gamma < sm_hashrate : 
                print("SM found block ")
                selfish_branch +=1 
                private_chain.append(0)
                honnest_orphan +=1 
                delta = len(private_chain)-len(public_chain)
                print("public : ",len(public_chain))
                print("pivate : ", len(private_chain))
                print("DELTA =",delta)
                if delta == 2 and selfish_branch == 2 : 
                    public_chain = private_chain
                    continue_cycle = False 
            if sm_hashrate < hm_hashrate and gamma < hm_hashrate : 
                print("Honest Miner found block ") 
                public_chain.append(1)
                selfish_orphan += 1
                delta = len(private_chain) - len(public_chain)
                print("public : ",len(public_chain))
                print("pivate : ", len(private_chain))
                print("DELTA =",delta)
                
               
                if delta == 0 : 
                    #SM abandon 
                    private_chain  = public_chain
                    continue_cycle = False 
                if delta == 2 : 
                    # Override 
                    public_chain = private_chain
                    continue_cycle = False 
                
                if delta == -2 : 
                    continue_cycle = False 

            if gamma > sm_hashrate and gamma > hm_hashrate : 
                print("gamma = ", gamma)
                print("Some Honnest Miners are mining on private chain")
                private_chain.append(1)
                selfish_orphan +=1 
                continue_cycle = False 
        print("END OF ATTACK / FORK THE PUBLIC BLOCKCHAIN ")
        selfish_branch = 0
        private_chain = public_chain 
        nb_attack +=1 

    M = len(public_chain)
    selfish_block = getTotalSMBlock(public_chain)
    honest_block =M - selfish_block 

    print(" Nb of Blocks  :", M)
    print(" Total Selfish Miner Blocks :", selfish_block)
    

main()