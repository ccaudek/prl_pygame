import pygame
import random
import time
import csv
import os
from datetime import datetime
import sys


# Initialize Pygame
pygame.init()

# Get Computer Screen Size
screen_info = pygame.display.Info()
SCREEN_WIDTH = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h

# Set Up Constants and Parameters
PROBABILITIES = [0.8, 0.2]
NUM_EPOCHS = 2
TRIALS_PER_EPOCH = 10
SLOT1_IMAGE_PATH = "pics/slot1_up.jpg"
SLOT2_IMAGE_PATH = "pics/slot2_up.jpg"
POS_FEEDBACK_PATH = "pics/euro.jpg"
NEG_FEEDBACK_PATH = "pics/noeuro.jpg"
POS_SOUND_PATH = "sounds/beep-good.wav"
NEG_SOUND_PATH = "sounds/beep-bad.wav"
BLACK = (0, 0, 0)
FIXATION_TIME = 0.3
BLANK_TIME = 0.2
FEEDBACK_TIME = 1.0

# Load Images
slot1_img = pygame.image.load(SLOT1_IMAGE_PATH)
slot2_img = pygame.image.load(SLOT2_IMAGE_PATH)
pos_feedback_img = pygame.image.load(POS_FEEDBACK_PATH)
neg_feedback_img = pygame.image.load(NEG_FEEDBACK_PATH)

# Load Sounds
pos_feedback_sound = pygame.mixer.Sound(POS_SOUND_PATH)
neg_feedback_sound = pygame.mixer.Sound(NEG_SOUND_PATH)

# Setup Screen and Clock
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Probabilistic Reversal Learning Task")
clock = pygame.time.Clock()

# Hide the Mouse Cursor
pygame.mouse.set_visible(False)


# Create Functions for Different Parts of the Trial
def draw_fixation():
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (SCREEN_WIDTH / 2 - 10, SCREEN_HEIGHT / 2),
        (SCREEN_WIDTH / 2 + 10, SCREEN_HEIGHT / 2),
        5,
    )
    pygame.draw.line(
        screen,
        (255, 255, 255),
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


def give_feedback(feedback_img, feedback_sound):
    screen.fill(BLACK)  # Clear the screen before showing the feedback
    feedback_sound.play()
    screen.blit(
        feedback_img,
        (
            SCREEN_WIDTH / 2 - feedback_img.get_width() / 2,
            SCREEN_HEIGHT / 2 - feedback_img.get_height() / 2,
        ),
    )
    pygame.display.update()
    time.sleep(FEEDBACK_TIME)


def get_filename(subject_code):
    """
    Generate a unique filename based on the subject code.
    It appends a number to the end of the filename if a file with that name already exists.
    """
    index = 1
    filename = f"{subject_code}.txt"

    while os.path.exists(filename):
        filename = f"{subject_code}_{index}.txt"
        index += 1

    return filename


def save_data(
    filename, epoch, trial, img_positions, key_pressed, feedback, reaction_time, optimal
):
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow(
            [
                current_time,
                epoch,
                trial,
                img_positions,
                key_pressed,
                feedback,
                reaction_time,
                optimal,
            ]
        )


def get_subject_code():
    """
    Get the subject code from the command line argument
    """
    if len(sys.argv) < 2:
        print("\nUsage: python prl_3.py <subject_code>")
        sys.exit(1)
    return sys.argv[1]


def show_instructions():
    instructions = """
    In questo compito, vedrai due immagini sullo schermo.
    Dovrai scegliere una delle due immagini premendo un tasto.
    Dopo la tua scelta, riceverai un feedback positivo o negativo.
    Il tuo obiettivo è imparare quale delle due immagini ha più
    probabilità di darti un feedback positivo.
    Attenzione: le probabilità possono cambiare durante l'esperimento.
    Premi 'a' per scegliere l'immagine a sinistra e
    'l' per scegliere quella a destra.
    Premi un tasto per iniziare.
    """
    instructions = instructions.strip().split("\n")

    font = pygame.font.Font(None, 36)
    line_spacing = 10
    start_y = (
        SCREEN_HEIGHT
        - (
            len(instructions) * font.get_height()
            + (len(instructions) - 1) * line_spacing
        )
    ) // 2

    for i, line in enumerate(instructions):
        text = font.render(line, True, (255, 255, 255))
        y_position = start_y + i * (font.get_height() + line_spacing)
        screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, y_position))

    pygame.display.update()

    # Wait for a key press to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False


def show_thank_you_message(correct_feedback_count, total_trials):
    message = f"""
    Grazie per la tua partecipazione!
    Hai ottenuto {correct_feedback_count} feedback corretti su un totale di {total_trials} tentativi.
    """
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text, text_rect)
    pygame.display.update()
    time.sleep(5)  # Show the message for 5 seconds


# Ask the subject for their code at the beginning of the experiment
subject_code = get_subject_code()
filename = get_filename(subject_code)

correct_feedback_count = 0
total_trials = 0

# Main Loop for the Experiment
if __name__ == "__main__":
    show_instructions()

    for epoch in range(1, NUM_EPOCHS + 1):
        for trial in range(1, TRIALS_PER_EPOCH + 1):
            total_trials += 1
            # Present a fixation cross
            draw_fixation()
            blank_screen(BLANK_TIME)

            # Randomly set image positions for this trial
            img_positions = "L1-R2" if random.choice([True, False]) else "L2-R1"
            left_img = slot1_img if img_positions == "L1-R2" else slot2_img
            right_img = slot2_img if img_positions == "L1-R2" else slot1_img

            # Draw images and wait for a key press
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

            # Calculate reaction time
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
                optimal = "incorrect" if random.random() < probs[1] else "correct"

            # Provide visual and acoustic feedback
            feedback_img = (
                pos_feedback_img if feedback == "positive" else neg_feedback_img
            )
            feedback_sound = (
                pos_feedback_sound if feedback == "positive" else neg_feedback_sound
            )

            give_feedback(feedback_img, feedback_sound)

            if optimal == "correct":
                correct_feedback_count += 1

            # Save the trial data
            save_data(
                filename,
                epoch,
                trial,
                img_positions,
                key_pressed,
                feedback,
                reaction_time,
                optimal,
            )

            # Show blank screen for a random duration between 0.2 and 1.2 seconds
            rand_interval = random.uniform(0.2, 1.2)
            blank_screen(rand_interval)

    show_thank_you_message(correct_feedback_count, total_trials)

    # Quit Pygame
    pygame.quit()
