# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        foodnum = successorGameState.getNumFood()
	successornum = currentGameState.getNumFood()
	(x,y) = newPos
	if successorGameState.hasWall(x,y): wall = 0.000000001
	else: wall = 1	
	capsule = 1
	for l in currentGameState.getCapsules():
		if newPos == l: capsule = 1000 
	if successornum == foodnum: f =1000
	else: f=0.0001
	newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
	foodlist = newFood.asList()
	dist = 0
	if foodnum == 0: distmin =0.001 
	else: distmin=1000
	for i in foodlist:
		temp =  util.manhattanDistance(newPos,i)
		dist = dist+temp
		if distmin>temp: distmin = temp
	f1 = distmin
	g1 = list()

	for j in newGhostStates:
		newGhostPos = j.getPosition()
		g1.append( util.manhattanDistance(newPos, newGhostPos))
	g = min(g1)
	e = 0.0
	temp1= 0.0
	temp2 = 0.0
	for time in newScaredTimes:
	
		if time > 0:
			
			temp1 = capsule*wall**5/((g+0.01)/g)/f/(f1**5)
			if temp1>e: e = temp1
		else:
			temp2 =capsule*wall**5*(g-0.9999999999)/f/((f1)**5)	
			if temp2>e: e = temp2
	return e	
        "*** YOUR CODE HERE ***"

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
import time
class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
       	def minimaxValue(agent, depth, state):
		if depth == self.depth:
			return [self.evaluationFunction(state), 0]
		elif agent == 0:
			return maxValue(agent, depth, state)
		else:
			return minValue(agent, depth, state)
		# PacMan - The Maximizing Agent - Pick the best action available
	def maxValue(agent, depth, state):
		if state.isWin() or state.isLose():
			return [self.evaluationFunction(state), 0]
		value = float("-inf")
		action = 0
		legalActions = state.getLegalActions(agent)
		for legalAction in legalActions:
			successor = state.generateSuccessor(agent, legalAction)
			actionValue = minimaxValue(agent+1, depth, successor)
			if actionValue[0] > value:
				value = actionValue[0]
				action = legalAction
		return (value, action)
		# Ghosts - The Minimizing/Adverserial Agents - Pick the worst action available (for PacMan)
	def minValue(agent, depth, state):
		value = float("inf")
		action = 0
		if state.isWin() or state.isLose():	
			return [self.evaluationFunction(state), 0]
		legalActions = state.getLegalActions(agent)
		if not legalActions:
			return [self.evaluationFunction(state), 0]
		for legalAction in legalActions:
			successor = state.generateSuccessor(agent, legalAction)
		# Base Case - Process the final ghost
			if agent == gameState.getNumAgents()-1:
				actionValue = minimaxValue(0, depth+1, successor)
				if actionValue[0] < value:
					value = actionValue[0]
					action = legalAction
			else:
				actionValue = minimaxValue(agent+1, depth, successor)
				if actionValue[0] < value:
					value = actionValue[0]
					action = legalAction
		return (value, action)
	return minimaxValue(0, 0, gameState)[1]


	




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
   """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
	alpha = float("-inf");
	beta = float("inf");
       	def minimaxValue(agent, depth, state, alpha, beta):
		if depth == self.depth:
			return [self.evaluationFunction(state), 0]
		elif agent == 0:
			return maxValue(agent, depth, state, alpha, beta)
		else:
			return minValue(agent, depth, state, alpha, beta)
		# PacMan - The Maximizing Agent - Pick the best action available
	def maxValue(agent, depth, state, alpha, beta):
		if state.isWin() or state.isLose():
			return [self.evaluationFunction(state), 0]
		value = float("-inf")
		action = 0
		legalActions = state.getLegalActions(agent)
		for legalAction in legalActions:
			successor = state.generateSuccessor(agent, legalAction)
			actionValue = minimaxValue(agent+1, depth, successor, alpha, beta)
			if actionValue[0] > value:
				value = actionValue[0]
				action = legalAction
			if actionValue[0] > beta: return (value,action);
			alpha = max(alpha,value);
		return (value, action)
		# Ghosts - The Minimizing/Adverserial Agents - Pick the worst action available (for PacMan)
	def minValue(agent, depth, state, alpha, beta):
		value = float("inf")
		action = 0
		if state.isWin() or state.isLose():	
			return [self.evaluationFunction(state), 0]
		legalActions = state.getLegalActions(agent)
		if not legalActions:
			return [self.evaluationFunction(state), 0]
		for legalAction in legalActions:
			successor = state.generateSuccessor(agent, legalAction)
		# Base Case - Process the final ghost

			if agent == gameState.getNumAgents() - 1:
		    		actionValue = minimaxValue(0, depth+1, successor, alpha, beta)
		   
		    # v = min(v, value(successor, alpha, beta)
		    		if actionValue[0] < value:
					value = actionValue[0]
					action = legalAction
		# if v <= alpha return v
		    		if value < alpha:
					return actionValue

		    # Beta = min(Beta, v)
		    		beta = min(beta, value)

		    # if v <= alpha return v
			else:		
		    		actionValue = minimaxValue(agent+1, depth, successor, alpha, beta)
		    
		    # v = min(v, value(successor, alpha, beta)
		    		if actionValue[0] < value:
					value = actionValue[0]
					action = legalAction
		# if v <= alpha return v
		    		if value < alpha:
					return actionValue

		    # Beta = min(Beta, v)
		    		beta = min(beta, value)

		    # if v <= alpha return v
		return (value, action)
	return minimaxValue(0, 0, gameState,alpha,beta)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
	def minimaxValue(agent, depth, state):
		if depth == self.depth:
			return [self.evaluationFunction(state), 0]
		elif agent == 0:
			return maxValue(agent, depth, state)
		else:
			return minValue(agent, depth, state)
		# PacMan - The Maximizing Agent - Pick the best action available
	def maxValue(agent, depth, state):
		if state.isWin() or state.isLose():
			return [self.evaluationFunction(state), 0]
		value = float("-inf")
		action = 0
		legalActions = state.getLegalActions(agent)
		for legalAction in legalActions:
			successor = state.generateSuccessor(agent, legalAction)
			actionValue = minimaxValue(agent+1, depth, successor)
			if actionValue[0] > value:
				value = actionValue[0]
				action = legalAction
		return (value, action)
		# Ghosts - The Minimizing/Adverserial Agents - Pick the worst action available (for PacMan)
	def minValue(agent, depth, state):
		value = 0
		action = 0
		if state.isWin() or state.isLose():	
			return [self.evaluationFunction(state), 0]
		legalActions = state.getLegalActions(agent)
		if not legalActions:
			return [self.evaluationFunction(state), 0]
		for legalAction in legalActions:
			successor = state.generateSuccessor(agent, legalAction)
		# Base Case - Process the final ghost
			prob = 1.0/len(legalActions)
			if agent == gameState.getNumAgents()-1:
				actionValue = minimaxValue(0, depth+1, successor)
				value += prob*actionValue[0]
			else:
				actionValue = minimaxValue(agent+1, depth, successor)
				value += prob*actionValue[0]
		
		return (value, action)
	return minimaxValue(0, 0, gameState)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
# AbbrevToFood = []
    distanceToNearestGhost = []
    distanceToCapsules = []
    score = 0

    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsuleList = currentGameState.getCapsules()
    numOfScaredGhosts = 0

    pacmanPos = list(currentGameState.getPacmanPosition())

    for ghostState in ghostStates:
        if ghostState.scaredTimer is 0:
            numOfScaredGhosts += 1
            distanceToNearestGhost.append(0)
            continue

        gCoord = ghostState.getPosition()
        x = abs(gCoord[0] - pacmanPos[0])
        y = abs(gCoord[1] - pacmanPos[1])
        if (x+y) == 0:
            distanceToNearestGhost.append(0)
        else:
            distanceToNearestGhost.append(-1.0/(x+y))

    for food in foodList:
        x = abs(food[0] - pacmanPos[0])
        y = abs(food[1] - pacmanPos[1])
        distanceToFood.append(-1*(x+y))  

    if not distanceToFood:
        distanceToFood.append(0)

    return max(distanceToFood) + min(distanceToNearestGhost) + currentGameState.getScore() - 100*len(capsuleList)
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
