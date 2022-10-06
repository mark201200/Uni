import dataset

def ingest_tweet(tweet):
    tweet= tweet.lower()

    score_meloni = 0
    for word in dataset.parole_meloni.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            dataset.parole_meloni[word] += 1
            score_meloni += dataset.parole_meloni[word]

    score_renzi = 0
    for word in dataset.parole_renzi.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            dataset.parole_renzi[word] += 1
            score_renzi += dataset.parole_renzi[word]

    score_totti = 0
    for word in dataset.parole_totti.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            dataset.parole_totti[word] += 1
            score_totti += dataset.parole_totti[word]


    return [score_meloni,score_renzi,score_totti]

def updateScore():
    global targetScore_meloni
    targetScore_meloni = (sum(dataset.parole_meloni.values()) / 2) - 1

if __name__ == '__main__':
    updateScore()
    print(targetScore)
    print(ingest_tweet("Giorgia a quando una visita in Uganda?"))


