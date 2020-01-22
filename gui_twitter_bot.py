import tkinter as tk

from loader import Loader
from trainer import Trainer
from generator import Generator


class GeneratorGUI:
    def __init__(self, root, tokenizer, model):
        self.model = model
        self.tokenizer = tokenizer

        self.root = root
        self.root.title('Tweet Generation')

        tk.Label(self.root, font="Helvetica 30 bold", text='Seed\nText:').grid(row=0)
        self.seed_text = tk.Text(self.root, font="Helvetica 30 bold", width=75, height=4)
        self.seed_text.bind('<KeyRelease>', self.seed_callback)
        self.seed_text.bind('<Return>', lambda e: "break")  # prevent newlines
        self.seed_text.tag_configure('green', foreground='green')
        self.seed_text.tag_configure('red', foreground='red', underline=1)
        self.seed_text.grid(row=0, column=1)

        self.button_generate = tk.Button(self.root, text='Generate Tweet', command=self.generate_command)
        self.button_generate.grid(row=2, column=1)

        tk.Label(self.root, font="Helvetica 30 bold", text='Generated\nText:').grid(row=4)
        self.generated_text = tk.Text(self.root, font="Helvetica 30 bold", width=75, height=8)
        self.generated_text.configure(state='disabled')
        self.generated_text.grid(row=4, column=1)

        self.root.mainloop()

    def generate_command(self):
        seed = self.seed_text.get('1.0', 'end-1c')
        # seq_length = len(seed.split())
        generated = Generator.generate_seq(self.model, self.tokenizer, 50, seed, 10)
        self.generated_text.configure(state='normal')
        self.generated_text.delete('1.0', 'end')
        self.generated_text.insert('end', Generator.postprocess(generated))
        self.generated_text.configure(state='disabled')

    def seed_callback(self, *args):
        seed = self.seed_text.get('1.0', 'end-1c')
        if seed:
            last_word = seed.split()[-1]
            if last_word:
                found = False
                offset = '+%dc' % len(last_word)
                pos_start = self.seed_text.search(last_word, '1.0', 'end')
                pos_end = pos_start + offset
                for word, index in self.tokenizer.word_index.items():
                    if word == last_word:
                        found = True
                        break

                if found:
                    self.seed_text.tag_remove('red', pos_start, pos_end)
                    self.seed_text.tag_add('green', pos_start, pos_end)
                else:
                    self.seed_text.tag_add('red', pos_start, pos_end)


if __name__ == '__main__':
    model_5000 = Generator.load_trained_model('trump_22_01_20.h5')
    tokenizer_5000 = Generator.load_tokenizer('tokenizer_trump_22_01_20.pkl')
    master = tk.Tk()
    GeneratorGUI(master, tokenizer_5000, model_5000)

