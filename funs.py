# Replace 'revl_funs' with the actual module name where 'draw_fixation' is defined
import pygame
import random
import time


def draw_fixation(screen, wdw, wdh):
    # Set line properties
    fx = 10  # Set your desired value
    grey = (128, 128, 128)  # Grey color in RGB

    # Clear the screen with a background color (optional)
    screen.fill((0, 0, 0))  # Fill with black color

    # Draw lines
    pygame.draw.line(screen, grey, (wdw / 2, wdh / 2 - fx), (wdw / 2, wdh / 2 + fx), 2)
    pygame.draw.line(screen, grey, (wdw / 2 - fx, wdh / 2), (wdw / 2 + fx, wdh / 2), 2)

    # Update the display
    pygame.display.flip()


def generate_experiment_design(trials_per_epoch, total_epochs, reward_probs):
    experiment_design = []

    for epoch in range(total_epochs):
        if epoch % 2 == 0:
            reward_prob = reward_probs[0]  # Use the first reward probability
            correct_choice = "left"
        else:
            reward_prob = reward_probs[1]  # Use the second reward probability
            correct_choice = "right"

        for trial in range(trials_per_epoch):
            img_positions = ["left", "right"]
            random.shuffle(img_positions)  

            img1_position, img2_position = img_positions

            if random.random() < reward_prob:
                feedback = "positive"
            else:
                feedback = "negative"

            if feedback == "positive":
                outcome_path = "pics/euro.jpg"
            else:
                outcome_path = "pics/noeuro1.jpg"

            experiment_design.append(
                {
                    "epoch": epoch + 1,
                    "trial": trial + 1,
                    "img1_position": img1_position,
                    "img2_position": img2_position,
                    "correct_choice": correct_choice == img1_position,
                    "feedback": feedback,
                    "outcome_path": outcome_path,
                }
            )

    return experiment_design


def display_images(
    screen, wdw, wdh, img1_path, img2_path, img1_position, img2_position
):
    screen.blit(pygame.image.load(img1_path), img1_position)
    screen.blit(pygame.image.load(img2_path), img2_position)
    pygame.display.flip()


def play_beep_sound(feedback, reward_prob):
    pygame.mixer.init()
    if feedback == "positive":
        if random.random() < reward_prob:
            beep_sound = pygame.mixer.Sound("sounds/beep-good.wav")
        else:
            beep_sound = pygame.mixer.Sound("sounds/beep-bad.wav")
    else:
        beep_sound = pygame.mixer.Sound(
            "sounds/beep-bad.wav"
        )  # Always play "beep-bad.wav" for negative feedback
    beep_sound.play()
    time.sleep(0.2)  # Adjust as needed


def execute_trial(
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
):
    draw_fixation(screen, wdw, wdh)
    pygame.display.flip()
    pygame.time.wait(200)  # Display fixation for 0.2 seconds

    screen.fill((0, 0, 0))  # Blank screen
    pygame.display.flip()
    pygame.time.wait(200)  # Blank screen for 0.2 seconds

    # Load the images for display
    img1 = pygame.image.load("pics/slot1_up.jpg")
    img2 = pygame.image.load("pics/slot2_up.jpg")

    # Calculate image positions based on your layout requirements
    img1_x, img1_y = img1_position
    img2_x, img2_y = img2_position

    # Display the images
    screen.blit(img1, (img1_x, img1_y))
    screen.blit(img2, (img2_x, img2_y))
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

    # Determine if the choice is correct
    if correct_choice:
        correct = (choice == "a" and img1_position == (wdw // 4, wdh // 2)) or (
            choice == "l" and img1_position == (wdw // 2, wdh // 2)
        )
    else:
        correct = (choice == "a" and img1_position == (wdw // 2, wdh // 2)) or (
            choice == "l" and img1_position == (wdw // 4, wdh // 2)
        )

    # Choose the outcome image based on feedback
    if feedback == "positive":
        outcome_image_path = "pics/euro.jpg"
    else:
        outcome_image_path = "pics/noeuro1.jpg"

    # Choose the outcome image based on feedback and reward_prob
    display_outcome(screen, wdw, wdh, feedback, reward_prob)
    play_beep_sound(feedback, reward_prob)

    return {"choice": choice, "correct": correct, "reaction_time": reaction_time}


def define_parameters():
    # Set screen dimensions (width and height)
    wdw = 800  # Set your desired value
    wdh = 600  # Set your desired value

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

    return (
        wdw,
        wdh,
        fx,
        grey,
        left_key,
        right_key,
        abort_key,
        trials_per_epoch,
        total_epochs,
    )


def display_outcome(screen, wdw, wdh, feedback, reward_prob):
    if feedback == "positive":
        if random.random() < reward_prob:
            outcome_image_path = "pics/euro.jpg"
        else:
            outcome_image_path = "pics/noeuro1.jpg"
    else:
        outcome_image_path = (
            "pics/noeuro1.jpg"  # Always show "noeuro1.jpg" for negative feedback
        )

    outcome_image = pygame.image.load(outcome_image_path)
    screen.fill((0, 0, 0))
    screen.blit(
        outcome_image,
        (
            wdw // 2 - outcome_image.get_width() // 2,
            wdh // 2 - outcome_image.get_height() // 2,
        ),
    )
    pygame.display.flip()
    pygame.time.wait(1000)  # Display outcome for 1 second
