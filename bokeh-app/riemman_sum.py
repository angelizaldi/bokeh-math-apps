from bokeh.plotting import figure
from bokeh.io import save
from bokeh.layouts import column
import numpy as np
from bokeh.models import Div, ColumnDataSource, Slider, CustomJS, Arrow, NormalHead, Label

BLUE = "#30ADB9"
BLACK = "#000000"
GRAY = "#7b7d7d"

# Título
titulo = Div(text="""<h1 style="text-align: center; font-family: Sans-serif, Serif; font-weight: 300;
                    text-decoration-line: underline; text-decoration-color: #30ADB9"> 
                    Suma de Riemann </h1>""")

# Texto
texto = Div(text=r"""El área real bajo la curva es: <b>6</b>""", width=600)
area = Div(text="El área aproximada es: <b>6.31</b>", width=600)
# Figura

dominio = (-.5, 5)
rango = (-.5, 3)

fig = figure(x_range=dominio, y_range=rango, tools="", toolbar_location=None,
   match_aspect=True, height=500, width=800)
fig.xaxis.visible = False
fig.yaxis.visible = False
fig.grid.grid_line_color = None

nh = NormalHead(fill_color=BLACK, size=10)
eje_x = Arrow(end=nh, x_start=dominio[0], y_start=0, x_end=dominio[1], y_end=0, 
           line_color=BLACK)
eje_y = Arrow(end=nh, x_start=0, y_start=rango[0], x_end=0, y_end=rango[1], 
         line_color=BLACK)

etq_y = Label(text="y", x=0.15, y=rango[1]*.93, x_units="data", y_units="data", 
              text_font_style="italic", text_font="times")
etq_x = Label(text=r"x", x=dominio[1]*.97, y=0.15, x_units="data", y_units="data", 
              text_font_style="italic", text_font="times")

fig.add_layout(eje_x)
fig.add_layout(eje_y)
fig.add_layout(etq_y)
fig.add_layout(etq_x)


# Grafica:

x = np.linspace(1, 4, 200)
y = .3*np.sin(2*(x+.3))+2

source_line = ColumnDataSource(data=dict(x=x, y=y))

xaxis_min=x[0]
xaxis_max=x[-1]
yaxis_min=y[0]
yaxis_max=y[-1]

# Boxes 

#mini = Span(dimension="height", location=1, line_dash="dashed")
#maxi = Span(dimension="height", location=-1, line_dash="dashed")

boxes=5

ranges=[0]
long = (200)/boxes
lefts = []
rights = []
tops = []

for end in range(boxes):
    ranges.append(int((end+1)*long))

    max_values=[]
for i in range(len(ranges)-1):
    max_values.append(max(y[ranges[i]:ranges[i+1]]))
    
for i in range(len(ranges)-1):
    lefts.append(x[ranges[i]])
    rights.append(x[ranges[i+1]-1])
    tops.append(max_values[i])

source_boxes = ColumnDataSource(data=dict(tops=tops, 
                                          bottoms=[0]*len(tops), 
                                          lefts=lefts, 
                                          rights=rights))

fig.quad(top="tops", bottom="bottoms", left="lefts",
       right="rights", color=BLUE, fill_alpha=0.4, source=source_boxes)


fig.line("x", "y", color=BLACK, line_width=2, source=source_line)
fig.line([xaxis_min, xaxis_min], [0, yaxis_min], color=GRAY, line_width=1, line_dash="dashed")
fig.line([xaxis_max, xaxis_max], [0, yaxis_max], color=GRAY, line_width=1, line_dash="dashed")

slider = Slider(start=1, end=30, value=5, step=1, title="Valor de n")

Callback = CustomJS(args=dict(slider=slider, source_boxes=source_boxes,
                             source_line=source_line, area=area),
                    code="""
    const boxes = slider.value
    const y = source_line.data.y
    const x = source_line.data.x
    const rango = 3/boxes 

    const ranges = [0];
    const long = 200 / boxes;

    for (let end = 0; end < boxes; end++) {
        ranges.push(Math.floor((end + 1) * long));
    }

    const maxValues = [];
    for (let i = 0; i < ranges.length - 1; i++) {
        maxValues.push(Math.max(...y.slice(ranges[i], ranges[i + 1])));
    }

    let sum = maxValues.map(maxValues => maxValues * rango).reduce((acc, val) => acc + val);

    const lefts = [];
    const rights = [];
    const tops = [];
    for (let i = 0; i < ranges.length - 1; i++) {
        lefts.push(x[ranges[i]]);
        rights.push(x[ranges[i + 1] - 1]);
        tops.push(maxValues[i]);
    }

    const bottoms = new Array(tops.length).fill(0);
    area.text = `El área aproximada es: <b>${sum.toFixed(2)}</b>`
    source_boxes.data = { tops, bottoms, lefts, rights }
""")

slider.js_on_change("value", Callback)


save(column(titulo, fig, slider, texto, area), "./riemman_sum.html")