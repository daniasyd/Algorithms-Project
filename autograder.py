# autograder.py
# -------------
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


# imports from python standard library
import optparse
import sys
import math

import algorithms

# register arguments and set default values
def readCommand(argv):
    parser = optparse.OptionParser(description = 'Run public tests on student code')
    parser.set_defaults(generateSolutions=False, edxOutput=False, gsOutput=False, muteOutput=False, printTestCase=False, noGraphics=False)
##    parser.add_option('--test-directory',
##                      dest = 'testRoot',
##                      default = 'test_cases',
##                      help = 'Root test directory which contains subdirectories corresponding to each question')
##    parser.add_option('--student-code',
##                      dest = 'studentCode',
##                      default = projectParams.STUDENT_CODE_DEFAULT,
##                      help = 'comma separated list of student code files')
##    parser.add_option('--code-directory',
##                    dest = 'codeRoot',
##                    default = "",
##                    help = 'Root directory containing the student and testClass code')
##    parser.add_option('--test-case-code',
##                      dest = 'testCaseCode',
##                      default = projectParams.PROJECT_TEST_CLASSES,
##                      help = 'class containing testClass classes for this project')
##    parser.add_option('--generate-solutions',
##                      dest = 'generateSolutions',
##                      action = 'store_true',
##                      help = 'Write solutions generated to .solution file')
##    parser.add_option('--edx-output',
##                    dest = 'edxOutput',
##                    action = 'store_true',
##                    help = 'Generate edX output files')
    parser.add_option('--gradescope-output',
                    dest = 'gsOutput',
                    action = 'store_true',
                    help = 'Generate GradeScope output files')
    parser.add_option('--mute',
                    dest = 'muteOutput',
                    action = 'store_true',
                    help = 'Mute output from executing tests')
    parser.add_option('--print-tests', '-p',
                    dest = 'printTestCase',
                    action = 'store_true',
                    help = 'Print each test case before running them.')
    parser.add_option('--test', '-t',
                      dest = 'runTest',
                      default = None,
                      help = 'Run one particular test.  Relative to test root.')
    parser.add_option('--question', '-q',
                    dest = 'gradeQuestion',
                    default = None,
                    help = 'Grade one particular question.')
##    parser.add_option('--no-graphics',
##                    dest = 'noGraphics',
##                    action = 'store_true',
##                    help = 'No graphics display for pacman games.')
    (options, args) = parser.parse_args(argv)
    return options




PrisonersDilemma = [[-1,-9],[0,-6]]
MatchingPenniesP1 = [[1,-1],[-1,1]]
MatchingPenniesP2 = [[-1,1],[1,-1]]
AsymmetricGame = [[1,2],[5,3],[5,6]]
ShapleyGame = [[0,0,1],[1,0,0],[0,1,0]]

def compareSolutions(student,answer):
    if len(student) != len(answer):
        return False
    comparisons = [math.isclose(student[i],answer[i],abs_tol=1e-06) for i in range(len(student))]
    return all(comparisons)

def gradeP1Helper(game,opponent,correctAnswer):
    expectations = algorithms.expectedValues(game,opponent)
    correct = compareSolutions(expectations,correctAnswer)
    if correct:
        return 1
    else:
        print("Game:\n" + str(game))
        print("Opponent Strategy:\n" + str(opponent))
        print("Your Answer:\n" + str(expectations))
        print("Correct Answer:\n" + str(correctAnswer))
        return 0

def gradeP1():
    score = 0

    score += gradeP1Helper(PrisonersDilemma,[1.0,0.0],[-1.0,0.0])
    score += gradeP1Helper(PrisonersDilemma,[0.0,1.0],[-9.0,-6.0])    
    score += gradeP1Helper(PrisonersDilemma,[0.5,0.5],[-5.0,-3.0])
    score += gradeP1Helper(MatchingPenniesP1,[0.5,0.5],[0.0,0.0])
    score += gradeP1Helper(AsymmetricGame,[0.5,0.5],[1.5,4.0,5.5])    

    print("#######################################")
    print("P1 SCORE: " + str(score) + " / 5 ")
    print("#######################################")

    return score

