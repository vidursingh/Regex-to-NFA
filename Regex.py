"""
Vidur Singh. 22 Feb 2018. All rights reserved.

This program will implement membership checking of an arbitrary
string with respect to an input language given by its regular expression.

IMPORTANT NOTE:
Regular expression only over {0,1}
"""


#IMPORTS------------------------------------------------------------------------
import ast
import copy
#GET INPUTS:--------------------------------------------------------------------
#i dont think this code is needed, but i have gotten kinda lost in this web
#so leaving it here just in case. 
"""
#get input for NFA from file.
file = open("NFAstring.txt", "r")
deltafunction = []
line = file.readline().rstrip()

while line:
    deltafunction = deltafunction + [line.split(",")]
    line = file.readline().rstrip()
print(deltafunction)
file.close()


#get string input from file.
string_input = ""
file = open("regex input.txt", "r")
line = file.readline()
string_input += line.strip()
while line:
    line = file.readline()
    string_input += line.strip()
file.close()

"""
#PLEASE ENTER INPUT MANUALY BELOW. REGEX MUST HAVE PARENTHESIS FOR ALL LEVELS OF PRECEDENCE. 

regex = "((1).((0.0)*))"      #"((1.1).0)*)U((0.1)*)"
userinput = "1000"    

# take input for regex:
#regex = str(input("Please enter valid regex (consisting of '()*01.UE'):"))
#Check Validity of regex input--------------------------------------------------

#check for basic validity errors (parenthesis, alphabet):
def valid_regex(expression):
    print("INSIDE VALID REGEX and char is:", expression, len(expression))
    #acceptable chars: U= Union, .=concatenate, E = Epsilon
    acceptable_chars = ["(", ")", "0", "1", ".", "U", "E", "*"]
    parenthesis_count = 0
    #print("len(expression) is:", len(expression))
    if expression == "":
        return False
    if expression == "1" or expression == "0":
        return True
    if len(expression)<3:
        #print("length of expression is less than 3")
        if "U" in expression or "." in expression:
            #print("1st condition satisfied")
            return False
        if "*" in expression:
            #print("2nd condition satisfied")
            if len(expression)<2:
                #print("print third condition satisifed")
                return False
        else:
            print("HAVE A LOOK AT THIS: in else")
            return False
    for char in expression:
        if parenthesis_count >=0 and char in acceptable_chars:
            if char == "(":
                parenthesis_count +=1
            elif char == ")":
                parenthesis_count -=1
        else:
            return False
    if parenthesis_count != 0:
        return False
    else:
        return True

#this function takes a list and an indent value as argument. Returns another list, with all
#integer items in the list updated to original value+ indent
def list_indent(lst, indent):
    indented_lst = []
    for element in (lst):
        
        sub_indented_lst = ''
        string_element = str(element)
        for char in range(0, len(string_element)):
            #see if you can convert char to num. If so, add one and then add to new list. Else, simply add. 
            try:
                new_addition = str(int(string_element[char])+indent)
            except ValueError:
                new_addition = string_element[char]
            sub_indented_lst += new_addition
            
        indented_lst += [ast.literal_eval(sub_indented_lst)]
    return (indented_lst)

#creates the union of two functions
def union(a_delta,b_delta):
    print("INSIDE UNION FUNCTION:\n The delta received were:\n",a_delta, b_delta)
    #new delta function
    new_delta = []
    no_of_states_a = (len(a_delta))-1
    no_of_states_b= (len(b_delta))-1
    #+1 because of new q0 state
    new_number_of_states = (no_of_states_a + no_of_states_b)+1
    #check format of delta function to understand
    new_delta.append([str(new_number_of_states), "01"])
    #delta function for new state 0.
    append_for_q0 = ["(1."+ str(no_of_states_a+1)+")", "q0", "n", "n"]
    new_delta.append(append_for_q0)
    #shift the numeric values of delta_a by 1 (to account for new q0)
    new_a_delta = list_indent(a_delta[1:], 1)
    #correspondingly shift these values by 1+ no of states in a
    new_b_delta = list_indent(b_delta[1:], 1+no_of_states_a)
    #update new delta function
    new_delta += new_a_delta + new_b_delta
    print("UNION FUNCTION DELTA BEING RETURNED IS:\n")
    print(new_delta)
    print("-------exit union-------------------------------")
    return(new_delta)

