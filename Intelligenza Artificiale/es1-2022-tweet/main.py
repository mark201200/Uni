import pandas as pd
from statistics import mean

parole_meloni = {
    "governo": 149,
    "meloni": 77,
    "giorgia": 54,
    "draghi": 31,
    "mucche": 30,
    "premier": 21,
    "destra": 18,
    "ugandese": 15,
    "fratelli": 12,
    "presidente": 12,
    "gas": 11
}

parole_renzi = {
    "partito": 17,
    "matteo": 43,
    "renzi": 72,
    "schlein": 16,
    "sinistra": 11,
    "calenda": 8,
    "pd": 57,
    "viva": 26,
    "italia viva": 26
}

parole_totti = {
    "auguri": 121,
    "capitano": 106,
    "francesco": 82,
    "totti": 99,
    "compleanno": 68,
    "ilary": 59,
    "blasi": 35,
    "gol": 24,
    "roma": 17
}


def calcScores(tweet):  # la funzione prende come argomento il testo di un tweet e ritorna i tre punteggi in una lista

    tweet = tweet.lower()

    score_meloni = 0
    for word in parole_meloni.keys():  # per ogni parola delle parole della meloni
        tweet.find(word)
        if tweet.find(word) != -1:  # se trovo la parola nel tweet
            # dataset.parole_meloni[word] += 1           #aumento il peso della parola che ho trovato (commentato perché è da implementare bene)
            score_meloni += parole_meloni[word]  # aggiungo allo score il peso della parola

    score_renzi = 0
    for word in parole_renzi.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            # dataset.parole_renzi[word] += 1
            score_renzi += parole_renzi[word]

    score_totti = 0
    for word in parole_totti.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            # dataset.parole_totti[word] += 1
            score_totti += parole_totti[word]

    return [score_meloni, score_renzi, score_totti]


if __name__ == '__main__':
    ##Testing
    scores = []
    # read excel file
    #df = pd.read_excel('dataset/renzi.xlsx')
    df = pd.read_excel('test_data/meloni_test.xlsx')
    tweets = df.drop(['topic', 'hashtags'], 1).values.tolist()
    for tweet in tweets:
        scores.append(calcScores(tweet[1]))

    meloniscores = []
    renziscores = []
    tottiscores = []
    for score in scores:
        meloniscores.append(score[0])
        renziscores.append(score[1])
        tottiscores.append(score[2])

    #print([mean(meloniscores),mean(renziscores),mean(tottiscores)])
    print(scores)
