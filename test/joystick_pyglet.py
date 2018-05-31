import pyglet

window = pyglet.window.Window()

joysticks = pyglet.input.get_joysticks()

if joysticks:
    joystick = joysticks[0]
joystick.open()

@joystick.event
def on_joybutton_press(joystick, button):
    print('joystick', button)

@joystick.event
def on_joyaxis_motion(joystick, axis, value):
    print('joystick', joystick, axis, 'value', value * 40)

@window.event
def on_key_press(symbol, modifiers):
    print('A key was pressed', symbol)

@window.event
def on_draw():
    window.clear()

@window.event
def on_mouse_press(x, y, button, modifiers):
    print('The mouse button was pressed.')

print('Joysticks', joysticks)
pyglet.app.run()