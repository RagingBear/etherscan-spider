from queue import Queue


class BFS:
    name = 'BFS'

    def __init__(self, source):
        self._queue = Queue()
        self._vis = set()
        self._vis.add(source)

    def push(self, edges: list):
        for e in edges:
            self._queue.put(e.get('from'))
            self._queue.put(e.get('to'))

    def pop(self):
        while not self._queue.empty():
            node = self._queue.get()
            if node not in self._vis:
                self._vis.add(node)
                return node
        return None
