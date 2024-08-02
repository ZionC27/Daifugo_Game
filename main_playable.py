import random
from collections import Counter
from typing import List, Tuple, Optional

CARDSHAPE = ["♠", "♡", "♢", "♣"]
CARDTYPE = ["3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "2"]
JOKER = "Joker"
FUNCTION_CARDS = {"5", "7", "8", "10", "J"}
FUNCTION_CARDS_2 = {"5", "7", "8", "9", "10", "J"}

class Card:
    def __init__(self, value: str, shape: str = None):
        self.value = value
        self.shape = shape
    
    def __str__(self):
        return f"{self.value}{self.shape or ''}"
    
    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return card_rank(self) < card_rank(other)

class Player:
    def __init__(self, name: str, is_human: bool = False):
        self.name = name
        self.cards: List[Card] = []
        self.rank = 0
        self.is_human = is_human

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def show_cards(self):
        print(*self.cards, sep=", ")

    def find_combinations(self) -> Tuple[List[List[Card]], List[List[Card]], List[List[Card]], List[List[Card]]]:
        card_count = Counter(card.value for card in self.cards if card.value != JOKER)
        jokers = [card for card in self.cards if card.value == JOKER]
        
        singles = [[card] for card in self.cards]
        pairs, triples, quads = [], [], []

        for value, count in card_count.items():
            cards = [card for card in self.cards if card.value == value]
            if count >= 2:
                pairs.extend([cards[:2]])
            if count >= 3:
                triples.extend([cards[:3]])
            if count == 4:
                quads.extend([cards])

        # Handle Jokers
        if jokers:
            for value, count in card_count.items():
                if count == 1:
                    pairs.extend([[jokers[0], next(card for card in self.cards if card.value == value)]])
                elif count == 2:
                    triples.extend([jokers[:1] + [card for card in self.cards if card.value == value][:2]])
                elif count == 3:
                    quads.extend([jokers[:1] + [card for card in self.cards if card.value == value]])

        return singles, pairs, triples, quads

    def possible_play(self, in_play: List[Card], high_priority: bool) -> List[List[Card]]:
        singles, pairs, triples, quads = self.find_combinations()
        playable = []

        if not in_play:
            playable = quads + triples + pairs + singles
        else:
            in_play_rank = card_rank(in_play[0])
            in_play_count = len(in_play)

            if in_play_count == 1:
                playable = [[card] for card in self.cards if (high_priority and card > in_play[0]) or (not high_priority and card < in_play[0])]
            elif in_play_count == 2:
                playable = [pair for pair in pairs if (high_priority and pair[0] > in_play[0]) or (not high_priority and pair[0] < in_play[0])]
            elif in_play_count == 3:
                playable = [triple for triple in triples if (high_priority and triple[0] > in_play[0]) or (not high_priority and triple[0] < in_play[0])]
            elif in_play_count == 4:
                playable = [quad for quad in quads if (high_priority and quad[0] > in_play[0]) or (not high_priority and quad[0] < in_play[0])]

        return sorted(playable, key=lambda x: (len(x), card_rank(x[0])), reverse=True)

    def sort_cards(self):
        self.cards.sort()

class Game:
    def __init__(self):
        self.players: List[Player] = []
        self.deck: List[Card] = []
        self.finished_players: List[Player] = []
        self.ruleset = 0

    def initialize_deck(self):
        self.deck = [Card(ct, cs) for cs in CARDSHAPE for ct in CARDTYPE] + [Card(JOKER)] 

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        while self.deck:
            for player in self.players:
                if self.deck:
                    player.add_card(self.deck.pop())

    def play(self):
        current_pile: List[Card] = []
        current_player_index = random.randint(0, len(self.players) - 1)
        skip_count = 0
        high_2 = True
        revolution = False
        game_round_count = 0
        game_direction_plus = True

        function_cards = FUNCTION_CARDS_2 if self.ruleset == 1 else FUNCTION_CARDS

        print(f"\nStarting player: {self.players[current_player_index].name}")

        while len(self.players) > 1:
            if skip_count == len(self.players) - 1:
                skip_count = 0
                current_pile = []
                if not revolution:
                    high_2 = True

            current_player = self.players[current_player_index]
            print(f"\n{current_player.name}'s turn:")
            if not current_player.is_human:
                print(f"{current_player.name}'s cards: {current_player.cards}")
            print(f"Current pile: {current_pile}")

            playable = current_player.possible_play(current_pile, high_2)
            print(f"High 2 status: {high_2} Revolution status: {revolution}")

            if not playable:
                print("No playable cards. Skipping turn.")
                current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                skip_count += 1
            else:
                if current_player.is_human:
                    to_play = self.human_turn(current_player, playable)
                else:
                    to_play = playable[0]
                
                if to_play:
                    current_pile = to_play
                    print(f"{current_player.name} plays: {to_play}")

                    for card in to_play:
                        current_player.remove_card(card)

                    print(f"{current_player.name}'s remaining cards: {current_player.cards}")

                    if not current_player.cards:
                        print(f"{current_player.name} has finished their cards!")
                        self.finished_players.append(current_player)
                        self.players.remove(current_player)
                        if len(self.players) == 1:
                            self.finished_players.append(self.players[0])
                            break
                        current_player_index %= len(self.players)
                        continue

                    num_of_cards = len(current_pile)
                    if num_of_cards == 4:
                        print("Revolution!")
                        current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                        revolution = not revolution
                        high_2 = not high_2
                        skip_count = 0 
                        game_round_count += 1
                    else:
                        ty = self.get_card_type(current_pile)
                        print(f"Type of card: {ty}")
                        if ty in function_cards:
                            result = self.handle_function_card(ty, num_of_cards, current_player, current_player_index, game_direction_plus, high_2)
                            if result:
                                current_player_index, skip_count, high_2, game_direction_plus = result
                            game_round_count += 1
                        else:
                            current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                            skip_count = 0 
                            game_round_count += 1
                else:
                    print(f"{current_player.name} passes.")
                    current_player_index = (current_player_index + (1 if game_direction_plus else -1)) % len(self.players)
                    skip_count += 1

        print("\nGame Over!")
        print("Final Rankings:")
        for i, player in enumerate(self.finished_players):
            player.rank = i + 1
            print(f"{player.rank}. {player.name}")

        print(f"\nThe game was played for {game_round_count} rounds")

    def human_turn(self, player: Player, playable: List[List[Card]]) -> List[Card]:
        print(f"\nYour cards: {player.cards}")
        print("\nPlayable options:")
        for i, play in enumerate(playable):
            print(f"{i + 1}. {play}")
        print(f"{len(playable) + 1}. Pass")

        while True:
            try:
                choice = int(input("Enter the number of your choice: ")) - 1
                if 0 <= choice < len(playable):
                    return playable[choice]
                elif choice == len(playable):
                    return []
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def get_card_type(self, pile: List[Card]) -> str:
        if not pile:
            return ""
        return pile[1].value if pile[0].value == JOKER and len(pile) > 1 else pile[0].value

    def handle_function_card(self, card_type, num_of_cards, current_player, current_player_index, game_direction_plus, high_2):
        if card_type == "5":
            return ((current_player_index + (num_of_cards + 1) * (1 if game_direction_plus else -1)) % len(self.players), 0, high_2, game_direction_plus)
        elif card_type == "7":
            self.handle_seven(current_player, current_player_index, num_of_cards)
            return ((current_player_index + (1 if game_direction_plus else -1)) % len(self.players), 0, high_2, game_direction_plus)
        elif card_type == "8":
            return (current_player_index, len(self.players) - 1, high_2, game_direction_plus)
        elif card_type == "9":
            return ((current_player_index + (1 if not game_direction_plus else -1)) % len(self.players), 0, high_2, not game_direction_plus)
        elif card_type == "10":
            self.handle_ten(current_player, num_of_cards)
            return ((current_player_index + (1 if game_direction_plus else -1)) % len(self.players), 0, high_2, game_direction_plus)
        elif card_type == "J":
            return ((current_player_index + (1 if game_direction_plus else -1)) % len(self.players), 0, not high_2, game_direction_plus)
        return None

    def handle_seven(self, current_player, current_player_index, num_of_cards):
        print(f"{current_player.name} can give up to {num_of_cards} card(s).")
        next_player = self.players[(current_player_index + 1) % len(self.players)]
        
        if current_player.is_human:
            cards_to_give = self.choose_cards(current_player, num_of_cards, "give")
        else:
            cards_to_give = sorted(current_player.cards)[:num_of_cards]

        for card in cards_to_give:
            current_player.remove_card(card)
            next_player.add_card(card)

        next_player.sort_cards()
        
        if current_player.is_human:
            print(f"You gave: {cards_to_give}")
            print(f"Your remaining cards: {current_player.cards}")
        else:
            print(f"{current_player.name} gave {len(cards_to_give)} card(s) to {next_player.name}.")

        if next_player.is_human:
            print(f"You received: {cards_to_give}")
            print(f"Your cards: {next_player.cards}")
        else:
            print(f"{next_player.name} received {len(cards_to_give)} card(s).")

    def handle_ten(self, current_player, num_of_cards):
        print(f"{current_player.name} can remove up to {num_of_cards} card(s).")
        
        if current_player.is_human:
            cards_to_remove = self.choose_cards(current_player, num_of_cards, "remove")
        else:
            cards_to_remove = sorted(current_player.cards)[:num_of_cards]

        for card in cards_to_remove:
            current_player.remove_card(card)

        if current_player.is_human:
            print(f"You removed: {cards_to_remove}")
            print(f"Your remaining cards: {current_player.cards}")
        else:
            print(f"{current_player.name} removed {len(cards_to_remove)} card(s).")

    def choose_cards(self, player: Player, max_cards: int, action: str) -> List[Card]:
        print(f"Your cards: {player.cards}")
        chosen_cards = []
        
        while len(chosen_cards) < max_cards:
            choice = input(f"Enter the index of a card to {action} (1-based), or press Enter to finish: ")
            if choice == "":
                break
            try:
                card_index = int(choice) - 1
                if 0 <= card_index < len(player.cards):
                    chosen_card = player.cards[card_index]
                    if chosen_card not in chosen_cards:
                        chosen_cards.append(chosen_card)
                        print(f"Card {chosen_card} selected.")
                    else:
                        print("You've already selected this card.")
                else:
                    print("Invalid index. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or press Enter to finish.")
        
        return chosen_cards

def card_rank(card: Card) -> int:
    return 14 if card.value == JOKER else CARDTYPE.index(card.value) + 1

# Game setup and execution
game = Game()

# Get number of players
while True:
    try:
        num_players = int(input("Enter the number of players (2-6): "))
        if 2 <= num_players <= 6:
            break
        else:
            print("Please enter a number between 2 and 6.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# Create players
game.players = [Player(f"AI Player {i+1}") for i in range(num_players - 1)]
game.players.append(Player("Human Player", is_human=True))

game.initialize_deck()
game.ruleset = int(input("Enter the ruleset (0 for default, 1 includes 9 reverse): "))
game.shuffle_deck()
game.deal_cards()
for player in game.players:
    player.sort_cards()
    if not player.is_human:
        player.show_cards()

game.play()