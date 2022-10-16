import random

def rat(mymoves, othermoves, totalRounds, currentRound):
    #Always Rats
    return True

def silent(mymoves, othermoves, totalRounds, currentRound):
    #Always stays silent
    return False

def ratLast(mymoves, othermoves, totalRounds, currentRound):
    #Stays silent until the very last round
    if currentRound == totalRounds-1:
        return True
    return False

def rand(mymoves, othermoves, totalRounds, currentRound):
    #Choose completely randomly 50-50
    return bool(random.getrandbits(1))

def kindaRandom(mymoves, othermoves, totalRounds, currentRound):
    #Chooses kinda randomly. Change the variable below to tell it how often to rat. For example, if randomness is set to 0.9, this player will rat 90% of the time
    randomness = 0.9
    
    randNumber = random.random()
    if randNumber < randomness:
        return True
    return False

def titFortat(mymoves, othermoves, totalRounds, currentRound):
    #Stays silent until the other player rats. If the other player's last move is rat this player only rats for this round. 
    if len(othermoves) == 0:
        return False
    if othermoves[-1]:
        return True
    return False

def titForTwotats(mymoves, othermoves, totalRounds, currentRound):
    #Stays silent until the other player rats twice in a row. If the other player's last 2 moves is rat this player only rats for this round. 
    if len(othermoves) < 2:
        return False
    if othermoves[-1] and othermoves[-2]:
        return True
    else:
        return False

def nukeFortat(mymoves, othermoves, totalRounds, currentRound):
    #Stays silent until the other player rats. If the other player's rats this player rats forever. 
    if len(othermoves) == 0:
        return False
    if True in othermoves:
        return True
    return False

def nukeForTwotats(mymoves, othermoves, totalRounds, currentRound):
    #Stays silent until the other player rats twice. If the other player's rats twice this player rats forever. 
    if len(othermoves) < 2:
        return False
    indices = [i for i, x in enumerate(othermoves) if x == True]
    for i in range(len(indices)-1):
        if indices[i] == indices[i+1]-1:
            return True
    return False