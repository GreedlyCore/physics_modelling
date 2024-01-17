from bokeh.plotting import figure, show
from bokeh.models import Div, RangeSlider, Spinner
from random import randint
x = [i for i in range(50)]
y = [randint(1,i) for i in range(1,50)]

p = figure(title="Example of bokeh", x_axis_label='x', y_axis_label='y', x_range=(1,9),widt=500, height=250)
points = p.circle(x=x,y=y, size=30)

div = Div(
    text = """
        <p>Select circle's size</p>
    """,
    width = 200,
    height = 30
)

spinner = Spinner(title="Circle size",
                  low = 0,
                  high=60,
                  step = 2,
                  value=points.glyph.size, # the initial value, our 30
                  width=200,
                  )
spinner.js_link("value", points.glyph, "size")

range_slider = RangeSlider(
    title="Adjust x-axis range",

)

p.line(x,y,legend_label="Temp.",color='red', line_width=2)
show(p)

# p = figure(title="Example of bokeh", x_axis_label='x', y_axis_label='y')
# p.line(x,y,legend_label="Temp.",color='red', line_width=2)
# show(p)