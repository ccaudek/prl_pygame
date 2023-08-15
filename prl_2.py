import pygame
import random
import time
import csv
from funs import *


def main():
    pygame.init()

    # Define parameters
    (
        wdw,
        wdh,
        fx,
        grey,
        left_key,
        right_key,
        abort_key,
        trials_per_epoch,
        total_epochs,
    ) = define_parameters()

    screen = pygame.display.set_mode((wdw, wdh))

    reward_probs = [0.8, 0.2]  # Define your reward probabilities here
    experiment_design = generate_experiment_design(
        trials_per_epoch, total_epochs, reward_probs
    )

    with open("experiment_design.csv", "w", newline="") as csvfile:
        fieldnames = [
            "epoch",
            "trial",
            "img1_position",
            "img2_position",
            "correct_choice",
            "feedback",
            "outcome_path",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(experiment_design)

    trial_data = []

    with open("experiment_design.csv", "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        for row in reader:
            epoch = int(row["epoch"])
            trial = int(row["trial"])
            # Convert img1_position and img2_position to positions
            img1_position = (
                (wdw // 4, wdh // 2)
                if row["img1_position"] == "left"
                else (wdw // 2, wdh // 2)
            )
            img2_position = (
                (wdw // 2, wdh // 2)
                if row["img2_position"] == "left"
                else (wdw // 4, wdh // 2)
            )

            correct_choice = row["correct_choice"] == "True"
            feedback = row["feedback"]
            outcome_path = row["outcome_path"]

            reward_prob = 1 if epoch % 2 == 0 else 0.0

            trial_result = execute_trial(
                screen,
                wdw,
                wdh,
                left_key,
                right_key,
                abort_key,
                img1_position,
                img2_position,
                outcome_path,
                correct_choice,
                feedback,
                reward_prob,
            )

            choice = trial_result["choice"]
            reaction_time = trial_result["reaction_time"]

            trial_data.append(
                {
                    "epoch": epoch,
                    "trial": trial,
                    "img1_position": img1_position,
                    "img2_position": img2_position,
                    "choice": choice,
                    "correct_choice": correct_choice,
                    "outcome": outcome_path,
                    "reaction_time": reaction_time,
                }
            )

    with open("trial_data.txt", "w") as file:
        for data in trial_data:
            file.write(
                f"Epoch: {data['epoch']}, Trial: {data['trial']}, "
                f"Image1_Position: {data['img1_position']}, "
                f"Image2_Position: {data['img2_position']}, "
                f"Choice: {data['choice']}, Correct_Choice: {data['correct_choice']}, "
                f"Outcome: {data['outcome']}, Reaction_Time (ms): {data['reaction_time']}\n"
            )

    pygame.quit()


if __name__ == "__main__":
    main()
