#Please do not add any imports
#This particularly includes numpy!
import math

############################## PROBLEM 1 ######################################

#This function should take a matrix with your payoffs for the game and your
#opponent's current strategy and compute your expected utility for each action.
#This will be useful in implementing the learning dynamics
def expectedValues(game,opponentStrategy):
    num_my_actions = len(game)
    num_opp_actions = len(game[0])
    
    result_list = []
    
    for i in range(num_my_actions):
        expected = 0.0
        for j in range(num_opp_actions):
            expected += game[i][j] * opponentStrategy[j]
            
        result_list.append(expected)
    
    return result_list


############################## PROBLEM 2 ######################################

#This function should implement one iteration of best response dynamics for
#a player.  It takes that players's payoff matrix and the opponent's strategy
#and returns a best response
def bestResponseDynamics(game,opponentStrategy):
    vals = expectedValues(game, opponentStrategy)
    best_index = vals.index(max(vals))

    strat_list = [0.0 for i in range(len(game))]
    strat_list[best_index] = 1.0
    
    return strat_list

############################## PROBLEM 3 ######################################

#This class should implement fictitious play for one player.
class FictitiousPlay:
    #You shouldn't need to change __init__
    def __init__(self,game):
        self.history = [0.0 for i in range(len(game[0]))]
        self.game = game

    #This should perform one iteration of fictitious play
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #and self.history (a list to track your opponent's history)
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        for k in range(len(self.history)):
            self.history[k] += opponentStrategy[k]
            
        total = sum(self.history)
        avgOpp = [h / total for h in self.history]
        
        exp_vals = expectedValues(self.game, avgOpp)
        best_index = exp_vals.index(max(exp_vals))
        
        strat_list = [0.0 for _ in range(len(self.game))]
        strat_list[best_index] = 1.0
        
        return strat_list

############################## PROBLEM 4 ######################################

#This class should implement smoothed fictitious play for one player.
class SmoothedFictitiousPlay:
    #You shouldn't need to change __init__
    def __init__(self,game,gamma):
        self.history = [0.0 for i in range(len(game[0]))]
        self.game = game
        self.gamma = gamma

    #This should perform one iteration of smoothed fictitious play
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #self.history (a list to track your opponent's history)
    #and self.gamma (see slides for what this does)
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        for k in range(len(self.history)):
            self.history[k] += opponentStrategy[k]
            
        total = sum(self.history)
        avgOpp = [h / total for h in self.history]

        
        exp_vals = expectedValues(self.game, avgOpp)
        
        scores = [math.exp(ev / self.gamma) for ev in exp_vals]
        Z = sum(scores)
        strat = [s / Z for s in scores]
        
        return strat

############################## PROBLEM 5 ######################################

#This class should implement regret matching for one player.
class RegretMatching:
    #You shouldn't need to change __init__
    def __init__(self,game):
        self.regretSums = [0.0 for i in range(len(game[0]))]
        self.game = game

    #You may optionally want to implement this helper function
    #It should convert your current regret sums to a strategy
    #My implementation of updateStrategy calls it twice
    def regretSumsToStrategy(self):
        positive_regrets = [max(r, 0.0) for r in self.regretSums]
        total_positive = sum(positive_regrets)  

        if total_positive > 0.0:
            return [r / total_positive for r in positive_regrets]
        else:
            num_actions = len(self.regretSums)
            return [1.0 / num_actions for _ in range(num_actions)]

    #This should perform one iteration of regret matching
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #and self.regretSums (a list to track your regret sums)
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        currentStrategy = self.regretSumsToStrategy()
        evs = expectedValues(self.game, opponentStrategy)
        
        currentUtility = 0.0
        for a in range(len(evs)):
            currentUtility += currentStrategy[a] * evs[a]
            
        for a in range(len(evs)):
            regret = evs[a] - currentUtility
            self.regretSums[a] += regret
            
        return self.regretSumsToStrategy()

############################## PROBLEM 6 ######################################

#Give priors so that Matching Pennies does not reach
#steady state with fictitious play but the empirical distribution converges    
#
#MatchingPenniesP1 = [[1,-1],[-1,1]] (defined in autograder)
#MatchingPenniesP2 = [[-1,1],[1,-1]] (defined in autograder)
MPPrior1 = None
MPPrior2 = None

############################## PROBLEM 7 ######################################

#Give priors so that the Shapley game's empircal distribution
#does not converge with fictitious play
#
#ShapleyGame = [[0,0,1],[1,0,0],[0,1,0]] (defined in autograder)
ShapleyPrior1 = None
ShapleyPrior2 = None

############################## PROBLEM 8 ######################################

#Give a game and priors so that best response self-play does not converge to
#the pure Nash equilibrium (0,0) but fictitious play
#reaches it as a steady state
#
P8Game1 = None
P8Game2 = None
P8Prior1 = None
P8Prior2 = None

############################## PROBLEM 9 ######################################

#Give a game and priors so that best response self-play converges to
#the pure Nash equilibrium (0,0) but fictitious play
#does not reach it as a steady state
#
P9Game1 = None
P9Game2 = None
P9Prior1 = None
P9Prior2 = None


############################## PROBLEM 10 ######################################

#Give a 2x2 game and priors so that smoothed fictitious play converges to a
#mixed Nash equilirbium in its current strategy but regret matching does not
#(both with converge in their empirical distribution)
#
P10Game1 = None
P10Game2 = None
P10Prior1 = None
P10Prior2 = None

############################## PROBLEM 11 ######################################

#This class should implement optimistic regret matching for one player.
class OptimisticRegretMatching:
    #You shouldn't need to change __init__
    def __init__(self,game):
        self.regretSums = [0.0 for i in range(len(game[0]))]
        self.lastRegrets = [0.0 for i in range(len(game[0]))]
        self.game = game

    #You may optionally want to implement this helper function
    #It should convert your current regret sums to a strategy
    #My implementation of updateStrategy calls it twoce
    def regretSumsToStrategy(self):
        "Your Code (Optionally) Here!"

        return [0.0]

    #This should perform one iteration of regret matching
    #The argument is your opponent's more recent strategy
    #You have access to self.game (your payoffs)
    #self.regretSums (a list to track your regret sums)
    #and self.lastRegret (save your regrets here before you return!) 
    #You should return the updated strategy
    def updateStrategy(self, opponentStrategy):
        "Your Code Here!"
        
        return [0.0]
