import os
from PIL import Image, ImageTk
import tkinter as tk
import keyboard
import time

root = tk.Tk()
root.attributes('-fullscreen', True)
root.bind_all("<Escape>",lambda e: root.destroy())
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.configure(bg='black')

setup_mode = True

global current_turn_player


characters_to_assign = ["Shippo", "Poet", "Neva", "Heavy", "Noah", "Monster1", "Monster2", "Monster3", "Monster4", "Monster5"]
assignment_index = 0

initiative_slots = {}
current_turn_player = "Set slot for: Shippo"

viewing_overviewe = False
current_slot_index = 0

round_marker = False
current_round = 1

#Image Setup 
STATUS_ICONS = {}
status_names = ["grappled", "unconscious", "stunned", "invisible", "advantage", "disadvantage", "exhausted", "restrained", "petrified", "poisoned", "paralysed", "prone", "concentration", "incapacitated", "frightened", "charmed", "blindness"]

try:
    raw_grapple = Image.open("./icons/Grappled.png")
    resized_grapple = raw_grapple.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["grappled"] = ImageTk.PhotoImage(resized_grapple)

    raw_unconscious = Image.open("./icons/Unconscious.png")
    resized_unconscious = raw_unconscious.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["unconscious"] = ImageTk.PhotoImage(resized_unconscious)

    raw_stunned = Image.open("./icons/Stunned.png")
    resized_stunned = raw_stunned.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["stunned"] = ImageTk.PhotoImage(resized_stunned)

    raw_invisible = Image.open("./icons/Invisible.png")
    resized_invisible = raw_invisible.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["invisible"] = ImageTk.PhotoImage(resized_invisible)

    raw_advantage = Image.open("./icons/Advantage.png")
    resized_advantage = raw_advantage.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["advantage"] = ImageTk.PhotoImage(resized_advantage)

    raw_disadvantage = Image.open("./icons/Disadvantage.png")
    resized_disadvantage = raw_disadvantage.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["disadvantage"] = ImageTk.PhotoImage(resized_disadvantage)

    raw_exhausted = Image.open("./icons/Exhausted.png")
    resized_exhausted = raw_exhausted.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["exhausted"] = ImageTk.PhotoImage(resized_exhausted)

    raw_restrained = Image.open("./icons/Restrained.png")
    resized_restrained = raw_restrained.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["restrained"] = ImageTk.PhotoImage(resized_restrained)

    raw_petrified = Image.open("./icons/Petrified.png")
    resized_petrified = raw_petrified.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["petrified"] = ImageTk.PhotoImage(resized_petrified)

    raw_poisoned = Image.open("./icons/Poisoned.png")
    resized_poisoned = raw_poisoned.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["poisoned"] = ImageTk.PhotoImage(resized_poisoned)

    raw_paralysed = Image.open("./icons/Paralysed.png")
    resized_paralysed = raw_paralysed.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["paralysed"] = ImageTk.PhotoImage(resized_paralysed)

    raw_prone = Image.open("./icons/Prone.png")
    resized_prone = raw_prone.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["prone"] = ImageTk.PhotoImage(resized_prone)

    raw_concentration = Image.open("./icons/Concentration.png")
    resized_concentration = raw_concentration.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["concentration"] = ImageTk.PhotoImage(resized_concentration)

    raw_incapacitated = Image.open("./icons/Incapacitated.png")
    resized_incapacitated = raw_incapacitated.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["incapacitated"] = ImageTk.PhotoImage(resized_incapacitated)

    raw_frightened = Image.open("./icons/Frightened.png")
    resized_frightened = raw_frightened.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["frightened"] = ImageTk.PhotoImage(resized_frightened)

    raw_charmed = Image.open("./icons/Charmed.png")
    resized_charmed = raw_charmed.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["charmed"] = ImageTk.PhotoImage(resized_charmed)

    raw_blindness = Image.open("./icons/Blindness.png")
    resized_blindness = raw_blindness.resize((50, 50), Image.LANCZOS)
    STATUS_ICONS["blindness"] = ImageTk.PhotoImage(resized_blindness)


except Exception as e:
    print(f"Error loading images: {e}")

