import numpy as np
from itertools import permutations
no_of_voters = 10

class Candidate:
    def __init__(self,name,no_of_votes, wins):
        self.name = name
        self.no_of_votes = no_of_votes
        self.wins = wins

class Plurality:
    def __init__(self,Candidate1, Candidate2, Candidate3,cwc_vio):
        self.Candidate1 = Candidate1
        self.Candidate2 = Candidate2
        self.Candidate3 = Candidate3
        self.cwc_vio = cwc_vio

    def determine_all_combinations(self):
        list1 = []
        for i in range(0, 11):
            for j in range(0, 11):
                for k in range(0, 11):
                    for l in range(0,11):
                        for m in range(0,11):
                            for n in range(0,11):
                                while True:
                                    if i+j+k+l+m+n == 10:
                                        list1.append([i,j,k,l,m,n])
                                        break
                                    else:
                                        break
        return list1

    def determine_winner(self):
        #all_permutations = list(permutations(["A", "B", "C"]))
        list1 = self.determine_all_combinations()
        for condition in list1:
            if(condition[0]+condition[1] > condition[2]+condition[3]) and (condition[0]+condition[1] > condition[4]+condition[5]):
                Candidate1.wins = Candidate1.wins + 1
            if(condition[2]+condition[3] > condition[1]+condition[0]) and (condition[2]+condition[3] > condition[4]+condition[5]):
                Candidate2.wins = Candidate2.wins + 1
            if(condition[4]+condition[5] > condition[1]+condition[0]) and (condition[4]+condition[5] > condition[3] + condition[2]):
                Candidate3.wins = Candidate3.wins + 1

    def find_Condorcet(self):
        list1 = self.determine_all_combinations()
        for condition in list1:
            if(condition[0]+condition[1]+condition[4] < condition[2]+condition[3]+condition[5]) and (condition[1]+condition[4]+condition[5] < condition[0]+condition[2]+condition[3]):
               if(condition[2]+condition[3]<=condition[1]+condition[0]) or (condition[2]+condition[3] <= condition[4] + condition[5]):
                   self.cwc_vio = self.cwc_vio + 1
            elif(condition[0] + condition[1] + condition[4] > condition[2] + condition[3] + condition[5]) and (
                   condition[0] + condition[1] + condition[2] > condition[3] + condition[4] + condition[5]):
                if(condition[0] + condition[1] <= condition[2] + condition[3]) or (condition[0] + condition[1] <= condition[4] + condition[5]):
                   self.cwc_vio = self.cwc_vio +  1
            elif(condition[0] + condition[2] + condition[3] < condition[1] + condition[4] + condition[5]) and (
                   condition[0] + condition[1] + condition[2] < condition[3] + condition[4] + condition[5]):
                if(condition[4] + condition[5] <= condition[0] + condition[1]) or condition[4]+condition[5] <= condition[2] + condition[3] :
                    self.cwc_vio = self.cwc_vio +1



Candidate1 = Candidate("A",0,0)
Candidate2 = Candidate("B",0,0)
Candidate3 = Candidate("C",0,0)
method1 = Plurality(Candidate1,Candidate2,Candidate3,0)
method1.determine_winner()
print(Candidate1.name + " wins " + str(Candidate1.wins))
print(Candidate2.name + " wins " + str(Candidate2.wins))
print(Candidate3.name + " wins " + str(Candidate3.wins))
method1.find_Condorcet()
print(method1.cwc_vio)
percentage_time = (method1.cwc_vio) / 3003
print(percentage_time*100)

"""" if (condition[0] + condition[1] >= condition[2] + condition[3]) and (
         condition[0] + condition[1] >= condition[4] + condition[5]) or (condition[4]+condition[5] >= condition[1]+condition[0]) and (condition[4]+condition[5] >= condition[3] + condition[2]):
     self.cwc_vio = self.cwc_vio + 1
if (condition[0] + condition[1] + condition[4] > condition[2] + condition[3] + condition[5]) and (
    condition[0] + condition[1] + condition[2] > condition[3] + condition[4] + condition[5]):
 if (condition[0] + condition[1] < condition[2] + condition[3]) and (
             condition[2] + condition[3] > condition[4] + condition[5]) or (
             condition[4] + condition[5] > condition[1] + condition[0]) and (
             condition[4] + condition[5] > condition[3] + condition[2]):
     self.cwc_vio = self.cwc_vio + 1
if (condition[0] + condition[2] + condition[3] < condition[1] + condition[4] + condition[5]) and (
    condition[0] + condition[1] + condition[2] < condition[3] + condition[4] + condition[5]):
 if (condition[0] + condition[1] > condition[2] + condition[3]) and (
             condition[0] + condition[1] > condition[4] + condition[5]) or (
             condition[2] + condition[3] > condition[1] + condition[0]) and (
             condition[4] + condition[5] < condition[3] + condition[2]):
     self.cwc_vio = self.cwc_vio + 1"""







