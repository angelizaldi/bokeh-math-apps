from bokeh.models import Div, ColumnDataSource, Slider, CustomJS, Arrow, NormalHead
from bokeh.plotting import figure
from bokeh.io import save
from bokeh.layouts import row, column
import numpy as np

BLUE = "#30ADB9"
BROWN = "#BA6A30"
BLACK = "#000000"
GRAY = "#b2babb"


# Título
titulo = Div(text="""<h1 style="text-align: center; font-family: Sans-serif, Serif; font-weight: 300;
                    text-decoration-line: underline; text-decoration-color: #30ADB9"> 
                    Círculo trigonométrico </h1>""")

angulos = np.linspace(0, 2*np.pi, 200)

x = np.cos(angulos)
y = np.sin(angulos)


# Primer grafica

angulo_inicial = np.pi/4

source_tangente = ColumnDataSource(
    data=dict(x_tan=[np.cos(angulo_inicial)], y_tan=[np.sin(angulo_inicial)]))
source_coseno = ColumnDataSource(data=dict(x_cos=[np.cos(angulo_inicial)]))
source_seno = ColumnDataSource(data=dict(y_sin=[np.sin(angulo_inicial)]))

source_circulo = ColumnDataSource(data=dict(x=x, y=y))

fig = figure(x_range=(-1.3, 1.3), y_range=(-1.3, 1.3), tools="", toolbar_location=None,
             match_aspect=True, height=350, width=350)
fig.line("x", "y", source=source_circulo, line_color=GRAY, line_width=2)
fig.xaxis.fixed_location = 0
fig.yaxis.fixed_location = 0
fig.aspect_ratio = 1

fig.xaxis.ticker = [-1.1, 1.1]
fig.yaxis.ticker = [-1.1, 1.1]

fig.xaxis.major_label_overrides = {-1.1: "-1", 1.1: "1"}
fig.yaxis.major_label_overrides = {-1.1: "-1", 1.1: "1"}

fig.xaxis.major_tick_out = 0
fig.yaxis.major_tick_out = 0

fig.xaxis.major_tick_in = 0
fig.yaxis.major_tick_in = 0

# Vectores

coseno = Arrow(end=None, x_start=0, y_start=0, x_end="x_cos", y_end=0,
               line_color=BLUE, line_width=3, source=source_coseno)
seno = Arrow(end=None, x_start=0, y_start=0, x_end=0, y_end="y_sin",
             line_color=BROWN, line_width=3, source=source_seno)

head = NormalHead(size=7, fill_color=BLACK)

tangente = Arrow(end=None, x_start=0, y_start=0, x_end="x_tan", y_end="y_tan",
                 line_color=GRAY, line_width=3, source=source_tangente)

fig.add_layout(coseno)
fig.add_layout(seno)
fig.add_layout(tangente)

# Segunda grafica

x_graph = np.linspace(0, angulo_inicial, 200)
sin = np.sin(x_graph)
cos = np.cos(x_graph)

source_sin = ColumnDataSource(data=dict(x_graph=x_graph, sin=sin))
source_cos = ColumnDataSource(data=dict(x_graph=x_graph, cos=cos))

fig_2 = figure(x_range=(0, 2*np.pi), y_range=(-1.2, 1.2), tools="", toolbar_location=None,
               match_aspect=False, height=350, width=560)

fig_2.line("x_graph", "cos", source=source_cos, line_color=BLUE, line_width=2,
           legend_label=r"cos(x)")
fig_2.line("x_graph", "sin", source=source_sin, line_color=BROWN, line_width=2,
           legend_label=r"sin(x)")

fig_2.legend.location = "bottom_left"
fig_2.legend.label_text_font = "times"
# Ejes
fig_2.yaxis.ticker = [-1, 0, 1]

fig_2.xaxis.ticker = [0, np.pi/2,  np.pi, 3*np.pi/2, np.pi*2]
fig_2.xaxis.major_label_overrides = {
    0: "0",
    np.pi/2: r"$$\frac{\pi}{2}$$",
    np.pi: r"$$\pi$$",
    3*np.pi/2: r"$$\frac{3\pi}{2}$$",
    np.pi*2: r"$$2\pi$$",
}

# Slider

slider = Slider(title="Ángulo", start=0, end=360, step=1, value=45, width=350)

Callback = CustomJS(args=dict(slider=slider, source_tangente=source_tangente,
                              source_coseno=source_coseno, source_seno=source_seno,
                              source_sin=source_sin, source_cos=source_cos),
                    code="""
    function makeArr(startValue, stopValue, cardinality) {
        var arr = [];
        var step = (stopValue - startValue) / (cardinality - 1);
        for (var i = 0; i < cardinality; i++) {
            arr.push(startValue + (step * i));
        }
        return arr;
    }
    
    // Angulo
    const angulo_grad = slider.value
    const angulo = angulo_grad*Math.PI/180
    
    // Coordendas de tangente
    const x_tan = [Math.cos(angulo)]
    const y_tan = [Math.sin(angulo)]
    
    // Coordenadas dot
    // const x_dot = [Math.cos(angulo)]
    // const y_dot = [Math.sin(angulo)]
    
    // Coordenadas coseno
    const x_cos = [Math.cos(angulo)]
    
    // Coordendas seno
    const y_sin = [Math.sin(angulo)]
    
    // Segunda grafica coseno
    const x_graph = makeArr(0, angulo, 200)
    const cos = Array.from(x_graph, (x) => Math.cos(x))
    const sin = Array.from(x_graph, (x) => Math.sin(x))
    
    // source_dot.data = { x_dot, y_dot }
    source_tangente.data = { x_tan, y_tan }
    source_coseno.data = { x_cos }
    source_seno.data = { y_sin }
    source_sin.data = { x_graph, sin }
    source_cos.data = { x_graph, cos }
""")

slider.js_on_change("value", Callback)

save(column(titulo, row(fig, fig_2), slider))
