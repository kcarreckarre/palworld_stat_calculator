import tkinter as tk
from tkinter import ttk
from stat_calcul import Stat, Pal, IV, EV, Bonus, calculate_palworld_damage
import sqlite3

def get_pals():
    conn = sqlite3.connect('pals.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, local_img_path FROM pals")
    pals = cursor.fetchall()
    conn.close()
    return pals

pals = get_pals()
pal_names = [pal[0] for pal in pals]
pal_images = {pal[0]: pal[1] for pal in pals}

def update_stats(pal_side):
    if pal_side == "left":
        pal_name = pal_name_var_left.get()
        lvl = int(lvl_var_left.get())
        iv = IV(int(iv_hp_var_left.get()), int(iv_def_var_left.get()), int(iv_att_var_left.get()))
        ev = EV(int(ev_hp_var_left.get()), int(ev_def_var_left.get()), int(ev_att_var_left.get()))
        stars = int(stars_var_left.get())
        ps_bonus_hp = int(ps_bonus_hp_var_left.get())
        ps_bonus_def = int(ps_bonus_def_var_left.get())
        ps_bonus_att = int(ps_bonus_att_var_left.get())
        bonus = Bonus(ps_bonus_hp, ps_bonus_def, ps_bonus_att)
        stats = Stat(Pal.from_name(pal_name), iv, ev, lvl, stars, bonus)
        
        hp_var_left.set(stats.calculate_hp())
        def_var_left.set(stats.calculate_defense())
        att_var_left.set(stats.calculate_att())
        
        pal_image = tk.PhotoImage(file=pal_images[pal_name])
        canvas_left.delete("all")  # Clear the canvas
        canvas_left.create_image(50, 50, image=pal_image)
        canvas_left.image = pal_image
    else:
        pal_name = pal_name_var_right.get()
        lvl = int(lvl_var_right.get())
        iv = IV(int(iv_hp_var_right.get()), int(iv_def_var_right.get()), int(iv_att_var_right.get()))
        ev = EV(int(ev_hp_var_right.get()), int(ev_def_var_right.get()), int(ev_att_var_right.get()))
        stars = int(stars_var_right.get())
        ps_bonus_hp = int(ps_bonus_hp_var_right.get())
        ps_bonus_def = int(ps_bonus_def_var_right.get())
        ps_bonus_att = int(ps_bonus_att_var_right.get())
        bonus = Bonus(ps_bonus_hp, ps_bonus_def, ps_bonus_att)
        stats = Stat(Pal.from_name(pal_name), iv, ev, lvl, stars, bonus)
        
        hp_var_right.set(stats.calculate_hp())
        def_var_right.set(stats.calculate_defense())
        att_var_right.set(stats.calculate_att())
        
        pal_image = tk.PhotoImage(file=pal_images[pal_name])
        canvas_right.delete("all")  # Clear the canvas
        canvas_right.create_image(50, 50, image=pal_image)
        canvas_right.image = pal_image
    
    update_damage_range()

def validate_integer(P):
    if P.isdigit() or P == "":
        return True
    return False

def filter_combobox(event, combobox, values):
    entry = combobox.get().lower()
    filtered_values = [value for value in values if entry in value.lower()]
    combobox['values'] = filtered_values
    combobox.event_generate('<Down>')

def update_damage_range():
    try:
        move_power = float(move_power_var.get())
        left_attack = float(att_var_left.get())
        right_defense = float(def_var_right.get())
        left_level = float(lvl_var_left.get())

        min_damage = calculate_palworld_damage(left_level, move_power, left_attack, right_defense, stab_var.get())["min_damage"]
        max_damage = calculate_palworld_damage(left_level, move_power, left_attack, right_defense, stab_var.get())["max_damage"]  # You can add variability if needed

        min_damage_var.set(f"{min_damage:.2f}")
        max_damage_var.set(f"{max_damage:.2f}")
    except ValueError:
        min_damage_var.set("N/A")
        max_damage_var.set("N/A")

app = tk.Tk()
app.title("Damage Calculator")

# Variables for left pal
pal_name_var_left = tk.StringVar(value=pal_names[0])
lvl_var_left = tk.StringVar(value="0")
iv_hp_var_left = tk.StringVar(value="0")
iv_def_var_left = tk.StringVar(value="0")
iv_att_var_left = tk.StringVar(value="0")
ev_hp_var_left = tk.StringVar(value="0")
ev_def_var_left = tk.StringVar(value="0")
ev_att_var_left = tk.StringVar(value="0")
stars_var_left = tk.StringVar(value="0")
ps_bonus_hp_var_left = tk.StringVar(value="0")
ps_bonus_def_var_left = tk.StringVar(value="0")
ps_bonus_att_var_left = tk.StringVar(value="0")
hp_var_left = tk.StringVar()
def_var_left = tk.StringVar()
att_var_left = tk.StringVar()

# Variables for right pal
pal_name_var_right = tk.StringVar(value=pal_names[0])
lvl_var_right = tk.StringVar(value="0")
iv_hp_var_right = tk.StringVar(value="0")
iv_def_var_right = tk.StringVar(value="0")
iv_att_var_right = tk.StringVar(value="0")
ev_hp_var_right = tk.StringVar(value="0")
ev_def_var_right = tk.StringVar(value="0")
ev_att_var_right = tk.StringVar(value="0")
stars_var_right = tk.StringVar(value="0")
ps_bonus_hp_var_right = tk.StringVar(value="0")
ps_bonus_def_var_right = tk.StringVar(value="0")
ps_bonus_att_var_right = tk.StringVar(value="0")
hp_var_right = tk.StringVar()
def_var_right = tk.StringVar()
att_var_right = tk.StringVar()

#Stab_var
stab_var = tk.BooleanVar(value=False)



# Validation command for integer entry
vcmd = (app.register(validate_integer), '%P')

# Left panel
left_frame = ttk.Frame(app)
left_frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(left_frame, text="Pal Image").grid(row=0, column=0)
canvas_left = tk.Canvas(left_frame, width=100, height=100, bg="white")
canvas_left.grid(row=1, column=0)
pal_image_left = tk.PhotoImage(file=pal_images[pal_names[0]])
canvas_left.create_image(50, 50, image=pal_image_left)
canvas_left.image = pal_image_left

ttk.Label(left_frame, text="Pal Name").grid(row=2, column=0)
pal_name_combobox_left = ttk.Combobox(left_frame, textvariable=pal_name_var_left, values=pal_names, state='normal')
pal_name_combobox_left.grid(row=3, column=0, columnspan=2)
pal_name_combobox_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))
pal_name_combobox_left.bind('<KeyRelease>', lambda event: filter_combobox(event, pal_name_combobox_left, pal_names))

