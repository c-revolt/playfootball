def list_gamer(players):
    gamers = []
    if (players):
        for player in players:
            players = player[4]
            gamers.append(players)
        gamers = '\n'.join(gamers)
    else:
        gamers = 'На эту игру ещё нет игроков'
    return gamers
