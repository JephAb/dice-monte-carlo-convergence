import random
import matplotlib.pyplot as plt
import math

# ----- Play one game -----
def play_single_game(num_sides, penalty, threshold):
  roll_1 = random.randint(1, num_sides)
  if roll_1 >= threshold:
    return roll_1
  else:
    roll_2 = random.randint(1, num_sides)
    return roll_2 - penalty

# ----- Play many games and track the running average -----
def run_monte_carlo(num_games, num_sides, penalty, threshold):
  results = []
  total = 0
  for game_num in range(1, num_games + 1):
    total = total + play_single_game(num_sides, penalty, threshold)
    running_average = total / game_num
    results.append(running_average)

  return results

# ----- Exact expected value of one game -----
def expected_value(num_sides, penalty, threshold):
  average_reroll = ((1 + num_sides) / 2) - penalty
  total = 0

  for roll_score in range(1, num_sides + 1):
    if roll_score >= threshold:
      total = total + roll_score
    else:
      total = total + average_reroll

  return total / num_sides

# ----- Exact standard deviation of one game -----
def std_dev(num_sides, penalty, threshold):
  variance = 0
  ev = expected_value(num_sides, penalty, threshold)

  for r1 in range(1, num_sides + 1):
    if r1 >= threshold:
      distance = r1 - ev
      variance = variance + (distance * distance) * (1 / num_sides)

    else:
      for r2 in range(1, num_sides + 1):
        distance = (r2 - penalty) - ev
        variance = variance + (distance * distance) * (1 / num_sides * 1 / num_sides)

  return math.sqrt(variance)

# ----- Settings -----
num_games, num_sides, penalty, threshold = 10000, 6, 1.0, 2.5

# ----- Exact values and the +/- 2 standard error band -----
ev = expected_value(num_sides, penalty, threshold)
sd = std_dev(num_sides, penalty, threshold)
games = []
upper = []
lower = []
for game_num in range(1, num_games + 1):
  se = sd / math.sqrt(game_num)
  games.append(game_num)
  upper.append(ev + 2 * se)
  lower.append(ev - 2 * se)

final_se = sd / math.sqrt(num_games)

# ----- Run the simulation -----
averages = run_monte_carlo(num_games, num_sides, penalty, threshold)

# ----- Compare the simulation to the exact value -----
simulated = averages[num_games - 1]
gap = simulated - ev
gap_in_se = gap / final_se

print(f'Expected Value of the entire 2-roll game is {ev:.4f}')
print(f'Simulated average of {num_games} games is {simulated:.4f}')
print(f'Standard deviation of the scores from the expected value is {sd:.2f}')
print(f'Standard error at {num_games} games is {final_se:.4f}')
print(f'Gap between simulated average and expected value is {gap:.4f}, which is {gap_in_se:.2f} standard errors')

# ----- Plot -----
plt.plot(games, averages, label='Running average')
plt.axhline(y=ev, linestyle='--', color='r', label=f'Total Expected Value: {ev:.4f}')
plt.fill_between(games, lower, upper, alpha=0.2, label='±2 standard errors')
plt.xscale('log')
plt.ylim(3.0, 4.7)
plt.xlabel('Number of Games (log scale)')
plt.ylabel('Running Average of Scores')
plt.title('Convergence of Running Averages to the Total Expected Value')
plt.legend()
plt.show()

# ----- Best threshold: expected score for every threshold -----
thresholds = []
evs = []

for t in range(1, num_sides + 2):
  threshold_ev = expected_value(num_sides, penalty, t)
  thresholds.append(t)
  evs.append(threshold_ev)

best_threshold = thresholds[0]
best_ev = evs[0]
for i in range(len(evs)):
  if evs[i] > best_ev:
    best_ev = evs[i]
    best_threshold = thresholds[i]

print(f'The best threshold is {best_threshold} and its expected value is {best_ev:.4f}.')

# ----- Plot: expected score by threshold -----
plt.plot(thresholds, evs, marker='o', label='Expected score')
plt.plot(best_threshold, best_ev, 'go', markersize=10, label=f'Best threshold: {best_threshold}')
plt.xlabel('Threshold (keep first roll if roll >= threshold)')
plt.ylabel('Expected score')
plt.title('Expected Score by Threshold')
plt.legend()
plt.show()
