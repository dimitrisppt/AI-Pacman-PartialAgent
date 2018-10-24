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



    def resetAvailableLegalMoves(self, state):
        legal = api.legalActions(state)
        if Directions.STOP in legal:
            legal.remove(Directions.STOP)
        return legal

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


    def searchForFood(self, pacman_pos, closest_food, legal):
        print "In search for food!!!!!!!!!!!!!!"
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

        # print "Length of legalmoves in searchforfood is %s" % (len(legal))
        # if len(legal) == 0:
        #     return None

        return legal


    def searchForCapsule(self, pacman_pos, closest_capsule, legal):
        print closest_capsule
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


    def searchForGhostsToEat(self, pacman_pos, closest_ghost, manh_dist_pac_ghost, legal):
        print "breaks here"
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
        if pacman_pos in ghosts_list:
            self.predator_mode_on = False
            self.super_powers_time = 40

        # Sets the flag "seen_any_ghosts" to True when pacman sees a ghost.
        # This happens to enter in a mode where it has to deal with ghosts.
        if len(ghosts_list) > 0:
            self.seen_any_ghosts = True


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


    # Tries to find any nearby ghosts from pacman's position, if any, out of the
    # list of visible ghosts that have been retrieved from the api. The calculation is
    # done using the manhattanDistance function that is provided in the "util.py" file.
    #
    # :param self: Object of the class PartialAgent
    # :param pacman_pos: Current pacman position
    def findNearbyGhosts(self, pacman_pos, ghosts_list):
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
        closestGhost = self.findNearbyGhosts(pacman_pos, ghosts_list) # Calculates and stores the closest ghost, if any, from pacman's position at that state.


        ##########################################################
        ## Safe mode, pacman doesn't have to worry about ghosts ##
        ##########################################################
        if self.seen_any_ghosts == False:
            # Pacman performs an action that is calculated using a depth first search.
            next_move = self.dfsearch(pacman_pos, legal)
            return api.makeMove(next_move, legal)

        else:

            if self.predator_mode_on == False or self.super_powers_time <= 0:

                if closestGhost:
                    print "there is a ghost aaaah"
                    manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, closestGhost)

                    if manh_dist_pac_ghost < 3:
                        next_move = self.avoidGhosts(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                        if next_move in legal:
                            return api.makeMove(next_move, legal)

                    elif manh_dist_pac_ghost <= 5:
                        #next_move = self.searchForGhostsToEat(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                        next_move = self.searchForGhostsToEat(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                        if next_move in legal:
                            return api.makeMove(next_move, legal)

                    else:
                        print "---- DO we ever get here? ----"
                        next_move = self.searchForFood(pacman_pos, closestFood, legal)
                        # if next_move in legal:
                        #     return api.makeMove(next_move, legal)
                        if len(next_move) > 0:
                            print "Oh shit"
                            #pause = raw_input("Press enter")
                        else:
                            return api.makeMove(next_move, legal)
                        # else:
                        #     # if len(legal) == 0:
                        #     #     legal = api.legalActions(state)
                        #     #     if Directions.STOP in legal:
                        #     #         legal.remove(Directions.STOP)
                        #     next_move = self.searchForCapsule(pacman_pos, closestCapsule, legal)
                        #     if next_move in legal:
                        #         return api.makeMove(next_move, legal)
                        #     else:
                        #         return api.makeMove(random.choice(legal), legal)
                else:
                    print "planning on getting even more confused"
                    next_move = self.searchForFood(pacman_pos, closestFood, legal)
                    if len(next_move) > 1:
                        print "Choosing randomly between available moves :("
                        #pause = raw_input("hi")
                        next_move = random.choice(next_move)
                    elif len(next_move) == 1:
                        print "Removed everything only one available move left"
                        #pause = raw_input("hi")
                        next_move = next_move[0]
                    else:
                        if len(legal) == 0:
                            legal = self.resetAvailableLegalMoves(state)
                        next_move = random.choice(legal)
                    return api.makeMove(next_move, legal)

                print "lets do random shit"
                #legal = api.legalActions(state)
                if Directions.STOP in legal:
                    legal.remove(Directions.STOP)

                if len(legal) == 0:
                    legal = self.resetAvailableLegalMoves(state)
                return api.makeMove(random.choice(legal), legal)

            ##########################
            ##---PREDATOR MODE ON---##
            ##########################
            elif self.predator_mode_on == True and self.super_powers_time > 0:
                self.super_powers_time -= 1
                if closestGhost:
                    print "there is a ghost aaaah"
                    manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, closestGhost)

                    next_move = self.searchForGhostsToEat(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)

                    if len(next_move) > 1:
                        print "Choosing randomly :("
                        #pause = raw_input("hi")
                        next_move = random.choice(next_move)
                    elif len(next_move) == 1:
                        print "Removed everything only one available move left ------- Breaks here"
                        #pause = raw_input("hi")
                        next_move = next_move[0]
                    else:
                        if len(legal) == 0:
                            legal = self.resetAvailableLegalMoves(state)
                        next_move = random.choice(legal)
                    return api.makeMove(next_move, legal)
                else:
                    return api.makeMove(random.choice(legal), legal)



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



    # def cornerSeekingAgent(self, state, pacman, corners, legal):
    #
    #     print corners
    #     # Setup variable to hold the values
    #     minX = float("inf")
    #     minY = float("inf")
    #     maxX = float("-inf")
    #     maxY = float("-inf")
    #
    #     # Sweep through corner coordinates looking for max and min
    #     # values.
    #     for i in range(len(corners)):
    #         cornerX = corners[i][0]
    #         cornerY = corners[i][1]
    #
    #         if cornerX < minX:
    #             minX = cornerX
    #         if cornerY < minY:
    #             minY = cornerY
    #         if cornerX > maxX:
    #             maxX = cornerX
    #         if cornerY > maxY:
    #             maxY = cornerY
    #
    #
    #     # Check we aren't there:
    #     if pacman[0] == minX + 1:
    #         if pacman[1] == minY + 1:
    #             print "Got to BL!"
    #             self.BL = True
    #
    #     # If not, move towards it, first to the West, then to the South.
    #     if self.BL == False:
    #         if pacman[0] > minX + 1:
    #             if Directions.WEST in legal:
    #                 return api.makeMove(Directions.WEST, legal)
    #             else:
    #                 pick = random.choice(legal)
    #                 return api.makeMove(pick, legal)
    #         else:
    #             if Directions.SOUTH in legal:
    #                 return api.makeMove(Directions.SOUTH, legal)
    #             else:
    #                 pick = random.choice(legal)
    #                 return api.makeMove(pick, legal)
    #     #
    #     # Now we've got the lower left corner
    #     #
    #
    #     # Move towards the top left corner
    #
    #     # Check we aren't there:
    #     if pacman[0] == minX + 1:
    #        if pacman[1] == maxY - 1:
    #             print "Got to TL!"
    #             self.TL = True
    #
    #     # If not, move West then North.
    #     if self.TL == False:
    #         if pacman[0] > minX + 1:
    #             if Directions.WEST in legal:
    #                 return api.makeMove(Directions.WEST, legal)
    #             else:
    #                 pick = random.choice(legal)
    #                 return api.makeMove(pick, legal)
    #         else:
    #             if Directions.NORTH in legal:
    #                 return api.makeMove(Directions.NORTH, legal)
    #             else:
    #                 pick = random.choice(legal)
    #                 return api.makeMove(pick, legal)
    #
    #     # Now, the top right corner
    #
    #     # Check we aren't there:
    #     if pacman[0] == maxX - 1:
    #        if pacman[1] == maxY - 1:
    #             print "Got to TR!"
    #             self.TR = True
    #
    #     # Move east where possible, then North
    #     if self.TR == False:
    #         if pacman[0] < maxX - 1:
    #             if Directions.EAST in legal:
    #                 return api.makeMove(Directions.EAST, legal)
    #             else:
    #                 pick = random.choice(legal)
    #                 return api.makeMove(pick, legal)
    #         else:
    #             if Directions.NORTH in legal:
    #                 return api.makeMove(Directions.NORTH, legal)
    #             else:
    #                 pick = random.choice(legal)
    #                 return api.makeMove(pick, legal)
    #
    #     # Fromto right it is a straight shot South to get to the bottom right.
    #
    #     if pacman[0] == maxX - 1:
    #        if pacman[1] == minY + 1:
    #             print "Got to BR!"
    #             self.BR = True
    #             self.explored_corners = True
    #             return api.makeMove(random.choice(legal), legal)
    #        else:
    #            print "Nearly there"
    #            return api.makeMove(Directions.SOUTH, legal)
    #
    #     print "Not doing anything!"
    #     return api.makeMove(random.choice(legal), legal)
