import base64
from io import BytesIO
from django.shortcuts import render
from matplotlib import pyplot as plt
from sympy import diff, lambdify, Symbol
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, split_symbols, convert_xor, implicit_multiplication

def index(request):
    return render(request, 'index.html', {})

def load_chart(request):

    func1 = request.GET.get('function1')
    func2 = request.GET.get('function2')
    
    transformations = (standard_transformations + (convert_xor,)) + (split_symbols, implicit_multiplication)

    func1 = parse_expr(func1, transformations = transformations)
    func2 = parse_expr(func2, transformations = transformations)

    func = func1 - func2
    derFunc = diff(func, 'x')
    
    f = lambdify('x', func)
    d = lambdify('x', derFunc)

    f1 = lambdify('x', func1)
    f2 = lambdify('x', func2)

    n = np.linspace(-5, 5, 500)
    m = f1(n)

    plt.plot(n, m)

    n = np.linspace(-5, 5, 500)
    m = f2(n)

    plt.plot(n, m)

    x0 = request.GET.get('x')
    
    if x0 == '':
       x1 = 5
       y1 = f1(x1)
       
    else:
        x0 = x0[4:]
        x0 = float(x0)

        x1 = x0 - f(x0) / d(x0)
        y1 = f1(x1)

        plt.plot([x1], [y1], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="red")

    buffer = BytesIO()

    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)

    chart = graph.decode('utf-8')
    buffer.close()

    plt.gcf().clear()

    y = f(x1)

    stop = (abs(y) <= 0.000000001)

    return render(request, 'chart.html', {'chart': chart, 'x': x1, 'y': y1, 'stop': stop})
