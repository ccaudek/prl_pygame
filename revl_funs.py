import pygame


def select_img_pair(img_pair, is_psychopathy_reward_first):
    if is_psychopathy_reward_first == 1:
        if img_pair == 1:
            blue_img = "im_disinhibition_1.jpg"
            orange_img = "im_neutral_1.jpg"
        elif img_pair == 2:
            blue_img = "im_disinhibition_2.jpg"
            orange_img = "im_neutral_2.jpg"
        elif img_pair == 3:
            blue_img = "im_disinhibition_3.jpg"
            orange_img = "im_neutral_3.jpg"
        elif img_pair == 4:
            blue_img = "im_boldness_1.jpg"
            orange_img = "im_neutral_4.jpg"
        elif img_pair == 5:
            blue_img = "im_boldness_2.jpg"
            orange_img = "im_neutral_5.jpg"
        elif img_pair == 6:
            blue_img = "im_boldness_3.jpg"
            orange_img = "im_neutral_6.jpg"
        elif img_pair == 7:
            blue_img = "im_meanness_1.jpg"
            orange_img = "im_neutral_7.jpg"
        elif img_pair == 8:
            blue_img = "im_meanness_2.jpg"
            orange_img = "im_neutral_8.jpg"
        elif img_pair == 9:
            blue_img = "im_meanness_3.jpg"
            orange_img = "im_neutral_9.jpg"
        else:
            print("*** Input for img_pair must be an integer between 1 and 9 ***")
            return

    elif is_psychopathy_reward_first == 0:
        if img_pair == 1:
            blue_img = "im_neutral_1.jpg"
            orange_img = "im_disinhibition_1.jpg"
        elif img_pair == 2:
            blue_img = "im_neutral_2.jpg"
            orange_img = "im_disinhibition_2.jpg"
        elif img_pair == 3:
            blue_img = "im_neutral_3.jpg"
            orange_img = "im_disinhibition_3.jpg"
        elif img_pair == 4:
            blue_img = "im_neutral_4.jpg"
            orange_img = "im_boldness_1.jpg"
        elif img_pair == 5:
            blue_img = "im_neutral_5.jpg"
            orange_img = "im_boldness_2.jpg"
        elif img_pair == 6:
            blue_img = "im_neutral_6.jpg"
            orange_img = "im_boldness_3.jpg"
        elif img_pair == 7:
            blue_img = "im_neutral_7.jpg"
            orange_img = "im_meanness_1.jpg"
        elif img_pair == 8:
            blue_img = "im_neutral_8.jpg"
            orange_img = "im_meanness_2.jpg"
        elif img_pair == 9:
            blue_img = "im_neutral_9.jpg"
            orange_img = "im_meanness_3.jpg"
        else:
            print("*** Input for img_pair must be an integer between 1 and 9 ***")
            return

    else:
        print(
            "*** Input for is_psychopathy_reward_first must be either 0 (no) or 1 (yes) ***"
        )
        return

    return blue_img, orange_img


# Assuming you have a pygame screen initialized as 'screen'
def draw_stimulus(wd, prep, cond, data, t, img):
    # draw fixation cross
    draw_fixation(wd)

    # draw stimuli at specified locations
    for iCue in range(prep.nStim):
        location = prep.locs[t, iCue]
        screen.blit(img.stim[iCue], prep.draw.rect.stim[location])

    # draw choice
    if cond > 0:
        choiceLoc = prep.locs[t, data.choice[t]]
        screen.blit(img.select[data.choice[t]], prep.draw.rect.stim[choiceLoc])
        screen.blit(img.select[data.choice[t]], prep.draw.rect.stim[1])
        screen.blit(img.select[data.choice[t]], prep.draw.rect.stim[2])
        # You might need to adjust the blit positions and sizes

    # draw feedback: for 0, get punish feedback, for 1, get reward feedback
    if cond > 1:
        fbimg = img.feedback[data.outcome[t] + 1]
        screen.blit(fbimg, prep.draw.rect.stim[5])
        # You might need to adjust the blit positions and sizes


# Call the function with the necessary arguments
# draw_stimulus(wd, prep, cond, data, t, img)

# Update the display
# pygame.display.flip()

# Add a delay to view the stimuli (optional)
# pygame.time.wait(1000)

# Close the pygame window when done
# pygame.quit()


def draw_stimulus(wd, prep, cond, data, t, img):
    # draw fixation cross
    draw_fixation(wd)

    # draw stimuli at specified locations
    for iCue in range(prep.nStim):
        location = prep.locs[t, iCue]
        screen.blit(img.stim[iCue], prep.draw.rect.stim[location])

    # draw choice
    if cond > 0:
        choiceLoc = prep.locs[t, data.choice[t]]
        screen.blit(img.select[data.choice[t]], prep.draw.rect.stim[choiceLoc])
        screen.blit(img.select[data.choice[t]], prep.draw.rect.stim[1])
        screen.blit(img.select[data.choice[t]], prep.draw.rect.stim[2])
        # You might need to adjust the blit positions and sizes

    # draw feedback: for 0, get punish feedback, for 1, get reward feedback
    if cond > 1:
        fbimg = img.feedback[data.outcome[t] + 1]
        screen.blit(fbimg, prep.draw.rect.stim[5])
        # You might need to adjust the blit positions and sizes


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


def generate_experiment_design(trials_per_epoch, total_epochs):
    experiment_design = []

    for epoch in range(total_epochs):
        if epoch % 2 == 0:
            reward_prob = 0.9
        else:
            reward_prob = 0.1

        for trial in range(trials_per_epoch):
            img1_position = random.choice(["left", "right"])
            img2_position = "right" if img1_position == "left" else "left"

            if random.random() < reward_prob:
                correct_choice = img1_position == "left"
                outcome_path = "pics/euro.jpg"
            else:
                correct_choice = img1_position == "right"
                outcome_path = "pics/noeuro1.jpg"

            if correct_choice:
                feedback = "positive"
            else:
                feedback = "negative"

            experiment_design.append(
                {
                    "epoch": epoch + 1,
                    "trial": trial + 1,
                    "img1_position": img1_position,
                    "img2_position": img2_position,
                    "correct_choice": correct_choice,
                    "feedback": feedback,
                    "outcome_path": outcome_path,
                }
            )

    return experiment_design
