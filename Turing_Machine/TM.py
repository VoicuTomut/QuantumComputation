class TuringMachine:
 
   '''
   initialize the Turing Machine, read the program and input
   '''

   def __init__(self, program, input_tape, N, state=0):
     self.trf = {}
     self.state = str(state)
     self.tape = ''.join(['_']*N)
     self.head = N // 2   # head is positioned in the middle
     self.tape = self.tape[:self.head] + input_tape + self.tape[self.head:]
     for line in program.splitlines():
       s, a, r, d, s1 = line.split(' ')
       self.trf[s,a] = (r, d, s1)

   '''
   step through a program
   '''
   def step(self):
     if self.state != 'H':
        # assert self.head >= 0 and self.head < len(self.tape) here
        a = self.tape[self.head]
        action = self.trf.get((self.state, a))
        if action:
           r, d, s1 = action
           self.tape = self.tape[:self.head] + r + self.tape[self.head+1:]
           if d != '*':
              self.head = self.head + (1 if d == 'r' else -1)
           self.state = s1
           print(self.tape.replace('_', ''), self.state)
 
   '''
   run a program
   '''
   def run(self, max_iter=9999):
      iter = 0
      while self.state != 'H' and iter < max_iter: # prevent infinite loop
          self.step()
          iter += 1
      print(self.tape.replace('_', ''), self.state)

