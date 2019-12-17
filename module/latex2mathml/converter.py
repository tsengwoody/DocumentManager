#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2016-2019, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import re
import xml.etree.cElementTree as eTree
from xml.sax.saxutils import unescape

from latex2mathml.aggregator import aggregate
from latex2mathml.commands import MATRICES, COMMANDS
from latex2mathml.symbols_parser import convert_symbol


def convert(latex, xmlns='http://www.w3.org/1998/Math/MathML'):
    math = eTree.Element('math')
    math.attrib['xmlns'] = xmlns
    row = eTree.SubElement(math, 'mrow')
    _classify_subgroup(aggregate(latex), row)
    return _convert(math)


def _convert(tree):
    xml_string = eTree.tostring(tree)
    try:
        return unescape(xml_string)
    except TypeError:
        return unescape(xml_string.decode('utf-8'))


def _convert_matrix_content(param, parent, alignment=None):
    for row in param:
        mtr = eTree.SubElement(parent, 'mtr')
        iterable = iter(range(len(row)))
        for i in iterable:
            element = row[i]
            if alignment:
                column_align = {'r': 'right', 'l': 'left', 'c': 'center'}.get(alignment)
                mtd = eTree.SubElement(mtr, 'mtd', columnalign=column_align)
            else:
                mtd = eTree.SubElement(mtr, 'mtd')
            if isinstance(element, list):
                _classify_subgroup(element, mtd)
            elif element in COMMANDS:
                _convert_command(element, row, i, iterable, mtd)
            else:
                _classify(element, mtd)


def _convert_array_content(param, parent, alignment=None):
    if '|' in alignment:
        _alignment, column_lines = [], []
        for i in alignment:
            if i == '|':
                column_lines.append('solid')
            else:
                _alignment.append(i)
            if len(_alignment) - len(column_lines) == 2:
                column_lines.append('none')
        parent.attrib['columnlines'] = ' '.join(column_lines)
    else:
        _alignment = list(alignment)
    row_lines = []
    row_count = 0
    for row in param:
        row_count += 1
        mtr = eTree.SubElement(parent, 'mtr')
        iterable = iter(range(len(row)))
        index = 0
        has_row_line = False
        for i in iterable:
            element = row[i]
            if element == r'\hline' and row_count > 1:
                row_lines.append('solid')
                has_row_line = True
                continue
            try:
                align = _alignment[index]
            except IndexError:
                align = None
            if align:
                column_align = {'r': 'right', 'l': 'left', 'c': 'center'}.get(align)
                mtd = eTree.SubElement(mtr, 'mtd', columnalign=column_align)
            else:
                mtd = eTree.SubElement(mtr, 'mtd')
            if isinstance(element, list):
                _classify_subgroup(element, mtd)
            elif element in COMMANDS:
                _convert_command(element, row, i, iterable, mtd)
            else:
                _classify(element, mtd)
            index += 1
        if not has_row_line and row_count > 1:
            row_lines.append('none')
    if 'solid' in row_lines:
        parent.set('rowlines', ' '.join(row_lines))


def _classify_subgroup(elements, row):
    iterable = iter(range(len(elements)))
    for i in iterable:
        element = elements[i]
        if isinstance(element, list):
            _row = eTree.SubElement(row, 'mrow')
            _classify_subgroup(element, _row)
        elif element in COMMANDS:
            _convert_command(element, elements, i, iterable, row)
        else:
            _classify(element, row)


def _convert_command(element, elements, index, iterable, parent):
    _get_prefix_element(element, parent)
    params, tag, attributes = COMMANDS[element]
    new_parent = eTree.SubElement(parent, tag, attributes)
    alignment = None
    if element in MATRICES and (element.endswith('*') or element == r'\array'):
        index += 1
        alignment = elements[index]
        next(iterable)
    for j in range(params):
        index += 1
        param = elements[index]
        if element == r'\left' or element == r'\right':
            if param == '.':
                pass
            else:
                symbol = convert_symbol(param)
                new_parent.text = param if symbol is None else '&#x{};'.format(symbol)
        elif element == r'\array':
            _convert_array_content(param, new_parent, alignment)
        elif element in MATRICES:
            _convert_matrix_content(param, new_parent, alignment)
        else:
            if isinstance(param, list):
                _parent = eTree.SubElement(new_parent, 'mrow')
                _classify_subgroup(param, _parent)
            else:
                _classify(param, new_parent)
    _get_postfix_element(element, parent)
    if element in (r'\overline', r'\bar'):
        mo = eTree.SubElement(new_parent, 'mo', stretchy='true')
        mo.text = '&#x000AF;'
    elif element == r'\underline':
        mo = eTree.SubElement(new_parent, 'mo', stretchy='true')
        mo.text = '&#x00332;'
    [next(iterable) for _ in range(params)]


def _convert_and_append_operator(symbol, parent):
    symbol = convert_symbol(symbol)
    mo = eTree.SubElement(parent, 'mo')
    mo.text = '&#x{};'.format(symbol)


def _get_postfix_element(element, row):
    if element in (r'\binom', r'\pmatrix'):
        _convert_and_append_operator(r'\rparen', row)
    elif element == r'\bmatrix':
        _convert_and_append_operator(r'\rbrack', row)
    elif element == r'\Bmatrix':
        _convert_and_append_operator(r'\rbrace', row)
    elif element == r'\vmatrix':
        _convert_and_append_operator(r'\vert', row)
    elif element == r'\Vmatrix':
        _convert_and_append_operator(r'\Vert', row)


def _get_prefix_element(element, row):
    if element in (r'\binom', r'\pmatrix'):
        _convert_and_append_operator(r'\lparen', row)
    elif element == r'\bmatrix':
        _convert_and_append_operator(r'\lbrack', row)
    elif element == r'\Bmatrix':
        _convert_and_append_operator(r'\lbrace', row)
    elif element == r'\vmatrix':
        _convert_and_append_operator(r'\vert', row)
    elif element == r'\Vmatrix':
        _convert_and_append_operator(r'\Vert', row)


def _classify(_element, parent):
    symbol = convert_symbol(_element)
    if re.match(r'\d+(.\d+)?', _element):
        mn = eTree.SubElement(parent, 'mn')
        mn.text = _element
    elif _element in '<>&':
        mo = eTree.SubElement(parent, 'mo')
        mo.text = {'<': '&lt;', '>': '&gt;', '&': '&amp;'}[_element]
    elif _element in '+-*/()=':
        mo = eTree.SubElement(parent, 'mo')
        mo.text = _element if symbol is None else '&#x{};'.format(symbol)
    elif symbol and (int(symbol, 16) in range(int('2200', 16), int('22FF', 16) + 1) or
                     int(symbol, 16) in range(int('2190', 16), int('21FF', 16) + 1)):
        mo = eTree.SubElement(parent, 'mo')
        mo.text = '&#x{};'.format(symbol)
    elif _element.startswith('\\'):
        if symbol:
            mi = eTree.SubElement(parent, 'mi')
            mi.text = '&#x{};'.format(symbol)
        else:
            e = _element.lstrip('\\')
            mi = eTree.SubElement(parent, 'mi')
            mi.text = e
    else:
        mi = eTree.SubElement(parent, 'mi')
        mi.text = _element
