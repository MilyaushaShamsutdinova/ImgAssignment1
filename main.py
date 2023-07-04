from melody_generator import Melody
from accompaniment_generator import Accompaniment

if __name__ == '__main__':
    melody = Melody()
    melody.define_orig_notes()
    markov_chain = melody.create_markov_chain()
    melody_notes = melody.generate_melody_notes()
    melody.create_midi()
    time = melody.melody_time()

    accompaniment = Accompaniment('MAJOR', markov_chain, melody_notes, time)
    accompaniment.generate_accomp_notes()
    accompaniment.create_midi()
