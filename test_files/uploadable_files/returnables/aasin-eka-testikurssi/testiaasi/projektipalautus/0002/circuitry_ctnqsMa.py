"""
circuitry - simple RLC circuit extension for guilib

@author Mika Oja, University of Oulu

This library is an extension to guilib - a simple user interface library. It
includes a new widget for (limited) circuit diagram drawing. Contains functions
for creating a circuit diagram and drawing to it. A simple example can be found
at the end of this file.

Uses the SchemDraw library:

https://cdelker.bitbucket.io/SchemDraw/SchemDraw.html

and SchemCanvas extension, which adds support for drawing to an embedded canvas
instead of a separate window. The extension file must be placed into the same
folder with this module and the rest of your program.
"""

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from tkinter import *
from tkinter.ttk import *

import SchemDraw as scm
import SchemDraw.elements as e
from SchemCanvas import CanvasDrawing
from SchemCanvas import CanvasDrawing, CanvasFigure

canvas_frame = {
    "figure": None,
    "canvas": None,
    "axes": None,
}

def _draw_component(circuit, component, value, length_unit):
    """
    Draws one component of the circuit to the drawing cursor's current position
    and updates the cursor position. The function is intended for the library's
    internal use. You will not need it unless you want to rewrite the circuit
    layout algorithm.
    
    :param str component: component type (R, L, or C)
    :param str value: component's value, can include prefix unit
    :param float length_unit: length factor used in layouting
    """
    
    if component[0].lower() == "r":
        circuit.add(e.RES, d="down", label="{}$\Omega$".format(value), l=3*length_unit)
    elif component[0].lower() == "c":
        circuit.add(e.CAP, d="down", label="{}F".format(value), l=3*length_unit)
    elif component[0].lower() == "l":
        circuit.add(e.INDUCTOR2, d="down", label="{}H".format(value), l=3*length_unit)

def _draw_odd_parallel(circuit, components, length_unit):
    """
    Draws a parallel connection with an odd number of components. It is drawn
    to the cursor's current position, and the cursor's position is updated
    after drawing. The function is intended for the library's internal use. You
    will not need it unless you want to rewrite the circuit layout algorithm.
    
    Draws components outward from the middle line to both directions.
    
    :param object circuit: circuit object to draw to
    :param list components: list of parallel connection components
    :param float length_unit: length factor used in layouting
    """
    
    # components are separated to two sides and the single middle component
    middle = len(components) // 2
    left = components[:middle]
    right = components[middle+1:]
    circuit.add(e.DOT)
    
    # save the middle line's cursor position
    circuit.push()
    
    # drawing left side components
    for i, comp in enumerate(left[::-1]):
        circuit.add(e.LINE, d="left", l=1)
        
        # the leftmost line doesn't have a connector dot
        if i != len(left) - 1:
            circuit.add(e.DOT)
            
        # saving the cursor position, drawing one component and connect it
        # to the previous one or the middle line
        circuit.push()
        _draw_component(circuit, comp[0], comp[1], length_unit)
        if i != len(left) - 1:
            circuit.add(e.DOT)
        circuit.add(e.LINE, d="right", l=1)
        
        # restore the cursor for the next component
        circuit.pop()
    
    # restore the cursor to the middle line
    circuit.pop()    
    circuit.push()
    
    # drawing right side components
    for i, comp in enumerate(right):
        circuit.add(e.LINE, d="right", l=1)
        
        # the rightmost line doesn't have a connector dot
        if i != len(right) - 1:
            circuit.add(e.DOT)
                        
        # saving the cursor position, drawing one component and connect it
        # to the previous one or the middle line
        circuit.push()
        _draw_component(circuit, comp[0], comp[1], length_unit)
        if i != len(right) - 1:
            circuit.add(e.DOT)
        circuit.add(e.LINE, d="left", l=1)
        circuit.pop()

    # restore the cursor to the middle line and draw the middle component
    circuit.pop()
    _draw_component(circuit, components[middle][0], components[middle][1], length_unit)
    circuit.add(e.DOT)
    

