from nim import train, play
import pickle

# Implementing a pickle file here to potentially save time on training
# It has an ai trained with n = 100,000

# Open a pickle file
filename = 'trained_ai.pk'

ai = train(10000)

# with open(filename, 'wb') as fi:
    # Dump data into the file
#    pickle.dump(ai, fi)

# load data back to memory when needed for gameplay
#with open(filename, 'rb') as fi:
#    ai = pickle.load(fi)

play(ai)
