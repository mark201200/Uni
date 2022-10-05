import dataset

def ingest_tweet(tweet):
    tweet= tweet.lower()
    score_meloni = 0
    for word in dataset.parole_meloni.keys():
        tweet.find(word)
        if tweet.find(word) != -1:
            dataset.parole_meloni[word] += 1
            score_meloni += dataset.parole_meloni[word]

    return score_meloni

def updateScore():
    global targetScore_meloni
    targetScore_meloni = (sum(dataset.parole_meloni.values()) / 2) - 1

if __name__ == '__main__':
    updateScore()
    print(targetScore)
    print(ingest_tweet("Giorgia a quando una visita in Uganda?"))


