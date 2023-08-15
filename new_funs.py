def draw_fixation():
    pygame.draw.line(
        screen,
        BLACK,
        (SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2),
        (SCREEN_WIDTH / 2 + 10, SCREEN_HEIGHT / 2),
        5,
    )
    pygame.draw.line(
        screen,
        BLACK,
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10),
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10),
        5,
    )
    pygame.display.update()
    time.sleep(FIXATION_TIME)


def blank_screen():
    screen.fill(WHITE)
    pygame.display.update()
    time.sleep(BLANK_TIME)


def draw_images(left_img, right_img):
    screen.blit(
        left_img,
        (
            SCREEN_WIDTH / 4 - left_img.get_width() / 2,
            SCREEN_HEIGHT / 2 - left_img.get_height() / 2,
        ),
    )
    screen.blit(
        right_img,
        (
            3 * SCREEN_WIDTH / 4 - right_img.get_width() / 2,
            SCREEN_HEIGHT / 2 - right_img.get_height() / 2,
        ),
    )
    pygame.display.update()


def give_feedback(feedback_img):
    screen.blit(
        feedback_img,
        (
            SCREEN_WIDTH / 2 - feedback_img.get_width() / 2,
            SCREEN_HEIGHT / 2 - feedback_img.get_height() / 2,
        ),
    )
    pygame.display.update()
    time.sleep(1.0)


def save_data(
    epoch, trial, img_positions, key_pressed, feedback, reaction_time, optimal
):
    with open("output.txt", "a", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            [epoch, trial, img_positions, key_pressed, feedback, reaction_time, optimal]
        )


# -------------------------------------------------------------------

import pygame
import random
import time
import csv

# Step 1: Initialize Pygame
pygame.init()

# Step 2: Set Up Constants and Parameters
PROBABILITIES = [0.9, 0.1]
NUM_EPOCHS = 2
TRIALS_PER_EPOCH = 10
SLOT1_IMAGE_PATH = "pics/slot1_up.jpg"
SLOT2_IMAGE_PATH = "pics/slot2_up.jpg"
POS_FEEDBACK_PATH = "pics/euro.jpg"
NEG_FEEDBACK_PATH = "pics/noeuro.jpg"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
FIXATION_TIME = 0.2
BLANK_TIME = 0.3
FEEDBACK_TIME = 1.0  # Duration to show the feedback image

# Step 3: Load Images
slot1_img = pygame.image.load(SLOT1_IMAGE_PATH)
slot2_img = pygame.image.load(SLOT2_IMAGE_PATH)
pos_feedback_img = pygame.image.load(POS_FEEDBACK_PATH)
neg_feedback_img = pygame.image.load(NEG_FEEDBACK_PATH)

# Step 4: Setup Screen and Clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Probabilistic Reversal Learning Task")
clock = pygame.time.Clock()
screen.fill(BLACK)  # Set background to black


# Step 5: Create Functions for Different Parts of the Trial
def draw_fixation():
    pygame.draw.line(
        screen,
        BLACK,
        (SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2),
        (SCREEN_WIDTH / 2 + 10, SCREEN_HEIGHT / 2),
        5,
    )
    pygame.draw.line(
        screen,
        BLACK,
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 10),
        (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 10),
        5,
    )
    pygame.display.update()
    time.sleep(FIXATION_TIME)


def blank_screen(duration):
    screen.fill(BLACK)
    pygame.display.update()
    time.sleep(duration)


def draw_images(left_img, right_img):
    screen.blit(
        left_img,
        (
            SCREEN_WIDTH / 4 - left_img.get_width() / 2,
            SCREEN_HEIGHT / 2 - left_img.get_height() / 2,
        ),
    )
    screen.blit(
        right_img,
        (
            3 * SCREEN_WIDTH / 4 - right_img.get_width() / 2,
            SCREEN_HEIGHT / 2 - right_img.get_height() / 2,
        ),
    )
    pygame.display.update()


def give_feedback(feedback_img):
    blank_screen(BLANK_TIME)  # Clear the screen before showing the feedback
    screen.blit(
        feedback_img,
        (
            SCREEN_WIDTH / 2 - feedback_img.get_width() / 2,
            SCREEN_HEIGHT / 2 - feedback_img.get_height() / 2,
        ),
    )
    pygame.display.update()
    time.sleep(FEEDBACK_TIME)


def save_data(
    epoch, trial, img_positions, key_pressed, feedback, reaction_time, optimal
):
    with open("output.txt", "a", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(
            [epoch, trial, img_positions, key_pressed, feedback, reaction_time, optimal]
        )


# Step 6: Main Loop for the Experiment
for epoch in range(1, NUM_EPOCHS + 1):
    for trial in range(1, TRIALS_PER_EPOCH + 1):
        draw_fixation()
        blank_screen(BLANK_TIME)

        img_positions = "L1-R2" if random.choice([True, False]) else "L2-R1"
        left_img = slot1_img if img_positions == "L1-R2" else slot2_img
        right_img = slot2_img if img_positions == "L1-R2" else slot1_img

        draw_images(left_img, right_img)
        start_time = time.time()
        key_pressed = None

        while key_pressed not in ["a", "l", "esc"]:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        key_pressed = "a"
                    elif event.key == pygame.K_l:
                        key_pressed = "l"
                    elif event.key == pygame.K_ESCAPE:
                        key_pressed = "esc"
                        break

        reaction_time = time.time() - start_time

        if key_pressed == "esc":
            pygame.quit()
            quit()

        # Determine the outcome of this trial
        if epoch == 1:
            probs = PROBABILITIES
        else:
            probs = PROBABILITIES[::-1]

        if (key_pressed == "a" and img_positions == "L1-R2") or (
            key_pressed == "l" and img_positions == "L2-R1"
        ):
            feedback = "positive" if random.random() < probs[0] else "negative"
            optimal = "correct" if random.random() < probs[0] else "incorrect"
        else:
            feedback = "positive" if random.random() < probs[1] else "negative"
            optimal = "correct" if random.random() < probs[1] else "incorrect"

        feedback_img = pos_feedback_img if feedback == "positive" else neg_feedback_img
        give_feedback(feedback_img)
        save_data(
            epoch, trial, img_positions, key_pressed, feedback, reaction_time, optimal
        )

        # Show blank screen for a random duration between 0.2 and 1.2 seconds
        rand_interval = random.uniform(0.2, 1.2)
        blank_screen(rand_interval)

# Step 7: Quit Pygame
pygame.quit()
