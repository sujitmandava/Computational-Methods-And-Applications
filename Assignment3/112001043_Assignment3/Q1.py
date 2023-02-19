class RowVectorFloat:
    def __init__(self, initialList) -> None:
        self.entries = initialList
        self.len = len(initialList)

    def __str__(self) -> str:
        if self.len == 0:
            return '[]'
        
        text = ''
        for i in self.entries:
            text += str(i) + ' '

        return text

    def __len__(self) -> int:
        return self.len

    def __getitem__(self, key):
        return self.entries[key]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def __add__(self, obj):
        if obj.len != self.len:
            raise Exception(
                'Invalid operation; Lengths of vectors must be equal')
        out = []
        for i in range(self.len):
            out.append(self[i] + obj[i])

        return RowVectorFloat(out)

    def __rmul__(self, coef):
        out = []
        for i in self.entries:
            out.append(i*coef)
        return RowVectorFloat(out)

    def __mul__(self, coef):
        out = []
        for i in self.entries:
            out.append(i*coef)
        return RowVectorFloat(out)


if __name__ == '__main__':
    r = RowVectorFloat([1, 2, 4])
    p = RowVectorFloat([])
    
    print(r)
    print(p)
    print(len(r))
    
    print(r[1])
    r[1] = 4
    print(r)
    
    q = RowVectorFloat([1, 2, 3])
    print(q+r)
    print(2*q+r)
