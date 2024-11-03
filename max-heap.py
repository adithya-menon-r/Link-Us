class MaxHeap:
    """
    MaxHeap implementation for getting top K hobbies efficiently
    Heap property: parent is always greater than or equal to its children
    """
    def __init__(self):
        self.heap = []

    def _get_parent_idx(self, idx: int) -> int:
        """Get index of parent node"""
        return (idx - 1) // 2

    def _get_left_child_idx(self, idx: int) -> int:
        """Get index of left child"""
        return 2 * idx + 1

    def _get_right_child_idx(self, idx: int) -> int:
        """Get index of right child"""
        return 2 * idx + 2

    def _swap(self, idx1: int, idx2: int) -> None:
        """Swap two elements in the heap"""
        self.heap[idx1], self.heap[idx2] = self.heap[idx2], self.heap[idx1]

    def insert(self, value) -> None:
        """Insert a new value into heap"""
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def _sift_up(self, idx: int) -> None:
        """Move a node up to its proper position"""
        parent_idx = self._get_parent_idx(idx)
        
        while idx > 0 and self.heap[parent_idx][0] < self.heap[idx][0]:
            self._swap(idx, parent_idx)
            idx = parent_idx
            parent_idx = self._get_parent_idx(idx)

    def extract_max(self):
        """Remove and return the maximum value from heap"""
        if not self.heap:
            return None

        max_value = self.heap[0]
        
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        
        if self.heap:
            self._sift_down(0)
            
        return max_value

    def _sift_down(self, idx: int) -> None:
        """Move a node down to its proper position"""
        max_idx = idx
        size = len(self.heap)

        while True:
            left_idx = self._get_left_child_idx(idx)
            right_idx = self._get_right_child_idx(idx)

            if left_idx < size and self.heap[left_idx][0] > self.heap[max_idx][0]:
                max_idx = left_idx

            if right_idx < size and self.heap[right_idx][0] > self.heap[max_idx][0]:
                max_idx = right_idx

            if max_idx == idx:
                break

            self._swap(idx, max_idx)
            idx = max_idx

    def is_empty(self) -> bool:
        """Check if heap is empty"""
        return len(self.heap) == 0
