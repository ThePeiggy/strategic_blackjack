from blackjack import Blackjack

def make_decision(distribution, dealer_hand, player_hand):
	return Blackjack.HIT

total_won = 0
total_lost = 0

for i in range(1000):
	bj = Blackjack(make_decision)
	won, lost = bj.run()
	total_won += won
	total_lost += lost

print("Win rate: " + str(round(total_won * 100.0/(total_won + total_lost), 2)) + "%")