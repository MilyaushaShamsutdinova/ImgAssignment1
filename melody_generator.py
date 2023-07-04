from mido import Message, MidiFile, MidiTrack
from random import choice


def check_note_pitch(note):
    """
    For a melody I chose 3-5 piano octaves.
    In midi notes it is in (47, 84) interval.
    So, method returns a midi note in this interval.

    :return: appropriate midi note
    """
    while note >= 84:
        note -= 12
    while note <= 47:
        note += 12
    return note


class Melody:

    def __init__(self):
        self.orig_midi = MidiFile('megalovania.mid', clip=True)

        self.melody_midi = MidiFile()
        self.track = MidiTrack()
        self.melody_midi.tracks.append(self.track)

        self.orig_notes = []
        self.markov_chain = {}
        self.melody_notes = []
        self.num_notes = 64

    def define_orig_notes(self):
        """
        Method fills list of notes with midi values of Megalovania melody.

        :return: None
        """
        for note in self.orig_midi.tracks[1]:
            if note.type == 'note_on':
                self.orig_notes.append(note.note)

    def create_markov_chain(self):
        """
        Method creates a first-order Markov chain based on the midi notes
        from Megalovania melody.

        :return: dictionary Markov chain
        """
        for i in range(len(self.orig_notes) - 1):
            current_note = self.orig_notes[i]
            next_note = self.orig_notes[i + 1]
            if self.markov_chain.get(current_note, 0) == 0:
                self.markov_chain[current_note] = [next_note]
            else:
                self.markov_chain[current_note].append(next_note)

        # # Prevent consecutive identical notes
        # for key, value in self.markov_chain.items():
        #     if key in value:
        #         value.remove(key)

        return self.markov_chain

    def generate_melody_notes(self):
        """
        Method generates sequence of midi notes for melody based on
        statistical data from created Markov chain.

        :return: list of midi notes of generated melody
        """
        current_note = choice(list(self.markov_chain.keys()))
        for _ in range(self.num_notes):
            self.melody_notes.append(current_note)
            next_notes = self.markov_chain.get(current_note)
            last_note = current_note
            if next_notes:
                current_note = check_note_pitch(choice(next_notes))
                while abs(current_note - last_note) < 2 or abs(current_note - last_note) > 24:
                    current_note = check_note_pitch(choice(next_notes))
            else:
                current_note = check_note_pitch(choice(list(self.markov_chain.keys())))
                while abs(current_note - last_note) < 2 or abs(current_note - last_note) > 24:
                    current_note = check_note_pitch(choice(list(self.markov_chain.keys())))

        return self.melody_notes

    def create_midi(self):
        """
        Method creates a midi file from list of midi notes.

        :return: None
        """
        for note in self.melody_notes:
            self.track.append(Message('note_on', note=note, velocity=127, time=500))
        self.melody_midi.save("melody.mid")

    def melody_time(self):
        """
        Method returns duration of a generated melody.

        :return: melody duration
        """
        time = 0
        for note in self.melody_midi.tracks[0]:
            if note.type == 'note_on' or note.type == 'note_off':
                time += note.time
        return time