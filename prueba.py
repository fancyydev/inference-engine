ar = [[['ae', 'h'], ['bc','d']], [['cd', 'e']], [['ab', 'c']], [['a', 'd']]]
second = []
juntar = ""
for i in ar:
    for j in i:
        antecedentes = j[0]
        conclusion = j[1]
        juntar += antecedentes + "->" + conclusion + ","
        print(juntar)
    second.append(juntar)
    juntar = ""
    print("---------")
    
print(second)