def update_epsilon_of_a(a_delta_local, where_to_put_new_apsilon_arrows, concatenate = False ):
    #print(a_delta_local)
    #print("INSIDE UPDATE EPSILON OF A FUNCTION")
    for element in range(0, len(a_delta_local)):
        #print("element is", element)
        if "final" in a_delta_local[element]:
            #print("THERE IS A FINAL IN:", a_delta_local[element])
            
            epsilons = a_delta_local[element][a_delta_local[element].index("q"+ str(element-1))-1]
            new_epsilons = epsilons.lstrip("(").rstrip(")")
            #print(new_epsilons)
            if len(new_epsilons) == 0:
                new_epsilons = "("+str(where_to_put_new_apsilon_arrows) + ")"
            else:
                new_epsilons = "(" + new_epsilons + "." + str(where_to_put_new_apsilon_arrows) + ")"
            a_delta_local[element][a_delta_local[element].index("q"+ str(element-1))-1] = new_epsilons
            if concatenate:
                a_delta_local[element] = a_delta_local[element][1:]
            
    #print("a delta is now:", a_delta)
    
    return (a_delta_local)

#there is some insane bug going on here. If I try to pass the same list to this function as its arguments,
#the update_epsilon_of_a function updates BOTH the arguments passed. Makes NO SENSE.
#making a deep copy of the function before passing it as an argument solves the bug, but there still seems to be
#a sketchy explanation for the issue. The only explanation I can think of is that even though the two lists
#were passed as distinct arguments, they still point to the same object, and hence updating one, changes the other.

def concatenate(a_delta, b_delta):
    print("INSIDE CONCATENATE FUNCTION. Original functions:")
    print("a_delta is originally:", a_delta)
    print("b_delta is originally:", b_delta)
    new_delta = []
    no_of_states_a = (len(a_delta))-1
    no_of_states_b= (len(b_delta))-1
    
    new_number_of_states = (no_of_states_a + no_of_states_b)

    new_delta.append([str(new_number_of_states), "01"])

    new_a_delta = update_epsilon_of_a(a_delta, no_of_states_a, concatenate = True)
    new_b_delta = list_indent(b_delta[1:], no_of_states_a)
    #new_b_delta = b_delta
    new_delta += new_a_delta[1:] + new_b_delta
    print("new_delta is now", new_delta)
    print("-------------------------------exit concatenate---------------")
    return(new_delta)


def star(a_delta):
    print("INSIDE STAR FUNCTION:\n")
    print("a_delta is originally:", a_delta)
    new_delta = []
    no_of_states_a = (len(a_delta))-1
    new_number_of_states = (no_of_states_a + 1)
    new_delta.append([str(new_number_of_states), "01"])
    append_for_q0 = ["final", "(1)", "q0", "n", "n"]
    new_delta += [append_for_q0]
    new_delta_a = list_indent(a_delta[1:], 1)
    new_delta += new_delta_a
    new_delta = update_epsilon_of_a(new_delta, 1, concatenate = False)
    append_for_q0 = ["final", "(1)", "q0", "n", "n"]
    new_delta[1] = append_for_q0
    print("new delta is now:\n")
    print(new_delta)
    print("-------------exit star----------------")
    return(new_delta)
    

def how_deep(expression):
    deepness_list = [0]*len(expression)
    operations = ["U", "*", "."]
    parenthesis_count=0
    max_number = len(expression)
    for index in range(len(expression)):
        if expression[index] == "(":
            parenthesis_count += 1
        elif expression[index] == ")":
            parenthesis_count -=1
        if expression[index] in operations:
            deepness_list[index] = parenthesis_count
        else:
            deepness_list[index] = max_number
    #print(deepness_list)
    return(deepness_list)

