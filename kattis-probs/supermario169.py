#WORK IN PROGRESS
#https://open.kattis.com/problems/supermario169 6.2 Difficulty

import math
from collections import deque

def distance(p1, p2):
    return math.sqrt(sum((a-b)**2 for a,b in zip(p1,p2)))

def mario_tsp(n, start, switches, coins):
    # Flatten all coins: (switch_id, coin_position)
    all_coins = []
    coin_indices_per_switch = []
    for i in range(n):
        idxs = []
        for c in coins[i]:
            idxs.append(len(all_coins))
            all_coins.append((i, c))
        coin_indices_per_switch.append(idxs)

    total_coins = len(all_coins)
    full_mask_s = (1 << n) - 1
    full_mask_c = (1 << total_coins) - 1

    INF = float('inf')
    dp = {}  # key: (mask_switch, mask_coins, last_node), value: distance

    # Initial state: no switches pressed, no coins collected, at start (node -1)
    start_state = (0, 0, -1)  # -1 means start position
    dp[start_state] = 0
    queue = deque([start_state])

    while queue:
        mask_s, mask_c, last = queue.popleft()
        cur_dist = dp[(mask_s, mask_c, last)]
        pos = start if last == -1 else (switches[last] if last < n else all_coins[last][1])

        # Press a new switch
        for i in range(n):
            if not (mask_s & (1 << i)):
                new_mask_s = mask_s | (1 << i)
                # All previously uncollected coins disappear
                new_mask_c = 0
                d = distance(pos, switches[i])
                new_state = (new_mask_s, new_mask_c, i)
                if new_state not in dp or dp[new_state] > cur_dist + d:
                    dp[new_state] = cur_dist + d
                    queue.append(new_state)

        # Collect visible coins (whose switch is last pressed)
        for idx, (sid, cpos) in enumerate(all_coins):
            # Coin is visible only if its switch has been pressed and it is the last pressed switch
            if (mask_s & (1 << sid)) and last == sid and not (mask_c & (1 << idx)):
                new_mask_c = mask_c | (1 << idx)
                d = distance(pos, cpos)
                new_state = (mask_s, new_mask_c, idx + n)  # node id >= n for coins
                if new_state not in dp or dp[new_state] > cur_dist + d:
                    dp[new_state] = cur_dist + d
                    queue.append(new_state)

    # Answer: all switches pressed, all coins collected
    ans = INF
    for (ms, mc, last), d in dp.items():
        if ms == full_mask_s and mc == full_mask_c:
            ans = min(ans, d)
    return ans


# Example usage:
n, mx, my, mz = map(int, input().split())
start = (mx, my, mz)
switches, coins = [], [[] for _ in range(n)]

for i in range(n):
    k, sx, sy, sz = map(int, input().split())
    switches.append((sx,sy,sz))
    for _ in range(k):
        coins[i].append(tuple(map(int, input().split())))

print(mario_tsp(n, start, switches, coins))