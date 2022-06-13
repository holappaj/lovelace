import circuitry
import guilib as ui

state = {
    "textfield": None,
    "textbox": None,
    "circuit": None,
    "components": [],
    "voltage": 0,
    "frequency": 0,
}

def set_voltage():
    try:
        state["voltage"] = float(ui.read_field(state["textfield"]))
    except ValueError:
        ui.open_msg_window(
            "Errore",
            "Invalid value",
            error=True
        )
    else:
        ui.write_to_textbox(state["textbox"], "Voltage {:.1f} V".format(state["voltage"]))
    ui.clear_field(state["textfield"])

def set_frequency():
    try:
        state["frequency"] = float(ui.read_field(state["textfield"]))
    except ValueError:
        ui.open_msg_window(
            "Errore",
            "Invalid value",
            error=True
        )
    else:
        ui.write_to_textbox(state["textbox"], "Frequency {:.1f} V".format(state["frequency"]))
    ui.clear_field(state["textfield"])

def add_resistor():
    try:
        value = float(ui.read_field(state["textfield"]))
    except ValueError:
        ui.open_msg_window(
            "Errore",
            "Invalid value",
            error=True
        )
    else:
        state["components"].append(("r", value))
        circuitry.draw_voltage_source(state["circuit"], state["voltage"], state["frequency"])
        circuitry.draw_loop(state["circuit"], state["components"], 4, last=True)
        circuitry.draw_circuit(state["circuit"])
    ui.clear_field(state["textfield"])
    
def main():
    window = ui.create_window("test window")
    left_f = ui.create_frame(window, ui.LEFT)
    right_f = ui.create_frame(window, ui.LEFT)
    ui.create_label(left_f, "value:")
    state["textfield"] = ui.create_textfield(left_f)
    ui.create_button(left_f, "set voltage", set_voltage)
    ui.create_button(left_f, "set frequency", set_frequency)
    ui.create_button(left_f, "add resistor", add_resistor)
    ui.create_button(left_f, "quit", ui.quit)
    state["textbox"] = ui.create_textbox(left_f, 20, 40)    
    state["circuit"] = circuitry.create_circuit(right_f, 600, 600, 10)
    ui.start()
    
if __name__ == "__main__":
    main()