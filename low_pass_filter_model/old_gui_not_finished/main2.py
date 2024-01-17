import dearpygui.dearpygui as dpg
from math import sin, cos, degrees, radians
import numpy as np
from calculate import signal, out_signal_calc

dpg.create_context()
# stands for time grid - time step
b = 5
t = np.linspace(0, b, b*100)
# Frequency, Hz
f = 1.6 * 10**3
# omega = 2 * np.pi * f
# # E0 - input voltage in V
E0 = 10
# Резистор в фильтре, Ом
r = 1000
# Нагрузка, внешняя, Ом
R = 10000
# # Ёмкость конденсатора, Фарады
C = 10*-9

cutoff_freq = 1/(2*np.pi*r*C)

def update_E0(sender):
    global E0,f,r,R, t, C
    E0 = dpg.get_value(sender)
    resolver_in = signal(E0,f,t)
    resolver_out = out_signal_calc(C,R,r, E0,f,t)
    
    dpg.set_value('in_signal_plot_tag', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag', resolver_out)
    dpg.set_value('in_signal_plot_tag2', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag2', resolver_out)

def update_f(sender):
    global E0,f,r,R, t, C
    f = dpg.get_value(sender)
    resolver_in = signal(E0,f,t)
    resolver_out = out_signal_calc(C,R,r, E0,f,t)
    
    dpg.set_value('in_signal_plot_tag', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag', resolver_out)
    dpg.set_value('in_signal_plot_tag2', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag2', resolver_out)

def update_end_time(sender):
    global E0,f,r,R, t, C
    end_time = dpg.get_value(sender)
    t_new = np.linspace(0, end_time, 1+round(end_time*50))
    resolver_in = signal(E0,f,t_new)
    resolver_out = out_signal_calc(C,R,r, E0,f,t_new)
    
    dpg.set_value('in_signal_plot_tag', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag', resolver_out)
    dpg.set_value('in_signal_plot_tag2', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag2', resolver_out)

def update_C(sender):
    global E0,f,r,R, t, C
    C = (10**-9) * dpg.get_value(sender)

    resolver_in = signal(E0,f,t)
    resolver_out = out_signal_calc(C,R,r, E0,f,t)
    
    dpg.set_value('in_signal_plot_tag', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag', resolver_out)
    dpg.set_value('in_signal_plot_tag2', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag2', resolver_out)
    dpg.set_value('cutoff_freq_tag', f"Cut off frequency: {1/(2*np.pi*r*C)} Hz")

def update_R(sender):
    global E0,f,r,R, t, C
    R = (10**3) * dpg.get_value(sender)

    resolver_in = signal(E0,f,t)
    resolver_out = out_signal_calc(C,R,r, E0,f,t)
    
    dpg.set_value('in_signal_plot_tag', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag', resolver_out)
    dpg.set_value('in_signal_plot_tag2', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag2', resolver_out)

def update_r(sender):
    global E0,f,r,R, t, C, cutoff_freq
    r = (10**3) * dpg.get_value(sender)

    resolver_in = signal(E0,f,t)
    resolver_out = out_signal_calc(C,R,r, E0,f,t)
    
    dpg.set_value('in_signal_plot_tag', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag', resolver_out)
    dpg.set_value('in_signal_plot_tag2', resolver_in.get_plot_data())
    dpg.set_value('out_signal_plot_tag2', resolver_out)
    dpg.set_value('cutoff_freq_tag', f"Cut off frequency: {1/(2*np.pi*r*C)}")

def update_combo_select(sender, app_data, user_data):
    print(f"sender: {sender}, \t app_data: {app_data}, \t user_data: {user_data}")
    # if


solver_in = signal(E0,f,t)
solver_out = out_signal_calc(C,R,r, E0,f,t)
x1, y1 = solver_in.get_plot_data()
x2, y2 = solver_out # solver_out.get_out_signal_plot_data()

with dpg.window(label="Setup input signal and scheme", tag="in_signal"):

    with dpg.group():
        dpg.add_text(f'Cut off frequincy: {1/(2*np.pi*R*C)}', tag='cutoff_freq_tag')
        with dpg.group(horizontal=True):
            dpg.add_text("The code for the most recent version of this demo can be found here:")

    combo_select_signal = dpg.add_combo(label="combo",
                                        items=("common sin", 
                                               "two peroids", 
                                               "three",
                                               "DDDD"),                           
                                        default_value="common sin", 
                                        callback=update_combo_select)

    slider_E0 = dpg.add_slider_float(label="E0",
                                    default_value=5,
                                    max_value=10,
                                    min_value=0,
                                    callback=update_E0)
    slider_freq = dpg.add_slider_float(label="f, kHz",
                                        default_value=5,
                                        min_value=1,
                                        max_value=100,
                                        callback=update_f)
    slider_time = dpg.add_slider_float(label="end time, seconds",
                                      min_value=1,
                                      default_value=3,
                                      max_value=10,
                                      callback=update_end_time)
    slider_C = dpg.add_slider_float(label="Capacity, nano farads",
                                    min_value=1,
                                    default_value=10,
                                    max_value=100,
                                    callback=update_C)
    slider_r = dpg.add_slider_float(label="Resistance - inner, kOhms",
                                    min_value=1,
                                    default_value=2,
                                    max_value=20,
                                    callback=update_r)
    slider_R = dpg.add_slider_float(label="Resistance - outer, kOhms",
                                    min_value=1,
                                    default_value=2,
                                    max_value=20,
                                    callback=update_R)
    
    dpg.set_item_callback(slider_E0, update_E0)
    dpg.set_item_callback(slider_freq, update_f)
    dpg.set_item_callback(slider_time, update_end_time)
    dpg.set_item_callback(slider_C, update_C)
    dpg.set_item_callback(slider_r, update_r)
    dpg.set_item_callback(slider_R, update_R)
    

    print(dpg.get_value(slider_E0))
    print(dpg.get_value(slider_freq))
    print(dpg.get_value(slider_time))

    with dpg.plot(label="Line Series", height=700, width=800):

        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis1")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis1")

        print(dpg.get_value(slider_E0))
        print(dpg.get_value(slider_freq))
        print(dpg.get_value(slider_time))

        dpg.add_line_series(x1, y1,  parent="y_axis1", tag="in_signal_plot_tag")

with dpg.window(label="Setup output signal", tag="out_signal"):
    with dpg.plot(label="Line Series", height=700, width=800) as plot_id:

        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis2")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis2")

        dpg.add_line_series(x2, y2,  parent="y_axis2", tag="out_signal_plot_tag")

# 3rd window - in & out signals together
with dpg.window(label="Final output - two signals", tag="in_out_signals"):
    with dpg.plot(label="Line Series", height=700, width=800) as plot_id:

        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis3")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis3")

        dpg.add_line_series(x1, y1, parent="y_axis3",label="input signal", tag="in_signal_plot_tag2")
        dpg.add_line_series(x2, y2, parent="y_axis3", label="output signal", tag="out_signal_plot_tag2")



dpg.create_viewport(title='Circuit sim', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()