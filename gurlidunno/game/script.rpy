# game/script.rpy
# Ren'Py script for "Stray's Journey" interactive story

default lives = 4

define d = Character("Doggo", color="#c8ffc8")

transform heartpos:
    xpos 0.01
    ypos 0.01

transform doggointro:
    xpos 0.68
    xoffset -48
    ypos 0.68
    yoffset -48

transform doggoroad:
    xpos 0.4
    xoffset -48
    ypos 0.5
    yoffset -48
    zoom 2.0

transform doggomarket:
    xpos 0.36
    xoffset -48
    ypos 0.65
    yoffset -48
    zoom 2.5

transform doggosunny:
    xpos 0.13
    xoffset -48
    ypos 0.55
    yoffset -48
    zoom 1.7

transform doggostream:
    xpos 0.25
    xoffset -48
    ypos 0.63
    yoffset -48
    zoom 2.9


image heart4flash:
    "heart empty.png"
    pause 0.5
    "heart 4.png"
    pause 0.5
    repeat
image heart3flash:
    "heart empty.png"
    pause 0.5
    "heart 3.png"
    pause 0.5
    repeat
image heart2flash:
    "heart empty.png"
    pause 0.5
    "heart 2.png"
    pause 0.5
    repeat
image heart1flash:
    "heart empty.png"
    pause 0.5
    "heart 1.png"
    pause 0.5
    repeat
image heart0flash:
    "heart empty.png"
    pause 0.5
    "heart 0.png"
    pause 0.5
    repeat

image dogidle:
    "dog idle.png"
    crop (0, 0, 48, 48)
    pause 0.2
    "dog idle.png"
    crop (48, 0, 48, 48)
    pause 0.2
    "dog idle.png"
    crop (96, 0, 48, 48)
    pause 0.2
    "dog idle.png"
    crop (144, 0, 48, 48)
    pause 0.2
    repeat

image dogattack:
    "dog attack.png"
    crop (0, 0, 48, 48)
    pause 0.2
    "dog attack.png"
    crop (48, 0, 48, 48)
    pause 0.2
    "dog attack.png"
    crop (96, 0, 48, 48)
    pause 0.2
    "dog attack.png"
    crop (144, 0, 48, 48)
    pause 0.2
    repeat

image doghurt:
    "dog hurt.png"
    crop (0, 0, 48, 48)
    pause 0.8
    "dog hurt.png"
    crop (48, 0, 48, 48)
    pause 0.2
    repeat

# -------------------------------
# Start of the Game
label start:
    scene bg start
    with fade

    show dogidle at doggointro
    "🐾 Welcome to Stray\’s Journey!" 
    "You will follow a stray dog through struggles it faces in its everyday life."
    show heart4flash at heartpos
    "You start with 4 lives."
    hide heart4flash
    show heart 4 at heartpos
    "Each wrong choice costs a life. Make safe choices to help the dog survive!"
    "Press START to begin."

    jump scenario1

# -------------------------------
# SCENARIO 1: Crossing the Road
# -------------------------------
label scenario1:
    scene bg road
    with fade

    show heart 4 at heartpos
    show dogattack at doggoroad
    pause 1.8
    hide dogattack
    show dogidle at doggoroad
    

    d "Help me cross the road safely!"
    d "Which path should I take?"

    menu:
        "Run across the road":
            $ lives -= 1
            hide dogidle
            show doghurt at doggoroad
            hide heart 4
            show heart3flash at heartpos
            "The dog tries running across the street. A scooter hits it! 😔"

        "Wait near the footpath":
            $ lives -= 1
            hide dogidle
            show doghurt at doggoroad
            hide heart 4
            show heart3flash at heartpos
            "The dog waits too long. A car brushes it. 😔"

        "Cross with people":
            "The dog safely crosses with people!"

        "Wait for help":
            "A traffic policeman notices and helps the dog!"

    jump scenario2

# -------------------------------
# SCENARIO 2: Searching for Food
# -------------------------------
label scenario2:
    scene bg market
    with fade

    show expression "heart %d" % lives at heartpos
    show dogattack at doggomarket
    pause 1.8
    hide dogattack
    show dogidle at doggomarket
    d "I'm so hungryyyy..."
    d "Help me find food!"

    menu:
        "Try some yummy fish from a stall":
            $ lives -= 1
            hide dogidle
            show doghurt at doggomarket
            hide heart % lives
            show expression "heart%dflash" % lives at heartpos
            "The vendor hits the dog with a stick! 😔"
            
        "Dig through the trash":
            $ lives -= 1
            hide dogidle
            show doghurt at doggomarket
            hide heart % lives
            show expression "heart%dflash" % lives at heartpos
            "The dog accidentally eats plastic from trash. 😔"

        "Puppy eyes at the tea stall owner":
            "A kind tea-stall owner gives bread!"

        "Sniff around the temple":
            "The dog finds rice near the temple!"


    jump scenario3

# -------------------------------
# SCENARIO 3: Escaping Heat
# -------------------------------
label scenario3:
    scene bg sunny
    with fade

    show expression "heart %d" % lives at heartpos
    show dogattack at doggosunny
    pause 1.8
    hide dogattack
    show dogidle at doggosunny

    d "It's so hot today..."
    d "Where can I find some shade?"

    menu:
        "Hide under a car":
            $ lives -= 1
            hide dogidle
            show doghurt at doggosunny
            hide heart % lives
            show expression "heart%dflash" % lives at heartpos
            "The engine starts. Ouch that burns! 😔"

        "Wander into a construction site":
            $ lives -= 1
            hide dogidle
            show doghurt at doggosunny
            hide heart % lives
            show expression "heart%dflash" % lives at heartpos
            "Accidentally step on nails! 😔"

        "Take a nap under a tree":
            "The shade is cool and refreshing."

        "Enter a shop to cool off":
            "The kind shopkeeper lets the dog rest inside!"

    jump scenario4

# -------------------------------
# SCENARIO 4: Seeking Companionship
# -------------------------------
label scenario4:
    scene bg stream
    with fade

    show expression "heart %d" % lives at heartpos
    show dogattack at doggostream
    pause 1.8
    hide dogattack
    show dogidle at doggostream

    d "I'm feeling lonely..."
    d "What should I do?"

    menu:
        "Play with the neighbourhood kids":
            $ lives -= 1
            hide dogidle
            show doghurt at doggostream
            hide heart % lives
            show expression "heart%dflash" % lives at heartpos
            "The kids think its fun to throw stones at the dog 😔"

        "Approach the goofy looking cat":
            $ lives -= 1
            hide dogidle
            show doghurt at doggostream
            hide heart % lives
            show expression "heart%dflash" % lives at heartpos
            "The cat gets spooked and scratches the dog 😔"

        "Follow the sweet grandma":
            "The dog gets pampered!"

        "Look for your friends":
            "The dog finds its friends and has a fun time!"

    jump ending

# -------------------------------
# ENDINGS
# -------------------------------
label ending:
    scene bg train
    "The stray’s journey ends here."
    "Many strays never make it because of the risks they face every day."
    "But you can help! Make sure you report, adopt, and care."
    "Remember: your awareness can change the life of a stray."
    $ lives = 4
    jump start
