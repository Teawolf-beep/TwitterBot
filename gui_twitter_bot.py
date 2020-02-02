import tkinter as tk

from trainer import Trainer
from generator import Generator
from gui_custom_seed import GuiCustomSeed
from gui_random_seed import GuiRandomSeed


class GuiTwitterBot:
    def __init__(self, root, tokenizer_trump, tokenizer_hillary, model_trump, model_hillary,
                 sequences_trump, sequences_clinton):
        self.custom_seed = GuiCustomSeed(tokenizer_trump, tokenizer_hillary, model_trump, model_hillary)
        self.random_seed = GuiRandomSeed(tokenizer_trump, tokenizer_hillary, model_trump, model_hillary,
                                         sequences_trump, sequences_clinton)

        self.root = root
        self.root.title('Tweet Generation')

        self.button_custom = tk.Button(self.root, text='Use custom seed', font='Helvetica 20 bold', bg='#ffb3fe',
                                       fg='black', command=self.call_custom_seed)
        self.button_custom.grid(row=0, column=0)

        self.button_random = tk.Button(self.root, text='Use random seed', font='Helvetica 20 bold', bg='#ffb3fe',
                                       fg='black', command=self.call_random_seed)
        self.button_random.grid(row=0, column=1)

    def call_custom_seed(self):
        self.root.destroy()
        self.custom_seed.build()
        self.custom_seed.show()

    def call_random_seed(self):
        self.root.destroy()
        self.random_seed.build()
        self.random_seed.show()


def main():
    model_trump_loaded = Generator.load_trained_model('model_trump_final.h5')
    tokenizer_trump_loaded = Generator.load_tokenizer('tok_trump_final.pkl')
    model_hillary_loaded = Generator.load_trained_model('model_clinton_final.h5')
    tokenizer_hillary_loaded = Generator.load_tokenizer('tok_clinton_final.pkl')
    sequences_trump_loaded = Trainer.load_file('sequenced_trump_data.txt')
    sequences_clinton_loaded = Trainer.load_file('sequenced_clinton_data.txt')
    master = tk.Tk()
    GuiTwitterBot(master, tokenizer_trump_loaded, tokenizer_hillary_loaded, model_trump_loaded, model_hillary_loaded,
                  sequences_trump_loaded, sequences_clinton_loaded)
    master.mainloop()


if __name__ == '__main__':
    main()

