# --------------------------------------------------------------------------- #
# ~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~ #
# =========================================================================== #
# EXTREME STOPWATCH!!!                                                        #
# v1.74                                                                       #
# By Chloe Unrau 2013                                                         #
# An event-driven program in Python created for CodeSkulptor.org.             #
# To play, paste this code into codeskulptor.org and press play.              #
#                                                                             #
# Dedicated to my dad, who needs something to do :)                           #
# =========================================================================== #
# ~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~==~ * ~ #
# --------------------------------------------------------------------------- #


# Import Modules
# =============================================================================
# -----------------------------------------------------------------------------

import simplegui
import random


# Define Global Variables
# =============================================================================
# -----------------------------------------------------------------------------

# frame elements
frame_width = 300
frame_height = 300
control_width = 300
button_width = control_width

# timers
stopwatch_interval = 100
# colour_interval : frequency of achievement message colour cycling
colour_interval = 100
# blink_interval : frequency of achievement message blinking
blink_interval = 500
# music_interval : the exact length of the music track
music_interval = 6007

# text
score_streak_font_size = 10
score_message_font_size = 20
message_event_font_size = 20
time_font_size = 60
font_face_all = "monospace"
colour_time = "#eaedc1"
colour_time_max = "#b70e0e"
colour_score = "#9ce4a8"
colour_streak = "#ffffff"
colour_stars = "#ffffff"

# colours for rainbow effect of event message
rainbow = {}
rainbow[0] = "#dea7dc"   #pink
rainbow[1] = "#9ce4a8"   #green
rainbow[2] = "#fdff7d"   #yellow
rainbow[3] = "#88d5e1"   #blue
rainbow[4] = "#ff5151"   #red
rainbow[5] = "#b95fff"   #purple
rainbow_colour = 0
colour_count = 0

# achievement messages
achievement_scores = {}
achievement_scores[5] = ["5 POINTS", "YOU'VE GOT IT", "FIIIVE GOOOLD RIIINGS", "5 5 5 5 5", "FIRST ACHIEVEMENT"]
achievement_scores[10] = ["KEEP STOPWATCHING", "10 10 10 10 10", "NOVICE STATUS"]
achievement_scores[25] = ["OOOOOH, WORK IT", "SHRUBBERY", "25 25 25 25 25", "EXPERT STATUS"]
achievement_scores[50] = ["HEROIC STATUS", "50 50 50 50 50", "COMMUNIST BATH PARTY"]
achievement_scores[100] = ["100 POINTS", "EXTREME STOPWATCHIST", "THE HUMAN MUSTACHE", "DIVINE STATUS"]

# effects
event_message = ""
message_displayed = False
music_is_muted = False
num_colours = 0
blink_count = 0
num_blinks = 0
message_x = 0
star_x = 0
star_i = 0

# score
my_score = 0
guess_count = 0
score_total = str(my_score) + "/" + str(guess_count)
current_streak = 0
best_streak = 0
new_streak = False
did_score = False
time_is_max = False

# stopwatch
a = 0
b = 0
c = 0
d = 0
time = str(a) + ":" + str(b) + str(c) + "." + str(d)


# Define Helper Fuctions
# =============================================================================
# -----------------------------------------------------------------------------

def update_time():
    global a, b, c, d, time
    time = str(a) + ":" + str(b) + str(c) + "." + str(d)

def update_score():
    global my_score, guess_count, score_total
    score_total = str(my_score) + "/" + str(guess_count)

def update_event_message(loc_did_score, loc_score):
    """
    Generate event messages

    NOTE: Achievement badges are drawn in the draw handler, independant of this function
    """
    global event_message, message_x, message_displayed, num_blinks

    # set the game over message if the timer is at its maximum
    if time_is_max:
        event_message = "GAME OVER : PLEASE RESET"
        num_blinks = 20

    if loc_did_score:

        # set and display an event message if score is an achievement score
        if loc_score in achievement_scores:
            sound_cheevo.play()
            # choose a random message among the choices available for the achievement
            event_message = achievement_scores[loc_score][random.randrange(0, len(achievement_scores[loc_score]))]
            num_blinks = 4

        # if user scores a new streak, and it's not an achievement, set the score streak message
        elif new_streak:
            event_message = "NEW SCORE STREAK"
            num_blinks = 1

    # process the event message if any of the event cases are true
    if (time_is_max) or (loc_did_score and (loc_score in achievement_scores)) or (new_streak):

        # centre the event message
        message_x = centre_x(event_message, score_message_font_size, font_face_all)

        # play the event message
        if message_displayed == True:
            # reset the event message if a message is already active
            message_displayed = False
            message_colour_timer.stop()
            message_blink_timer.stop()
        message_displayed = True
        message_colour_timer.start()
        message_blink_timer.start()

    # if no event message to be displayed, clear the event message
    else:
        event_message = ""
        message_displayed = False
        message_colour_timer.stop()
        message_blink_timer.stop()

