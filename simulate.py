#!/usr/bin/env python3

from random import *

class Simulator(object):
	def __init__(self,*args):
		self.alpha  = input("Alpha : ")
		self.gamma  = input("Gamma : ")
		self.cycle  = input("Cycle : ") 
		self.adjust = False
	
		
		self.public_chain       = []  # list of  block of the official Blockchain 
		self.private_chain      = []  # list of block of the Selfish Miner Blockchain 
		
		self.save_time 			= []
		self.t0                 = 600 # Average Time to  mine a block 
		self.t2016				= 0 
		self.time_public        = 0   # Time to mine 2016 blocks in the official chain
		self.time_private       = 0   # Time to mine 2016 blocks in the SM fork
		self.lambda_HM          = 0   # Time to mine a block for HM
		self.lambda_SM          = 0   # Time to mine a block for SM  
		self.delta 				= 1   # if =! 1 need to ajust difficulty 
		self.difficulty		    = 1   # Difficulty adjusted every 2016 blocs 

		#OUTPUT 
		self.time_dico 			= {}
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
		if not isinstance(value, float):
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
		if not isinstance(value, float):
			try : 
				value = float(value)
			except Exception as e :               
				raise TypeError("Gamma's value must be a float")
		else : 
			self.__gamma = value      


	@property
	def cycle(self):
		return self.__cycle
	@cycle.setter
	def cycle(self, value):
		if not isinstance(value, int):
			try : 
				value = int(value)
			except Exception as e : 
				raise TypeError("Cycle's value must be a integer")
		else : 
			self.__cycle = value  


	def showTime(self): 
		i=2016 
		for time in self.save_time :
			print(str(i) + "  : " + str( time / 84600 ) )
			i = i+2016 

	def updateT2016 (self): 
		t = len(self.save_time) 
		if t > 1 :
			self.t2016 = self.save_time[t-1]-self.save_time[t-2]
			#print(self.t2016/86400)
		else : 
			self.t2016 = self.time_public

	def timeToMining(self): 
		p = 1 - self.alpha # 0.5 <= p < 1
		if len(self.public_chain) % 2016 == 0  and len(self.public_chain) != 0 : # difficulty adjustement 
			if self.adjust == False :
				self.adjust = True 
				self.save_time.append(self.time_public)
				self.updateT2016()
				self.delta = self.t2016 / (self.t0 * 2016)
				self.time_dico[len(self.public_chain)] = self.t2016
				if self.delta != 1 :
					self.difficulty = self.difficulty / self.delta 
				
		if len(self.public_chain) % 2016 == 1 and len(self.public_chain) > 1 :
			self.adjust = False 
		self.lambda_HM = (self.t0 / p ) * self.difficulty
		self.lambda_SM = (self.t0 / self.alpha ) * self.difficulty

		if expovariate(self.lambda_HM) > expovariate(self.lambda_SM):
			#print(" HM found a block first")
			return 0 
		else : 
			#print ("SM found a block first ")
			return -1 

 # Simulate awarding a Bitcoin block
 #  a => Percent of the total network owned by the selfish mining pool
 #  g => If two branches are competing, g (gamma) is the percent of the
 #       honest miners which join the selfish mining pool in mining on
 #       top of the selfish block

	# In case of competition
	def getFirstMiner(self, a, g) :
		rnd = uniform(0,1)
		if rnd > a and rnd <= (a + (1 - a) * g) : 
			#HM found a block on top of the selfish blockchain
			return 1 
		if rnd > (a + (1 - a) * g) :
			# HM found a block first on the official Blockchain
			return 0 
		else : 
			# SM found a block 
			return -1 

	def override(self) :
		self.public_chain = []
		self.time_public = self.time_private
		#self.time_private = 0 
		for private_block in self.private_chain : 
			self.public_chain.append(private_block)

	def fork(self):
		self.private_chain = []
		self.time_private = self.time_public
		#self.time_private = 0 
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
			height_diff = len(self.private_chain) - len(self.public_chain)
			self.timeToMining()
			#Initial
			if height_diff == 0 :
				#print("height_diff == 0 ")
				if selfish_blocks == 1 : 
					res = self.getFirstMiner(self.alpha, self.gamma)
					if res == 0 :
						#print("HM found a block first")
						#print("End of attack : SM abandon")
						self.public_chain.append(0) 
						self.selfish_orphan += 1 
						self.time_public += self.t0
						attack = False 
					elif res == 1 :
						#print("HM found a block first on PRIVATE CHAIN")
						#print("End attack : override official Blockchain")
						self.selfish_orphan += 1 
						self.honnest_orphan += 1
						self.private_chain.append(1)
						self.time_private += self.t0
						self.override()
						attack = False   
					elif res == -1 : 
					   # print("SM found a block first")
					   # print("End attack : override official Blockchain ")    
						self.private_chain.append(-1)
						self.time_private 	+= self.t0
						selfish_blocks    	+= 1
						self.honnest_orphan += 1
						self.override()
						attack = False 
				else : # initial 
					res = self.timeToMining()
					if res == 0 :
						#print("HM found a block first")
						self.public_chain.append(0)
						self.selfish_orphan += 1 
						self.time_public += self.lambda_HM
					elif res == -1 : 
						#print("SM found a block first")
						selfish_blocks += 1
						self.private_chain.append(-1) 
						self.time_private += self.lambda_SM
			if height_diff == 1 : 
				#print("height_diff == 1 ")
				res = self.getFirstMiner(self.alpha, self.gamma)
				if res == 0 : 
				    #print("HM found a block first on PUBLIC chain")
					self.public_chain.append(0)
					self.selfish_orphan += 1 
					self.time_public 	+= self.t0
				elif res == 1 : 
				   # print("HM found a block first on PRIVATE CHAIN")
				   # print("end attack : override official Blockchain")
					self.private_chain.append(1)
					self.selfish_orphan += 1 
					self.honnest_orphan += 1
					self.time_private += self.t0 
					self.override()
					attack = False 
				elif res == -1 : 
				   # print("SM found a block first")
					selfish_blocks += 1 
					self.private_chain.append(-1)
					self.honnest_orphan += 1
					self.time_private += self.t0
					self.override()
					attack = False 
				   # print("end attack : override official Blockchain ")
			if height_diff == -1 :
				# print("height_diff == -1 ")
				res = self.timeToMining()
				if res == 0 : 
					#print("HM found a block first")
					#print("end attack : SM abandon") 
					self.public_chain.append(0)
					self.selfish_orphan += 1 
					self.time_public 	+= self.lambda_HM
					attack = False 
				elif res == -1 : 
					#print("SM found a block first")
					self.private_chain.append(-1)
					selfish_blocks 		+= 1  
					self.honnest_orphan += 1
					self.time_private 	+= self.lambda_SM
		selfish_blocks = 0 
		self.fork()

	def runSimulation(self): 
		print("runSimulation methode")
		i = 0 
		while i < self.cycle :
			i += 1         
			if len(self.private_chain) != len(self.public_chain) : 
				raise TypeError (" height_diff != 0 ")
			else : 
				self.cycle_attack()
	
	def annalizeBlocks(self): 
		for block in self.public_chain :
			if block ==  1 :
				self.honnest_bis_blocks += 1
			elif block ==  0 :
				self.honnest_blocks += 1 
			elif block == -1: 
				self.selfish_blocks += 1
			self.total_blocks +=1 

	def getResult(self):
		self.runSimulation()
		self.annalizeBlocks()
		print("\n")
		print("o     Blocks in the public chain       : " + str(self.total_blocks))
		print("      	-> Mined by the SM pools      : " + str(self.selfish_blocks))
		print("      	-> Mined by the HM pools      : " + str(self.total_blocks - self.selfish_blocks))
		print("       	  -> Mined on top of HM chain : " + str(self.honnest_blocks))
		print("       	  -> Mined on top of SM chain : " + str(self.honnest_bis_blocks))
		print("\n")
		print("o     Orphan blocks mined by SM pools  : " + str(self.selfish_orphan))
		print("o     Orphan blocks mined by HM pools  : " + str(self.honnest_orphan))
		print("\n")
		print("o     Days to attend "+ str(self.total_blocks) + " blocks       : " + str(int((self.time_public)/86400)) + " d ")
		print("o     Days to attend 2016 blocks by DA : ")
		for key, val in self.time_dico.items() :
			print("		   - " + str(key) + " : " + str(int(val/84600))+ " d ")		
		print("o     Average minutes to mined a block : " + str(int((self.time_public/self.total_blocks) /60))+ " min ")
		
		print("o     Average blocks mined during 1 attack cycle : " + str(int(self.total_blocks/self.cycle ) )) 
		print("o     Average blocks mined by SM during 1 attack cycle  :" + str(int(self.selfish_blocks/self.cycle )) )
		print("\n")
		print("o     Revenue ratio of the miner       : " + str((self.selfish_blocks / self.time_public) *self.t0)) 
		print("o     Long-term apparent hash rate     : "+ str(self.selfish_blocks/self.total_blocks)) 



def main(): 
	simule = Simulator()
	#print(simule.cycle)
	simule.getResult()
	#simule.cycle_attack()
	#simule.test()

main()