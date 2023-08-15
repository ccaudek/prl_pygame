"""
Call the main function:
revl_run(23, 6, 1, "mario_rossi_1993_03_23", 1)

img_pair = a number from 1 to 9 that identifies the pair of psychopathy
and neutral images defined in the script selectImgPair.m
Numbers from 1 to 3 are for dishinibition
Numbers from 4 to 6 are for boldness
Numbers from 7 to 12 are for meanness

Each subject must complete 9 blocks of trials. In each block, the value 
img_pair will be different, with possible values going from 1 to 9, each
value used once only for each subject. The sequence of the img_pair
numbers will be randomly determined for each subject. For example, for
one suject we have the sequence 274951386; for another subject the
sequence 814273956, and so on.

is_psychopathy_reward_first = if 1, yes; 0 = no. 
If 1, the first epoch will reward the image related to psychopathy;
otherwise, the first epoch rewards the neutral image.

subject_name = subject identification code; MUST be between quotes!

block_of_trials = integer starting from 1 and increasing for each
subcessive block of trials

When running different subjects, half will start with 
is_psychopathy_reward_first = 1 and half will start with 
is_psychopathy_reward_first = 0

When running the same subject, half of the blocks will start with 
is_psychopathy_reward_first = 1 and half will start with 
is_psychopathy_reward_first = 0. However, the sequence of 1s and 0s will
not always be the same. For example, for one subject, it will be
001101011, for another subject 001110101.

This is the main code that runs the reversal task described below and
will plot and save data to the 'data' subfolder. 

TASK DESCRIPTION:
2 images are presented on every trial, each associated with either a 0.7 
or a 0.3 probability of reward. 
At various points during the task the identity of the high and low reward
image are reversed. Subjects have to continuously keep track which
image is currently best. 

In each block there are 4 epochs, with 40 trials each.

The experiment parameters are set in the revlParams.m file. 

"""

import pygame
import random
import os
import pygame

from revl_funs import select_img_pair

# Initialize pygame
pygame.init()


def revl_run(sID, img_pair, is_psychopathy_reward_first, subject_name, block_of_trials):
    # Set up Pygame
    pygame.init()

    # Define constants and parameters
    nt = 40  # Number of trials per block
    img = None  # Define how 'img' is obtained
    wdw = 800  # Window width
    wdh = 600  # Window height
    dataFile = f"data_{subject_name}_{block_of_trials}.json"
    # Define more constants and parameters based on your script

    # Create the display
    wd = pygame.display.set_mode((wdw, wdh))

    # Check for OpenGL compatibility and skip sync tests
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 0)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 0)
    pygame.display.set_caption("Reversal Task")

    # Check if all needed parameters are given
    if any(
        param is None
        for param in (
            sID,
            img_pair,
            is_psychopathy_reward_first,
            subject_name,
            block_of_trials,
        )
    ):
        print(
            "Must provide required input parameters: sID, img_pair, is_psychopathy_reward_first, subject_name, and block_of_trials!"
        )
        pygame.quit()
        return

    # Initialize the random number generator
    random.seed()

    # Select the pair of images and initialize other parameters
    blue_img, orange_img = select_img_pair(img_pair)
    img = [blue_img, orange_img]  # Assuming img is a list containing image data

    # Debug mode
    debug = False  # Set to True for debug mode

    # Initialize other variables and objects
    # Define more variables and objects based on your script

    # Create the screen
    screen_dimensions = (wdw, wdh)
    screen = pygame.display.set_mode(screen_dimensions)

    try:
        # Present instructions and wait for key press
        revl_instr(wd)
        pygame.time.wait(1000)  # Wait for 1 second

        if not debug:
            pygame.time.wait(2000)  # Wait for 2 seconds

        # Loop over all trials
        for t in range(1, nt + 1):
            # Draw stimuli
            wd = revl_draw_stim(wd, prep, 0, None, t, img)
            pygame.display.flip()

            # Get choice and check for abort
            choice = None
            while choice is None:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == prep.left:
                            choice = 0  # Choose left image
                        elif event.key == prep.right:
                            choice = 1  # Choose right image
                        elif event.key == prep.abort:
                            print("You have aborted the game")
                            pygame.quit()
                            return

            # Check for valid response, determine feedback, and present choice
            outcome = None
            # Define more processing based on your script

            # Present outcome and wait for next trial
            revl_draw_stim(wd, prep, 2, data, t, img)
            pygame.time.wait(
                int(
                    (
                        tm.outcome[t]
                        + prep.time.iti
                        - prep.time.black
                        - pygame.time.get_ticks()
                    )
                    * 1000
                )
            )
            pygame.draw.rect(wd, prep.draw.black, (0, 0, wdw, wdh))
            pygame.display.flip()
            pygame.time.wait(
                int((tm.outcome[t] + prep.time.iti - pygame.time.get_ticks()) * 1000)
            )

        # Save and wrap things up
        pygame.draw.rect(wd, prep.draw.black, (0, 0, wdw, wdh))
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.quit()

        # Save data
        data = {
            "today": None,
            "tm": None,
            "prep": None,
            "img_pair": img_pair,
            "is_psychopathy_reward_first": is_psychopathy_reward_first,
            "subject_name": subject_name,
            "block_of_trials": block_of_trials,
            "RT": None,
            "totalReward": None,
        }
        # Populate 'data' dictionary with relevant data

        # Save data to JSON file
        if os.path.exists(dataFile):
            rand_attach = str(random.randint(0, 9999)).zfill(4)
            dataFile = f"{dataFile[:-5]}_{rand_attach}.json"

        # Uncomment the following lines to save the 'data' dictionary to a JSON file
        with open(dataFile, "w") as json_file:
            json.dump(data, json_file)

        # Print feedback and thank subjects
        print(f'Congratulations, you won {data["totalReward"]} Euro!')
        print("Thank you for participating")

    except Exception as e:
        print(f"An error occurred: {e}")
        pygame.quit()


# Define functions 'select_img_pair', 'revl_instr', 'revl_draw_stim', etc. based on your script
