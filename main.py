from time import sleep

from pynput.keyboard import Key, Controller as KeyboardController

from mimicpy.actors import Trainer, Actor


def main():
    trainer = Trainer()
    trainer.learn()
    saved_path = trainer.save_scenario()
    sleep(3)
    actor = Actor()
    actor.play_scenario(saved_path)

if __name__ == "__main__":
    main()
