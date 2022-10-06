import dataset

def calcScores(tweet):                                   #la funzione prende come argomento il testo di un tweet e ritorna i tre punteggi in una lista

    tweet= tweet.lower()

    score_meloni = 0
    for word in dataset.parole_meloni.keys():            #per ogni parola delle parole della meloni
        tweet.find(word)
        if tweet.find(word) != -1:                       #se trovo la parola nel tweet
            #dataset.parole_meloni[word] += 1            #aumento il peso della parola che ho trovato (commentato perché è da implementare bene)
            score_meloni += dataset.parole_meloni[word]  #aggiungo allo score il peso della parola

    score_renzi = 0
    for word in dataset.parole_renzi.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            #dataset.parole_renzi[word] += 1
            score_renzi += dataset.parole_renzi[word]

    score_totti = 0
    for word in dataset.parole_totti.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            #dataset.parole_totti[word] += 1
            score_totti += dataset.parole_totti[word]


    return [score_meloni,score_renzi,score_totti]

def updateScore():
    global targetScore_renzi
    targetScore_meloni = (sum(dataset.parole_meloni.values()) / 2) - 1
    global targetScore_renzi
    targetScore_renzi = (sum(dataset.parole_renzi.values()) / 2) - 1
    global targetScore_totti
    targetScore_totti = (sum(dataset.parole_totti.values()) / 2) - 1

if __name__ == '__main__':
    updateScore()
    print(targetScore)
    print(calcScores("Giorgia a quando una visita in Uganda?"))