def centre_x(text, size, font):
    """ Returns the x coordinate to centre text horizontally within the frame """
    text_width = frame.get_canvas_textwidth(text, size, font)
    return ((frame_width / 2) - (text_width / 2))


# Define Event Handlers
# =============================================================================
# -----------------------------------------------------------------------------

def start_stop_stopwatch():
    global guess_count, my_score, did_score, current_streak, best_streak, new_streak
    # stop the timer if it's running
    if timer.is_running() and not time_is_max:
        timer.stop()

        # increment the score
        guess_count += 1
        if d == 0:
            did_score = True
            my_score += 1
            current_streak += 1
            if current_streak > best_streak:
                best_streak = current_streak
                new_streak = True
                # play special sound if current score streak beats best score streak
                sound_score_streak.play()
            else:
                # play regular sound otherwise
                sound_score.play()
        else:
            did_score = False
            new_streak = False
            current_streak = 0
            sound_fail.play()

        update_score()

        # display a message at achievement scores or score streaks
        update_event_message(did_score, my_score)

        # reset new_streak to ensure new streak message doesn't play when failing after a new streak
        new_streak = False

    # start the timer if it's stopped
    elif not timer.is_running() and not time_is_max:
        timer.start()
        music_timer.start()

def reset_stopwatch():
    global a, b, c, d, time_is_max, my_score, guess_count, current_streak, best_streak, star_x, star_i
    sound_reset.play()
    # stop the timer
    timer.stop()
    # reset the timer
    a, b, c, d = 0, 0, 0, 0
    star_x, star_i = 0, 0
    time_is_max = False
    update_time()
    # reset the score and streaks
    my_score, guess_count = 0, 0
    current_streak, best_streak = 0, 0
    update_score()
    # clear the event message
    update_event_message(False, 0)

def keydown(key):
    """ Create keyboard controls """
    # start / stop : spacebar
    if key == simplegui.KEY_MAP["space"]:
        start_stop_stopwatch()
    # reset : r
    if key == simplegui.KEY_MAP["r"]:
        reset_stopwatch()
    # mute / unmute music : m
    if key == simplegui.KEY_MAP["m"]:
        mute_unmute()

def tick():
    """ Increment the timer by 1/10th of a second, and stop if maximum """
    global a, b, c, d, time_is_max, star_x, star_i
    d += 1
    if d == 10:
        d = 0
        c += 1
        if c == 10:
            c = 0
            b += 1
            # b is 6 because the last second before a new minute is 59
            if b == 6:
                b = 0
                a += 1
                if a == 10:
                    # stop the timer before the minutes digit becomes 10
                    timer.stop()
                    # maintain the timer text at its maximum until it is reset
                    a, b, c, d = 9, 5, 9, 9
                    time_is_max = True
                    # play the game-over sound and event message
                    update_event_message(False, my_score)
                    sound_game_over.play()
    update_time()

    # update the position of the animated stars so that each
    # full pass is one full increment of the seconds digit
    star_i += (frame_width / (stopwatch_interval / 10))
    star_x = star_i % (frame_width)

def message_colour_tick():
    """ Create rainbow cycling effect for the event messages """
    global colour_count
    colour_count += 1

def message_blink_tick():
    """ Create blink effect for the event messages """
    global message_displayed, blink_count
    # stop the event message after set number of blinks
    if blink_count >= ((num_blinks * 2) - 1):
        # stop blink and colour timers (started in update_event_message)
        message_blink_timer.stop()
        message_colour_timer.stop()
        # disable event message
        blink_count = 0
        message_displayed = False
    # increment blinks
    else:
        message_displayed = not message_displayed
        blink_count += 1

def music_tick():
    if not music_is_muted:
        music.play()
        music.rewind()
        music.play()

def mute_unmute():
    global music_is_muted
    if music_is_muted:
        music_timer.start()
        music.play()
    else:
        music.pause()
    music_is_muted = not music_is_muted

