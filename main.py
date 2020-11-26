from AIPlayer import *
from Player import *
from simple_term_menu import TerminalMenu

terminal_menu = TerminalMenu(["Play as a Human", "Play with a Model", "Train a Model (Makes changes to config.py first!)"])

if __name__ == "__main__":
  choice_index = terminal_menu.show()
  if choice_index == 0:
    playAsHuman()
  elif choice_index == 1:
    playAsAI()
  else:
    trainAI()
