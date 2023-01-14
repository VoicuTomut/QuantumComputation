class TuringMachine:
    '''
    initialize the Turing Machine, read the program and input
    '''

    def __init__(self, program, input_tapes, tapes_sizes, starting_card=0):

        self.card = str(starting_card)

        self.tapes = [''.join(['_'] * n) for n in tapes_sizes]
        self.heads = [ n // 2 for n in tapes_sizes]  # head is positioned in the middle
        self.tapes = [self.tapes[i][:self.heads[i]] + input_tapes[i] + self.tapes[i][self.heads[i]:] for i in
                      range(len(self.tapes))]
        self.nr_tapes = len(self.tapes)

        self.trf = {}  # card:{card:{write, move, next_card}}
        for line in program.splitlines():
            line = line.split(' ')
            if line[0] not in self.trf.keys():
                self.trf[line[0]] = {}

            order = ''
            write = ''
            move = ''
            for i in range(1, self.nr_tapes + 1):
                order += line[i]
                write += line[self.nr_tapes + i]
                move += line[self.nr_tapes * 2 + i]

            self.trf[line[0]][order] = {"write": write, "move": move, "next_card": line[-1]}

    '''
    step through a program
    '''

    def step(self):

        if self.card != 'H':

            head_order = ''
            for had_nr, h in enumerate(self.heads):
                head_order += self.tapes[had_nr][h]

            instruction = self.trf[self.card][head_order]

            # write
            for had_nr, h in enumerate(self.heads):
                l = list(self.tapes[had_nr])
                l[h] = instruction["write"][had_nr]
                self.tapes[had_nr]= ''.join(l)

            # move
            for had_nr in range(len(self.heads)):

                if instruction["move"][had_nr] == "l":
                    move = -1
                elif instruction["move"][had_nr] == "r":
                    move = 1
                else:
                    move = 0

                self.heads[had_nr] += move

            # update card
            self.card = instruction["next_card"]

    '''
    run a program
    '''

    def run(self, max_iter=9999, history=True):
        h = []
        iter = 0
        while self.card != 'H' and iter < max_iter:  # prevent infinite loop
            self.step()
            iter += 1
            if history:
                h.append({"tapes": self.tapes, "head": self.heads, "card": self.card})
        return h
