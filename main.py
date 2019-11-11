import argparse

from trainer import Trainer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch_size', type=int, default=128)
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--steps_per_epoch', type=int, default=200)
    parser.add_argument('--val_steps', type=int, default=50)
    config = parser.parse_args()

    trainer = Trainer(config)

    trainer.train()


if __name__ == "__main__":
    main()