def gradeP2Helper(game,opponent,correctAnswer):
    strategy = algorithms.bestResponseDynamics(game,opponent)
    correct = compareSolutions(strategy,correctAnswer)
    if correct:
        return 1
    else:
        print("Game:\n" + str(game))
        print("Opponent Strategy:\n" + str(opponent))
        print("Your Answer:\n" + str(strategy))
        print("Correct Answer:\n" + str(correctAnswer))
        return 0

def gradeP2HelperTie(game,opponent,correctAnswers):
    strategy = algorithms.bestResponseDynamics(game,opponent)
    correct = True
    Reason = 0
    #must be a valid strategy
    if len(strategy) != len(game) or not math.isclose(sum(strategy),1.0):
        correct = False
        reason = 1
    #must only play optimal actions
    else:
        for i in range(len(strategy)):
            if not math.isclose(strategy[i],0.0,abs_tol=1e-06) and not(i in correctAnswers):
                correct = False
                reason = 2
    
    if correct:
        return 1
    else:
        print("Game:\n" + str(game))
        print("Opponent Strategy:\n" + str(opponent))
        print("Your Answer:\n" + str(strategy))
        if reason == 1:
            print("Your answer does not appear to be a valid strategy for this game")
        elif reason == 2:
            print("Only the following actions are best replies:\n" + str(correctAnswers))
        return 0

def gradeP2():
    score = 0

    score += gradeP2Helper(PrisonersDilemma,[1.0,0.0],[0.0,1.0])
    score += gradeP2Helper(PrisonersDilemma,[0.0,1.0],[0.0,1.0])    
    score += gradeP2Helper(PrisonersDilemma,[0.5,0.5],[0.0,1.0])
    score += gradeP2Helper(MatchingPenniesP1,[0.6,0.4],[1.0,0.0])
    score += gradeP2HelperTie(AsymmetricGame,[1.0,0.0],[1,2])    

    print("#######################################")
    print("P2 SCORE: " + str(score) + " / 5 ")
    print("#######################################")

    return score

def gradeAgentHelper(agent,opponent,correctAnswer,roundNumber):
    strategy = agent.updateStrategy(opponent)
    correct = compareSolutions(strategy,correctAnswer)
    print("In round " + str(roundNumber) + " your opponent played:\n" + str(opponent))
    if correct:
        return 1
    else:
        print("Error in Round " + str(roundNumber))
        print("Your Answer:\n" + str(strategy))
        print("Correct Answer:\n" + str(correctAnswer))
        return 0

def gradeP3():
    score = 0

    agent = algorithms.FictitiousPlay(MatchingPenniesP1)
    print("Playing Matching Pennies with your agent.  Payoffs are:\n" + str(MatchingPenniesP1))
    score += gradeAgentHelper(agent,[0.6,0.4],[1.0,0.0],1)
    score += gradeAgentHelper(agent,[0.7,0.3],[1.0,0.0],2)
    score += gradeAgentHelper(agent,[0.0,1.0],[0.0,1.0],3)
    score += gradeAgentHelper(agent,[0.5,0.5],[0.0,1.0],4)
    score += gradeAgentHelper(agent,[1.0,0.0],[1.0,0.0],5)    
    print("#######################################")
    print("P3 SCORE: " + str(score) + " / 5 ")
    print("#######################################")

    return score

def gradeP4():
    score = 0

    agent = algorithms.SmoothedFictitiousPlay(MatchingPenniesP1,1.0)
    print("Playing Matching Pennies with your agent.  Payoffs are:\n" + str(MatchingPenniesP1))
    score += gradeAgentHelper(agent,[0.6,0.4],[0.598687660112452, 0.401312339887548],1)
    score += gradeAgentHelper(agent,[0.7,0.3],[0.6456563062257955, 0.35434369377420455],2)
    score += gradeAgentHelper(agent,[0.0,1.0],[0.4337256058045608, 0.5662743941954392],3)
    score += gradeAgentHelper(agent,[0.5,0.5],[0.4501660026875221, 0.549833997312478],4)
    score += gradeAgentHelper(agent,[1.0,0.0],[0.5597136492671929, 0.4402863507328071],5)    
    print("#######################################")
    print("P4 SCORE: " + str(score) + " / 5 ")
    print("#######################################")

    return score

