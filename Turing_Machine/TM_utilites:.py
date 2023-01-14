from MTM import TuringMachine

# Snake

# input -> map (with the snake and apple)

# snake_had_position: x=0010; y=010

# apple1: x,y
# apple2: x,y
# apple3: x,y

# count = ___-> 111

# movements
# l, r, u, d (00, 01, 10, 11)

# TM1: make screen white.
# TM2: make screen black:
# #if count = 111

# TM2: draw apple
# # if count =___ draw the first apple
# # if count =1__ draw the second apple
# # if count =11_ draw the third apple
# for e, v in apple_tape_y:  if v==1 write_tape_on_position(x_tape=tapes[e], position=apple_tape_x, 1 )

# TM3: write_tape_on_position # just for the screen tapes
# # go to the start of the tape _0 , _1
# # go to the start of the tape x_tape
# # go to the right till the bans are done but when x_tape ==1 write 1 on tape

# TM4: draw a snake
# #  if count =___ draw it as an apple

#TM5 : erase tail
# for e, v in apple_tape_y:  if v==1 write_tape_on_position(x_tape=tapes[e], position=apple_tape_x, 0 )





