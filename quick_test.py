import pygame
import time

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

    # Define key constants
    left_key = pygame.K_a
    right_key = pygame.K_l
    abort_key = pygame.K_ESCAPE

    # Number of trials
    num_trials = 10

    # Initialize a list to store choices for each trial
    choices = []

    for trial in range(num_trials):
        # Call the function to draw fixation
        draw_fixation(screen, wdw, wdh)

        pygame.display.flip()

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

        # Beep for 'a' or 'l' keypress
        if choice in ["a", "l"]:
            pygame.mixer.init()
            pygame.mixer.music.load("beep.wav")  # Replace with your beep sound file
            pygame.mixer.music.play()
            time.sleep(0.5)  # Adjust as needed

        # Clear the screen with a background color
        screen.fill((0, 0, 0))  # Fill with black color
        pygame.display.flip()

        # Save choice data to the output file
        choices.append(choice)
        with open("output_file.txt", "a") as file:
            file.write(f"Trial {trial + 1}: Choice: {choice}\n")

        # Wait for 1 second
        time.sleep(1)

    # Quit pygame
    pygame.quit()


if __name__ == "__main__":
    main()
