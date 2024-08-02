import random

CARDSHAPE = ["♠", "♡", "♢", "♣"]
CARDTYPE = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2"]
JOKER = ["Joker"]
FUNCTION_CARDS = ["5", "7", "8", "10", "J"]
FUNCTION_CARDS_2 = ["5", "7", "8", "9", "10", "J"]

class Player:
    def __init__(self, name):
        self.name = name
        self.cards = []
        self.rank = 0

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def get_cards(self):
        return self.cards
    
    def __str__(self):
        return f"Player: {self.name}, Cards: {self.cards}"
    
    def show_cards(self):
        print(*self.cards, sep=", ")

    def find_singles(self):
        return [[card] for card in self.cards]
    
    def find_pairs(self):
        pairs = []
        card_count = {}
        for card in self.cards:
            if card == "Joker":
                continue  # Handle Joker separately
            card_type = card[:-1]
            if card_type not in card_count:
                card_count[card_type] = 0
            card_count[card_type] += 1

        for card_type, count in card_count.items():
            if count >= 2:
                pairs.append([card_type + s for s in CARDSHAPE if card_type + s in self.cards][:2])

        if "Joker" in self.cards:
            for card_type, count in card_count.items():
                if count == 1:
                    # Find an existing card of that type 
                    for shape in CARDSHAPE:
                        card = card_type + shape
                        if card in self.cards:
                            pairs.append(["Joker", card])
                            break  # Only add one pair with Joker
        return pairs

    def find_triples(self):
        triples = []
        card_count = {}
        for card in self.cards:
            if card == "Joker":
                continue  # Handle Joker separately
            card_type = card[:-1]
            if card_type not in card_count:
                card_count[card_type] = 0
            card_count[card_type] += 1

        for card_type, count in card_count.items():
            if count >= 3:
                triples.append([card_type + s for s in CARDSHAPE if card_type + s in self.cards][:3])

        # Handle Joker as part of a triple
        if "Joker" in self.cards:
            for card_type, count in card_count.items():
                if count == 2: 
                    temp_triple = [card_type + s for s in CARDSHAPE if card_type + s in self.cards]
                    temp_triple.append("Joker")
                    triples.append(temp_triple)
        return triples
    
    def find_quads(self):
        quads = []
        card_count = {}
        for card in self.cards:
            if card == "Joker":
                continue  # Handle Joker separately
            card_type = card[:-1]
            if card_type not in card_count:
                card_count[card_type] = 0
            card_count[card_type] += 1

        for card_type, count in card_count.items():
            if count == 4:
                quads.append([card_type + s for s in CARDSHAPE if card_type + s in self.cards])

        # Handle Joker as part of a quad
        if "Joker" in self.cards:
            for card_type, count in card_count.items():
                if count == 3:
                    temp_quad = [card_type + s for s in CARDSHAPE if card_type + s in self.cards]
                    temp_quad.append("Joker")
                    quads.append(temp_quad)
        
        return quads  
    
    def possible_play(self, in_play, high_priority):
        in_play_count = len(in_play)
        playable_singles = []
        playable_pairs = []
        playable_triples = []
        playable_quads = []

        if in_play_count == 0:
            print("Pile is empty")
            playable_quads = self.find_quads()
            playable_triples = self.find_triples()
            playable_pairs = self.find_pairs()
            playable_singles = self.find_singles()
        else:
            in_play_rank = card_rank(in_play[0])
            print(f"Pile is rank {in_play_rank}")

            if in_play_count == 1:
                print("Pile has single cards")
                if high_priority:
                    playable_singles = [[card] for card in self.cards if card_rank(card) > in_play_rank]
                else:
                    playable_singles = [[card] for card in self.cards if card_rank(card) < in_play_rank]
            elif in_play_count == 2:
                print("Pile has pairs")
                if high_priority:
                    playable_pairs = [pair for pair in self.find_pairs() if card_rank(pair[0]) > in_play_rank or (pair[0] == "Joker" and card_rank(pair[1]) > in_play_rank)]
                else:
                    playable_pairs = [pair for pair in self.find_pairs() if card_rank(pair[0]) < in_play_rank or (pair[0] == "Joker" and card_rank(pair[1]) < in_play_rank)]
            elif in_play_count == 3:
                print("Pile has triples")
                if high_priority:
                    playable_triples = [triple for triple in self.find_triples() if card_rank(triple[0]) > in_play_rank or (triple[0] == "Joker" and card_rank(triple[1]) > in_play_rank)]
                else:
                    playable_triples = [triple for triple in self.find_triples() if card_rank(triple[0]) < in_play_rank or (triple[0] == "Joker" and card_rank(triple[1]) < in_play_rank)]
            elif in_play_count == 4:
                print("Pile has quads")
                if high_priority:
                    playable_quads = [quad for quad in self.find_quads() if card_rank(quad[0]) > in_play_rank or (quad[0] == "Joker" and card_rank(quad[1]) > in_play_rank)]
                else:
                    playable_quads = [quad for quad in self.find_quads() if card_rank(quad[0]) < in_play_rank or (quad[0] == "Joker" and card_rank(quad[1]) < in_play_rank)]

        # Print playable cards in an organized manner
        print("Playable cards:")
        if playable_singles:
            print("  Singles:", ", ".join([f"[{', '.join(single)}]" for single in playable_singles]))
        if playable_pairs:
            print("  Pairs:", ", ".join([f"[{', '.join(pair)}]" for pair in playable_pairs]))
        if playable_triples:
            print("  Triples:", ", ".join([f"[{', '.join(triple)}]" for triple in playable_triples]))
        if playable_quads:
            print("  Quads:", ", ".join([f"[{', '.join(quad)}]" for quad in playable_quads]))

        # Combine all playable options
        playable = playable_quads + playable_triples + playable_pairs + playable_singles
        return self.play_order(playable)
    
