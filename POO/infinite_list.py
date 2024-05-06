class InfiniteList:
    def __init__(self, *args, fill_value=None):
        self.items = args
        self.fill_value = fill_value
        self.data = []

    def __getitem__(self, index: int):
        for i in range(*index.indices(len(self.data) + 1)):
            if i < len(self.data):
                result.append

    def __len__(self):
        return len(self.prueba)

    def __setitem__(self, index: int, item) -> None:
        return self.items[index]

    def __str__(self):
        return f'{self.prueba}'
