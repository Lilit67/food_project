import os
import pandas as pd
import argparse

def read_text_recipe(filepath):
    lines = []
    with open(filepath) as f:
        lines = f.readlines()
    return lines

def scale_ingredients(lines, scale):
    """
    Most primitive, assume ingredient line
    starts with number
    :param lines:
    :return:
    """
    ingredients_list = []
    for line in lines:
        words = line.split()
        if not words:
            continue
        if words[0].isnumeric():
            words[0] = str(float(words[0]) * scale)
            newline = ' '.join(words)
            ingredients_list.append(newline)

    return ingredients_list

def parse_line(line, scale):
    words = line.split()
    recipe_line_list = []
    if not words:
        return None
    if words[0].isnumeric():
        words[0] = str(float(words[0]) * scale)
        newline = ' '.join(words)
    return newline


def parse_args():
    parser = argparse.ArgumentParser(description='Scale text recipe, return the scaled ingredients list')
    parser.add_argument('-f', "--filepath",
                        metavar='filepath',
                        type=str,
                        help='file path',
                        required=True)
    parser.add_argument('-s', "--scale",
                        metavar='scale',
                        type=float,
                        help='times scale',
                        required=False)

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    lines = read_text_recipe(args.filepath)
    scaled_text = scale_ingredients(lines, args.scale)
    print('Scaling {} times'.format(args.scale))
    print(scaled_text)


if __name__ == '__main__':
    main()
