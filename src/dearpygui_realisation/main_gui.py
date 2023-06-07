import dearpygui.dearpygui as dpg
from math import sin, cos, degrees, radians

from src.Calculation import perfect_trajectory, trajectory

dpg.create_context()

# all units in SI system
g = 9.81
bucket_r = 0.23
ball_r = 0.11
H = 3.05
h = 1.05
L = 6.25
human_height = 1.7
height = H + h

left_bucket = L - 2 * bucket_r
right_bucket = L

low_shield = H
high_shield = H + h

# format> [x0, x1], [y0, y1]
shield_line = [[L, L], [H, H + h]]
bucket_line = [[L - 2 * bucket_r, L], [H, H]]

v = 20
a = radians(30)
k = 0.3
time_step = 0.05

is_hidden = True

def bool_plot(sender):
    global is_hidden
    print((is_hidden))
    if dpg.get_value(sender) == True:
        is_hidden = False
    else:
        is_hidden = True

def update_trajectory_velocity(sender):
    global v,a,k,time_step
    v = dpg.get_value(sender)
    resolver = trajectory(human_height, v, radians(a), k, time_step)
    resolver.calculate()
    dpg.set_value('main_plot_tag', resolver.get_plot_data())
    # solver = perfect_trajectory(human_height, v, radians(a))
    # solver.calculate()
    # dpg.set_value('additional_plot_tag', solver.get_plot_data())

def update_trajectory_angle(sender):
    global v,a,k,time_step
    a = dpg.get_value(sender)
    resolver = trajectory(human_height, v, radians(a), k, time_step)
    resolver.calculate()
    dpg.set_value('main_plot_tag', resolver.get_plot_data())
    # solver = perfect_trajectory(human_height, v, radians(a))
    # solver.calculate()
    # dpg.set_value('additional_plot_tag', solver.get_plot_data())

def update_trajectory_air_resistance(sender):
    global v,a,k,time_step
    k = dpg.get_value(sender)
    resolver = trajectory(human_height, v, radians(a), k, time_step)
    resolver.calculate()
    dpg.set_value('main_plot_tag', resolver.get_plot_data())


def update_trajectory_time_step(sender):
    global v,a,k,time_step
    time_step = dpg.get_value(sender)
    resolver = trajectory(human_height, v, radians(a), k, float(time_step))
    resolver.calculate()
    dpg.set_value('main_plot_tag', resolver.get_plot_data())


with dpg.window(label="Bulding trajectories", tag="win"):

    slider_v = dpg.add_slider_float(label="v0",
                                    default_value=10,
                                    max_value=22,
                                    min_value=5,
                                    callback=update_trajectory_velocity)
    slider_angle = dpg.add_slider_float(label="angle, degrees",
                                        default_value=30,
                                        min_value=10,
                                        max_value=90,
                                        callback=update_trajectory_angle)
    slider_air = dpg.add_slider_float(label="air resistance k",
                                      min_value=0,
                                      default_value=1,
                                      max_value=1.5,
                                      callback=update_trajectory_air_resistance)
    slider_step = dpg.add_slider_float(label="time step",
                                       default_value=0.1,
                                       min_value=0.1,
                                       max_value=0.005,
                                       callback=update_trajectory_time_step)
    #TODO make a normal btn
    analysis_plot_show_btn = dpg.add_checkbox(label="show analysis", callback=bool_plot)
    dpg.set_item_callback(slider_v, update_trajectory_velocity)
    dpg.set_item_callback(slider_angle, update_trajectory_angle)
    dpg.set_item_callback(slider_air, update_trajectory_air_resistance)
    dpg.set_item_callback(slider_step, update_trajectory_time_step)


    print(dpg.get_value(slider_air))
    print(dpg.get_value(slider_v))
    print(dpg.get_value(slider_step))
    print(dpg.get_value(slider_angle))

    with dpg.plot(label="Line Series", height=700, width=800):
        # plt.plot([L, L], [H, H + h])
        # plt.plot([L - 2 * bucket_r, L], [H, H])
        # plt.plot([0, L], [0, 0], 'b')


        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")

        print(dpg.get_value(slider_air))
        print(dpg.get_value(slider_v))
        print(dpg.get_value(slider_step))
        print(dpg.get_value(slider_angle))



        solver_main = trajectory(human_height, v, radians(a), k, time_step)
        solver_main.calculate()
        x1, y1 = solver_main.get_plot_data()



        dpg.add_line_series([L, L], [H, H + h], label="meow", parent="y_axis" )
        dpg.add_line_series([L - 2 * bucket_r, L], [H, H], label="meow", parent="y_axis" )
        dpg.add_line_series([0, L], [0, 0], label="meow", parent="y_axis" )
        dpg.add_line_series(x1, y1,  parent="y_axis", tag="main_plot_tag")

        solver = perfect_trajectory(human_height, 5, radians(10))
        solver.calculate()
        x2, y2 = solver.get_plot_data()
        # dpg.add_line_series(x2, y2, parent="y_axis", tag="additional_plot_tag")
dpg.create_viewport(title='Main', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()