ttk.Label(left_frame, text="Stars").grid(row=2, column=3)
stars_menu_left = ttk.OptionMenu(left_frame, stars_var_left, "0", *[str(i) for i in range(5)], command=lambda _: update_stats("left"))
stars_menu_left.grid(row=3, column=3)

ttk.Label(left_frame, text="Lvl").grid(row=4, column=0)
lvl_menu_left = ttk.Combobox(left_frame, textvariable=lvl_var_left, values=[str(i) for i in range(101)], state='normal')
lvl_menu_left.grid(row=5, column=0)
lvl_menu_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))

ttk.Label(left_frame, text="HP").grid(row=6, column=0)
ttk.Label(left_frame, textvariable=hp_var_left).grid(row=7, column=0)

ttk.Label(left_frame, text="EV HP %").grid(row=6, column=1)
ev_hp_menu_left = ttk.Combobox(left_frame, textvariable=ev_hp_var_left, values=[str(i) for i in range(31)], state='normal')
ev_hp_menu_left.grid(row=7, column=1)
ev_hp_menu_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))

ttk.Label(left_frame, text="IV HP").grid(row=6, column=2)
iv_hp_menu_left = ttk.Combobox(left_frame, textvariable=iv_hp_var_left, values=[str(i) for i in range(101)], state='normal')
iv_hp_menu_left.grid(row=7, column=2)
iv_hp_menu_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))

ttk.Label(left_frame, text="PS_Bonus HP").grid(row=6, column=3)
ps_bonus_hp_entry_left = ttk.Entry(left_frame, textvariable=ps_bonus_hp_var_left, validate="key", validatecommand=vcmd)
ps_bonus_hp_entry_left.grid(row=7, column=3)

