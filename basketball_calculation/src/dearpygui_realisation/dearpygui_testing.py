import dearpygui.dearpygui as dpg
from math import sin
dpg.create_context()




with dpg.window(label="Bulidng trajectories"):
    dpg.add_text("Choose variables")
    # dpg.add_button(label="Save")
    silder1 = dpg.add_slider_float(label="float", default_value=0.1, max_value=20)
    # create plot
    with dpg.plot(label="Line Series", height=700, width=800):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

        # series belong to a y axis
        dpg.add_line_series(sindatax, sindatay, label="0.5 + 0.5 * sin(x)", parent="y_axis")

dpg.create_viewport(title='Custom Title', width=900, height=1000)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()