def remove_redundant_brackets(expression):
    print("INSIDE REMOVE REDUNDANT BRACKETS AND CHAR IS:", expression)
    new_expression = expression
    if len(expression) <3:
        return expression
    while valid_regex(new_expression[1:-1]):
        new_expression = new_expression[1:-1]
    print("expression without redundant brackets was:", new_expression)
    print("----------exit remove redundant brackets---------")
    return (new_expression)
    
def highest_priority(char):
    print("INSIDE HIGHEST PRIORITY AND CHAR IS:", char)
    operations_dictionary = {"U": "union", "*": "star", ".": "concatenate"}
    char_without_redundant_brackets = remove_redundant_brackets(char)
    deepness_list = how_deep(char_without_redundant_brackets)
    min_index = deepness_list.index(min(deepness_list))
    #print("char_without_redundant_brackets :", char_without_redundant_brackets[min_index])
    l = char_without_redundant_brackets[0:min_index]
    r = char_without_redundant_brackets[min_index+1:]
    #print(l, "------", r)
    print(operations_dictionary)
    operation = operations_dictionary[char_without_redundant_brackets[min_index]]
    if operation != "star":
        return_tuple = (operation, l, r)

    elif operation == "star":
        return_tuple = (operation, l)
    print("highest priority tuple is:", return_tuple)
    print("------exit highest priority--------")
    return(return_tuple)


def NFA_1_0(one_or_zero):
    print("INSIDE TO NFA_0_1")
    NFA_1 = [["2", "01"], ["()", "q0", "n", "1"], ["final", "()", "q1", "n", "n"]]
    NFA_0 = [["2", "01"], ["()", "q0", "1", "n"], ["final", "()", "q1", "n", "n"]]
    if one_or_zero ==1:
        print("returned NFA1")
        print("-------------exit one or zero function--------")
        return (NFA_1)
    elif one_or_zero ==0:
        print("returned NFA0")
        print("-------------exit one or zero function--------")
        return (NFA_0)
    else:
        print("woah! something wrong in NFA_1_0 function")
    
def NFA(char):
    print("INSIDE NFA FUNCTION AND CHAR IS", char)
    if char == "1" or char == "(1)":
        print("char is 1")
        return (NFA_1_0(1))
    elif char == "0" or char == "(0)":
        print("char is 0")
        return (NFA_1_0(0))
    else:
        possible_operation = highest_priority(char)
        #print("highest priority returned", possible_operation)
        if possible_operation[0]=="star":
            print("INSIDE STAR", "possible operation = ", possible_operation)
            return(star(NFA(possible_operation[1])))
        elif possible_operation[0] == "concatenate":
            print("INSIDE CONCATENATE", "possible operation = ", possible_operation)
            return(concatenate(NFA(possible_operation[1]),NFA(possible_operation[2])))
        elif possible_operation[0] == "union":
            print("INSIDE UNION", "possible operation = ", possible_operation)
            return(union(NFA(possible_operation[1]),NFA(possible_operation[2])))

nfa = NFA(regex)
#---------Convert regex to ENFA done----------------------------------


#now we must write this delta function to a file.

file = open("regex_delta_function.txt", "w+")
for element in nfa:
    string_to_print = str(element)[1:-1].replace('\'', "").replace(' ','')
    print(string_to_print)
    file.write(string_to_print+"\n")
file.close()

#----------Run the NFA simulation code-----------------------------
#THERE IS A BUG HERE I THINK. I DONT THINK IT WORKS FOR (Q0, N, N). FIX IT TONIGHT. 

file = open("regex_delta_function.txt", "r")
deltafunction = []
line = file.readline().rstrip()

while line:
    deltafunction = deltafunction + [line.split(",")]
    line = file.readline().rstrip()

file.close()
numberofstates = deltafunction[0][0]
alphabet = list(deltafunction[0][1])
currentstates = ["0"]
#activestates = []

