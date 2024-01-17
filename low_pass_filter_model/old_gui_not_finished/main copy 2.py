import dearpygui.dearpygui as dpg
import numpy as np
from calculate import signal
import matplotlib.pyplot as plt

dpg.create_context()
# stands for time grid - time step
b = 3
t = np.linspace(0, b, b*1000) * 10**-5
# Frequency, Hz
f = 1 * 10**3
# omega = 2 * np.pi * f
# # E0 - input voltage in V
E0 = 5
# Резистор в фильтре, Ом
r = 20*1000
# Нагрузка, внешняя, Ом
R = 30*1000
# # Ёмкость конденсатора, наноФарады
C = 10*(10**(-9))
# counter for plotting
l = 0

form = "sin wave"

cutoff_freq = 1/(2*np.pi*r*C)

solver = signal(form, C,R,r, E0,f,t)



def update_E0(sender):
    global E0, solver
    E0 = round(dpg.get_value(sender),1)
    solver.set_E0(E0)

def update_f(sender):
    global f, solver
    f = 1000*round(dpg.get_value(sender),1)
    solver.set_f(f)

def update_end_time(sender):
    global t, solver
    end_time = dpg.get_value(sender)
    t = np.linspace(0, end_time, 1+round(end_time*1000))
    solver.set_t(t)

def update_C(sender):
    global C, solver
    C = (10**-9) * round(dpg.get_value(sender),1)
    solver.set_C(C)
    dpg.set_value('cutoff_freq_tag', f"Cut off frequency: {1/(2*np.pi*r*C)} Hz")

def update_R(sender):
    global R, solver
    R = round(dpg.get_value(sender),1) * 1000
    solver.set_R(R)

def update_r(sender):
    global r, solver
    r = round(dpg.get_value(sender),1)  * 1000
    solver.set_r(r)

    dpg.set_value('cutoff_freq_tag', f"Cut off frequency: {1/(2*np.pi*r*C)}")

def update_combo_select(sender, app_data, user_data):
        solver.set_form(app_data)


def update_button(sender, app_data, user_data):
    global l, solver
    solver.calculate_in()
    solver.calculate_out()
    print(solver.get_Out_plot_data())
    solver.calculate_final()
    dpg.set_value('in_signal_plot_tag', solver.get_Final_plot_data())
    dpg.set_value('in_signal_plot_tag2', solver.get_In_plot_data())
    dpg.set_value('out_signal_plot_tag2', solver.get_Out_plot_data())

    print(f"Finished plotting!! id: {l} \n \
          Btw, now we have: ...")

          
    print(f"E0: {E0}")
    print(f"f: {f}")
    print(f"r: {r}")
    print(f"R: {R}")
    print(f"C: {C}")
    l +=1

solver.set_C(47*10**-5)
solver.set_E0(10)
solver.set_f(1400)
solver.set_R(10**5)
solver.set_r(8*10**4)
solver.set_t(np.linspace(0, 10, 1+round(10*1000)))

solver.calculate_in()
solver.calculate_out()
solver.calculate_final()

x1, y1 = solver.get_In_plot_data()
x2, y2 = solver.get_Out_plot_data()
x3,y3 = solver.get_Final_plot_data()



with dpg.window(label="Setup input signal and scheme", tag="in_signal"):

    with dpg.group():
        dpg.add_text(f'Cut off frequincy: {1/(2*np.pi*R*C)}', tag='cutoff_freq_tag')
        
    with dpg.group(horizontal=True):
        dpg.add_button(label="Confirm", callback=update_button)

    combo_select_signal = dpg.add_combo(label="combo",
                                        items=("sin wave", 
                                               "half wave", 
                                               "full wave"),                           
                                        default_value="sin wave", 
                                        callback=update_combo_select)

    slider_E0 = dpg.add_slider_float(label="Amplitude, V",
                                    default_value=5,
                                    max_value=10,
                                    min_value=0,
                                    callback=update_E0)
    slider_freq = dpg.add_slider_float(label="f, kHz",
                                        default_value=1,
                                        min_value=0.2,
                                        max_value=4,
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
                                    min_value=0.1,
                                    default_value=2,
                                    max_value=20,
                                    callback=update_R)
    
    dpg.set_item_callback(slider_E0, update_E0)
    dpg.set_item_callback(slider_freq, update_f)
    dpg.set_item_callback(slider_time, update_end_time)
    dpg.set_item_callback(slider_C, update_C)
    dpg.set_item_callback(slider_r, update_r)
    dpg.set_item_callback(slider_R, update_R)
    

    with dpg.plot(label="Line Series", height=700, width=800):
        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis1")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis1")
        # dpg.add_line_series(x4, y4,  parent="y_axis1", tag="in_signal_plot_tag")
        dpg.add_line_series(x3, y3,  parent="y_axis1", tag="in_signal_plot_tag")

# 2nd window - in & out signals together
with dpg.window(label="Final output - two signals", tag="in_out_signals"):

    with dpg.plot(label="Line Series", height=700, width=800) as plot_id:
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis3")
        with dpg.plot_axis(dpg.mvYAxis, label="y", tag="y_axis3"):
            
            dpg.add_line_series(x1, y1, parent="y_axis3",label="input signal", tag="in_signal_plot_tag2")
            dpg.add_line_series(x2, y2, parent="y_axis3", label="output signal", tag="out_signal_plot_tag2")

                        


dpg.create_viewport(title='Circuit sim', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()