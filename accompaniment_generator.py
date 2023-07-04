from mido import Message, MidiFile, MidiTrack
from random import randint


def check_note_pitch(this_note):
    """
    For a melody I chose 1-3 piano octaves.
    In midi notes it is in (23, 60) interval.
    So, method returns a midi note in this interval.

    :return: appropriate midi note
    """
    while this_note >= 60:
        this_note -= 12
    while this_note <= 23:
        this_note += 12
    return this_note


class Accompaniment:

    def __init__(self, scale, markov_chain, melody_notes, time):
        self.melody_midi = MidiFile('melody.mid', clip=True)

        self.accomp_midi = MidiFile()
        self.track = MidiTrack()
        self.accomp_midi.tracks.append(self.track)

        self.chords = {}
        if scale == 'MAJOR':
            for i in range(0, 128):
                self.chords[i] = [i, i + 4, i + 7]
        elif scale == 'MINOR':
            for i in range(0, 128):
                self.chords[i] = [i, i + 3, i + 7]

        self.markov_chain = markov_chain
        self.melody_notes = melody_notes

        self.parts = 16
        self.unit_time = time // self.parts
        self.accomp_notes = []

    def generate_accomp_notes(self):
        """
        Method generates sequence of midi notes for accompaniment based on
        statistical data from created Markov chain.

        :return: None
        """
        num_notes = len(self.melody_notes)
        step = num_notes // self.parts - 1
        for i in range(self.parts):
            start_note = self.melody_notes[num_notes * i // self.parts]
            end_note = self.melody_notes[num_notes * i // self.parts + step]
            possible_chords = self.markov_chain.get(start_note, []) + self.markov_chain.get(end_note, [])

            best_chords = []
            for j in range(len(possible_chords)):
                if abs(possible_chords[j] - start_note) < 24 and abs(possible_chords[j] - end_note) < 24:
                    best_chords.append(possible_chords[j])

            chord_ind = randint(0, len(best_chords) - 1)
            self.accomp_notes.append(check_note_pitch(best_chords[chord_ind]))

    def create_midi(self):
        """
        Method creates a midi file from chords formed by list of midi notes.

        :return: None
        """
        for i in range(len(self.accomp_notes)):
            chord = self.chords[self.accomp_notes[i]]
            self.accomp_midi.tracks[0].append(Message('note_on', channel=0, note=chord[0], velocity=127, time=0))
            self.accomp_midi.tracks[0].append(Message('note_on', channel=0, note=chord[1], velocity=127, time=0))
            self.accomp_midi.tracks[0].append(Message('note_on', channel=0, note=chord[2], velocity=127, time=0))
            self.accomp_midi.tracks[0].append(Message('note_off', channel=0, note=chord[0], velocity=127,
                                                      time=self.unit_time))
            self.accomp_midi.tracks[0].append(Message('note_off', channel=0, note=chord[1], velocity=127, time=0))
            self.accomp_midi.tracks[0].append(Message('note_off', channel=0, note=chord[2], velocity=127, time=0))

        self.melody_midi.tracks.append(self.accomp_midi.tracks[0])
        self.melody_midi.save('melody_with_accomp.mid')