# use to sort playable card in order that joker is not used first 
    def play_order(self, playable):
        """Prioritizes playable combinations, placing those without Jokers first."""
        plays_without_joker = []
        plays_with_joker = []

        for play in playable:
            if "Joker" in play:
                plays_with_joker.append(play)
            else:
                plays_without_joker.append(play)

        # Combine the lists, giving priority to plays_without_joker
        return plays_without_joker + plays_with_joker
        


    def sort_cards(self):
        self.cards.sort(key=card_rank)


class Game:
    def __init__(self):
        self.players = []
        self.deck = []
        self.finished_players = []
        self.ruleset = 0

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_players(self):
        return self.players

    def add_players_from_input(self):
        num_players = int(input("Enter the number of players: "))
        for i in range(num_players):
            player_name = str(i+1)
            player = Player(player_name)
            self.add_player(player)

    def set_defult_players(self):
        # num of players
        num = 4
        for i in range(num):
            player_name = str(i+1)
            player = Player(player_name)
            self.add_player(player)

    def set_ruleset(self):
        self.ruleset = int(input("Enter the ruleset (0 for default, 1 includes 9 reverse): "))

    def initialize_deck(self):
        for cs in CARDSHAPE:
            for ct in CARDTYPE:
                self.deck.append(ct+cs)
        self.deck.extend(JOKER)

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        while len(self.deck) > 0:
            for player in self.players:
                if len(self.deck) == 0:
                    break
                card = self.deck.pop()
                player.add_card(card)

    def players_sort_cards(self):
        for player in self.players:
            player.sort_cards()

    def play(self):
        current_pile = []
        current_player_index = 0  
        skip_count = 0
        high_2 = True
        Revolution = False
        game_round_count = 0
        game_direction_plus = True
        
        while len(self.players) > 1:  # Continue while there are at least 2 players
            if skip_count == len(self.players)-1:
                skip_count = 0
                current_pile = []
                if not Revolution:
                    high_2 = True

            current_player = self.players[current_player_index]
            print(f"\n{current_player.name}'s turn:")
        
            print(f"{current_player.name}'s cards: {current_player.cards}")
            print(f"Current pile: {current_pile}")

            playable = current_player.possible_play(current_pile, high_2)
            print("High 2 status: {} Revolutions status: {}".format(high_2, Revolution))
            
            if not playable:
                print("No playable cards. Skipping turn.")
                current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                skip_count += 1
            else:
                to_play = playable[0]
                current_pile = to_play  # Replace the current pile with the new play
                print(f"{current_player.name} plays: {to_play}")

                for card in to_play:
                    current_player.remove_card(card)

                print(f"{current_player.name}'s remaining cards: {current_player.cards}")
                if current_player.cards == []:
                    print(f"{current_player.name} has finished their cards!")
                    self.finished_players.append(current_player)
                    self.players.remove(current_player)
                    if len(self.players) == 1:
                        self.finished_players.append(self.players[0])
                        break
                    current_player_index = current_player_index % len(self.players)
                    continue
                
                # Revolution
                num_of_cards = len(current_pile)
                if num_of_cards == 4:
                    print("Revolution!")
                    current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                    Revolution = not Revolution
                    high_2 = not high_2
                    skip_count = 0 
                    game_round_count += 1
                else:
                    if current_pile[0] == "Joker":
                        ty = current_pile[1][:-1]
                    else:
                        ty = current_pile[0][:-1]
                    print(f"Type of card: {ty}")
                    if ty in FUNCTION_CARDS:
                        match ty:
                            case "5":
                                if game_direction_plus:
                                    if num_of_cards == 1:
                                        current_player_index = (current_player_index + 2) % len(self.players)
                                    elif num_of_cards == 2:
                                        current_player_index = (current_player_index + 3) % len(self.players)
                                    elif num_of_cards == 3:
                                        current_player_index = (current_player_index + 4) % len(self.players)
                                else:
                                    if num_of_cards == 1:
                                        current_player_index = (current_player_index - 2) % len(self.players)
                                    elif num_of_cards == 2:
                                        current_player_index = (current_player_index - 3) % len(self.players)
                                    elif num_of_cards == 3:
                                        current_player_index = (current_player_index - 4) % len(self.players)
                                game_round_count += 1
                            case "7":
                                if num_of_cards in [1, 2, 3]:
                                    cards_to_give = num_of_cards
                                    print(f"{current_player.name} can give {cards_to_give} card(s).")
                                    next_player = self.players[(current_player_index + 1) % len(self.players)]
                                    for _ in range(cards_to_give):
                                        if current_player.cards:
                                            lowest_card = min(current_player.cards, key=lambda x: card_rank(x))
                                            current_player.remove_card(lowest_card)
                                            print(f"{current_player.name} removes: {lowest_card}")
                                            next_player.add_card(lowest_card)
                                            print(f"{next_player.name} adds: {lowest_card}")
                                            
                                    # sort after adding cards
                                    next_player.sort_cards()
                                    print(f"{next_player.name}'s remaining cards: {next_player.cards}")
                                    print(f"{current_player.name}'s remaining cards: {current_player.cards}")
                                    current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                                    skip_count = 0
                                    game_round_count += 1
                            case "8":
                                skip_count = len(self.players)-1
                                game_round_count += 1
                            case "10":
                                if num_of_cards in [1, 2, 3]:
                                    cards_to_remove = num_of_cards
                                    print(f"{current_player.name} can remove {cards_to_remove} card(s).")
                                    for _ in range(cards_to_remove):
                                        if current_player.cards:
                                            lowest_card = min(current_player.cards, key=lambda x: card_rank(x))
                                            current_player.remove_card(lowest_card)
                                            print(f"{current_player.name} removes: {lowest_card}")
                                    print(f"{current_player.name}'s remaining cards: {current_player.cards}")
                                    if game_direction_plus:
                                        current_player_index = (current_player_index + 1) % len(self.players)
                                    else:
                                        current_player_index = (current_player_index - 1) % len(self.players)
                                    skip_count = 0
                                    game_round_count += 1
                            case "J":
                                high_2 = not high_2
                                current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                                skip_count = 0
                                game_round_count += 1
                    else:
                        current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                        skip_count = 0 
                        game_round_count += 1

                if current_player.cards == []:
                    print(f"{current_player.name} has finished their cards!")
                    self.finished_players.append(current_player)
                    self.players.remove(current_player)
                    if len(self.players) == 1:
                        self.finished_players.append(self.players[0])
                        break
                    current_player_index = current_player_index % len(self.players)

        print("\nGame Over!")
        print("Final Rankings:")
        for i, player in enumerate(self.finished_players):
            player.rank = i + 1
            print(f"{player.rank}. {player.name}")

        print(f"\nThe game was played for {game_round_count} rounds")

    def __str__(self):
        player_names = ", ".join([player.name for player in self.players])
        return f"Game with players: {player_names}, Deck: {self.deck}"

def card_rank(card):
    """Returns the rank of a card (higher number is stronger)."""
    if card == "Joker":
        return 14  # Joker is the highest
    return CARDTYPE.index(card[:-1]) + 1 

def choose_non_joker(card_list):
    for card in card_list:
        if card != 'Joker':
            return card


game = Game()


## num of players 
##game.add_players_from_input()
game.set_defult_players()

game.initialize_deck()
game.set_ruleset()
game.shuffle_deck()
game.deal_cards()
game.players_sort_cards()
for i in range(len(game.players)):
    game.players[i].show_cards()

print(game)

game.play()

# game.players[0].add_card("Joker")
# print(game.players[0])
# game.players[0].remove_card("Joker")
# print(game.players[0])