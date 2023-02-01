from bokeh.plotting import figure
from bokeh.io import save
from bokeh.layouts import column
import numpy as np
from bokeh.models import Div, ColumnDataSource, Slider, CustomJS, Arrow, NormalHead, Label

def funcion(x):
    return np.exp(x/1.5)/4

def inter_pendiente(x1, x2):
    y1 = funcion(x1)
    y2 = funcion(x2)
    
    m = (y2-y1)/(x2-x1)
    b = y1-m*x1
    return m, b

BLUE = "#30ADB9"
BROWN = "#BA6A30"
BLACK = "#000000"
GRAY = "#7b7d7d"


# Título
titulo = Div(text="""<h1 style="text-align: center; font-family: Sans-serif, Serif; font-weight: 300;
                    text-decoration-line: underline; text-decoration-color: #30ADB9"> 
                    Derivada de una función </h1>""")

# Texto
texto = Div(text="La pendiente real es: <b>0.32</b>", width=600)
derivada = Div(text="La pendiente aproximada es: <b>6.31</b>", width=600)

# Figura

dominio = (-1,5)
rango = (-1,5)

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

x = np.linspace(0, 5)
y = funcion(x)
fig.line(x, y, color=BLUE, line_width=3)

# punto x1 - estático
fig.circle(1, funcion(1), color=BROWN, radius=.1)

# punto x2 - dinámico
source_x2 = ColumnDataSource(data=dict(x_dot=[4], y_dot=[funcion(4)]))
fig.circle("x_dot", "y_dot", color=BROWN, radius=.1, source=source_x2)

# secante
m, b = inter_pendiente(1, 4)
x_recta = np.linspace(-1, 5, 200)
y_recta = m*x_recta+b
source_recta = ColumnDataSource(data=dict(x=x_recta, y=y_recta))
fig.line("x", "y", source=source_recta, line_width=2, color=BLACK)

# derivada
x_der = np.linspace(-1, 5, 200)
y_der = 0.3246223401757793*x_recta-(0.3246223401757793-0.48693351026366893)
fig.line(x_der, y_der, line_width=1, color=GRAY)


# label
#derivada = Label(x=0.45, y=4.5, text=f"Dₓ(𝑥₁) = 0.32", text_font="times", text_font_size="20px")
#fig.add_layout(derivada)

# label
etiqueta_x1 = Label(x=1, y=-0.3, text="𝑥₁", text_align="center")
etiqueta_fx1 = Label(x=-0.3, y=funcion(1), text="ƒ(𝑥₁)", text_align="center")
fig.add_layout(etiqueta_x1)
fig.add_layout(etiqueta_fx1)

# slider

slider = Slider(start=0.01, end=4, value=3, step=0.01, title="h", width=400)

Callback = CustomJS(args=dict(slider=slider, source_x2=source_x2, source_recta=source_recta,
                             etiqueta=derivada),
                    code="""
function funcion(x) {
  if (Array.isArray(x)) {
    return x.map(element => Math.exp(element / 1.5) / 4);
  } else {
    return Math.exp(x / 1.5) / 4;
  }
}

function interPendiente(x1, x2) {
  let y1 = funcion(x1);
  let y2 = funcion(x2);

  let m = (y2 - y1) / (x2 - x1);
  let b = y1 - m * x1;
  return [m, b];
}

const h = slider.value

const x_dot = 1 + h
const y_dot = funcion(x_dot)

const x_recta = source_recta.data.x
let [m, b] = interPendiente(1, x_dot);
let y_recta = Array.from(x_recta, (x) => m * x + b)

etiqueta.text = `La pendiente aproximada es: <b>${m.toFixed(2)}</b>`
source_x2.data = { x_dot: [x_dot], y_dot: [y_dot] }
source_recta.data = { x: x_recta , y: y_recta }
""")

slider.js_on_change("value", Callback)

save(column(titulo, fig, slider, texto, derivada))