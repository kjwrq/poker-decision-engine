from treys import Card, Deck, Evaluator

# str -> int
def card_to_treys(card):
    suit_dict = {
        chr(9830): "d",
        chr(9827): "c",
        chr(9829): "h",
        chr(9824): "s"
    }
    return Card.new(card[0] + suit_dict[card[1]])

# List[int] -> Deck
def unknown_cards(known_cards):
    deck = Deck()
    for c in known_cards:
        deck.cards.remove(c)
    return deck

# Deck -> int
def deal_card(deck):
    return deck.cards.pop()

# List[int] List[int] int Evaluator Random -> str
def simulate(hole, board, opponents, evaluator):
    hole_cards = [card_to_treys(c) for c in hole]
    board_cards = [card_to_treys(c) for c in board]
    deck = unknown_cards(hole_cards + board_cards)

    opp_hands = [[] for o in range(opponents)]
    for i in range(2):
        for o in range(opponents):
            opp_hands[o] += [deal_card(deck)]
    
    for i in range(5 - len(board)):
        deal_card(deck) # burn card
        board_cards += [deal_card(deck)]

    score = evaluator.evaluate(hole_cards, board_cards)
    best_opp_score = None

    for o in range(opponents):
        opp_score = evaluator.evaluate(opp_hands[o], board_cards)
        if opp_score < score:
            return "loss"
        if best_opp_score is None or opp_score < best_opp_score:
            best_opp_score = opp_score
    
    if score < best_opp_score:
        return "win"
    return "tie"

# Dict int -> Dict
def chances(game_state, n_sims = 2000):
    evaluator = Evaluator()

    wins = 0
    ties = 0
    losses = 0

    for i in range(n_sims):
        outcome = simulate(game_state["hole"], game_state["board"], game_state["opponents"], evaluator)
        if outcome == "win":
            wins += 1
        elif outcome == "tie":
            ties += 1
        else:
            losses += 1
    
    win_chance = wins / n_sims
    tie_chance = ties / n_sims
    loss_chance = losses / n_sims

    return {
        "win_chance": round(win_chance, 4),
        "tie_chance": round(tie_chance, 4),
        "loss_chance": round(loss_chance, 4),
        "n_sims": n_sims
    }