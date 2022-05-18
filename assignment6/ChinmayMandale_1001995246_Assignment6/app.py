### Chinmay Mandale
### 1001995246
### Assignment 6


from flask import Flask, render_template, request

app = Flask(__name__)
app.config["DEBUG"] = True

player1turn = True
player2turn = False
totalStones = 0

sharedData = {
    'totalStones': 0,
    'pile1' : 0,
    'pile2' : 0,
    'pile3' : 0,
    'player1' : {
        'lastCount': 0,
        'lastPile': 0
    },
    'player2' : {
        'lastCount': 0,
        'lastPile': 0
    },
    'score':0
}



@app.route('/')
def index():
    return render_template('index.html')


##Set properties for initial of game
@app.route("/judgeEntry", methods=['POST', 'GET'])
def judgeEntry():
    if request.method == 'POST':

        pile1 = request.form.get("pile1")
        pile2 = request.form.get("pile2")
        pile3 = request.form.get("pile3")

        minimum = request.form.get("min")
        maximum = request.form.get("max")

        if pile1 != None and pile2 != None and pile3 != None and minimum != None and maximum != None :

            # Set the game rules
            gamePlay(int(pile1), int(pile2), int(pile3), int(minimum), int(minimum))
            result = []
            result.append(pile1)
            result.append(pile2)
            result.append(pile3)
            result.append(minimum)
            result.append(maximum)
            return render_template('data.html', result=result)

@app.route("/userEntry", methods=['POST', 'GET'])
def userEntry():
    if request.method == 'POST':

        player1Name = request.form.get("player1")
        player2Name = request.form.get("player2")
        judge = request.form.get("judge")



# Form for search criteria
@app.route("/game")
def game():
    return render_template('game.html')

@app.route("/userForm")
def userForm():
    return render_template('userForm.html')

@app.route("/judgeForm")
def judgeForm():
    return render_template('judgeForm.html')



def gamePlay(player1turn, player2turn, pile1, pile2, pile3, pileChosen, stonesToRemove, maximum, minimum):
    #Store in DB
    # totalStones = pile1 + pile2 + pile3

    if stonesToRemove > maximum or stonesToRemove < minimum:
        return "Please enter stones to remove between" + minimum + " and " + maximum

    while totalStones > 0:
        while player1turn == True:
            if pileChosen == "pile1":
                pile1 -= stonesToRemove
            elif pileChosen == "pile2":
                pile2 -= stonesToRemove
            elif pileChosen == "pile3":
                pile3 -= stonesToRemove
            player1turn = False
            player2turn = True
        while player2turn == True:
            if pileChosen == "pile1":
                pile1 -= stonesToRemove
            elif pileChosen == "pile2":
                pile2 -= stonesToRemove
            elif pileChosen == "pile3":
                pile3 -= stonesToRemove
            player2turn = False
            player1turn = True

    if player2turn:
        return "Player 1 Wins"
    else:
        return "Player 2 Wins"



def validate(stonesToRemove, pileChosen):
    global storedData
    if stonesToRemove >= storedData.minimum and stonesToRemove <= storedData.maximum:
        if pileChosen.count >= stonesToRemove:
            return True
        else:
            return False
    else:
        return False


if (__name__ == "__app__"):
    app.run(port=5000)
