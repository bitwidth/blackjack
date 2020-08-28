'''
Simple game of BlackJack:
HAS:
	Two Players who can:
		Dealer(Computer):
			Hit
			Deal
		Player(Human):
			Hit
			Stand
			Bet
moves only
'''
import modules.cards as cd
import random


class Card():
	
	def __init__(self, suit, rank):
		self.suit = suit
		self.rank = rank
		self.value = cd.values[rank]

	def __str__(self):
		return (f"| {self.rank} of {self.suit} |")


class Deck():

	def __init__(self):
		self.deck = []
		for suit in cd.suits:
			for rank in cd.ranks:
				self.deck.append(Card(suit, rank))
		self.shuffle_deck()

	def __len__(self):
		return len(self.deck)

	def shuffle_deck(self):
		random.shuffle(self.deck)
	
	def deal(self):
		return self.deck.pop()

# d1 = Deck()
# print(d1.deal())

class Player():
	def __init__(self, chips=100):
		self.chips = chips
		self.won = 0
		self.bust = 0
		self.hand = []
		self.score = 0
	
	def __str__(self):
		return (f"Chips: {self.chips}\nWon : {self.won}\nBusts : {self.bust}")

	def won_bust(self):
		self.won+=1
		self.bust+=1
	
	def bet(self, bet_chips):
		if self.chips < bet_chips:
			print(f"Can't bet that much\nYou have -> Chips: {self.chips}")
			return False
		else:
			self.chips -= bet_chips
			print(f"Bet of \'{bet_chips}\' is set.")
			return True
	
	def show_score(self):
		return self.score


class Dealer():
	def __init__(self):
		self.hand = []
		self.won = 0
		self.bust = 0
		self.score = 0

	def __str__(self):
		return "Computer Dealer"
	
	def won_bust(self):
		self.won+=1
		self.bust+=1
	
	def deal(self, deck):
		return deck.deal()
	
	def show_score(self):
		return self.score

def start_game_deal(deck ,dealer, player):
	for i in range(0,2):
		card = ace_card(dealer.deal(deck), dealer)
		dealer.hand.append(card)
		dealer.score += dealer.hand[i].value
		card = ace_card(dealer.deal(deck), player)
		player.hand.append(card)
		player.score += player.hand[i].value

def show_table(d_hand, p_hand,d_score, p_score, game_over):
	temp = d_hand[0]
	global playing
	if playing and not game_over:
#		d_hand[0] = "|  HIDDEN  |"
		show_hands(d_hand, p_hand)
		print(f"Dealer: {d_score-temp.value}	Player: {p_score}")
	else:
		show_hands(d_hand, p_hand)
		print(f"Dealer: {d_score}	Player: {p_score}")
	d_hand[0] = temp

def show_hands(d_hand, p_hand):
	print("Dealer: ")
	for i in range(0,len(d_hand)):
		print(d_hand[i], end='    ')
	print()
	print("Player: ")
	for i in range(0,len(p_hand)):
		print(p_hand[i], end='    ')
	print()

def hit(deck, dealer, player):
	global playing
	card = dealer.deal(deck)
	if playing:
		player.hand.append(ace_card(card, player))
		player.score += card.value
	else:
		dealer.hand.append(ace_card(card, dealer))
		dealer.score += card.value

def stand():
	global playing
	playing = False

def dealer_won(dealer, player):
	d_score, p_score = dealer.score, player.score
	if d_score>21:
		return (True,False)
	elif not playing and d_score<=21 and d_score>p_score:
		return (True, True)
	elif d_score == p_score == 21:
		return(True, True)
	else:
		return (False,False)

def ace_card(card, cur_player):
	if card.rank == 'Ace' and cur_player.score > 10:
		card.value = 1
	return card		

def game_reset(deck, dealer, player):
	global playing
	playing = True
	deck = Deck()
	dealer.hand = []
	dealer.score = 0
	player.hand = []
	player.score = 0
	return (deck, dealer, player)

def update_won_bust(person_won, person_lost):
	person_lost.bust += 1
	person_won.won += 1