def _draw_even_parallel(circuit, components, length_unit):
    """
    Draws a parallel connection with an even number of components. It is drawn
    to the cursor's current position, and the cursor's position is updated
    after drawing. The function is intended for the library's internal use. You
    will not need it unless you want to rewrite the circuit layout algorithm.
    
    Draws components outward from the middle line to both directions. The
    middle line itself is not drawn.
    
    :param object circuit: circuit object to draw to
    :param list components: list of parallel connection components
    :param float length_unit: length factor used in layouting
    """
    
    # components are separated to two halves
    middle = len(components) // 2
    left = components[:middle]
    right = components[middle:]
    circuit.add(e.DOT)
    
    # middle line cursor position is saved
    circuit.push()
    
    # drawing left side components
    for i, comp in enumerate(left[::-1]):
        
        # the first connector is shorter by half
        if i == 0:            
            circuit.add(e.LINE, d="left", l=0.5)
        else:
            circuit.add(e.LINE, d="left", l=1)
            
        # the leftmost connector doesn't have a dot            
        if i != len(left) - 1:
            circuit.add(e.DOT)
        
        # saving the cursor position, drawing one component and connect it
        # to the previous one or the middle line
        circuit.push()
        _draw_component(circuit, comp[0], comp[1], length_unit)
        if i != len(left) - 1:
            circuit.add(e.DOT)

        if i == 0:
            circuit.add(e.LINE, d="right", l=0.5)
        else:            
            circuit.add(e.LINE, d="right", l=1)
            
        # cursor position is restored to draw the next component
        circuit.pop()
        
    # cursor position is returned to the middle
    circuit.pop()
    
    # drawing right side components
    for i, comp in enumerate(right):

        # the first connector is shorter by half
        if i == 0:
            circuit.add(e.LINE, d="right", l=0.5)
        else:
            circuit.add(e.LINE, d="right", l=1)

        # the leftmost connector doesn't have a dot
        if i != len(right) - 1:
            circuit.add(e.DOT)

        # saving the cursor position, drawing one component and connect it
        # to the previous one or the middle line
        circuit.push()
        _draw_component(circuit, comp[0], comp[1], length_unit)
        if i != len(right) - 1:
            circuit.add(e.DOT)
        if i == 0:
            circuit.add(e.LINE, d="left", l=0.5)
            
            # the position where the right side connects back to the middle
            # is saved separately
            circuit._state.insert(-1, (circuit.here, circuit.theta))
        else:
            circuit.add(e.LINE, d="left", l=1)

        # cursor position is restored to draw the next component
        circuit.pop()
    
    # cursor position is returned to the middle
    circuit.pop()
    circuit.add(e.DOT)

def create_circuit(frame, width=600, height=400, font_size=16):
    """
    Creates a circuit diagram, and the associated matplotlib figure, axes, and
    canvas in a panel inside the UI window. Fixed width and height are set for
    the canvas by giving the corresponding arguments. The circuit diagram will
    scale based on the canvas size but text does not. You can set the font
    size separately with another argument. Returns a circuit object that is
    needed later for drawing loops ands components.
    
    :param object frame: frame to host the circuit canvas
    :param int width: canvas width as pixels
    :param int height: canvas height as pixels
    :param int font_size: font size as points
    
    :return: circuit diagram object
    """
    
    circuit = CanvasDrawing(fontsize=font_size)
    basefigure = Figure(figsize=(width / 100, height / 100), dpi=100)
    axes = basefigure.add_axes((0.0, 0.0, 1.0, 1.0))
    axes.axis("equal")
    canvas = FigureCanvasTkAgg(basefigure, master=frame)
    canvas.get_tk_widget().pack(side=TOP)
    figure = CanvasFigure(basefigure, axes)
    canvas_frame["figure"] = figure
    canvas_frame["axes"] = axes
    canvas_frame["canvas"] = canvas
    return circuit


def clear_circuit(circuit):
    """
    Clears the previous circuit diagram from the canvas. Must be used before
    drawing a new one.
    
    :param object circuit: circuit object to clear
    """
    
    circuit.clear()
    canvas_frame["axes"].clear()

def draw_circuit(circuit):
    """
    Draws the circuit on the canvas (i.e. makes it actually visible)
    
    :param object circuit: circuit to draw
    """
    
    circuit.draw(canvas_frame["canvas"], canvas_frame["figure"], canvas_frame["axes"])        