ttk.Label(left_frame, text="DEF").grid(row=8, column=0)
ttk.Label(left_frame, textvariable=def_var_left).grid(row=9, column=0)

ttk.Label(left_frame, text="EV DEF %").grid(row=8, column=1)
ev_def_menu_left = ttk.Combobox(left_frame, textvariable=ev_def_var_left, values=[str(i) for i in range(31)], state='normal')
ev_def_menu_left.grid(row=9, column=1)
ev_def_menu_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))

ttk.Label(left_frame, text="IV DEF").grid(row=8, column=2)
iv_def_menu_left = ttk.Combobox(left_frame, textvariable=iv_def_var_left, values=[str(i) for i in range(101)], state='normal')
iv_def_menu_left.grid(row=9, column=2)
iv_def_menu_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))

ttk.Label(left_frame, text="PS_Bonus DEF").grid(row=8, column=3)
ps_bonus_def_entry_left = ttk.Entry(left_frame, textvariable=ps_bonus_def_var_left, validate="key", validatecommand=vcmd)
ps_bonus_def_entry_left.grid(row=9, column=3)

ttk.Label(left_frame, text="ATT").grid(row=10, column=0)
ttk.Label(left_frame, textvariable=att_var_left).grid(row=11, column=0)

ttk.Label(left_frame, text="EV ATT %").grid(row=10, column=1)
ev_att_menu_left = ttk.Combobox(left_frame, textvariable=ev_att_var_left, values=[str(i) for i in range(31)], state='normal')
ev_att_menu_left.grid(row=11, column=1)
ev_att_menu_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))

ttk.Label(left_frame, text="IV ATT").grid(row=10, column=2)
iv_att_menu_left = ttk.Combobox(left_frame, textvariable=iv_att_var_left, values=[str(i) for i in range(101)], state='normal')
iv_att_menu_left.grid(row=11, column=2)
iv_att_menu_left.bind("<<ComboboxSelected>>", lambda _: update_stats("left"))

ttk.Label(left_frame, text="PS_Bonus ATT").grid(row=10, column=3)
ps_bonus_att_entry_left = ttk.Entry(left_frame, textvariable=ps_bonus_att_var_left, validate="key", validatecommand=vcmd)
ps_bonus_att_entry_left.grid(row=11, column=3)

# Right panel
right_frame = ttk.Frame(app)
right_frame.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(right_frame, text="Pal Image").grid(row=0, column=0)
canvas_right = tk.Canvas(right_frame, width=100, height=100, bg="white")
canvas_right.grid(row=1, column=0)
pal_image_right = tk.PhotoImage(file=pal_images[pal_names[0]])
canvas_right.create_image(50, 50, image=pal_image_right)
canvas_right.image = pal_image_right

ttk.Label(right_frame, text="Pal Name").grid(row=2, column=0)
pal_name_combobox_right = ttk.Combobox(right_frame, textvariable=pal_name_var_right, values=pal_names, state='normal')
pal_name_combobox_right.grid(row=3, column=0, columnspan=2)
pal_name_combobox_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))
pal_name_combobox_right.bind('<KeyRelease>', lambda event: filter_combobox(event, pal_name_combobox_right, pal_names))

ttk.Label(right_frame, text="Stars").grid(row=2, column=3)
stars_menu_right = ttk.OptionMenu(right_frame, stars_var_right, "0", *[str(i) for i in range(5)], command=lambda _: update_stats("right"))
stars_menu_right.grid(row=3, column=3)

ttk.Label(right_frame, text="Lvl").grid(row=4, column=0)
lvl_menu_right = ttk.Combobox(right_frame, textvariable=lvl_var_right, values=[str(i) for i in range(101)], state='normal')
lvl_menu_right.grid(row=5, column=0)
lvl_menu_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))

ttk.Label(right_frame, text="HP").grid(row=6, column=0)
ttk.Label(right_frame, textvariable=hp_var_right).grid(row=7, column=0)

ttk.Label(right_frame, text="EV HP %").grid(row=6, column=1)
ev_hp_menu_right = ttk.Combobox(right_frame, textvariable=ev_hp_var_right, values=[str(i) for i in range(31)], state='normal')
ev_hp_menu_right.grid(row=7, column=1)
ev_hp_menu_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))