def gradeP5():
    score = 0

    agent = algorithms.RegretMatching(MatchingPenniesP1)
    print("Playing Matching Pennies with your agent.  Payoffs are:\n" + str(MatchingPenniesP1))
    score += gradeAgentHelper(agent,[0.6,0.4],[1.0, 0.0],1)
    score += gradeAgentHelper(agent,[0.7,0.3],[1.0, 0.0],2)
    score += gradeAgentHelper(agent,[0.0,1.0],[0.16666666666666663, 0.8333333333333334],3)
    score += gradeAgentHelper(agent,[0.5,0.5],[0.16666666666666663, 0.8333333333333334],4)
    score += gradeAgentHelper(agent,[1.0,0.0],[0.736842105263158, 0.26315789473684215],5)    
    print("#######################################")
    print("P5 SCORE: " + str(score) + " / 5 ")
    print("#######################################")

    return score

def selfPlay(player1,player2,prior1,prior2,numRounds):
    oldStrategy2 = prior1
    oldStrategy1 = prior2
    totalStrategy1 = [0.0 for i in range(len(prior2))]
    totalStrategy2 = [0.0 for i in range(len(prior1))]
                      
    for r in range(numRounds):
        newStrategy1 = player1.updateStrategy(oldStrategy2)
        newStrategy2 = player2.updateStrategy(oldStrategy1)
        oldStrategy1 = newStrategy1
        oldStrategy2 = newStrategy2
        for i in range(len(newStrategy1)):
            totalStrategy1[i] += newStrategy1[i]
        for i in range(len(newStrategy2)):
            totalStrategy2[i] += newStrategy2[i]   

    averageStrategy1 = [i/numRounds for i in totalStrategy1]
    averageStrategy2 = [i/numRounds for i in totalStrategy2]
    return [oldStrategy1,oldStrategy2,averageStrategy1,averageStrategy2]

def gradeP6():
    score = 0

    if algorithms.MPPrior1 is None or algorithms.MPPrior2 is None:
        print("P6 Not Implemented!")
        return 0

    agent1 = algorithms.FictitiousPlay(MatchingPenniesP1)
    agent2 = algorithms.FictitiousPlay(MatchingPenniesP2)
    _ , _ ,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.MPPrior1,algorithms.MPPrior2,10000)   

    print("After 10,000 rounds your average strategies were:\n",averageStrategy1,averageStrategy2)
    if (abs(averageStrategy1[0] - 0.5) < 0.01 and abs(averageStrategy2[0] - 0.5) < 0.01):
        score = 2
    else:  
        print("They should be closer to:\n [0.5,0.5],[0.5,0.5]")

    print("#######################################")
    print("P6 SCORE: " + str(score) + " / 2 ")
    print("#######################################")
    return score

def gradeP7():
    score = 0

    if algorithms.ShapleyPrior1 is None or algorithms.ShapleyPrior2 is None:
        print("P7 Not Implemented!")
        return 0

    agent1 = algorithms.FictitiousPlay(ShapleyGame)
    agent2 = algorithms.FictitiousPlay(ShapleyGame)
    _ , _ ,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.ShapleyPrior1,algorithms.ShapleyPrior2,10000)   

    print("After 10,000 rounds your average strategies were:\n",averageStrategy1,averageStrategy2)
    if (abs(averageStrategy1[0] - 0.33) > 0.01 or
        abs(averageStrategy1[1] - 0.33) > 0.01 or
        abs(averageStrategy1[2] - 0.33) > 0.01 or
        abs(averageStrategy2[0] - 0.33) > 0.01 or
        abs(averageStrategy2[1] - 0.33) > 0.01 or
        abs(averageStrategy2[2] - 0.33) > 0.01):
        score = 2
    else:
        print("They should be further from:\n [1/3,1/3,1/3],[1/3,1/3,,1/3]")

    print("#######################################")
    print("P7 SCORE: " + str(score) + " / 2 ")
    print("#######################################")
    return score

