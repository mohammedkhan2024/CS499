# heap_expenses.py
# Implements a max-heap structure to efficiently track and retrieve top expenses.

import heapq
import itertools

class ExpenseHeap:
    def __init__(self):
        self.heap = []
        self.counter = itertools.count()  # Unique sequence count for tie breaking

    def push(self, expense):
        # Push a tuple of (-value, unique count, expense) to create a max heap
        count = next(self.counter)
        heapq.heappush(self.heap, (-expense.value, count, expense))

    def pop(self):
        # Pop the largest expense with highest value
        if self.heap:
            return heapq.heappop(self.heap)[2]  # Return the expense object
        return None

    def peek(self):
        # Peek at the largest expense without popping
        if self.heap:
            return self.heap[0][2]
        return None

    def get_top_n(self, n):
        # Get top n expenses without modifying the heap
        # Sort by the negative value only
        return [item[2] for item in heapq.nsmallest(n, self.heap, key=lambda x: x[0])]
