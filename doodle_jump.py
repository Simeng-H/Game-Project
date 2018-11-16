# Written by Simeng Hao (sh4aj) and Derek Habron (hjb5ek)

import gamebox
camera = gamebox.Camera(400,600)

# Key attributes


# Definitions
user = gamebox.from_color(200, 550, "brown", 20, 20)


# Mainloop
def tick(keys):
    camera.clear("white")

    camera.draw(user)
    camera.display()

# Initiation
gamebox.timer_loop(60,tick)