def assign_initiative_rank(event):
    global setup_mode, assignment_index, viewing_overview
    global current_turn_player, round_marker, current_round
    
    if setup_mode and event.char == 'x':
       skipped_name = characters_to_assign[assignment_index]
       print(f"Setup Skip: Skipping {skipped_name} entirely for this encounter")
       assignment_index += 1
       if assignment_index >= len(characters_to_assign):
            print("All characters assigned! Combat begins now!")
            setup_mode = False
            round_marker = True
            current_round = 1
            current_round_index = -1
            current_turn_player = f"Combat Round {current_round}"
            update_ui()
       else:
           current_turn_player= f"Set slot for: {characters_to_assign[assignment_index]}"
           update_ui()       
       return

    try:
        chosen_slot = int(event.char)
    except ValueError:
            return
    if setup_mode:

        if assignment_index >= len(characters_to_assign):
            print("All characters assigned! Combat begins now!")
            setup_mode = False
            round_marker = True
            current_round = 1
            current_round_index = -1
            current_turn_player = f"Combat Round {current_round}"
            update_ui()
            return

        character_name = characters_to_assign[assignment_index]
        initiative_slots[chosen_slot] = character_name
        print(f"Assigned {character_name} to slot {chosen_slot}")
        assignment_index += 1

        if assignment_index < len(characters_to_assign):
            current_turn_player = f"Set slot for: {characters_to_assign[assignment_index]}"

        initiative_slots[chosen_slot] = character_name
        print(f"Assigned {character_name} to slot {chosen_slot}")

       
        update_ui()
    else:
        chosen_slot=int(event.char)
        if chosen_slot in initiative_slots:
            viewing_overview = False
            current_turn_player = initiative_slots[chosen_slot]
            update_ui()
        else:
            print(f"COMBAT: No player assigned to slot {chosen_slot}")

#UI Layout Setup 
main_container = tk.Frame(root, bg='black')
main_container.pack(expand=True)

name_label = tk.Label(main_container, text=current_turn_player, font=("Arial", 25, "bold"), fg="white", bg="#2D6E1F", width=20, wraplength=1200, justify="center")
name_label.pack(side="top", anchor="center",pady=(0,20))

status_frame = tk.Frame(main_container, bg='black')
status_frame.pack(side="top",anchor="center")
   

combat_registry = {
        "Shippo": {
            "conditions": []
        },
        "Poet": {
            "conditions": []
        },
        "Neva": {
            "conditions": []
        },
        "Heavy": {
            "conditions": []
        },
        "Noah": {
            "conditions": []
        },
        "Monster1": {
            "conditions": []
        },
        "Monster2": {
            "conditions": []
        },
        "Monster3": {
            "conditions": []
        },
        "Monster4": {
            "conditions": []
        },
        "Monster5": {
            "conditions": []
        },
}
#event handler
def initiative(event):
    global current_turn_player, initiative_slots, setup_mode, viewing_overview
    if setup_mode:
        return

    viewing_overview = True
    print("Initiative")
    display_text = "--- Initiative Order --- \n"
    for rank in sorted(initiative_slots.keys()):
        character_at_rank = initiative_slots[rank]
        display_text += f"{rank}: {character_at_rank}\n"

    for widget in status_frame.winfo_children():
        widget.destroy()

    root.configure(bg="black")
    main_container.configure(bg="black")
    status_frame.configure(bg="black")

    name_label.configure(text=display_text,font=("Arial", 25, "bold"), bg="black", fg="white")

    current_turn_player = "Initiative"
    root.update_idletasks()
    

def shippo(event):
    print("Shippo's turn")
    global current_turn_player 
    current_turn_player = "Shippo"
    update_ui() 

def poet(event):
    print("Poet's turn")
    global current_turn_player 
    current_turn_player = "Poet"
    update_ui()

def neva(event):
    print("Neva's turn")
    global current_turn_player 
    current_turn_player = "Neva"
    update_ui()

def heavy(event):
    print("Heavy's turn")
    global current_turn_player 
    current_turn_player = "Heavy"
    update_ui()

def noah(event):
    print("Noah's turn")
    global current_turn_player 
    current_turn_player = "Noah"
    update_ui()

def monster1(event):
    print("Monster1's turn")
    global current_turn_player 
    current_turn_player = "Monster1"
    update_ui()

def monster2(event):
    print("Monster2's turn")
    global current_turn_player 
    current_turn_player = "Monster2"
    update_ui()

def monster3(event):
    print("Monster3's turn")
    global current_turn_player 
    current_turn_player = "Monster3"
    update_ui()

def monster4(event):
    print("Monster4's turn")
    global current_turn_player 
    current_turn_player = "Monster4"
    update_ui()

def monster5(event):
    print("Monster5's turn")
    global current_turn_player 
    current_turn_player = "Monster5"
    update_ui()

