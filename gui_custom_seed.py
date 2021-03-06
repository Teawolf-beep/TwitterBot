import tkinter as tk

from loader import Loader
from trainer import Trainer
from generator import Generator


class GuiCustomSeed:
    def __init__(self, tokenizer_trump, tokenizer_hillary, model_trump, model_hillary):
        self.model_trump = model_trump
        self.model_hillary = model_hillary
        self.tokenizer_trump = tokenizer_trump
        self.tokenizer_hillary = tokenizer_hillary
        self.root = None
        self.seed_text = None
        self.button_generate = None
        self.trump_text = None
        self.clinton_text = None

    def build(self):
        self.root = tk.Tk()
        self.root.title('Custom Seed')

        tk.Label(self.root, font="Helvetica 30 bold", text='Seed Text:').grid(row=0, columnspan=2)
        self.seed_text = tk.Text(self.root, font="Helvetica 30 bold", width=87, height=4)
        self.seed_text.bind('<KeyRelease>', self.seed_callback)
        self.seed_text.bind('<Return>', lambda e: "break")  # prevent newlines
        self.seed_text.tag_configure('green', foreground='green')
        self.seed_text.tag_configure('orange', foreground='orange', underline=1)
        self.seed_text.tag_configure('red', foreground='red', underline=1)
        self.seed_text.grid(row=1, column=0, columnspan=2)

        self.button_generate = tk.Button(self.root, text='Generate Tweet', font='Helvetica 20 bold', bg='#ffb3fe',
                                         fg='black', command=self.generate_command)
        self.button_generate.grid(row=2, column=0, columnspan=2)

        tk.Label(self.root, font="Helvetica 30 bold", text='Trump says:').grid(row=3, column=0)
        self.trump_text = tk.Text(self.root, font="Helvetica 30 bold", width=43, height=16)
        self.trump_text.configure(state='disabled')
        self.trump_text.grid(row=4, column=0)

        tk.Label(self.root, font="Helvetica 30 bold", text='Clinton says:').grid(row=3, column=1)
        self.clinton_text = tk.Text(self.root, font="Helvetica 30 bold", width=43, height=16)
        self.clinton_text.configure(state='disabled')
        self.clinton_text.grid(row=4, column=1)

    def show(self):
        self.root.mainloop()

    def generate_command(self):
        seed = self.seed_text.get('1.0', 'end-1c')
        # seq_length = len(seed.split())
        generated_trump = Generator.generate_seq(self.model_trump, self.tokenizer_trump, 50, seed, 10, 30)
        generated_hillary = Generator.generate_seq(self.model_hillary, self.tokenizer_hillary, 50, seed, 10, 30)
        self.trump_text.configure(state='normal')
        self.trump_text.delete('1.0', 'end')
        self.trump_text.insert('end', Generator.postprocess(generated_trump))
        self.trump_text.configure(state='disabled')

        self.clinton_text.configure(state='normal')
        self.clinton_text.delete('1.0', 'end')
        self.clinton_text.insert('end', Generator.postprocess(generated_hillary))
        self.clinton_text.configure(state='disabled')

    def seed_callback(self, *args):
        seed = self.seed_text.get('1.0', 'end-1c')
        last_word = seed.split()[-1]
        if last_word:
            found_trump = False
            found_hillary = False
            offset = '+%dc' % len(last_word)
            pos_start = "1.{}".format(seed.rfind(last_word))
            pos_end = pos_start + offset
            for word, index in self.tokenizer_trump.word_index.items():
                if word == last_word:
                    found_trump = True
                    break

            for word, index in self.tokenizer_hillary.word_index.items():
                if word == last_word:
                    found_hillary = True
                    break

            if found_trump and found_hillary:
                self.seed_text.tag_remove('orange', pos_start, pos_end)
                self.seed_text.tag_remove('red', pos_start, pos_end)
                self.seed_text.tag_add('green', pos_start, pos_end)
            elif not found_hillary and not found_trump:
                self.seed_text.tag_remove('orange', pos_start, pos_end)
                self.seed_text.tag_add('red', pos_start, pos_end)
            else:
                self.seed_text.tag_remove('red', pos_start, pos_end)
                self.seed_text.tag_add('orange', pos_start, pos_end)
