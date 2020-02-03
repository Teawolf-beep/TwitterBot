import tkinter as tk
from random import randint

from loader import Loader
from trainer import Trainer
from generator import Generator


class GuiRandomSeed:
    def __init__(self, tokenizer_trump, tokenizer_clinton, model_trump, model_clinton,
                 sequence_file_trump, sequence_file_clinton):
        self.model_trump = model_trump
        self.model_clinton = model_clinton
        self.tokenizer_trump = tokenizer_trump
        self.tokenizer_clinton = tokenizer_clinton

        lines = sequence_file_trump.split('\n')
        self.lines_trump = [word.lower() for word in lines]
        self.seq_length_trump = len(self.lines_trump[0].split()) - 1

        lines = sequence_file_clinton.split('\n')
        self.lines_clinton = [word.lower() for word in lines]
        self.seq_length_clinton = len(self.lines_clinton[0].split()) - 1

        self.root = None
        self.button_generate = None
        self.trump_seed = None
        self.clinton_seed = None
        self.trump_text = None
        self.clinton_text = None

    def build(self):
        self.root = tk.Tk()
        self.root.title('Custom Seed')

        tk.Label(self.root, font="Helvetica 30 bold", text='Seed for Trump:').grid(row=1, column=0)
        self.trump_seed = tk.Text(self.root, font="Helvetica 30 bold", width=43, height=10)
        self.trump_seed.configure(state='disabled')
        self.trump_seed.grid(row=2, column=0)

        tk.Label(self.root, font="Helvetica 30 bold", text='Seed for Clinton:').grid(row=1, column=1)
        self.clinton_seed = tk.Text(self.root, font="Helvetica 30 bold", width=43, height=10)
        self.clinton_seed.configure(state='disabled')
        self.clinton_seed.grid(row=2, column=1)

        self.button_generate = tk.Button(self.root, text='Get random seed', font='Helvetica 20 bold', bg='#ffb3fe',
                                         fg='black', command=self.get_seeds)
        self.button_generate.grid(row=3, column=0)

        self.button_generate = tk.Button(self.root, text='Generate Tweet', font='Helvetica 20 bold', bg='#ffb3fe',
                                         fg='black', command=self.generate_command)
        self.button_generate.grid(row=3, column=1)

        tk.Label(self.root, font="Helvetica 30 bold", text='Trump says:').grid(row=4, column=0)
        self.trump_text = tk.Text(self.root, font="Helvetica 30 bold", width=43, height=10)
        self.trump_text.configure(state='disabled')
        self.trump_text.grid(row=5, column=0)

        tk.Label(self.root, font="Helvetica 30 bold", text='Clinton says:').grid(row=4, column=1)
        self.clinton_text = tk.Text(self.root, font="Helvetica 30 bold", width=43, height=10)
        self.clinton_text.configure(state='disabled')
        self.clinton_text.grid(row=5, column=1)

    def show(self):
        self.root.mainloop()

    def get_seeds(self):
        self.trump_seed.configure(state='normal')
        self.clinton_seed.configure(state='normal')
        self.trump_seed.delete('1.0', 'end')
        self.clinton_seed.delete('1.0', 'end')
        seed = self.lines_trump[randint(0, len(self.lines_trump))]
        self.trump_seed.insert('end', seed[seed.rfind(';') + 2:])
        seed = self.lines_clinton[randint(0, len(self.lines_clinton))]
        self.clinton_seed.insert('end', seed[seed.rfind(';') + 2:])
        self.trump_seed.configure(state='disabled')
        self.clinton_seed.configure(state='disabled')

    def generate_command(self):
        generated_trump = Generator.generate_seq(self.model_trump, self.tokenizer_trump, self.seq_length_trump,
                                                 self.trump_seed.get('1.0', 'end-1c'), 10, 30)
        generated_clinton = Generator.generate_seq(self.model_clinton, self.tokenizer_clinton, self.seq_length_clinton,
                                                   self.clinton_seed.get('1.0', 'end-1c'), 10, 30)

        self.trump_text.configure(state='normal')
        self.trump_text.delete('1.0', 'end')
        self.trump_text.insert('end', Generator.postprocess(generated_trump))
        self.trump_text.configure(state='disabled')

        self.clinton_text.configure(state='normal')
        self.clinton_text.delete('1.0', 'end')
        self.clinton_text.insert('end', Generator.postprocess(generated_clinton))
        self.clinton_text.configure(state='disabled')
