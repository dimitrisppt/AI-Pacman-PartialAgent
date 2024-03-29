# partialAgent.py
# parsons/15-oct-2017
#
# Version 1
#
# The starting point for CW1.
#
# Intended to work with the PacMan AI projects from:
#
# http://ai.berkeley.edu/
#
# These use a simple API that allow us to control Pacman's interaction with
# the environment adding a layer on top of the AI Berkeley code.
#
# As required by the licensing agreement for the PacMan AI we have:
#
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# The agent here is was written by Simon Parsons, based on the code in
# pacmanAgents.py

from pacman import Directions
from game import Agent
import api
import random
import game
import util

class PartialAgent(Agent):

    # Constructor: this gets run when we first invoke pacman.py
    def __init__(self):
        print "Starting up!"
        name = "Pacman"

        self.explored_food = [] # List of food that have been explored but not yet been eaten
        self.explored_capsules = [] # List of capsules that have been explored but not yet been eaten

        self.predator_mode_on = False # Flag that changes the behaviour of the pacman from prey to predator
        self.seen_any_ghosts = False # Flag that is set to true the first time when the pacman senses(sees/hears) any ghosts, initially false

        self.super_powers_time = 40 # Found that from the pacman.py file, SCARED_TIME = 40,
                                    # used to know when to turn off the super powers if pacman can't find a ghost to eat.

        # --- The following variables are needed for the implementation of the Depth First Search --- #
        self.visited_nodes = [] # List of nodes that have been visited form the pacman
        self.stack = [] # List that acts as a stack
        # ------------------------------------------------------------------------------------------- #

        self.positions_history = []
        self.was_stuck = False

        self.pacman_was_next_to_ghost = False


    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like I just died!"

        self.explored_food = [] # List of food that have been explored but not yet been eaten
        self.explored_capsules = [] # List of capsules that have been explored but not yet been eaten

        self.predator_mode_on = False # Flag that changes the behaviour of the pacman from prey to predator
        self.seen_any_ghosts = False # Flag that is set to true the first time when the pacman senses(sees/hears) any ghosts, initially false

        self.super_powers_time = 40 # Found that from the pacman.py file, SCARED_TIME = 40,
                                    # used to know when to turn off the super powers if pacman can't find a ghost to eat.

        # --- The following variables are needed for the implementation of the Depth First Search --- #
        self.visited_nodes = [] # List of nodes that have been visited form the pacman
        self.stack = [] # List that acts as a stack
        # ------------------------------------------------------------------------------------------- #

        self.positions_history = []
        self.was_stuck = False

        self.pacman_was_next_to_ghost = False

    # Adds legal moves back to the list of legal moves and returns the list
    def resetAvailableLegalMoves(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        return legal

    # Calculates the manhattan distance of each and every direction, taken from Directions,
    # and checks whether it's less than the manhattan distance between pacman and ghost.
    # If that's the case then that direction is not a good move because brings the pacman closer
    # to the ghost and hence it is removed from the list of available legal moves.
    #
    # Example: pacman coordinates: x = 7
    #                              y = 1
    #           ghost coordinates: x = 10
    #                              y = 1
    #         manh_dist_pac_ghost: abs(7-10) + abs(1-1) = 3
    #         ---------------------------------------------
    #              Direction.East: (x+1, y)
    #          pacman coordinates: x = 8
    #                              y = 1
    #           ghost coordinates: x = 10
    #                              y = 1
    #         manh_dist_pac_ghost: abs(8-10) + abs(1-1) = 2
    #         ---------------------------------------------
    # If pacman moves East then the new position brings him closer to the ghost, thus it's not
    # a good move and it's removed from the list of available legal moves.
    def avoidGhosts(self, pacman_pos, closest_ghost, manh_dist_pac_ghost, legal_moves):
        x_pac, y_pac = pacman_pos
        x_ghost, y_ghost = closest_ghost

        for direction in legal_moves:

            if direction == Directions.EAST:
                if util.manhattanDistance((x_pac + 1, y_pac), (x_ghost, y_ghost)) < manh_dist_pac_ghost:
                    legal_moves.remove(direction)

            if direction == Directions.WEST:
                if util.manhattanDistance((x_pac - 1, y_pac), (x_ghost, y_ghost)) < manh_dist_pac_ghost:
                    legal_moves.remove(direction)

            if direction == Directions.NORTH:
                if util.manhattanDistance((x_pac, y_pac + 1), (x_ghost, y_ghost)) < manh_dist_pac_ghost:
                    legal_moves.remove(direction)

            if direction == Directions.SOUTH:
                if util.manhattanDistance((x_pac, y_pac - 1), (x_ghost, y_ghost)) < manh_dist_pac_ghost:
                    legal_moves.remove(direction)

        return legal_moves



    # Calculates the manhattan distance of each and every direction, taken from Directions,
    # and checks whether it's greater than the manhattan distance between pacman and food.
    # If that's the case then that direction is not a good move because brings the pacman further away
    # from the nearest food and hence it is removed from the list of available legal moves.
    #
    # Example: pacman coordinates: x = 10
    #                              y = 1
    #            food coordinates: x = 7
    #                              y = 1
    #         manh_dist_pac_food: abs(10-7) + abs(1-1) = 3
    #         ---------------------------------------------
    #              Direction.East: (x+1, y)
    #          pacman coordinates: x = 11
    #                              y = 1
    #            food coordinates: x = 7
    #                              y = 1
    #         manh_dist_pac_food: abs(11-7) + abs(1-1) = 4
    #         ---------------------------------------------
    # If pacman moves East then the new position brings him further away from the food, thus it's not
    # a good move and it's removed from the list of available legal moves.
    def searchForFood(self, pacman_pos, closest_food, legal):
        x_pac, y_pac = pacman_pos
        x_food, y_food = closest_food
        manh_dist_pac_food = util.manhattanDistance(pacman_pos, closest_food)

        for direction in legal:
            if direction == Directions.EAST:
                if util.manhattanDistance((x_pac + 1, y_pac), (x_food, y_food)) > manh_dist_pac_food:
                    legal.remove(direction)

            if direction == Directions.WEST:
                if util.manhattanDistance((x_pac - 1, y_pac), (x_food, y_food)) > manh_dist_pac_food:
                    legal.remove(direction)

            if direction == Directions.NORTH:
                if util.manhattanDistance((x_pac, y_pac + 1), (x_food, y_food)) > manh_dist_pac_food:
                    legal.remove(direction)

            if direction == Directions.SOUTH:
                if util.manhattanDistance((x_pac, y_pac - 1), (x_food, y_food)) > manh_dist_pac_food:
                    legal.remove(direction)

        return legal


    # Calculates the manhattan distance of each and every direction, taken from Directions,
    # and checks whether it's greater than the manhattan distance between pacman and a capsule.
    # If that's the case then that direction is not a good move because brings the pacman further away
    # from the nearest capsule and hence it is removed from the list of available legal moves.
    #
    # Example: pacman coordinates: x = 10
    #                              y = 1
    #         capsule coordinates: x = 7
    #                              y = 1
    #       manh_dist_pac_capsule: abs(10-7) + abs(1-1) = 3
    #       -----------------------------------------------
    #              Direction.East: (x+1, y)
    #          pacman coordinates: x = 11
    #                              y = 1
    #         capsule coordinates: x = 7
    #                              y = 1
    #       manh_dist_pac_capsule: abs(11-7) + abs(1-1) = 4
    #       -----------------------------------------------
    # If pacman moves East then the new position brings him further away from the capsule, thus it's not
    # a good move and it's removed from the list of available legal moves.
    def searchForCapsule(self, pacman_pos, closest_capsule, legal):
        x_pac, y_pac = pacman_pos
        x_capsule, y_capsule = closest_capsule
        manh_dist_pac_capsule = util.manhattanDistance(pacman_pos, closest_capsule)

        for direction in legal:

            if direction == Directions.EAST:
                if util.manhattanDistance((x_pac + 1, y_pac), (x_capsule, y_capsule)) > manh_dist_pac_capsule:
                    legal.remove(direction)

            if direction == Directions.WEST:
                if util.manhattanDistance((x_pac - 1, y_pac), (x_capsule, y_capsule)) > manh_dist_pac_capsule:
                    legal.remove(direction)

            if direction == Directions.NORTH:
                if util.manhattanDistance((x_pac, y_pac + 1), (x_capsule, y_capsule)) > manh_dist_pac_capsule:
                    legal.remove(direction)

            if direction == Directions.SOUTH:
                if util.manhattanDistance((x_pac, y_pac - 1), (x_capsule, y_capsule)) > manh_dist_pac_capsule:
                    legal.remove(direction)

        if len(legal) == 0:
            return None
        return legal


    # This function is to make the pacman to chase the ghosts.
    # Calculates the manhattan distance of each and every direction, taken from Directions,
    # and checks whether it's greater than the manhattan distance between pacman and a ghost.
    # If that's the case then that direction is not a good move because brings the pacman further away
    # from the nearest ghost and hence it is removed from the list of available legal moves.
    #
    # Example: pacman coordinates: x = 10
    #                              y = 1
    #           ghost coordinates: x = 7
    #                              y = 1
    #         manh_dist_pac_ghost: abs(10-7) + abs(1-1) = 3
    #       -----------------------------------------------
    #              Direction.East: (x+1, y)
    #          pacman coordinates: x = 11
    #                              y = 1
    #           ghost coordinates: x = 7
    #                              y = 1
    #         manh_dist_pac_ghost: abs(11-7) + abs(1-1) = 4
    #       -----------------------------------------------
    # If pacman moves East then the new position brings him further away from the ghost, thus it's not
    # a good move and it's removed from the list of available legal moves.
    def chaseGhosts(self, pacman_pos, closest_ghost, manh_dist_pac_ghost, legal):
        x_pac, y_pac = pacman_pos
        x_ghost, y_ghost = closest_ghost

        for direction in legal:

            if direction == Directions.EAST:
                if util.manhattanDistance((x_pac + 1, y_pac), (x_ghost, y_ghost)) > manh_dist_pac_ghost:
                    legal.remove(direction)

            if direction == Directions.WEST:
                if util.manhattanDistance((x_pac - 1, y_pac), (x_ghost, y_ghost)) > manh_dist_pac_ghost:
                    legal.remove(direction)

            if direction == Directions.NORTH:
                if util.manhattanDistance((x_pac, y_pac + 1), (x_ghost, y_ghost)) > manh_dist_pac_ghost:
                    legal.remove(direction)

            if direction == Directions.SOUTH:
                if util.manhattanDistance((x_pac, y_pac - 1), (x_ghost, y_ghost)) > manh_dist_pac_ghost:
                    legal.remove(direction)

        return legal


    # Updates all the globally defined lists.
    # If pacman explores something new which is not in the list of explored_food or explored_capsules,
    # then their position is added to those lists.
    # If pacman eats food or capsule their position is removed from the corresponding list.
    # If pacman eats a capsule he gains super powers and the flag "predator_mode_on" is set to True,
    # also, the super_powers_time reset to 40.
    # If pacman eats a ghost while having super powers then the flag "predator_mode_on" is set to False,
    # and the super_powers_time reset to 40.
    def updateListsOfExploredNodes(self, pacman_pos, food_list, capsules_list, ghosts_list):

        # Loop through the list of visible food and add any unexplored food to the list of explored food
        for food in food_list:
            if food not in self.explored_food:
                self.explored_food.append(food)

        # Loop through the list of visible capsules and add any unexplored capsules to the list of explored food
        for capsule in capsules_list:
            if capsule not in self.explored_capsules:
                self.explored_capsules.append(capsule)

        # Remove food that have beeen eaten from the list of explored food
        if pacman_pos in self.explored_food:
            self.explored_food.remove(pacman_pos)

        # Pacman eats a capsule and is removed from the list of explored capsules.
        # Pacman enters predator mode.
        if pacman_pos in self.explored_capsules:
            self.explored_capsules.remove(pacman_pos)
            self.predator_mode_on = True
            self.super_powers_time = 40

        # Pacman eats a ghost and exits the predator mode because he cannot identify
        # edible ghosts from non-edible ones.
        self.decideToExitPredatorMode(pacman_pos, ghosts_list)

        # Sets the flag "seen_any_ghosts" to True when pacman sees a ghost.
        # This happens to enter in a mode where it has to deal with ghosts.
        if len(ghosts_list) > 0:
            self.seen_any_ghosts = True

        # Keep track of every visited position
        self.positions_history.append(pacman_pos)


    # Function that decides if it's time to exit predator mode
    # To actually check whether pacman ate a ghost
    #
    #
    #
    #
    #
    #
    #
    #
    #
    def decideToExitPredatorMode(self, pacman_pos, ghosts_list):
        new_round = True
        closest_ghost = self.findClosestGhost(pacman_pos, ghosts_list)

        if closest_ghost and self.predator_mode_on == True:
            manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, closest_ghost)
            print "Manh dis is -> ", manh_dist_pac_ghost
            print " positions are:", closest_ghost, " and ", pacman_pos

            if manh_dist_pac_ghost <= 2:
                self.pacman_was_next_to_ghost = True
                new_round = False
            else:
                self.pacman_was_next_to_ghost = False
                new_round = False

        if self.pacman_was_next_to_ghost == True and new_round == True:
            self.predator_mode_on = False
            self.super_powers_time = 40
            self.pacman_was_next_to_ghost == False


    # Calculates the closest food from pacman's position, if any, out of the
    # list of explored food that pacman hasn't eaten yet. The calculation is
    # done using the manhattanDistance function that is provided in the "util.py" file.
    #
    # :param self: Object of the class PartialAgent
    # :param pacman_pos: Current pacman position
    def calculateClosestFood(self, pacman_pos):
        min_dist_to_food = float("inf") # Set minimum distance to be infinity
        closestFood = []
        # Loop through the list of explored food and find the closest one to pacman's position
        for food in self.explored_food:
            manh_dist_pac_food = util.manhattanDistance(pacman_pos, food)
            if manh_dist_pac_food < min_dist_to_food:
                min_dist_to_food = manh_dist_pac_food
                closestFood = food
        return closestFood


    # Calculates the closest capsule from pacman's position, if any, out of the
    # list of explored capsules that pacman hasn't eaten yet. The calculation is
    # done using the manhattanDistance function that is provided in the "util.py" file.
    #
    # :param self: Object of the class PartialAgent
    # :param pacman_pos: Current pacman position
    def calculateClosestCapsule(self, pacman_pos):
        min_dist_to_capsule = float("inf") # Set minimum distance to be infinity
        closestCapsule = []
        # Loop through the list of explored capsules and find the closest one to pacman's position
        for capsule in self.explored_capsules:
            manh_dist_pac_capsule = util.manhattanDistance(pacman_pos, capsule)
            if manh_dist_pac_capsule < min_dist_to_capsule:
                min_dist_to_capsule = manh_dist_pac_capsule
                closestCapsule = capsule
        return closestCapsule


    # Tries to find the closest visible ghost from pacman's position, if any, out of the
    # list of visible ghosts that have been retrieved from the api. The calculation is
    # done using the manhattanDistance function that is provided in the "util.py" file.
    #
    # :param self: Object of the class PartialAgent
    # :param pacman_pos: Current pacman position
    def findClosestGhost(self, pacman_pos, ghosts_list):
        min_dist_to_ghost = float("inf") # Set minimum distance to be infinity
        closestGhost = []
        # Loop through the list of visible ghosts, if any, and find the closest one to pacman's position
        for ghost in ghosts_list:
            manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, ghost)
            if manh_dist_pac_ghost < min_dist_to_ghost:
                min_dist_to_ghost = manh_dist_pac_ghost
                closestGhost = ghost
        return closestGhost


    def getAction(self, state):

        food_list = api.food(state) # Retrieves from the api, a list of any visible food, on each state of the pacman.
        capsules_list = api.capsules(state) # Retrieves from the api, a list of any visible capsules, on each state of the pacman.
        pacman_pos = api.whereAmI(state) # Retrieves from the api, a tuple of the current position of the pacman, on each state.
        ghosts_list = api.ghosts(state) # Retrieves from the api, a list of any visible ghosts, on each state of the pacman.
        walls_list = api.walls(state) # Retrieves from the api, a list of any visible walls, on each state of the pacman.
        corner_list = api.corners(state) # Retrieves from the api, a list of the extreme x and y values of the grid.
        legal = api.legalActions(state) # Retrieves from the api, a list of legal actions that the pacman is allowed to perform.

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        # Updates the global variables of the class with the new state of the world.
        # This is done, to keep only relevant information to the lists and to update some variables that affect the behaviour of the pacman.
        self.updateListsOfExploredNodes(pacman_pos, food_list, capsules_list, ghosts_list)

        closestFood = self.calculateClosestFood(pacman_pos) # Calculates and stores the closest food, if any, from pacman's position at that state.
        closestCapsule = self.calculateClosestCapsule(pacman_pos) # Calculates and stores the closest capsule, if any, from pacman's position at that state.
        closestGhost = self.findClosestGhost(pacman_pos, ghosts_list) # Calculates and stores the closest ghost, if any, from pacman's position at that state.


        ##########################################################
        ## Safe mode, pacman doesn't have to worry about ghosts ##
        ##########################################################
        if self.seen_any_ghosts == False:
            # Pacman performs an action that is calculated using a depth first search.
            next_move = self.dfsearch(pacman_pos, legal)
            return api.makeMove(next_move, legal)


        ###################################################################################################################
        ## Alert mode, pacman saw at least one ghost and is now anticipating to deal with them when they come in his way ##
        ###################################################################################################################
        else:



            #if self.predator_mode_on == False or self.super_powers_time <= 0:




                # If there is a closest ghost then prioritise to avoid it when it's to close to pacman's position. (< 3 squares)
                # If it can see it but it's not very close (3 <= distance <= 5) and any potential moves that it might try to do,
                # do not lead to the death of pacman that means, for that round pacman is still safe to do any available legal move.
                if closestGhost:
                    self.clearDfSearchVars() # clear dfs variables
                    manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, closestGhost) # calculate manhattan distance between pacman and ghost

                    # Their distance must be less than 3 squares for pacman to get scared
                    # (pacman tries to avoid the ghost because he needs to have at least two squares difference, as in one round the may end up in the same square)
                    if manh_dist_pac_ghost < 3:
                        next_move = self.avoidGhosts(pacman_pos, closestGhost, manh_dist_pac_ghost, legal) # calculate the next move that keeps the pacman away from the ghost
                        if next_move in legal:
                            return api.makeMove(next_move, legal)

                    # If pacman sees a ghost and their distance is not very close it chases it
                    # I found that strategy to be quite effective and fun to explore the world, before implementing any path searching algorithm.
                    elif manh_dist_pac_ghost <= 5:
                        next_move = self.chaseGhosts(pacman_pos, closestGhost, manh_dist_pac_ghost, legal) # calculate the next move that brings the pacman closer to the ghost
                        if next_move in legal:
                            return api.makeMove(next_move, legal)

                # If there is no ghost to avoid or chase, and the pacman doesn't really know what to do,
                # Check whether pacman is stuck, if he's not stuck try to find the nearest food and eat it,
                # if it can see any food perform a depth first search until he finds any.
                else:
                    isStuck = self.isPacmanStuck(pacman_pos)
                    # If pacman is stuck or pacman was stuck but it still can't see any food or capsule then he randomly performs a move
                    if isStuck or (self.was_stuck and not (closestFood or closestCapsule)):
                        next_move = random.choice(legal)
                        self.was_stuck = True

                    # Pacman searches for food, by removing moves from a list of legal moves that bring him furthest away from the closest food
                    # if there are more than one good moves that he can perform then randomly chooses between them.
                    else:
                        next_move = self.searchForFood(pacman_pos, closestFood, legal) # calculate the next move that brings the pacman closer to the closest food
                        # if there are more than one good moves,
                        if len(next_move) > 1:
                            self.clearDfSearchVars() # clears dfs variables
                            next_move = random.choice(next_move) # choose randomly between the moves that are left, (doesn't matter which one both of them have the same manhattan distance)
                        # if there is only one good move,
                        elif len(next_move) == 1:
                            self.clearDfSearchVars() # clears dfs variables
                            next_move = next_move[0] # get the first and only element of the list
                        # Otherwise,
                        else:
                            # if the list of legal moves is empty, that means we removed all the legal moves and we need to add them back in order to perform a move.
                            if len(legal) == 0:
                                legal = self.resetAvailableLegalMoves(state) # resets the list of legal moves.
                            next_move = self.dfsearch(pacman_pos, legal) # calculate the next step by performing a depth first search

                        return api.makeMove(next_move, legal)

                if Directions.STOP in legal:
                    legal.remove(Directions.STOP) # remove the stop from the list of legal moves because is not very useful

                # if the list of legal moves is empty, that means we removed all the legal moves and we need to add them back in order to perform a move.
                if len(legal) == 0:
                    legal = self.resetAvailableLegalMoves(state) # resets the list of legal moves.
                next_move = self.dfsearch(pacman_pos, legal) # calculate the next step by performing a depth first search

                return api.makeMove(next_move, legal)







            ##########################
            ##---PREDATOR MODE ON---##
            ##########################
            # elif self.predator_mode_on == True and self.super_powers_time > 0:
            #     self.super_powers_time -= 1
            #     if closestGhost:
            #         #print "there is a ghost aaaah"
            #         manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, closestGhost)
            #
            #         next_move = self.chaseGhosts(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
            #
            #         if len(next_move) > 1:
            #             self.clearDfSearchVars()
            #             #print "Choosing randomly :("
            #             #pause = raw_input("hi")
            #             next_move = random.choice(next_move)
            #         elif len(next_move) == 1:
            #             self.clearDfSearchVars()
            #             #print "Removed everything only one available move left ------- Breaks here"
            #             #pause = raw_input("hi")
            #             next_move = next_move[0]
            #         else:
            #             if len(legal) == 0:
            #                 legal = self.resetAvailableLegalMoves(state)
            #             #next_move = random.choice(legal)
            #             next_move = self.dfsearch(pacman_pos, legal)
            #         return api.makeMove(next_move, legal)
            #     else:
            #         if len(legal) == 0:
            #             legal = self.resetAvailableLegalMoves(state)
            #         next_move = self.dfsearch(pacman_pos, legal)
            #         return api.makeMove(next_move, legal)




    # If pacman is stuck then checks the history of pacman's moves and find the last two odd moves.
    # That means pacman visited the same position twice. A counter keeps track of that record and it returns true when that happens.
    def isPacmanStuck(self, pacman_pos):
        counter = 0 # keep track of how many times pacman visited the same position

        # perform the following part when pacman visited at list 4 positions, to prevent any errors from happening.
        if len(self.positions_history) > 4:
            # list = [start:stop:step]
            #
            lastTwoOdd = self.positions_history[-5:-2:2]
            #print self.positions_history
            #p = raw_input("Last three odd" + str(lastTwoOdd))
            for position in lastTwoOdd:
                #print "pac pos: ", pacman_pos
                #print " last3 pos: ", position
                if pacman_pos == position:
                    counter += 1
                    #print "counter: ", counter
                    if counter == 2:
                        return True
        return False

    # Clears the variables that are used for the depth first search
    def clearDfSearchVars(self):
        self.stack = []
        self.visited_nodes = []

    def dfsearch(self, pacman_pos, legal):

        legal_pos_list = []
        unexplored_pos_list = []

        self.visited_nodes.append(pacman_pos)
        x_pac, y_pac = pacman_pos

        for legal_pos in legal:
            if legal_pos == Directions.EAST:
                new_legal_pos = (x_pac + 1, y_pac)
                legal_pos_list.append(new_legal_pos)

            if legal_pos == Directions.WEST:
                new_legal_pos = (x_pac - 1, y_pac)
                legal_pos_list.append(new_legal_pos)

            if legal_pos == Directions.NORTH:
                new_legal_pos = (x_pac, y_pac + 1)
                legal_pos_list.append(new_legal_pos)

            if legal_pos == Directions.SOUTH:
                new_legal_pos = (x_pac, y_pac - 1)
                legal_pos_list.append(new_legal_pos)

        for position in legal_pos_list:
            if position not in self.visited_nodes:
                unexplored_pos_list.append(position)

        if not unexplored_pos_list:
            next_pos = self.stack[-1]
            self.stack.remove(next_pos)
        else:
            self.stack.append(pacman_pos)
            next_pos = unexplored_pos_list[0]


        if next_pos[0] == x_pac - 1 and next_pos[1] == y_pac:
            return Directions.WEST
        elif next_pos[0] == x_pac + 1 and next_pos[1] == y_pac:
            return Directions.EAST
        elif next_pos[1] == y_pac - 1 and next_pos[0] == x_pac:
            return Directions.SOUTH
        elif next_pos[1] == y_pac + 1 and next_pos[0] == x_pac:
            return Directions.NORTH
