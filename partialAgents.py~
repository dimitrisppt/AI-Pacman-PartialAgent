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

        self.explored_food = []
        self.explored_capsules = []
        self.empty_nodes = []
        self.predator_mode_on = False
        self.seen_any_ghosts = False
        self.counter = 0

        self.super_powers_time = 40 # Found that from the pacman.py file, SCARED_TIME = 40

        self.explored_corners = False
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False

        # Needed for dfsearch
        self.visited_nodes = []
        self.stack = []



    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like I just died!"

        self.visited_nodes = []
        self.explored_food = []
        self.explored_capsules = []
        self.empty_nodes = []
        self.predator_mode_on = False
        self.seen_any_ghosts = False
        self.super_powers_time = 40

        self.explored_corners = False
        self.BL = False
        self.TL = False
        self.BR = False
        self.TR = False


    # For now I just move randomly
    def getAction(self, state):

        food_list = api.food(state)
        capsules_list = api.capsules(state)
        pacman_pos = api.whereAmI(state)
        ghosts_list = api.ghosts(state)
        walls_list = api.walls(state)
        corner_list = api.corners(state) # Get extreme x and y values for the grid
        legal = api.legalActions(state)

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        self.updateListsOfExploredNodes(state, pacman_pos, food_list, capsules_list, ghosts_list)
        closestFood = self.calculateClosestFood(state, pacman_pos)
        closestCapsule = self.calculateClosestCapsule(state, pacman_pos)
        closestGhost = self.findNearbyGhosts(state, pacman_pos, ghosts_list)


        if self.seen_any_ghosts == False:
            # if self.explored_corners == False and self.counter < 20:
            #     if self.counter > 10:
            #         nextAction = self.cornerSeekingAgent(state, pacman_pos, corner_list, legal)
            #         if nextAction in legal:
            #             self.counter += 1
            #             return api.makeMove(nextAction, legal)
            #
            #     elif self.counter < 20:
            #         nextAction = self.searchForFood(pacman_pos, closestFood, legal)
            #         if nextAction in legal:
            #             self.counter += 1
            #             return api.makeMove(nextAction, legal)
            #         else:
            #             nextAction = self.searchForCapsule(pacman_pos, closestFood, legal)
            #             if nextAction in legal:
            #                 self.counter += 1
            #                 return api.makeMove(nextAction, legal)
            #             else:
            #                 if len(legal) == 0:
            #                     legal = self.resetAvailableLegalMoves(state)
            #                 self.counter += 1
            #                 return api.makeMove(random.choice(legal), legal)
            # else:
            #     self.counter = 0;
            #     nextAction = self.searchForFood(pacman_pos, closestFood, legal)
            #     if nextAction in legal:
            #         return api.makeMove(nextAction, legal)
            #     else:
            #         nextAction = self.searchForCapsule(pacman_pos, closestFood, legal)
            #         if nextAction in legal:
            #             return api.makeMove(nextAction, legal)
            #         else:
            #             if len(legal) == 0:
            #                 legal = self.resetAvailableLegalMoves(state)
            #             return api.makeMove(random.choice(legal), legal)
            nextAction = self.dfsearch(pacman_pos, legal)
            return api.makeMove(nextAction, legal)

        else:

            if self.predator_mode_on == False or self.super_powers_time <= 0:

                if closestGhost:
                    print "there is a ghost aaaah"
                    manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, closestGhost)

                    if manh_dist_pac_ghost < 3:
                        nextAction = self.avoidGhosts(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                        if nextAction in legal:
                            return api.makeMove(nextAction, legal)

                    elif manh_dist_pac_ghost <= 5:
                        #nextAction = self.searchForGhostsToEat(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                        nextAction = self.searchForGhostsToEat(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                        if nextAction in legal:
                            return api.makeMove(nextAction, legal)

                    else:
                        print "---- DO we ever get here? ----"
                        nextAction = self.searchForFood(pacman_pos, closestFood, legal)
                        # if nextAction in legal:
                        #     return api.makeMove(nextAction, legal)
                        if len(nextAction) > 0:
                            print "Oh shit"
                            #pause = raw_input("Press enter")
                        else:
                            return api.makeMove(nextAction, legal)
                        # else:
                        #     # if len(legal) == 0:
                        #     #     legal = api.legalActions(state)
                        #     #     if Directions.STOP in legal:
                        #     #         legal.remove(Directions.STOP)
                        #     nextAction = self.searchForCapsule(pacman_pos, closestCapsule, legal)
                        #     if nextAction in legal:
                        #         return api.makeMove(nextAction, legal)
                        #     else:
                        #         return api.makeMove(random.choice(legal), legal)
                else:
                    print "planning on getting even more confused"
                    nextAction = self.searchForFood(pacman_pos, closestFood, legal)
                    if len(nextAction) > 1:
                        print "Choosing randomly between available moves :("
                        #pause = raw_input("hi")
                        nextAction = random.choice(nextAction)
                    elif len(nextAction) == 1:
                        print "Removed everything only one available move left"
                        #pause = raw_input("hi")
                        nextAction = nextAction[0]
                    else:
                        if len(legal) == 0:
                            legal = self.resetAvailableLegalMoves(state)
                        nextAction = random.choice(legal)
                    return api.makeMove(nextAction, legal)

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

                    nextAction = self.searchForGhostsToEat(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)

                    if len(nextAction) > 1:
                        print "Choosing randomly :("
                        #pause = raw_input("hi")
                        nextAction = random.choice(nextAction)
                    elif len(nextAction) == 1:
                        print "Removed everything only one available move left ------- Breaks here"
                        #pause = raw_input("hi")
                        nextAction = nextAction[0]
                    else:
                        if len(legal) == 0:
                            legal = self.resetAvailableLegalMoves(state)
                        nextAction = random.choice(legal)
                    return api.makeMove(nextAction, legal)
                else:
                    return api.makeMove(random.choice(legal), legal)

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


    def updateListsOfExploredNodes(self, state, pacman_pos, food_list, capsules_list, ghosts_list):
        for food in food_list:
            if food not in self.explored_food:
                self.explored_food.append(food)

        for capsule in capsules_list:
            if capsule not in self.explored_capsules:
                self.explored_capsules.append(capsule)

        if pacman_pos in self.explored_food:
            #self.visited_nodes.append(pacman_pos)
            self.explored_food.remove(pacman_pos)

        if pacman_pos in self.explored_capsules:
            #self.visited_nodes.append(pacman_pos)
            self.explored_capsules.remove(pacman_pos)
            self.predator_mode_on = True
            self.super_powers_time = 40


        if pacman_pos in ghosts_list:
            self.predator_mode_on = False
            self.super_powers_time = 40

        if len(ghosts_list) > 0:
            self.seen_any_ghosts = True



    def calculateClosestFood(self, state, pacman_pos):
        min_dist_to_food = float("inf")
        closestFood = []
        for food in self.explored_food:
            manh_dist_pac_food = util.manhattanDistance(pacman_pos, food)
            if manh_dist_pac_food < min_dist_to_food:
                min_dist_to_food = manh_dist_pac_food
                closestFood = food
        return closestFood


    def calculateClosestCapsule(self, state, pacman_pos):
        min_dist_to_capsule = float("inf")
        closestCapsule = []
        for capsule in self.explored_capsules:
            manh_dist_pac_capsule = util.manhattanDistance(pacman_pos, capsule)
            if manh_dist_pac_capsule < min_dist_to_capsule:
                min_dist_to_capsule = manh_dist_pac_capsule
                closestCapsule = capsule
        return closestCapsule


    def findNearbyGhosts(self, state, pacman_pos, ghosts_list):
        min_dist_to_ghost = float("inf")
        closestGhost = []
        for ghost in ghosts_list:
            manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, ghost)
            if manh_dist_pac_ghost < min_dist_to_ghost:
                min_dist_to_ghost = manh_dist_pac_ghost
                closestGhost = ghost
        return closestGhost

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



    def cornerSeekingAgent(self, state, pacman, corners, legal):

        print corners
        # Setup variable to hold the values
        minX = float("inf")
        minY = float("inf")
        maxX = float("-inf")
        maxY = float("-inf")

        # Sweep through corner coordinates looking for max and min
        # values.
        for i in range(len(corners)):
            cornerX = corners[i][0]
            cornerY = corners[i][1]

            if cornerX < minX:
                minX = cornerX
            if cornerY < minY:
                minY = cornerY
            if cornerX > maxX:
                maxX = cornerX
            if cornerY > maxY:
                maxY = cornerY


        # Check we aren't there:
        if pacman[0] == minX + 1:
            if pacman[1] == minY + 1:
                print "Got to BL!"
                self.BL = True

        # If not, move towards it, first to the West, then to the South.
        if self.BL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.SOUTH in legal:
                    return api.makeMove(Directions.SOUTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
        #
        # Now we've got the lower left corner
        #

        # Move towards the top left corner

        # Check we aren't there:
        if pacman[0] == minX + 1:
           if pacman[1] == maxY - 1:
                print "Got to TL!"
                self.TL = True

        # If not, move West then North.
        if self.TL == False:
            if pacman[0] > minX + 1:
                if Directions.WEST in legal:
                    return api.makeMove(Directions.WEST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Now, the top right corner

        # Check we aren't there:
        if pacman[0] == maxX - 1:
           if pacman[1] == maxY - 1:
                print "Got to TR!"
                self.TR = True

        # Move east where possible, then North
        if self.TR == False:
            if pacman[0] < maxX - 1:
                if Directions.EAST in legal:
                    return api.makeMove(Directions.EAST, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)
            else:
                if Directions.NORTH in legal:
                    return api.makeMove(Directions.NORTH, legal)
                else:
                    pick = random.choice(legal)
                    return api.makeMove(pick, legal)

        # Fromto right it is a straight shot South to get to the bottom right.

        if pacman[0] == maxX - 1:
           if pacman[1] == minY + 1:
                print "Got to BR!"
                self.BR = True
                self.explored_corners = True
                return api.makeMove(random.choice(legal), legal)
           else:
               print "Nearly there"
               return api.makeMove(Directions.SOUTH, legal)

        print "Not doing anything!"
        return api.makeMove(random.choice(legal), legal)
