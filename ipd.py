class play_ipd:
    """
    Class to play Iterable Prisoner's Dilemma.
    """
    @classmethod
    def __init__(self, N, strategy):
        self.N = N
        self.counter = 0
        self.strategy = strategy
        self.user_running_total = 0
        self.comp_running_total = 0
        self.user_history = []
        self.comp_history = []
        self.comp_response = ""

    @classmethod
    def set_payoffs(self, T, R, P, S):
        """
        Set payoffs for the game.

        T=Temptation, R=Reward, P=Punishment, S=Sucker
        """
        assert (T > R > P > S)
        self.T = T
        self.R = R
        self.P = P
        self.S = S

    def get_computer_decision(self):
        """
        Get computer decision, dependent on their strategy.
        """
        if self.strategy == "UB":
            self.comp_last_decision = "betray"

    @classmethod
    def request_user_decision(self):
        """
        Request the user for their next decision.
        """
        # Prompt the user for input
        user_input = input("Cooperate (C) or Betray (B) your fellow prisoner? Enter a value: ")

        # Keep asking for input until the user provides a valid value
        while user_input not in ["C", "B"]:
            print("Invalid input, please try again.")
            user_input = input("Cooperate (C) or Betray (B) your fellow prisoner? Enter a value: ")

        # Add the user input to the last decision attribute
        self.user_last_decision = user_input

    def update_running_totals(self):
        """
        Update running totals for both the user and the computer.
        """
        if self.user_last_decision == "cooperate" and self.comp_last_decision == "cooperate":
            self.user_running_total += self.R
            self.comp_running_total += self.R
        elif self.user_last_decision == "cooperate" and self.comp_last_decision == "betray":
            self.user_running_total += self.S
            self.comp_running_total += self.T
        elif self.user_last_decision == "betray" and self.comp_last_decision == "cooperate":
            self.user_running_total += self.T
            self.comp_running_total += self.S
        elif self.user_last_decision == "betray" and self.comp_last_decision == "betray":
            self.user_running_total += self.P
            self.comp_running_total += self.P

    def update_history(self):
        """
        Update history of choices made by the user and computer.
        """
        self.user_history.append(self.user_last_decision)
        self.comp_history.append(self.comp_last_decision)

    def computer_response(self):
        os.system("afplay " + "ResponseExample1.mp3")
        self.comp_response = "I am sorry for betraying you..."

# Example game initialisation
import os
game_obj = play_ipd(N=3, strategy="UB")
game_obj.set_payoffs(5,3,1,0)
game_obj.get_computer_decision()
game_obj.computer_response()