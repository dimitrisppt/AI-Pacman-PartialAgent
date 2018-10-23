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

        self.visited_nodes = []
        self.explored_food = []
        self.explored_capsules = []
        self.empty_nodes = []
        self.predator_mode_on = False


    # This is what gets run in between multiple games
    def final(self, state):
        print "Looks like I just died!"

        self.visited_nodes = []
        self.explored_food = []
        self.explored_capsules = []
        self.empty_nodes = []
        self.predator_mode_on = False


    # For now I just move randomly
    def getAction(self, state):

        food_list = api.food(state)
        capsules_list = api.capsules(state)
        pacman_pos = api.whereAmI(state)
        ghosts_list = api.ghosts(state)
        walls_list = api.walls(state)
        corner_list = api.corners(state)
        legal = api.legalActions(state)

        if Directions.STOP in legal:
            legal.remove(Directions.STOP)

        self.updateListsOfExploredNodes(state, pacman_pos, food_list, capsules_list, ghosts_list)
        closestFood = self.calculateClosestFood(state, pacman_pos)
        closestCapsule = self.calculateClosestCapsule(state, pacman_pos)
        closestGhost = self.findNearbyGhosts(state, pacman_pos, ghosts_list)

        #nextAction = self.decideNextAction(state, pacman_pos, closestFood, closestCapsule, legal)
        # if closestGhost is not None:
        #     nextAction = self.avoidGhosts(pacman_pos, closestGhost, legal)
        #     if nextAction in legal:
        #         return api.makeMove(nextAction, legal)
        #     else:
        #         return api.makeMove(random.choice(legal), legal)
        # else:
        #     return api.makeMove(random.choice(legal), legal)
        #return api.makeMove(random.choice(legal), legal)

        if self.predator_mode_on == False:

            if closestGhost:
                print "there is a ghost aaaah"
                manh_dist_pac_ghost = self.calculateDistanceFromGhosts(pacman_pos, closestGhost)

                if manh_dist_pac_ghost < 3:
                    nextAction = self.avoidGhosts(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                    if nextAction in legal:
                        return api.makeMove(nextAction, legal)

                elif manh_dist_pac_ghost <= 5:
                    #nextAction = self.searchForGhostsToEat(pacman_pos, closestGhost, manh_dist_pac_ghost, legal)
                    nextAction = self.searchForGhostsToEat(pacman_pos, closestFood, manh_dist_pac_ghost, legal)
                    if nextAction in legal:
                        return api.makeMove(nextAction, legal)

                else:
                    print "---- DO we ever get here? ----"
                    nextAction = self.searchForFood(pacman_pos, closestFood, legal)
                    if nextAction in legal:
                        return api.makeMove(nextAction, legal)
                    else:
                        nextAction = self.searchForCapsule(pacman_pos, closestFood, legal)
                        if nextAction in legal:
                            return api.makeMove(nextAction, legal)
                        else:
                            return api.makeMove(random.choice(legal), legal)
            else:
                print "planning on getting even more confused"
                nextAction = self.searchForFood(pacman_pos, closestFood, legal)
                if nextAction in legal:
                    print "there's no ghosts and I am chill af"

                    return api.makeMove(nextAction, legal)

            print "lets do random shit"
            #legal = api.legalActions(state)
            if Directions.STOP in legal:
                legal.remove(Directions.STOP)

            if len(legal) == 0:
                legal = api.legalActions(state)
                if Directions.STOP in legal:
                    legal.remove(Directions.STOP)
            return api.makeMove(random.choice(legal), legal)

        else:

            nextAction = self.searchForGhostsToEat(pacman_pos, closestGhost, legal)
            if nextAction in legal:
                return api.makeMove(nextAction, legal)
            else:
                return api.makeMove(random.choice(legal), legal)


        # Get the actions we can try, and remove "STOP" if that is one of them.


        # Random choice between the legal options.

    # def avoidGhosts(self, state, pacman_pos, closestGhost, legal):
    #     x_pac, y_pac = pacman_pos
    #     x_ghost, y_ghost = closestGhost
    #
    #     x_dist_ghost = x_pac - x_ghost
    #     y_dist_ghost = y_pac - y_ghost
    #
    #     distance_to_ghost = util.manhattanDistance(pacman_pos, closestGhost)
    #     if distance_to_ghost < 4:
    #         if x_dist_ghost < y_dist_ghost:
    #             if x_dist_ghost < 0:
    #                 if Directions.WEST in legal:
    #                     return Directions.WEST
    #             elif x_dist_ghost > 0:
    #                 if Directions.EAST in legal:
    #                     return Directions.EAST
    #             else:
    #                 return random.choice(legal)
    #         else:
    #             if y_dist_ghost < 0:
    #                 if Directions.SOUTH in legal:
    #                     return Directions.SOUTH
    #             elif y_dist_ghost > 0:
    #                 if Directions.NORTH in legal:
    #                     return Directions.NORTH
    #             else:
    #                 return random.choice(legal)
    #     else:
    #         return random.choice(legal)


    def calculateDistanceFromGhosts(self, pacman_pos, closest_ghost):
        manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, closest_ghost)
        return manh_dist_pac_ghost

    def calculateDistanceFromFood(self, pacman_pos, closest_food):
        manh_dist_pac_food = util.manhattanDistance(pacman_pos, closest_food)
        return manh_dist_pac_food

    def calculateDistanceFromFood(self, pacman_pos, closest_capsule):
        manh_dist_pac_capsule = util.manhattanDistance(pacman_pos, closest_capsule)
        return manh_dist_pac_capsule


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

        print "Length of legalmoves in searchforfood is %s" % (len(legal))
        if len(legal) == 0:
            return None

        return legal


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


    def searchForGhostsToEat(self, pacman_pos, closest_ghost, manh_dist_pac_ghost, legal):

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

        if len(legal) == 0:
            return None
        return legal


    def updateListsOfExploredNodes(self, state, pacman_pos, food_list, capsules_list, ghosts_list):
        for food in food_list:
            if food not in self.explored_food:
                self.explored_food.append(food)

        for capsule in capsules_list:
            if capsule not in self.explored_capsules:
                self.explored_capsules.append(capsule)

        if pacman_pos in self.explored_food:
            self.visited_nodes.append(pacman_pos)
            self.explored_food.remove(pacman_pos)

        if pacman_pos in self.explored_capsules:
            self.visited_nodes.append(pacman_pos)
            self.explored_capsules.remove(pacman_pos)

        if pacman_pos in ghosts_list:
            self.predator_mode_on = True



    def calculateClosestFood(self, state, pacman_pos):
        min_dist_to_food = 999
        closestFood = ()
        print len(self.explored_food)
        for food in self.explored_food:
            manh_dist_pac_food = util.manhattanDistance(pacman_pos, food)
            if manh_dist_pac_food < min_dist_to_food:
                min_dist_to_food = manh_dist_pac_food
                closestFood = food
        print min_dist_to_food
        return closestFood
        #return min_dist_to_food


    def calculateClosestCapsule(self, state, pacman_pos):
        min_dist_to_capsule = float("inf")
        closestCapsule = []
        for capsule in self.explored_capsules:
            manh_dist_pac_capsule = util.manhattanDistance(pacman_pos, capsule)
            if manh_dist_pac_capsule < min_dist_to_capsule:
                min_dist_to_capsule = manh_dist_pac_capsule
                closestCapsule = capsule
        #print min_dist_to_capsule
        return closestCapsule
        #return min_dist_to_capsule


    def findNearbyGhosts(self, state, pacman_pos, ghosts_list):
        min_dist_to_ghost = 999
        closestGhost = []
        for ghost in ghosts_list:
            manh_dist_pac_ghost = util.manhattanDistance(pacman_pos, ghost)
            if manh_dist_pac_ghost < min_dist_to_ghost:
                min_dist_to_ghost = manh_dist_pac_ghost
                closestGhost = ghost
        return closestGhost


    def decideNextAction(self, state, pacman_pos, closestFood, closestCapsule, legal):
        x_pac, y_pac = pacman_pos
        x_food, y_food = closestFood

        x_dist_food = x_pac - x_food
        y_dist_food = y_pac - y_food

        x_dist_capsule = x_pac - x_food
        y_dist_capsule = y_pac - y_food

        if x_dist_food > y_dist_food:
            print "INSIDE IF!"
            # Move east or west
            # move west
            if x_dist_food > 0:
                print "1st"
                if Directions.WEST in legal:
                    return Directions.WEST
            # move east
            elif x_dist_food < 0:
                print "2nd"
                if Directions.EAST in legal:
                    return Directions.EAST
            else:
                print "3rd"
                if Directions.EAST in legal and Directions.WEST in legal:
                    return random.choice([Directions.WEST, Directions.EAST])
                elif Directions.EAST in legal:
                    return Directions.EAST
                elif Directions.WEST in legal:
                    return Directions.WEST
                else:
                    return random.choice(legal)

        elif y_dist_food > x_dist_food:
            print "INSIDE ELIF"
            # Move north or south
            # move south
            if y_dist_food > 0:
                print "4th"
                if Directions.SOUTH in legal:
                    return Directions.SOUTH
            # move north
            elif y_dist_food < 0:
                print "5th"
                if Directions.NORTH in legal:
                    return Directions.NORTH
            else:
                print "6th"
                if Directions.NORTH in legal and Directions.SOUTH in legal:
                    return random.choice([Directions.NORTH, Directions.SOUTH])
                elif Directions.NORTH in legal:
                    return Directions.NORTH
                elif Directions.SOUTH in legal:
                    return Directions.SOUTH
                else:

                    return random.choice(legal)
        else:
            print "INSIDE ELSE"

            return random.choice(legal)
