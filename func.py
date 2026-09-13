import ast
from typing import List

def minEatingSpeed(piles: List[int], h: int) -> int:
    low = 1
    high = max(piles)
    ans = high

    while low <= high:
        mid = (low + high) // 2
        hours = 0

        for pile in piles:
            hours += (pile + mid - 1) // mid

        if hours <= h:
            ans = mid
            high = mid - 1
        else:
            low = mid + 1

    return ans

# Take input
piles = ast.literal_eval(input())  # e.g. [3,6,7,11]
h = int(input())                   # e.g. 8

print(minEatingSpeed(piles, h))