class bestResponsePlayer:
    def __init__(self,game):
        self.game = game
    
    def updateStrategy(self,opponentStrategy):
        return algorithms.bestResponseDynamics(self.game,opponentStrategy)

def gradeP8():
    score = 0

    if algorithms.P8Prior1 is None or algorithms.P8Prior2 is None:
        print("P8 Not Implemented!")
        return 0

    agent1 = bestResponsePlayer(algorithms.P8Game1)
    agent2 = bestResponsePlayer(algorithms.P8Game2)
    curStrategy1 , curStrategy2,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.P8Prior1,algorithms.P8Prior2,10000)   

    print("After 10,000 rounds your average strategies with best response dynamics were:\n",averageStrategy1,averageStrategy2)
    print("After 10,000 rounds your current strategies with best response dynamics were:\n",curStrategy1,curStrategy2)
    if (not math.isclose(curStrategy1[0],1.0,abs_tol=1e-06) or not math.isclose(curStrategy2[0],1.0,abs_tol=1e-06)):
        score += 1
    else:
        print("Best response dynamics reached (0,0)! The problem asks you to prevent this.")

    agent1 = algorithms.FictitiousPlay(algorithms.P8Game1)
    agent2 = algorithms.FictitiousPlay(algorithms.P8Game2)
    curStrategy1 , curStrategy2,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.P8Prior1,algorithms.P8Prior2,10000)   

    print("After 10,000 rounds your average strategies with fictitions play were:\n",averageStrategy1,averageStrategy2)
    print("After 10,000 rounds your current strategies with fictitions play were:\n",curStrategy1,curStrategy2)
    if (math.isclose(curStrategy1[0],1.0,abs_tol=1e-06) and math.isclose(curStrategy2[0],1.0,abs_tol=1e-06)):
        score += 1
    else:
        print("Fictitious play failed to reach (0,0)")

    print("#######################################")
    print("P8 SCORE: " + str(score) + " / 2 ")
    print("#######################################")
    return score

def gradeP9():
    score = 0

    if algorithms.P9Prior1 is None or algorithms.P9Prior2 is None:
        print("P9 Not Implemented!")
        return 0

    agent1 = bestResponsePlayer(algorithms.P9Game1)
    agent2 = bestResponsePlayer(algorithms.P9Game2)
    curStrategy1 , curStrategy2,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.P9Prior1,algorithms.P9Prior2,10000)   

    print("After 10,000 rounds your average strategies with best response dynamics were:\n",averageStrategy1,averageStrategy2)
    print("After 10,000 rounds your current strategies with best response dynamics were:\n",curStrategy1,curStrategy2)
    if (math.isclose(curStrategy1[0],1.0,abs_tol=1e-06) and math.isclose(curStrategy2[0],1.0,abs_tol=1e-06)):
        score += 1
    else:
        print("Best response dynamics failed to reach (0,0)")

    agent1 = algorithms.FictitiousPlay(algorithms.P9Game1)
    agent2 = algorithms.FictitiousPlay(algorithms.P9Game2)
    curStrategy1 , curStrategy2,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.P9Prior1,algorithms.P9Prior2,10000)   

    print("After 10,000 rounds your average strategies with fictitions play were:\n",averageStrategy1,averageStrategy2)
    print("After 10,000 rounds your current strategies with fictitions play were:\n",curStrategy1,curStrategy2)
    if (not math.isclose(curStrategy1[0],1.0,abs_tol=1e-06) or not math.isclose(curStrategy2[0],1.0,abs_tol=1e-06)):
        score += 1
    else:
        print("Fictitious play reached (0,0)! The problem asks you to prevent this.")

    print("#######################################")
    print("P9 SCORE: " + str(score) + " / 2 ")
    print("#######################################")
    return score

