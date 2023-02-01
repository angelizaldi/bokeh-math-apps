from bokeh.models import Div, ColumnDataSource, Slider, CustomJS, Arrow, NormalHead, Label
from bokeh.models import CheckboxGroup, Select, Button
from bokeh.plotting import figure
from bokeh.io import save
from bokeh.layouts import row, column
import numpy as np

BLUE = "#30ADB9"
BLACK = "#000000"
GRAY = "#7b7d7d"

# Figura
dominio = (-7, 7)
rango = (-3, 3)

plot = figure(height=475, width=760, title="",
              tools="", x_range=dominio, y_range=rango,
              toolbar_location=None, match_aspect=True)

plot.xaxis.fixed_location = 0
plot.yaxis.fixed_location = 0

nh = NormalHead(fill_color=BLACK, size=10)
eje_x = Arrow(end=nh, x_start=dominio[0], y_start=0, x_end=dominio[1], y_end=0, 
           line_color=BLACK)
eje_y = Arrow(end=nh, x_start=0, y_start=rango[0], x_end=0, y_end=rango[1], 
         line_color=BLACK)

etq_y = Label(text="y", x=0.15, y=rango[1]*.93, x_units="data", y_units="data", 
              text_font_style="italic", text_font="times")
etq_x = Label(text=r"x", x=dominio[1]*.97, y=0.15, x_units="data", y_units="data", 
              text_font_style="italic", text_font="times")

plot.add_layout(eje_x)
plot.add_layout(eje_y)
plot.add_layout(etq_y)
plot.add_layout(etq_x)

# Label
texto = Div(text="y = sin (x)", width=200)

# Título
titulo = Div(text="""<h1 style="text-align: center; font-family: Sans-serif, Serif; font-weight: 300;
                    text-decoration-line: underline; text-decoration-color: #30ADB9"> 
                    Transformación de Funciones </h1>""")

# Seleccionar
seleccionar = Select(title="Elegir una función",
                     value="sin(x)",
                     options=["sin(x)", "x^2", "x^3"])

# Sliders
traslacion_v = Slider(title="Traslación Vertical", value=0.0, start=-3.0, end=3.0, step=1, width=200)
traslacion_h = Slider(title="Traslación Horizontal", value=0.0, start=-5.0, end=5.0, step=1, width=200)
dilatacion_h = Slider(title="Dilatacion Horizontal", value=1, start=1, end=5, step=1, width=200)
compresion_h = Slider(title="Comprension Horizontal", value=1, start=1, end=5, step=1, width=200)
dilatacion_v = Slider(title="Dilatacion Vertical", value=1, start=1, end=5, step=1, width=200)
compresion_v = Slider(title="Comprension Vertical", value=1, start=1, end=5, step=1, width=200)

# Checkbox
reflexiones = CheckboxGroup(labels=["Reflexión eje X", "Reflexión eje Y"], active=[])

# Botón
boton = Button(label="Limpiar todo")

# Gráfica
x = np.linspace(-6, 6, 200)
y = np.sin(x)

source = ColumnDataSource(data=dict(x=x, y=y))
plot.line('x', 'y', source=source, color=BLUE, line_width=2)