ttk.Label(right_frame, text="IV HP").grid(row=6, column=2)
iv_hp_menu_right = ttk.Combobox(right_frame, textvariable=iv_hp_var_right, values=[str(i) for i in range(101)], state='normal')
iv_hp_menu_right.grid(row=7, column=2)
iv_hp_menu_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))

ttk.Label(right_frame, text="PS_Bonus HP").grid(row=6, column=3)
ps_bonus_hp_entry_right = ttk.Entry(right_frame, textvariable=ps_bonus_hp_var_right, validate="key", validatecommand=vcmd)
ps_bonus_hp_entry_right.grid(row=7, column=3)

ttk.Label(right_frame, text="DEF").grid(row=8, column=0)
ttk.Label(right_frame, textvariable=def_var_right).grid(row=9, column=0)

ttk.Label(right_frame, text="EV DEF %").grid(row=8, column=1)
ev_def_menu_right = ttk.Combobox(right_frame, textvariable=ev_def_var_right, values=[str(i) for i in range(31)], state='normal')
ev_def_menu_right.grid(row=9, column=1)
ev_def_menu_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))

ttk.Label(right_frame, text="IV DEF").grid(row=8, column=2)
iv_def_menu_right = ttk.Combobox(right_frame, textvariable=iv_def_var_right, values=[str(i) for i in range(101)], state='normal')
iv_def_menu_right.grid(row=9, column=2)
iv_def_menu_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))

ttk.Label(right_frame, text="PS_Bonus DEF").grid(row=8, column=3)
ps_bonus_def_entry_right = ttk.Entry(right_frame, textvariable=ps_bonus_def_var_right, validate="key", validatecommand=vcmd)
ps_bonus_def_entry_right.grid(row=9, column=3)

ttk.Label(right_frame, text="ATT").grid(row=10, column=0)
ttk.Label(right_frame, textvariable=att_var_right).grid(row=11, column=0)

ttk.Label(right_frame, text="EV ATT %").grid(row=10, column=1)
ev_att_menu_right = ttk.Combobox(right_frame, textvariable=ev_att_var_right, values=[str(i) for i in range(31)], state='normal')
ev_att_menu_right.grid(row=11, column=1)
ev_att_menu_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))

ttk.Label(right_frame, text="IV ATT").grid(row=10, column=2)
iv_att_menu_right = ttk.Combobox(right_frame, textvariable=iv_att_var_right, values=[str(i) for i in range(101)], state='normal')
iv_att_menu_right.grid(row=11, column=2)
iv_att_menu_right.bind("<<ComboboxSelected>>", lambda _: update_stats("right"))

ttk.Label(right_frame, text="PS_Bonus ATT").grid(row=10, column=3)
ps_bonus_att_entry_right = ttk.Entry(right_frame, textvariable=ps_bonus_att_var_right, validate="key", validatecommand=vcmd)
ps_bonus_att_entry_right.grid(row=11, column=3)

# Move power and damage range
center_frame = ttk.Frame(app)
center_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

ttk.Label(center_frame, text="Move Power").grid(row=0, column=0)
move_power_var = tk.StringVar(value="0")
move_power_entry = ttk.Entry(center_frame, textvariable=move_power_var, validate="key", validatecommand=vcmd)
move_power_entry.grid(row=0, column=1)
move_power_entry.bind("<KeyRelease>", lambda _: update_damage_range())

ttk.Label(center_frame, text="Min Damage").grid(row=0, column=2)
min_damage_var = tk.StringVar(value="N/A")
ttk.Label(center_frame, textvariable=min_damage_var).grid(row=0, column=3)

ttk.Label(center_frame, text="Max Damage").grid(row=0, column=4)
max_damage_var = tk.StringVar(value="N/A")
ttk.Label(center_frame, textvariable=max_damage_var).grid(row=0, column=5)


# Add the checkbox on the left of move power
stab_checkbox = ttk.Checkbutton(center_frame, text="STAB", variable=stab_var, command=update_damage_range)
stab_checkbox.grid(row=1, column=0, padx=10, pady=10)




# Initialize stats
update_stats("left")
update_stats("right")

app.mainloop()






























