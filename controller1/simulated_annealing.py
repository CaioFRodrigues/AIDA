import controller_template as controller_template
from copy import deepcopy
from random import randint
from random import randrange
from math import exp
class Simulated_Annealing:
    '''
    Classe Simulated_Annealing - Executa o Simulated_Annealing alterando os thetas com temperatura 100
    Chamar com:
        anneal = Simulated_Annealing(weights,self)
        weights = anneal.simulate(self)
    '''
    def __init__ (self, weights,controller):
        self.__weights = deepcopy(weights)
        self.__result = controller.run_episode(weights) 
        self.__temp = 100
        
    def simulate (self, controller):
        while (self.__temp != 0):
            self.__weights = self.__get_neightbor(controller)
            self.__temp = self.__temp - 10
        
        return self.__weights
 
    def __get_neightbor(self, controller)->list:
        '''
        Generate the nearest thetas for the function, for each weight passed it will try to increase and decrease,
        returning a list with twice the size
        '''
        weights = deepcopy(self.__weights)
        N = 100
        for i in range(0,N):
            weights = deepcopy(self.__weights)
            
            
            ''' 
            index defines a random number that goes from 0 to the double of the size of the list of weights.
            This is so if random is over the list of weights, it is then made the operation of - instead of +
            '''
            index = randint(0,(len(self.__weights) * 2 - 1)) 


            
            if (index >= len(self.__weights)):
                position = index - len(self.__weights)
                weights[position] = weights[position] - 1
                result = controller.run_episode(weights)
                if (self.__choose_to_change(result,controller) == True):
                    self.__weights = weights
                    self.__result = result
            else:
                position = index
                weights[position] = weights[position] + 1
                result = controller.run_episode(weights)
                if (self.__choose_to_change(result,controller)):
                    self.__weights = weights
                    self.__result = result
            
            

     
        return self.__weights
    
       
    def __choose_to_change(self,result, controller):
        '''
        Decides whether or not the current weights will changed based on the formula
        '''
        delta = result - self.__result 
        
        print ("Delta:")
        print (delta)
        print ("Result:")
        print (self.__temp)
        print (result)
        print(self.__result)
        if delta == 0:
            return False
        if (delta > 0):
            return True
        else:
            percent = exp(delta/self.__temp)
            
            rand =  randrange(0,100)

            if (percent < rand):
                return False
            else:
                print ("Went somewhere worse")
                return True
                
        