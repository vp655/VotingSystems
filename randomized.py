import random as rand
import numpy as np

def factorial(num):
    if(num ==1):
        return 1
    else:
        return num * factorial(num-1)


def randomized(voters, candidates):
    possibilities = factorial(candidates)
    preference_schedule = np.zeros(possibilities)
    random_choice = []
    for i in range(0,possibilities):
        random_choice.append(i)
    sum = voters
    for i in range(0,possibilities):
        index = rand.choice(random_choice)
        if (i == possibilities - 1):
            preference_schedule[index] = sum
        else:
            temp = rand.randint(0,sum)
            preference_schedule[index] = temp
            sum = sum - temp
        random_choice.remove(index)

    return preference_schedule

print(randomized(30,3))


#this randomize implementation is not fully functioning
#stars and bars method much better for the IAC assumption