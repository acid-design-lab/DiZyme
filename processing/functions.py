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
import csv
def Redox(element, os1, os2):
    with open('redox1.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            el1, el2, potential = row
            if el1 == f"{element}[{os1}]" and el2 == f"{element}[{os2}]":
                return float(potential)
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

def separate_formulas(df, column):
    formulas = []
    components = []

    for entry in column:
        if not isinstance(entry, str):
            formulas.append(None)
            components.append(None)
            continue
        match = re.split(r'\s*\+\s*', entry)
        if match and len(match) == 2:
            formulas.append(match[0])
            components.append(match[1])
        else:
            formulas.append(match[0])
            components.append(None)

    df['sub1'] = formulas
    df['sub2'] = components
    return df
def split(strings):
    excluded_strings = ['1,3,5-benzenetricarboxylate', '3,5-Dimethylpyridine']
    result = []
    for string in strings:
        if string in excluded_strings:
            result.append(string)
            continue
        if ',' in string:
            parts = string.split(',')
            result.extend(parts)
        else:
            result.append(string)
    return result

def monomer(string_list):
    substrings = []
    for string in string_list:
        if string == "Tetrakis(4-carboxyphenyl)porphine":
            substrings.append(string)
            continue
        match = re.search(r'\((.*?)\)', string)
        if match:
            substrings.append(match.group(1))
        else:
            substrings.append(string)
    return substrings

import pubchempy as pcp
def smiles(name):
    smiles_list = []
    if name == '0' or name == 0:
        pass
    else:
        if ',' not in name:  # Single smiles
            try:
                smiles = pcp.get_compounds(name, 'name')[0].isomeric_smiles
                smiles_list.append(smiles)
            except:
                pass
        else:  # String of molecule names
            names = name.split(',')
            merged_names = []
            temp_name = ""
            for n in names:
                if temp_name == "":
                    temp_name = n
                elif temp_name.endswith('-') or temp_name.endswith('_'):
                    temp_name += n
                else:
                    merged_names.append(temp_name)
                    temp_name = n
            merged_names.append(temp_name)

            for merged_name in merged_names:
                try:
                    smiles = pcp.get_compounds(merged_name, 'name')[0].isomeric_smiles
                    smiles_list.append(smiles)
                except:
                    pass

    return '.'.join(smiles_list)