def draw(canvas):
    """ Draws all elements inside the CodeSkulptor frame """

    # draw the background graphic
    canvas.draw_image(background, (150, 150), (300, 300), (150, 150), (300, 300))

    # draw the stopwatch text
    if not time_is_max:
        # normal colour: light yellow
        canvas.draw_text(time, [centre_x(time, time_font_size, font_face_all), 143], time_font_size, colour_time, font_face_all)
    else:
        # maximum time colour: red
        canvas.draw_text(time, [centre_x(time, time_font_size, font_face_all), 143], time_font_size, colour_time_max, font_face_all)

    # draw the score as 'correct guesses / total guesses'
    canvas.draw_text(score_total, [200, 40], score_message_font_size, colour_score, font_face_all)

    # draw the score message
    if message_displayed:
        # modulus loops all the colours in rainbow
        # colour_count incremented in message_colour_tick
        rainbow_colour = colour_count % len(rainbow)
        canvas.draw_text(event_message, [message_x, 70], message_event_font_size, rainbow[rainbow_colour], font_face_all)

    # draw the animated stars (two white dots)
    canvas.draw_text(".", [star_x, 86], 12, colour_stars, font_face_all)
    canvas.draw_text(".", [star_x, 165], 12, colour_stars, font_face_all)

    # draw the achievement badges
    if my_score >= 5:
        canvas.draw_image(cheevo5, (10, 10), (21, 20), (12, 31), (21, 20))
    if my_score >= 10:
        canvas.draw_image(cheevo10, (10, 10), (21, 20), (35, 31), (21, 20))
    if my_score >= 25:
        canvas.draw_image(cheevo25, (10, 10), (21, 20), (58, 31), (21, 20))
    if my_score >= 50:
        canvas.draw_image(cheevo50, (10, 10), (21, 20), (81, 31), (21, 20))
    if my_score >= 100:
        canvas.draw_image(cheevo100, (10, 10), (21, 20), (104, 31), (21, 20))

    # draw the score streak counters
    canvas.draw_text("Current Streak:", [30, 180], score_streak_font_size, colour_streak, font_face_all)
    canvas.draw_text(str(current_streak), [125, 180], score_streak_font_size, colour_streak, font_face_all)
    canvas.draw_text("Best Streak:", [170, 180], score_streak_font_size, colour_streak, font_face_all)
    canvas.draw_text(str(best_streak), [247, 180], score_streak_font_size, colour_streak, font_face_all)

    
# Define Frame Elements
# =============================================================================
# -----------------------------------------------------------------------------

# define the CodeSkulptor frame
frame = simplegui.create_frame("Stopwatch", frame_width, frame_height, control_width)

# define timers
timer = simplegui.create_timer(stopwatch_interval, tick)
message_colour_timer = simplegui.create_timer(colour_interval, message_colour_tick)
message_blink_timer = simplegui.create_timer(blink_interval, message_blink_tick)
music_timer = simplegui.create_timer(music_interval, music_tick)

# load graphics
background = simplegui.load_image("http://www.chloeunrau.com/stuff/es-c.jpg")
cheevo5 = simplegui.load_image("http://www.chloeunrau.com/stuff/es-5a.jpg")
cheevo10 = simplegui.load_image("http://www.chloeunrau.com/stuff/es-10a.jpg")
cheevo25 = simplegui.load_image("http://www.chloeunrau.com/stuff/es-25a.jpg")
cheevo50 = simplegui.load_image("http://www.chloeunrau.com/stuff/es-50a.jpg")
cheevo100 = simplegui.load_image("http://www.chloeunrau.com/stuff/es-100a.jpg")

# load sounds
music = simplegui.load_sound("http://www.chloeunrau.com/stuff/music.ogg")
music.set_volume(0.5)
# music source:
# http://www.flashkit.com/
sound_cheevo = simplegui.load_sound("http://www.chloeunrau.com/stuff/achievement.ogg")
sound_cheevo.set_volume(1.0)
sound_score = simplegui.load_sound("http://www.chloeunrau.com/stuff/score.ogg")
sound_score.set_volume(0.5)
sound_fail = simplegui.load_sound("http://www.chloeunrau.com/stuff/fail.ogg")
sound_fail.set_volume(0.5)
sound_score_streak = simplegui.load_sound("http://www.chloeunrau.com/stuff/score-streak.ogg")
sound_score_streak.set_volume(0.5)
sound_reset = simplegui.load_sound("http://www.chloeunrau.com/stuff/reset.ogg")
sound_reset.set_volume(1.0)
sound_game_over = simplegui.load_sound("http://www.chloeunrau.com/stuff/game-over.ogg")
sound_game_over.set_volume(1.0)
# sound-effects source:
# http://www.freesound.org/

# define the draw handler
frame.set_draw_handler(draw)


# Register Event Handlers (elements that appear in the Control area)
# =============================================================================
# -----------------------------------------------------------------------------

button_start_stop = frame.add_button("START / STOP (spacebar)", start_stop_stopwatch, button_width)
keyboard_start_stop = frame.set_keydown_handler(keydown)

space = frame.add_label("")

button_mute = frame.add_button("MUTE / UNMUTE MUSIC (m)", mute_unmute, button_width)

space = frame.add_label("")

button_reset = frame.add_button("RESET (r)", reset_stopwatch, button_width)

space = frame.add_label("")

rules2 = frame.add_label("Stop on an exact second to score!")
rules3 = frame.add_label("Score: points / total tries")

space = frame.add_label("")

hint = frame.add_label("Hint: To use keyboard shortcuts, you may have to click once on the game.")


# Initiate Program
# =============================================================================
# -----------------------------------------------------------------------------

frame.start()
music_timer.start()
music.play()