def g(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "grappled" in current_statuses:
       current_statuses.remove("grappled")
       print("Removing grappled status")
   else:
       current_statuses.append("grappled")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}") 
   update_ui()

def u(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "unconscious" in current_statuses:
       current_statuses.remove("unconscious")
   else:
       current_statuses.append("unconscious")

   update_ui()

def back(event):
    global running
    running = False

def advance_turn(event):
    global current_turn_player, current_slot_index, current_round, round_marker, setup_mode, viewing_overview

    if setup_mode:
       print("Cannot advance turn. In setup mode")
       return

    active_slots = sorted(initiative_slots.keys())

    if not active_slots:
       return

    viewing_overview = False

    if round_marker:
       round_marker = False
       current_slot_index = -1
       current_turn_player = initiative_slots[active_slots[current_slot_index]]
       update_ui()

    current_slot_index += 1

    if current_slot_index >= len(active_slots):
       current_round += 1
       round_marker = True
       current_turn_player = f"Round {current_round}"
       update_ui()
       return

    next_slot_number = active_slots[current_slot_index]
    current_turn_player = initiative_slots[next_slot_number]

    update_ui()

def reset(event):
    global setup_mode, assignment_index, current_turn_player, initiative_slots, current_slot_index, current_round, round_marker
    
    initiative_slots.clear()
    assignment_index = 0
    current_slot_index = -1


    for character in combat_registry:
        if "conditions" in combat_registry[character]:
            combat_registry[character]["conditions"].clear()

    setup_mode = True
    viewing_mode = False
    round_marker = False
    current_round = 1

    current_turn_player = "Set slot for: Shippo"
    update_ui()


def a(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "advantage" in current_statuses:
       current_statuses.remove("advantage")
       print("Removing advantage")
   else:
       current_statuses.append("advantage")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()

def b(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "blindness" in current_statuses:
       current_statuses.remove("blindness")
       print("Removing blinded status")
   else:
       current_statuses.append("blindness")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()

def c(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "charmed" in current_statuses:
       current_statuses.remove("charmed")
       print("Removing charmed status")
   else:
       current_statuses.append("charmed")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def d(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "disadvantage" in current_statuses:
       current_statuses.remove("disadvantage")
       print("Removing grappled status")
   else:
       current_statuses.append("disadvantage")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def e(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "exhausted" in current_statuses:
       current_statuses.remove("exhausted")
       print("Removing grappled status")
   else:
       current_statuses.append("exhausted")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def f(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "frightened" in current_statuses:
       current_statuses.remove("frightened")
       print("Removing grappled status")
   else:
       current_statuses.append("frightened")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def h(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "incapacitated" in current_statuses:
       current_statuses.remove("incapacitated")
       print("Removing grappled status")
   else:
       current_statuses.append("incapacitated")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def inv(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "invisible" in current_statuses:
       current_statuses.remove("invisible")
       print("Removing grappled status")
   else:
       current_statuses.append("invisible")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def j(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "concentration" in current_statuses:
       current_statuses.remove("concentration")
       print("Removing grappled status")
   else:
       current_statuses.append("concentration")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def k(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "paralysed" in current_statuses:
       current_statuses.remove("paralysed")
       print("Removing grappled status")
   else:
       current_statuses.append("paralysed")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def o(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "poisoned" in current_statuses:
       current_statuses.remove("poisoned")
       print("Removing grappled status")
   else:
       current_statuses.append("poisoned")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


def p(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "prone" in current_statuses:
       current_statuses.remove("prone")
       print("Removing grappled status")
   else:
       current_statuses.append("prone")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()



def r(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "restrained" in current_statuses:
       current_statuses.remove("restrained")
       print("Removing grappled status")
   else:
       current_statuses.append("restrained")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()

def s(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "stunned" in current_statuses:
       current_statuses.remove("stunned")
       print("Removing grappled status")
   else:
       current_statuses.append("stunned")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()

def t(event):
   current_statuses = combat_registry[current_turn_player]["conditions"]

   if "petrified" in current_statuses:
       current_statuses.remove("petrified")
       print("Removing grappled status")
   else:
       current_statuses.append("petrified")
       print(f"Debug: Current registry content for {current_turn_player}:{combat_registry[current_turn_player]}")
   update_ui()


#Keyboard logic 

#root.bind_all("<Key>", key_press)
for i in range(1,10):
    root.bind_all(str(i), assign_initiative_rank)
root.bind_all('0', assign_initiative_rank)
root.bind_all('x', assign_initiative_rank)
root.bind_all(',', initiative)
root.bind_all('-', back)
root.bind_all('<space>', advance_turn)
root.bind_all(';', reset)
root.bind_all('g', g) #grapple
root.bind_all('u', u) #unconscious
root.bind_all('a', a) #advantage
root.bind_all('b', b) #blinded
root.bind_all('c', c) #charmed 
root.bind_all('d', d) #disadvantage
root.bind_all('e', e) #exhausted
root.bind_all('f', f) #frightened
root.bind_all('h', h) #incapacitated
root.bind_all('i', inv) #invisible
root.bind_all('j', j) #concentration
root.bind_all('k', k) #paralysed
root.bind_all('o', o) #poisoned
root.bind_all('p', p) #prone
root.bind_all('r', r) #restrained
root.bind_all('s', s) #stunned
root.bind_all('t', t) #petrified

def update_ui():
    global setup_mode, current_turn_player, round_number, round_marker
    if setup_mode:
        background = "#2D6E1F"
        foreground = 'white'
    else:
        if current_turn_player == "Shippo":
           background = "#75DAE0"
           foreground = 'black'
        elif current_turn_player == "Poet":
           background = "#7823B8"
           foreground = 'white'
        elif current_turn_player =="Neva":
           background = "#D1B7E8"
           foreground = 'black'
        elif current_turn_player == "Heavy":
           background = "#195CD4"
           foreground = 'white'
        elif current_turn_player == "Noah":
           background = "#7793C9"
           foreground = 'black'
        elif current_turn_player == "Initiative":
           background = "#2D6E1F"
           foreground = 'white'
        elif round_marker:
           background = "#2D6E1F"
           foreground = 'white'
        else:
           background = "#DE1D3C"
           foreground = 'white'

    root.configure(bg='black')
    main_container.configure(bg='black')
    name_label.configure(text=current_turn_player,font=("Arial", 74, "bold"),fg = foreground, bg=background, width=20, wraplength=1200, justify="center")
    status_frame.configure(bg='black')
    
    if setup_mode:
       name_label.configure(text=current_turn_player, font=("Arial", 25, "bold"))
       
       for widget in status_frame.winfo_children():
           widget.destroy()
    elif round_marker:
       name_label.configure(text=current_turn_player, font=("Arial", 50, "bold"))

       for widget in status_frame.winfo_children():
           widget.destroy()
    else:
        name_label.configure(text=current_turn_player)
        for widget in status_frame.winfo_children():
            widget.destroy()

        if current_turn_player in combat_registry:
           active_conditions = combat_registry[current_turn_player]["conditions"]
           for condition in active_conditions:
               if condition in STATUS_ICONS:
                  mini_block = tk.Frame(status_frame, bg="black")
                  mini_block.pack(side="left", padx=10, fill="both", expand=True)

                  icon_label = tk.Label(mini_block, image=STATUS_ICONS[condition], bg="black")
                  icon_label.pack(side="top")
                  icon_label.image = STATUS_ICONS[condition]
                  text_label = tk.Label(mini_block, text=condition.capitalize(), font=("Arial", 14, "bold"), fg="white", bg="black")
                  text_label.pack(side="top", anchor="center", pady=(5,5), fill = "x")


    update_status_display(background)
 
    root.update_idletasks()

   
def update_status_display(current_bg):   
   for widget in status_frame.winfo_children():
       widget.destroy()


   #active_conditions = combat_registry[current_turn_player]["conditions"]
   if current_turn_player in combat_registry and "conditions" in combat_registry[current_turn_player]:
      active_conditions = combat_registry[current_turn_player]["conditions"]
      for condition in active_conditions:
          if condition in STATUS_ICONS:
             mini_block = tk.Frame(status_frame, bg="black")
             mini_block.pack(side="left", padx=10, fill="both", expand=True)

             icon_label = tk.Label(mini_block, image=STATUS_ICONS[condition], bg="black")
             icon_label.pack(side="top")
             icon_label.image = STATUS_ICONS[condition]
             text_label = tk.Label(mini_block, text=condition.capitalize(), font=("Arial", 14, "bold"), fg="white", bg="black")
             text_label.pack(side="top", anchor="center", pady=(5,5), fill = "x")
   else:
       for widget in status_frame.winfo_children():
           widget.destroy()

def on_closing():
  global combat_registry

  print("Safely clearing combat states and shutting down tracker")

  for player in combat_registry:
      if "conditions" in combat_registry[player]:
         combat_registry[player]["conditions"].clear()

  root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)  
   


root.lift()
root.focus_force()
root.mainloop()

