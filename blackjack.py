import random
import pdb

class Blackjack:
	HIT = 'H'
	SPLIT = 'P'
	STAND = 'S'
	DOUBLE_DOWN = 'D'

	def __init__(self, make_decision, num_decks=8, cutoff=104):
		self._cutoff = cutoff
		self._num_decks = num_decks
		self._num_cards_remaining = num_decks * 52

		self._hands_won = 0
		self._hands_lost = 0

		self._make_decision = make_decision

		self._generate_shoe()
		self._generate_distribution()

	def get_distribution(self):
		return self._distribution

	def run(self):
		while not self._is_finished():
			won, lost = self.play()
			self._hands_won += won
			self._hands_lost += lost

		return self._hands_won, self._hands_lost

	def play(self): #returns the number of games won and lost after one round

		dealer_hand = [self._draw(), self._draw()]
		player_hand = [self._draw(), self._draw()]

		#check for blackjacks
		dbj = self._blackjack(dealer_hand)
		pbj = self._blackjack(player_hand)
		if dbj and pbj: return 0, 0
		if dbj: return 0, 1
		if pbj: return 1, 0

		#split hands
		player_games = map(lambda hand: (hand, 'U', 0), self._expand_hands(dealer_hand, player_hand))

		#run each hand
		new_player_games = []
		for game in player_games:
			new_player_games.append((game[0], self._run_player_hand(dealer_hand, game[0]), 0))
		player_games = new_player_games

		#split the busted games and nonbusted games
		bust_games = []
		nonbust_games = []
		for game in player_games:
			if game[1] == 'DB':
				game = (game[0], game[1], -2)
				bust_games.append(game)
			elif game[1] == 'B':
				game = (game[0], game[1], -1)
				bust_games.append(game)
			else:
				nonbust_games.append(game)

		#run the dealer hand
		dealer_result = self._run_dealer_hand(dealer_hand)
		#print("Dealer hand: ", dealer_hand)

		#compare against each player hand
		new_nonbust_games = []
		for game in nonbust_games:
			results = self._hand_result(dealer_hand, game[0])
			if game[1] == 'DS': results *= 2

			#put the losses in bust games
			if results < 0:
				bust_games.append((game[0], game[1], results))
			else:
				new_nonbust_games.append((game[0], game[1], results))
		nonbust_games = new_nonbust_games

		#cumulate results
		hands_won = 0
		hands_lost = 0
		for game in bust_games:
			hands_lost -= game[2]
		for game in nonbust_games:
			hands_won += game[2]

		return hands_won, hands_lost


	#private helpers

	def _draw(self):
		card = self._cards[self._pointer]
		self._distribution[card] -= 1

		self._pointer += 1
		return card

	#returns a list of non-splittable hands
	def _expand_hands(self, dealer_hand, player_hand):
		if player_hand[0] == player_hand[1] and self._make_decision(self._distribution, [0, dealer_hand[0]], player_hand) == self.SPLIT:
			return self._expand_hands(dealer_hand, [player_hand[0], self._draw()]) + self._expand_hands(dealer_hand, [player_hand[0], self._draw()])
		return [player_hand]

	def _run_player_hand(self, dealer_hand, player_hand):
		next_move = 'U'
		while True: 
			#check if previous move required a draw, and check for busts
			if next_move == 'H' or next_move == 'D':
				player_hand.append(self._draw())
				#check if last move was double down
				if next_move == 'D':
					if self._hard_value(player_hand) > 21: return 'DB'
					return 'DS'
				else: #last move was hit, check for bust
					if self._hard_value(player_hand) > 21: return 'B'

			#calc next move
			next_move = self._make_decision(self._distribution, [0] + dealer_hand[1 - len(dealer_hand):], player_hand)

			if next_move == 'S' or next_move == 'P':
				return next_move

	def _run_dealer_hand(self, dealer_hand):
		next_move = 'U'
		while True:
			if self._hard_value(dealer_hand) > 21: return 'B'
			if self._soft_value(dealer_hand) >= 17: return 'S'
			dealer_hand.append(self._draw())

	def _hand_result(self, dealer_hand, player_hand): #assumes player didn't bust
		#we'll need these more than once
		soft_value = self._soft_value(player_hand)
		dealer_soft_value = self._soft_value(dealer_hand)
		#finalize winner and return net gain/loss
		if dealer_soft_value > 21 or dealer_soft_value < soft_value: 
			return 1
		elif dealer_soft_value > soft_value:
			return -1
		else:
			return 0

	def _blackjack(self, hand):
		if len(hand) == 2 and 1 in hand and 10 in hand: return True
		return False

	def _is_finished(self):
		if self._num_decks * 52 - self._pointer <= self._cutoff:
			return True 
		return False

	def _hard_value(self, hand):
		sum = 0
		for card in hand:
			sum += card
		return sum

	def _soft_value(self, hand):
		ace = False
		sum = 0
		for card in hand:
			sum += card
			if card == 1:
				ace = True
		if ace and sum <= 11:
			return sum + 10
		return sum

	#private fcns

	def _generate_shoe(self):
		self._pointer = 0
		self._cards = [0 for i in range(52 * self._num_decks)]
		indices = set(range(52 * self._num_decks))
		for i in range(1, 10):
			for j in range(self._num_decks * 4):
				index = random.sample(indices, 1)[0]
				indices.remove(index)
				self._cards[index] = i
		for i in range(4):
			for j in range(self._num_decks * 4):
				index = random.sample(indices, 1)[0]
				indices.remove(index)
				self._cards[index] = 10

	def _generate_distribution(self):
		count_per_value = self._num_decks * 4
		self._distribution = [count_per_value for i in range(11)]
		self._distribution[0] = 0
		self._distribution[10] = 4 * count_per_value