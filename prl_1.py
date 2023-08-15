import pygame
import time
import random

# Replace 'revl_funs' with the actual module name where 'draw_fixation' is defined
from revl_funs import draw_fixation


def main():
    # Initialize pygame
    pygame.init()

    # Set screen dimensions (width and height)
    wdw = 800  # Set your desired value
    wdh = 600  # Set your desired value

    # Create the screen
    screen = pygame.display.set_mode((wdw, wdh))

    # Set line properties
    fx = 10  # Set your desired value
    grey = (128, 128, 128)  # Grey color in RGB

    # Define key constants
    left_key = pygame.K_a
    right_key = pygame.K_l
    abort_key = pygame.K_ESCAPE

    # Number of trials per epoch
    trials_per_epoch = 5
    total_epochs = 2
    total_trials = trials_per_epoch * total_epochs

    # Initialize a list to store trial data
    trial_data = []

    for epoch in range(total_epochs):
        # Determine reward and punishment probabilities based on epoch
        if epoch % 2 == 0:
            reward_prob = 0.9
        else:
            reward_prob = 0.1

        for trial in range(trials_per_epoch):
            # Randomly determine the position of the images
            if random.choice([True, False]):
                img1_path = "pics/slot1_up.jpg"
                img2_path = "pics/slot2_up.jpg"
                img1_position = "left"
                img2_position = "right"
            else:
                img1_path = "pics/slot2_up.jpg"
                img2_path = "pics/slot1_up.jpg"
                img1_position = "right"
                img2_position = "left"

            # Display the fixation cross
            draw_fixation(screen, wdw, wdh)
            pygame.display.flip()
            time.sleep(1)

            # Display the images without the fixation cross
            img1 = pygame.image.load(img1_path)
            img2 = pygame.image.load(img2_path)
            screen.blit(img1, (wdw // 4, wdh // 2))
            screen.blit(img2, (wdw // 2, wdh // 2))
            pygame.display.flip()

            # Record the start time
            start_time = pygame.time.get_ticks()

            # Wait for a keypress (a, l, or abort)
            choice = None
            while choice is None:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == left_key:
                            choice = "a"
                        elif event.key == right_key:
                            choice = "l"
                        elif event.key == abort_key:
                            print("You have aborted the game")
                            pygame.quit()
                            return

            # Record the end time
            end_time = pygame.time.get_ticks()

            # Calculate reaction time
            reaction_time = end_time - start_time

            # Determine reward or punishment based on probability
            correct_choice = (img1_position == "left" and choice == "a") or (
                img1_position == "right" and choice == "l"
            )
            if (correct_choice and random.random() < reward_prob) or (
                not correct_choice and random.random() < (1 - reward_prob)
            ):
                outcome_path = "pics/euro.jpg"
            else:
                outcome_path = "pics/noeuro1.jpg"

            # Show the outcome image
            outcome_image = pygame.image.load(outcome_path)
            screen.fill((0, 0, 0))
            screen.blit(
                outcome_image,
                (
                    wdw // 2 - outcome_image.get_width() // 2,
                    wdh // 2 - outcome_image.get_height() // 2,
                ),
            )
            pygame.display.flip()

            # Play a beep sound
            pygame.mixer.init()
            if correct_choice:
                beep_sound = pygame.mixer.Sound("sounds/beep-good.wav")
            else:
                beep_sound = pygame.mixer.Sound("sounds/beep-bad.wav")
            beep_sound.play()
            time.sleep(0.2)  # Adjust as needed

            # Save trial data
            trial_data.append(
                {
                    "epoch": epoch + 1,
                    "trial": trial + 1,
                    "img1_position": img1_position,
                    "img2_position": img2_position,
                    "choice": choice,
                    "correct_choice": correct_choice,
                    "outcome": outcome_path,
                    "reaction_time": reaction_time,
                }
            )

    # Save trial data to the output file
    with open("trial_data.txt", "w") as file:
        for data in trial_data:
            file.write(
                f"Epoch: {data['epoch']}, Trial: {data['trial']}, "
                f"Image1_Position: {data['img1_position']}, "
                f"Image2_Position: {data['img2_position']}, "
                f"Choice: {data['choice']}, Correct_Choice: {data['correct_choice']}, "
                f"Outcome: {data['outcome']}, Reaction_Time (ms): {data['reaction_time']}\n"
            )

    # Quit pygame
    pygame.quit()


if __name__ == "__main__":
    main()