file.close()


def EpsilonFunction(deltafunction, activestates, numberofstates):
    print("INSIDE EPSILON FUNCTION AND ACTIVE STATES ARE", activestates)

    newstates = []
    #go through the list of newstates repeatedly until no new changes occur
    while len(newstates)!= len(activestates):
        print("INSIDE EPSILON WHILE LOOP")
        #if while loop condition is true, then we must make the newstates = active
        #states for the current iteration. If changes arise, the while loop
        #condition will become true again. If no changes, that means
        #we need to return the newstates list.

        #add all the active states to the new states.
        #this way, any changes made are only through epsilon functions.
        newstates = copy.deepcopy(activestates)
        #print("newstate = activestate in the beginning of the loop?:", newstates == activestates)
        #print("newstates:", newstates, "activestates:", activestates)
        #list stores the new states, for one iteration through the list. 
        states_to_add =[]
        
        #now, go through the newstates, and find the epsilon arrows:
        for state in newstates:
            state_delta = deltafunction[int(state)+1]
            epsilons = state_delta[state_delta.index("q"+str(state))-1].split(".")
            if epsilons != ["()"]:
                for epsilon in epsilons:
                    states_to_add += [epsilon.lstrip("(").rstrip(")")]
        #print("states_to_add", states_to_add)
        #now remove duplicate elements from states to add
        non_duplicate = []
        for element in states_to_add:
            if element not in non_duplicate:
                non_duplicate.append(element)
        #print("non_duplicate", non_duplicate)
        #now add all elements that were not previously in newstates to it
        for element in non_duplicate:
            if element not in activestates:
                activestates.append(element)
        #print("newstates:", newstates, "activestates:", activestates)
        #print("newstate = activestate at the end of the loop?:", newstates == activestates)
        #now, we have a newstates list with a possibility of new states.
        #if there are new states, while loop condition will be true.
        #else, while loop condition will fail.
    print("STATES RETURNED FROM EPSILON LOOP ARE:", newstates)
    #if while loop condition fails, it means no new states.
    print("------------exit epsilon function-----------")
    return newstates            



def UpdateFunction(alphabet, deltafunction, activestates, inpt):
    newstates = []
    print("INSIDE UPDATE FUNCTION AND ACTIVE STATES ARE", activestates)
    print("INPUT IS:", inpt)
    for state in activestates:
        print("state:", state)
        state_delta = deltafunction[int(state) + 1]
        #print("statedelta", state_delta)
        possible_state_add = [state_delta[state_delta.index("q"+str(state))+ alphabet.index(str(inpt))+1]]
        #print("possible_state_add", possible_state_add)
        if possible_state_add != ["n"]:
            print("!!!!!!!!!!!!!thi is a possible state add:::", possible_state_add)
            newstates += possible_state_add
            print("newstates after adding possible new states", newstates)
    
    newstates = list(set(newstates))
    print("UPDATE FUNCTION RETURNS:", newstates)
    print("--------------exit update function---------------")
    return(newstates)



newstates = EpsilonFunction(deltafunction, currentstates, numberofstates)
while userinput:
    newstates = EpsilonFunction(deltafunction, currentstates, numberofstates)
    #print("1 After Epsilon Function!!!!!!!!", newstates)
    currentinput = userinput[0]
    newstates = UpdateFunction(alphabet, deltafunction, newstates, currentinput)
    #print("2 After Update Function4444444444444", newstates)
    newstates = EpsilonFunction(deltafunction, newstates, numberofstates)
    #print("3 After Epsilon Function!!!!!!!!", newstates)
    userinput = userinput[1:]
    currentstates = newstates



finalstates =currentstates

print(finalstates)
print(nfa)

acceptedflag = False
for state in finalstates:
    if "final" in nfa[int(state)+1]:
        print("ACCEPTED")
        acceptedflag = True
        break

if not acceptedflag:
    print("NOT ACCEPTED")