def play_again_player(player):
	global play_again 
	while True:
		try:
			bet_again = input("Want to bet again?(Yes/No) : ")
		except ValueError:
			print("enter \'Yes\' or \'No\' please")
			continue
		else:
			if bet_again == "Yes" or  bet_again == "yes":
				if player.chips >= 1:
					bet_again = True
				else:
					print("Not enough chips. Game Over.")
					while True:
						try:
							play_again = input("Want to start all over again?(yes/no)")
						except ValueError:
							print("enter \'Yes\' or \'No\' please")
							continue
						else:
							if play_again == "Yes" or  play_again == "yes":
								play_again=True
								bet_again = False
							elif play_again == "No" or  play_again == "no":
								play_again=False
								bet_again = False
							else:
								continue
							break
			elif bet_again == "No" or  bet_again == "no":
				bet_again = False
				play_again = False
			else:	
				continue
			break
	return bet_again
	
def game(deck, dealer, player):
	bet_again = True
	while bet_again:
		game_over = False
		while True:
			try:
				bet_amount = int(input("Enter the bet amount: "))
				bet_set = player.bet(bet_amount)
				if bet_set:
					pass
				else:
					raise ValueError
			except ValueError:
				print("Please enter valid value")
				continue
			else:
				print("The Dealer will now deal \'2\' cards for themselves and \'2\' cards for the player...")
				start_game_deal(deck, dealer, player)
				break
		
		# GAME STARTS HERE
		while playing:
			print("Cards on the table: \n")
			show_table(dealer.hand, player.hand, dealer.score, player.score, game_over)
			try:
				if player.score<=21:
					move = 0
					while move!='1' and move != '2':
						move = input("Would you like to \'Hit\' or \'Stand\'?(1 or 2): ")
				else:
					show_table(dealer.hand, player.hand, dealer.score, player.score, game_over)
					print("\n\nPlayer busts. DEALER WON!\n")
					update_won_bust(dealer, player)
					game_over = True
					break
			except ValueError:
				print("Please enter valid value(1/2)")
				continue
			else:
				if move == '1':
					print("Hit")
					hit(deck, dealer, player)
				elif move== '2':
					print("Stand.\nDealer is going to play now...\n")
					stand()
		else:
			if not game_over:
				d_won = False
				while not game_over:
					print("Cards on the table: \n")
					hit(deck, dealer, player)
					show_table(dealer.hand, player.hand, dealer.score, player.score, game_over)
					game_over, d_won = dealer_won(dealer, player)
				else:
					if d_won == True and dealer.score == player.score == 21:
						print("\n\nIt's a push. Draw. Your bet was cancelled.\n")
						player.chips += bet_amount
					elif d_won == True:
						print("\n\nPlayer busts. DEALER WON!\n")
						update_won_bust(dealer, player)				
					else:
						print("\n\nDealer busts. PLAYER WON!\n")
						update_won_bust(player, dealer)
						player.chips += (bet_amount*2)
		
		print("\nALL CARDS ON THE TABLE: ")
		show_table(dealer.hand, player.hand, dealer.score, player.score, game_over)

		print("\nYOUR STATS: ")
		print(player)
		print("\n Bet is over!")
		bet_again = play_again_player(player)
		if bet_again:
			deck, dealer, player = game_reset(deck, dealer, player)

def game_start():
	print("Welcome Player!")
	while(True):
		try:
			chips = input("Enter the amount of chips you have(default: 100): ")
			if chips=='':
				chips = 100
				break 
			chips = int(chips)
		except ValueError:
			print("please enter valid value.")
			continue
		else:
			print("Thank you! We welcome you to our casino's BlackJack!")
			break
	player = Player(chips)
	dealer = Dealer()
	deck = Deck()
	while True:
		try:
			call_game = input("Would you like to start the game?(Yes/No)")
		except ValueError:
			print("enter \'Yes\' or \'No\' please")
			continue
		else:
			if call_game == "Yes" or  call_game == "yes" or call_game == "y" or call_game == "Y":
				game(deck, dealer, player)
			elif call_game == "No" or call_game == "no" or call_game == "N" or call_game == "n":
				print("Thank you for visiting us!")
			else:
				continue
			break

playing = True
play_again = True
while play_again:
	game_start()
print("Thank you! For visiting us.\nWe hope you visit us again!")