def gradeP10():
    score = 0

    if algorithms.P10Prior1 is None or algorithms.P10Prior2 is None:
        print("P10 Not Implemented!")
        return 0

    agent1 = algorithms.SmoothedFictitiousPlay(algorithms.P10Game1,2)
    agent2 = algorithms.SmoothedFictitiousPlay(algorithms.P10Game2,2)
    curStrategy1 , curStrategy2,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.P10Prior1,algorithms.P10Prior2,10000)   

    print("After 10,000 rounds your average strategies with smoothed fictitious play were:\n",averageStrategy1,averageStrategy2)
    print("After 10,000 rounds your current strategies with smoothed fictitious play were:\n",curStrategy1,curStrategy2)
    if math.isclose(curStrategy1[0],averageStrategy1[0],abs_tol=0.01) and math.isclose(curStrategy2[0],averageStrategy2[0],abs_tol=0.01):
        score += 1
    else:
        print("Smoothed fictitious play's current strategy failed to converge")

    agent1 = algorithms.RegretMatching(algorithms.P10Game1)
    agent2 = algorithms.RegretMatching(algorithms.P10Game2)
    curStrategy1 , curStrategy2,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.P10Prior1,algorithms.P10Prior2,10000) 

    print("After 10,000 rounds your average strategies with regret matching were:\n",averageStrategy1,averageStrategy2)
    print("After 10,000 rounds your current strategies with regret matching were:\n",curStrategy1,curStrategy2)
    if not math.isclose(curStrategy1[0],averageStrategy1[0],abs_tol=0.01) or not math.isclose(curStrategy2[0],averageStrategy2[0],abs_tol=0.01):
        score += 1
    else:
        print("Regret matching's current strategy converged! The problem asks you to prevent this.")

    print("#######################################")
    print("P10 SCORE: " + str(score) + " / 2 ")
    print("#######################################")
    return score

def gradeP11():
    score = 0

    if algorithms.P10Prior1 is None or algorithms.P10Prior2 is None:
        print("P10 Not Implemented! It is required to do this problem!")
        return 0

    agent1 = algorithms.OptimisticRegretMatching(algorithms.P10Game1)
    agent2 = algorithms.OptimisticRegretMatching(algorithms.P10Game2)
    curStrategy1 , curStrategy2,averageStrategy1,averageStrategy2 = selfPlay(agent1,agent2,algorithms.P10Prior1,algorithms.P10Prior2,10000) 

    print("After 10,000 rounds your average strategies with optimistic regret matching were:\n",averageStrategy1,averageStrategy2)
    print("After 10,000 rounds your current strategies with optimistic regret matching were:\n",curStrategy1,curStrategy2)
    if not math.isclose(curStrategy1[0],averageStrategy1[0],abs_tol=0.05) or not math.isclose(curStrategy2[0],averageStrategy2[0],abs_tol=0.01):
        score += 5
    else:
        print("Optimistic regret matching's current strategy failed to converge.")

    print("#######################################")
    print("P11 SCORE: " + str(score) + " / 5 ")
    print("#######################################")
    return score

def gradeAll():
    total = 0
    total += gradeP1()
    total += gradeP2()
    total += gradeP3()
    total += gradeP4()
    total += gradeP5()
    total += gradeP6()
    total += gradeP7()
    total += gradeP8()
    total += gradeP9()
    total += gradeP10()
    total += gradeP11()
    print("#######################################")
    print("Total Score: " + str(total) + " / 40 ")
    print("#######################################")

if __name__ == '__main__':
    options = readCommand(sys.argv)
    if options.gradeQuestion == "1":
        gradeP1()
    elif options.gradeQuestion == "2":
        gradeP2()
    elif options.gradeQuestion == "3":
        gradeP3()
    elif options.gradeQuestion == "4":
        gradeP4()
    elif options.gradeQuestion == "5":
        gradeP5()
    elif options.gradeQuestion == "6":
        gradeP6()
    elif options.gradeQuestion == "7":
        gradeP7()
    elif options.gradeQuestion == "8":
        gradeP8() 
    elif options.gradeQuestion == "9":
        gradeP9()
    elif options.gradeQuestion == "10":
        gradeP10()
    elif options.gradeQuestion == "11":
        gradeP11()
    elif options.gradeQuestion is not None:
        print("Unknown question: ",options.gradeQuestion)
    else:
        gradeAll()
    
