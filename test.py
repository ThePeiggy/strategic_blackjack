from blackjack import Blackjack

def always_stand(distribution, dealer_hand, player_hand):
	return Blackjack.STAND

def always_hit(distribution, dealer_hand, player_hand):
	return Blackjack.HIT


#always hit
total_won = 0
total_lost = 0
total_tied = 0

for i in range(1000):
	bj = Blackjack(always_hit)
	won, lost, tied = bj.run()
	total_won += won
	total_lost += lost
	total_tied += tied

print("Win rate, always hit: " + str(round(total_won * 100.0/(total_won + total_lost + total_tied), 2)) + "%")


#always stand
total_won = 0
total_lost = 0
total_tied = 0

for i in range(1000):
	bj = Blackjack(always_stand)
	won, lost, tied = bj.run()
	total_won += won
	total_lost += lost
	total_tied += tied

print("Win rate, always_stand: " + str(round(total_won * 100.0/(total_won + total_lost + total_tied), 2)) + "%")