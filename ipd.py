import random
import pandas as pd

class play_ipd:
    """
    Class to play Iterable Prisoner's Dilemma.
    """
    @classmethod
    def __init__(self, N, strategy, treatment):
        assert (treatment in ["faceless", "text_only", "text_and_audio"])
        self.N = N
        self.counter = 0
        self.strategy = strategy
        self.treatment = treatment
        self.user_running_total = 0
        self.comp_running_total = 0
        self.user_history = []
        self.comp_history = []
        self.comp_response_text = ""
        self.comp_response_audio_file = ""
        self.user_last_decision = ""

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

    def update_counter(self):
        self.counter += 1

    def get_computer_decision(self):
        """
        Get computer decision - dependent on strategy being played.
        """
        # First round strategy differs
        if self.counter == 1:
            if self.strategy == "TFT-C":
                self.comp_last_decision = "cooperate"
            elif self.strategy == "TFT-B":
                self.comp_last_decision = "betray"
        # After first round basic TFT is employed
        else:
            self.comp_last_decision = self.user_prev_decision

    @classmethod
    def request_user_decision(self):
        """
        Request the user for their next decision.
        - Only need this function for development purposes
        """
        # Prompt the user for input
        user_input = input("Cooperate or Betray your fellow prisoner? Enter a value: ")

        # Keep asking for input until the user provides a valid value
        while user_input not in ["cooperate", "betray"]:
            print("Invalid input, please try again.")
            user_input = input("Cooperate or Betray your fellow prisoner? Enter a value: ")

        # Store previous user decision, and add the user input to the last decision attribute
        self.user_prev_decision = self.user_last_decision
        self.user_last_decision = user_input

    def store_user_prev_decision(self):
        self.user_prev_decision = self.user_last_decision

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

    def update_comp_response(self):
        print(f"counter is: {self.counter}")
        user_history_abrv = list(map(lambda x: {"cooperate": "C", "betray": "B"}[x], self.user_history))
        comp_history_abrv = list(map(lambda x: {"cooperate": "C", "betray": "B"}[x], self.comp_history))
        print(f"user history was: {user_history_abrv}")
        print(f"comp history was: {comp_history_abrv}")

        # Create couple history
        coupled_history = []
        for user, comp in zip(user_history_abrv, comp_history_abrv):
            coupled_history.append(user + comp)
        coupled_recent_history = [coupled_history[-2], coupled_history[-1]] if self.counter >=2 else coupled_history
        print(f"coupled history was: {coupled_history}")
        print(f"coupled recent history was: {coupled_recent_history}")

        # Read in dialogue dictionary
        dialogue_dict = pd.read_csv("comp_dialogue/dialogue.csv").set_index('filename').to_dict()['text_response']

        # Cooperating
        if coupled_recent_history in [["CC"], ["CC","CC"], ["CB","CC"]]:
            # Randomly select response from first response list
            response_list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            selected = random.sample(response_list1, 1)[0]
            response_list1.remove(selected)
            # Update text/audio file path attributes
            self.comp_response_audio_file = "cooperating_" + str(selected) + ".mp3"
            self.comp_response_text = dialogue_dict["cooperating_" + str(selected) + ".mp3"]
        # Human betrayal
        elif coupled_recent_history in [["BC"], ["CC", "BC"], ["CB","BC"]]:
            # Randomly select response from first response list
            response_list2 = [1, 2, 3, 4, 5]
            selected = random.sample(response_list2, 1)[0]
            response_list2.remove(selected)
            # Update text/audio file path attributes
            self.comp_response_audio_file = "human_betrayal_" + str(selected) + ".mp3"
            self.comp_response_text = dialogue_dict["human_betrayal_" + str(selected) + ".mp3"]
        # Computer retaliation
        elif coupled_recent_history in [["CB"], ["BC", "CB"], ["BC", "BB"], ["BB", "CB"]]:
            # Randomly select response from first response list
            response_list3 = [1, 2, 3, 4, 5]
            selected = random.sample(response_list3, 1)[0]
            response_list3.remove(selected)
            # Update text/audio file path attributes
            self.comp_response_audio_file = "comp_retaliation_" + str(selected) + ".mp3"
            self.comp_response_text = dialogue_dict["comp_retaliation_" + str(selected) + ".mp3"]
        # Betrayal cycle
        elif coupled_recent_history in [["BB"], ["BB", "BB"]]:
            # Randomly select response from first response list
            response_list4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            selected = random.sample(response_list4, 1)[0]
            response_list4.remove(selected)
            # Update text/audio file path attributes
            self.comp_response_audio_file = "betrayal_" + str(selected) + ".mp3"
            self.comp_response_text = dialogue_dict["betrayal_" + str(selected) + ".mp3"]

        print(f"comp_response_audio_file: {self.comp_response_audio_file}")
        print(f"comp_response_text: {self.comp_response_text}")
        print("")
        print("")

    # def play_computer_response_audio(self):
    #     os.system(f"afplay {self.comp_response_audio_file}")
    #     self.comp_response_text = "I am sorry for betraying you..."

# Example game initialisation
import os
game_obj = play_ipd(N=3, strategy="TFT-C", treatment="text_only")
game_obj.set_payoffs(5,3,1,0)

# Play the round / starts when user chooses
game_obj.request_user_decision()
game_obj.update_counter()
game_obj.get_computer_decision()
game_obj.update_history()
game_obj.update_comp_response()

# Play the round / starts when user chooses
game_obj.request_user_decision()
game_obj.update_counter() # this informs comp decision so must happen first
game_obj.get_computer_decision()
game_obj.update_history()
game_obj.update_comp_response()




