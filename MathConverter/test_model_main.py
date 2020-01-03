#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 15:00:17 2019

@author: Wei-Po(偽菠菜)
reference:https://www.intmath.com/help/asciimath-input-latex-katex-output.php
reference:https://www.codecogs.com/latex/eqneditor.php?lang=zh-cn
"""

import os
os.chdir("/Users/Wei-Po/Desktop/mathconverter-master")

import asciimathml
from xml.etree.ElementTree import tostring
import latex2mathml.converter

# ===latex2mathml測試===
latex2mathml_test_list = {
    "a":r"xyz",
    "b":r"839",
    "c":r"12.34",
    "d":r"12x",
    "e":r"3-2",
    "f":r"a_b",
    "g":r"a^b",
    "h":r"a_b^c",
    "i":r"\frac{1}{2}",
    "j":r"\sqrt{2}",
    "k":r"\sqrt[3]{2}",
    "l":r"\begin{matrix}a & b \\ c & d \end{matrix}",
    "m":r"A_{m,n} = \begin{bmatrix}a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\\vdots  & \vdots  & \ddots & \vdots  \\a_{m,1} & a_{m,2} & \cdots & a_{m,n} \end{bmatrix}"
    }
for key in latex2mathml_test_list.keys():
    test = latex2mathml.converter.convert(latex2mathml_test_list[key])
    print(key,latex2mathml_test_list[key])
    print(test)
    print()
    

# ===asciimathml測試===
asciimathml_test_list = {
    "a":r"xyz",
    "b":r"839",
    "c":r"12.34",
    "d":r"12x",
    "e":r"3-2",
    "f":r"a_b",
    "g":r"a^b",
    "h":r"a_b^c",
    "i":r"1/2",
    "j":r"sqrt(2)",
    "k":r"root3(2)",
    "l":r"[[a,b],[c,d]]((2),(2))",
    "m":r"sqrt(b^2 – 4ac) / (2a)",
    "n":r"(-b)/(2a)"
    }
for key in asciimathml_test_list.keys():
    test = tostring(asciimathml.parse(asciimathml_test_list[key])) 
    print(key,asciimathml_test_list[key])
    print(test)
    print()
    

import mathml2latex
# ===mathml2latex_yarosh測試===
mathml2latex_test_list = {
    "a":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mi>x</mi><mi>y</mi><mi>z</mi></mrow></math>",
    "b":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mn>839</mn></mrow></math>",
    "c":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mn>12.34</mn></mrow></math>",
    "d":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mn>12</mn><mi>x</mi></mrow></math>",
    "e":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mn>3</mn><mo>&#x02212;</mo><mn>2</mn></mrow></math>",
    "f":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><msub><mi>a</mi><mi>b</mi></msub></mrow></math>",
    "g":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><msup><mi>a</mi><mi>b</mi></msup></mrow></math>",
    "h":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><msubsup><mi>a</mi><mi>b</mi><mi>c</mi></msubsup></mrow></math>",
    "i":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mfrac><mrow><mn>1</mn></mrow><mrow><mn>2</mn></mrow></mfrac></mrow></math>",
    "j":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><msqrt><mrow><mn>2</mn></mrow></msqrt></mrow></math>",
    "k":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mroot><mrow><mn>2</mn></mrow><mrow><mn>3</mn></mrow></mroot></mrow></math>",
    "l":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><mtable><mtr><mtd><mi>a</mi></mtd><mtd><mi>b</mi></mtd></mtr><mtr><mtd><mi>c</mi></mtd><mtd><mi>d</mi></mtd></mtr></mtable></mrow></math>",
    "m":r"<math xmlns='http://www.w3.org/1998/Math/MathML'><mrow><msub><mi>A</mi><mrow><mi>m</mi><mi>,</mi><mi>n</mi></mrow></msub><mo>&#x0003D;</mo><mo>&#x0005B;</mo><mtable><mtr><mtd><msub><mi>a</mi><mrow><mn>1</mn><mi>,</mi><mn>1</mn></mrow></msub></mtd><mtd><msub><mi>a</mi><mrow><mn>1</mn><mi>,</mi><mn>2</mn></mrow></msub></mtd><mtd><mo>&#x022EF;</mo></mtd><mtd><msub><mi>a</mi><mrow><mn>1</mn><mi>,</mi><mi>n</mi></mrow></msub></mtd></mtr><mtr><mtd><msub><mi>a</mi><mrow><mn>2</mn><mi>,</mi><mn>1</mn></mrow></msub></mtd><mtd><msub><mi>a</mi><mrow><mn>2</mn><mi>,</mi><mn>2</mn></mrow></msub></mtd><mtd><mo>&#x022EF;</mo></mtd><mtd><msub><mi>a</mi><mrow><mn>2</mn><mi>,</mi><mi>n</mi></mrow></msub></mtd></mtr><mtr><mtd><mo>&#x022EE;</mo></mtd><mtd><mo>&#x022EE;</mo></mtd><mtd><mo>&#x022F1;</mo></mtd><mtd><mo>&#x022EE;</mo></mtd></mtr><mtr><mtd><msub><mi>a</mi><mrow><mi>m</mi><mi>,</mi><mn>1</mn></mrow></msub></mtd><mtd><msub><mi>a</mi><mrow><mi>m</mi><mi>,</mi><mn>2</mn></mrow></msub></mtd><mtd><mo>&#x022EF;</mo></mtd><mtd><msub><mi>a</mi><mrow><mi>m</mi><mi>,</mi><mi>n</mi></mrow></msub></mtd></mtr></mtable><mo>&#x0005D;</mo></mrow></math>"
    }
for key in mathml2latex_test_list.keys():
    test = mathml2latex.mathml2latex_yarosh(mathml2latex_test_list[key])
    print(key)
    print(test)
    print()
    