def draw_voltage_source(circuit, voltage, frequency, v_interval=2):
    """
    Draws the circuit's voltage source. Because the library has been optimized
    for the course project, adding more than one source will result in weird
    diagrams. Both voltage and frequency are given as strings so they can
    include prefix units. Their unit symbols are added by the library. 
    
    The default value of 2 usually works well for v_interval but if you don't
    like the way your circuit looks vertically, you can try to adjust this
    value.
    
    :param object circuit: circuit object that is being drawn
    :param str voltage: source voltage as string
    :param str frequency: source frequency as string
    :param float v_interval: factor related to circuit layout
    """
    
    circuit.clear()
    canvas_frame["axes"].clear()
    circuit.add(e.LINE, d="right", l=0.5, move_cur=False)
    circuit.add(e.SOURCE_V, label="{}V\n{}Hz".format(voltage, frequency), reverse=True, l=6*v_interval)    
    circuit.add(e.LINE, d="right", l=0.5)
    
def draw_loop(circuit, components, h_interval, v_interval=2, last=False):
    """
    Draws one loop (branch) with all its components and parallel connections.
    Components must be given as a list where each individual component is a
    tuple containing at least two values: the componen's type ("r", "c", "l")
    and the component's value as a string. Parallel connections must be
    included as lists that contain components (as previously described tuples).
    A simple example with three resistors, two of which are in parallel
    connection:
    
    loop = [("r", "100"), [("r", "100"), ("r", "100")]]
    
    The v_interval parameter affects vertical placement of components (the
    default is usually ok). The h_interval defines how much empty space is left
    on both sides of the loop in the diagram. The circuit draws quite well if
    this value is set equal to the number of components in the biggest parallel
    connection in the loop.
    
    The last parameter indicates whether this is the last loop in the diagram.
    If it's not set, connectors for another loop will be drawn.
    
    :param object circuit: circuit object that is being drawn
    :param list components: list of components
    :param int h_interval: factor for horizontal placement
    :param float v_interval: factor for vertical placement
    :param bool last: is this the last loop
    """
    
    circuit.pop()
    circuit.add(e.LINE, d="right", l=h_interval/2)
    if not last:
        circuit.push()        
        circuit.add(e.DOT)
        circuit.add(e.LINE, d="right", l=h_interval/2)
        circuit._state.insert(-1, (circuit.here, circuit.theta))
        circuit.pop() 
        
    parallels = sum([1 for k in components if isinstance(k, list)])
    if isinstance(components[0], list) and isinstance(components[-1], list):
        terminator = True
        length_unit = v_interval / (len(components) + 2) * 2  
        circuit.add(e.LINE, d="down", l=3*length_unit)
    elif isinstance(components[0], list):
        terminator = False
        length_unit = v_interval / (len(components) + 1) * 2  
        circuit.add(e.LINE, d="down", l=3*length_unit)
    elif isinstance(components[-1], list):
        terminator = True
        length_unit = v_interval / (len(components) + 1) * 2  
    else:
        terminator = False
        length_unit = v_interval / len(components) * 2  
    for component in components:
        if isinstance(component, list):
            if len(component) % 2 == 0:
                _draw_even_parallel(circuit, component, length_unit)
            else:
                _draw_odd_parallel(circuit, component, length_unit)
        else:
            _draw_component(circuit, component[0], component[1], length_unit)
    
    if terminator:
        circuit.add(e.LINE, d="down", l=3*length_unit)
    
    if not last:
        circuit.add(e.DOT)
        circuit.add(e.LINE, d="right", l=h_interval/2, move_cur=False)
        
    circuit.add(e.LINE, d="left", l=h_interval/2)


if __name__ == "__main__":
    import guilib as ui
    
    def draw_test_circuit():
        loop = [[("r", 100), ("r", 100)], ("r", 200), [("r", 100), ("r", 100), ("r", 100)]]
        draw_voltage_source(circuit, 10, "10k", 2)
        draw_loop(circuit, loop, 3, 2, last=True)
        loop = [("c", "1.0n")]
        #draw_loop(circuit, loop, 1, 2, last=True)
        draw_circuit(circuit)
        
        
    window = ui.create_window("much circuit")
    frame = ui.create_frame(window, TOP)
    ui.create_button(frame, "TEST", draw_test_circuit)
    ui.create_button(frame, "QUIT", ui.quit)
    circuit = create_circuit(frame, 600, 600, 10)
    ui.start()