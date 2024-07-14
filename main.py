from gathering_data import getInputs
from simulation import SimStats, TennisGame, match_scores_occurence, set_scores_occurence



firstserveA, winsfirstA, winssecondA, aceA, dfA, firstserveB, winsfirstB, winssecondB, aceB, dfB, n, nameA, nameB, sets_in_a_match= getInputs()
stats = SimStats(nameA, nameB)


for i in range(n):
    theMatch = TennisGame(firstserveA, winsfirstA, winssecondA, aceA, dfA, firstserveB, winsfirstB, winssecondB, aceB, dfB, nameA, nameB, sets_in_a_match)
    theMatch.playMatch()
    stats.update(theMatch)



print("5 most occuring match scores: ")
sorted_match_occurence = dict(sorted(match_scores_occurence.items(), key=lambda item: item[1], reverse=True))

i = 0
for key, value in sorted_match_occurence.items():
    print(f"{key} - {value}  {round((value/n)*100,2)}%")
    if i == 9:
        break
    i += 1



print("10 most occuring set scores: ")
sorted_set_occurence = dict(sorted(set_scores_occurence.items(), key=lambda item: item[1], reverse=True))

number_of_sets = int(stats.number_of_sets)
i = 0
for key, value in sorted_set_occurence.items():
    print(f"{key} - {value}  {round((value/number_of_sets)*100,2)}%")
    if i == 9:
        break
    i += 1

stats.printReport()