Callback = CustomJS(args=dict(source=source, 
                              traslacion_v=traslacion_v, traslacion_h=traslacion_h, 
                              compresion_h=compresion_h, dilatacion_h=dilatacion_h, 
                              dilatacion_v=dilatacion_v, compresion_v=compresion_v,
                              reflexiones=reflexiones,
                              seleccionar=seleccionar,
                              label=texto),
                    code="""
function makeArr(startValue, stopValue, cardinality) {
        var arr = [];
        var step = (stopValue - startValue) / (cardinality - 1);
        for (var i = 0; i < cardinality; i++) {
            arr.push(startValue + (step * i));
        }
        return arr;
    }
    

const fun = seleccionar.value;
let funStart, funEnd;
if (fun === "sin(x)") {
    funStart = "sin(";
    funEnd = ")";
} else if (fun === "x^2") {
funStart = "(";
funEnd = ")^2";
} else if (fun === "x^3") {
    funStart = "(";
    funEnd = ")^3";
}

const activeIndices = reflexiones.active;

const tv = traslacion_v.value;
const th = traslacion_h.value;
const dh = dilatacion_h.value;
const ch = compresion_h.value;
const dv = dilatacion_v.value;
const cv = compresion_v.value;

// Update label
// Traslaciones
let tvStr = "";
if (tv !== 0) {
    tvStr = `${tv}`;
}

let thStr = "";
if (th !== 0) {
    thStr = `${th}`;
}

let tvSig = "";
if (tv > 0) {
    tvSig = "+";
} else {
    tvSig = "";
}

let thSig = "";
if (th > 0) {
    thSig = "+";
} else {
    thSig = "";
}

// Horizontales
let horStr = "";
if (dh === ch) {
    horStr = "";
} else if (dh === 1) {
    horStr = `${ch}*`;
} else {
    horStr = `(${ch})/(${dh})*`;
}

// Verticales
let verStr = "";
if (dv === cv) {
    verStr = "";
} else if (dv === 1) {
    verStr = `${cv}*`;
} else {
    verStr = `(${cv})/(${dv})*`;
}

// Reflexiones
let refX = "";
if (activeIndices.includes(0)) {
    refX = "-";
} else {
    refX = ""
}

let refY = "";
if (activeIndices.includes(1)) {
    refY = "-";
} else {
    refY = "";
}

let text = `y = ${refX}${verStr}${funStart}${refY}${horStr}x${thSig}${thStr}${funEnd}${tvSig}${tvStr}`;

// Update figure data
const x_dom = makeArr(-6, 6, 200);

function evaluateFun(val, fun) {
if (fun === "sin(x)") {
  return Math.sin(val);
} else if (fun === "x^2") {
  return val ** 2;
} else if (fun === "x^3") {
  return val ** 3;
}
}

let y;
if (!activeIndices.includes(0) && !activeIndices.includes(1)) {
  y = Array.from(x_dom, (x) => dv * evaluateFun((ch * x) / dh + th, fun) / cv + tv)
}
if (activeIndices.includes(0) && !activeIndices.includes(1)) {
  y = Array.from(x_dom, (x) => -(dv * evaluateFun((ch * x) / dh + th, fun) / cv + tv))
}
if (!activeIndices.includes(0) && activeIndices.includes(1)) {
  y = Array.from(x_dom, (x) => dv * evaluateFun((ch * -x) / dh + th, fun) / cv + tv)
}
if (activeIndices.includes(0) && activeIndices.includes(1)) {
  y = Array.from(x_dom, (x) => -(dv * evaluateFun((ch * -x) / dh + th, fun) / cv + tv))
}

// Make changes
label.text = text;
source.data = { x: x_dom, y: y };
""")

limpiar = CustomJS(args=dict(source=source, 
                              traslacion_v=traslacion_v, traslacion_h=traslacion_h, 
                              compresion_h=compresion_h, dilatacion_h=dilatacion_h, 
                              dilatacion_v=dilatacion_v, compresion_v=compresion_v,
                              reflexiones=reflexiones,
                              seleccionar=seleccionar,
                              texto=texto),
                    code="""
function makeArr(startValue, stopValue, cardinality) {
    var arr = [];
    var step = (stopValue - startValue) / (cardinality - 1);
    for (var i = 0; i < cardinality; i++) {
        arr.push(startValue + (step * i));
    }
    return arr;
}

function evaluateFun(val, fun) {
    if (fun === "sin(x)") {
    return Math.sin(val);
    } else if (fun === "x^2") {
    return val ** 2;
    } else if (fun === "x^3") {
    return val ** 3;
    }
}

reflexiones.active = [];

traslacion_v.value = 0;
traslacion_h.value = 0;
dilatacion_h.value = 1;
compresion_h.value = 1;
dilatacion_v.value = 1;
compresion_v.value = 1;

const fun = seleccionar.value

const x_dom = makeArr(-6, 6, 200);
const y = Array.from(x_dom, (x) => evaluateFun(x, fun));

// Make changes
label.text = $`{fun}`;
source.data = { x: x_dom, y: y };          
"""
)

# Selector
seleccionar.js_on_change("value", Callback)

# Sliders
sliders = [traslacion_v, traslacion_h, compresion_h, dilatacion_h, dilatacion_v, compresion_v]#
for slider in sliders:
    slider.js_on_change('value', Callback)

# Checkbox
reflexiones.js_on_change('active', Callback)

# Boton
boton.js_on_click(limpiar)

inputs = column(seleccionar, texto, *sliders, reflexiones, boton)

save(column(titulo, row(inputs, plot)))