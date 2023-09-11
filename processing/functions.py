def CoreShell():
    class CoreShell(object):
        parts = formula.split("@")
        if "@" in parts[0]:
            comp1 = parts[0]
            comp1 = comp1.replace("-", "")
            comp2 = None
        else:
            comp1 = parts[1]
            comp1 = comp1.replace("-", "")
            comp2 = None
    return CoreShell


def Composite():
    class Composite(object):
        components = formula.split("/")
        comp1 = components[0].replace('-', '')
        comp2 = components[1].replace('-', '')
    return Composite

def Alloy():
    class Alloy(object):
        comp = formula.split("-")
        comp1 = comp[0]
        comp2 = comp[1]
    return Alloy

def Matter():
    class Matter(object):
        comp1 = formula
        comp2 = None
    return Matter

def comp_norm(formula):
    if "@" in formula:
        composition = CoreShell()
    elif "/" in formula:
        composition = Composite()
    elif "-" in formula:
        composition = Alloy()
    else:
        composition = Matter()
    return composition
#%%
def intindex(formula):
    comp = Composition(formula)
    formula = comp.formula
    pattern = r'([A-Za-z]+)(\d+\.\d+|\d+)([A-Za-z]*)'
    floating_point_indices = re.findall(r'\d+\.\d+', formula)
    if len(floating_point_indices) > 0:
        def multiply(match_obj):
            index = match_obj.group(2)
            new_index = str(int(float(index) * 100))
            return match_obj.group(1) + new_index + match_obj.group(3)
        new_formula = re.sub(pattern, multiply, formula)
        return new_formula
    else:
        return formula

import csv
def Redox(element, os1, os2):
    with open(r'C:\Users\julia\PycharmProjects\NZymes\redox1.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader) # skip the header row
        for row in reader:
            try:
                el1, el2, potential = row
                if el1 == f"{element}[{os1}]" and el2 == f"{element}[{os2}]":
                    return float(potential)
            except ValueError:
                print(f"Error on line {row}")
    return None

def OS(comp):
    comp1 = Composition(intindex(comp))
    try:
        os = comp1.oxi_state_guesses()[0]
    except IndexError:
        os = {}
        formula = comp1.formula
        pattern = r'([A-Z][a-z]*)(\d*)'
        matches = re.findall(pattern, formula)
        for i, match in enumerate(matches):
            symbol, index = match
            element_var_name = symbol
            os[element_var_name] = 0.0
    return os

from pymatgen.core.composition import Composition
import re
def elfromcomp(comp):
    elements = {}
    formula = comp.formula
    pattern = r'([A-Z][a-z]*)(\d*\.?\d*)'
    matches = re.findall(pattern, formula)
    for i, match in enumerate(matches):
        symbol, index = match
        if index == '':
            index = '1'
        element_var_name = symbol
        elements[element_var_name] = float(index)
    return elements