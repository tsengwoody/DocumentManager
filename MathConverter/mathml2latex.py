#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 19:43:07 2019

@author: Wei-Po(偽菠菜)
"""
import os
from lxml import etree

def mathml2latex_yarosh(equation):
    """"
    Cited from https://github.com/oerpub/mathconverter/blob/master/converter.py
    MathML to LaTeX conversion with XSLT from Vasil Yaroshevich
    """
    script_base_path = os.path.dirname(os.path.realpath(__file__))
    xslt_file = os.path.join(script_base_path, 'xsl_yarosh', 'mmltex.xsl')
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return str(newdom)