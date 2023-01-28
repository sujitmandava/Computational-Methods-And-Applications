from random import choices


class TextGenerator:
    # Attributes
    prefixDict = {}

    def assimilateText(self, filename):
        # Input text -> prefix dictionary
        self.prefixDict.clear()

        input = open(filename)
        inputText = input.read()

        # Split text at " "
        words = inputText.split()

        if len(words) < 3:
            raise Exception("Number of words in text file less than 3.")

        # Prefix dictionary generation
        word1, word2 = words[0], words[1]

        for i in range(2, len(words)):
            currWord = words[i]
            currTuple = (word1, word2)
            # Checking if tuple is in dictionary
            if currTuple not in self.prefixDict:
                self.prefixDict[currTuple] = []
            self.prefixDict[currTuple].append(currWord)

            word1 = word2
            word2 = currWord

    def generateText(self, n, startWord=''):
        # prefix dictionary -> random text
        tuples = list(self.prefixDict.keys())
        currTuple = ()
        if startWord == '':  # No start word
            currTuple = choices(tuples)[0]
        else:
            startTuples = []
            for t in tuples:  # Selecting first tuple with fixed word
                if t[0] == startWord:
                    startTuples.append(t)
            if startTuples == []:
                raise Exception(
                    'Unable to produce text with the specified start word.')
            currTuple = choices(startTuples)[0]

        if n == 1:
            print(currTuple[0])
            return

        # Generating text
        wordCount = 0
        text = ""
        while wordCount < n:
            # if tuple exists in prefix dictionary
            if currTuple in list(self.prefixDict.keys()):
                text = text + "{currWord} ".format(currWord=currTuple[0])
                wordCount += 1
                newWord = choices(self.prefixDict[currTuple])[0]
                currTuple = (currTuple[1], newWord)
            else:
                currTuple = choices(tuples)[0]
                text = text + "{currWord} ".format(currWord=currTuple[0])
                wordCount += 1
                newWord = choices(self.prefixDict[currTuple])[0]
                currTuple = (currTuple[1], newWord)

        print(text)
        return


def main():
    gen = TextGenerator()
    gen.assimilateText("sherlock.txt")

    # Prefix dictionary that is generated
    f = open("prefixes.txt", "w")
    f.write(str(gen.prefixDict))
    f.close()

    gen.generateText(100, startWord='London')


if __name__ == "__main__":
    main()
