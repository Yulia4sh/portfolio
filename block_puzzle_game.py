#!/usr/bin/env python
# coding: utf-8

# In[ ]:


"""
This script allows players to choose game levels and place figures on the field according to the given rules.
The game ends when no more figures can be placed, and the winner is determined based on the count of figures on the field.

Dependencies:
- tabulate: for displaying the game field in a grid format
- random: for random figure selection and game level
- copy: for deep copying lists
- doctest: for testing functions with embedded examples

Functions:
- reading_files(name: str) -> list: Reads and parses data from a file.
- make_field(lst: list, num: int) -> None: Creates a game field based on the provided field number.
- print_field(lst: list) -> None: Prints the game field in a grid format.
- choose_field_and_figures(lst_field: list, lst_figures: list, choose_level: int) -> list: Selects the game field and figures based on the chosen level.
- place_figure(lst_field: list, figure: list, x_or_o='x', is_comp=False, row=None, column=None, check=False) -> list: Places a figure on the field and validates the placement.
- check_possibility_accommodation(lst_field: list, lst_figures: list) -> bool: Checks if any figure can be placed on the field.
- game_for_two() -> None: Starts a two-player game session.
- game_for_one() -> None: Starts a single-player game session against the computer.
- main(): Main function to choose the opponent and start the game.

Examples:
>>> place_figure([['.', '.', '.']], [['*']], 'x', False, 0, 0, True)
[['x', '.', '.']]

>>> check_possibility_accommodation([['.', '.', '.']], [['*'], ['*', '*']])
False
"""

from tabulate import tabulate
from random import choice
from copy import deepcopy
import doctest

def reading_files(name: str) -> list:
    """
    Reads and parses data from a file.
    
    :param name: Name of the file to read.
    :return: A list of parsed data.
    """
    result = []
    with open(name, 'r') as file:
        for line in file:
            result.append(eval(line))
    return result

def make_field(lst: list, num: int) -> None:
    """
    Creates a game field based on the provided field number.
    
    :param lst: List of field configurations.
    :param num: Field number to create.
    :return: The generated game field.
    """
    for dictionary in lst:
        if dictionary['field_number'] == num:
            field_lst = [['.' for _ in range(dictionary['field_size'][1])] for _ in range(dictionary['field_size'][0])]
            x_pos_x, x_pos_y = dictionary['x_initial_positions']
            o_pos_x, o_pos_y = dictionary['o_initial_position']
            field_lst[x_pos_x][x_pos_y], field_lst[o_pos_x][o_pos_y] = 'x', 'o'
            return field_lst

def print_field(lst: list) -> None:
    """
    Prints the game field in a grid format.
    
    :param lst: The game field to print.
    """
    print(tabulate(lst, tablefmt="grid"))

def choose_field_and_figures(lst_field: list, lst_figures: list, choose_level: int) -> list:
    """
    Selects the game field and figures based on the chosen level.
    
    :param lst_field: List of available fields.
    :param lst_figures: List of available figures.
    :param choose_level: Chosen game level.
    :return: The selected field and figures.
    """
    match choose_level:
        case 1:
            field_num, all_figures_num = choice([7, 8, 9]), [1, 2, 3, 4, 5]
        case 2:
            field_num, all_figures_num = choice([4, 5, 6]), [6, 7, 8, 9, 10]
        case 3:
            field_num, all_figures_num = choice([1, 2, 3]), [11, 12, 13, 14, 15]
    choose_field = make_field(lst_field, field_num)
    all_figure_lst = [figure['figure_view'] for figure in lst_figures if figure['figure_number'] in all_figures_num]
    return choose_field, all_figure_lst

def place_figure(lst_field: list, figure: list, x_or_o='x', is_comp=False, row=None, column=None, check=False) -> list:
    """
    Places a figure on the field and validates the placement.
    
    :param lst_field: The current game field.
    :param figure: The figure to place.
    :param x_or_o: The player symbol ('x' or 'o').
    :param is_comp: Whether the move is for the computer.
    :param row: Row position to place the figure.
    :param column: Column position to place the figure.
    :param check: Whether to only check for placement validity.
    :return: The updated game field.
    
    >>> place_figure([['.', '.', '.']], [['*']], 'x', False, 0, 0, True)
    [['x', '.', '.']]
    """
    for_not_valid = deepcopy(lst_field)
    count_another_star = choose = 0
    opponent = 'o' if x_or_o == 'x' else 'x'
    
    while choose != 1:
        if not is_comp:
            if row is None and column is None:
                row = int(input('Enter row (starting from 0): '))
                column = int(input('Enter column (starting from 0): '))
                
        lst_field = deepcopy(for_not_valid)
        just_count_1 = 0
        try:
            for i in range(row, len(figure) + row):
                just_count_2 = 0
                for j in range(column, len(figure[0]) + column):
                    if lst_field[i][j] == x_or_o and figure[just_count_1][just_count_2] != '.':
                        count_another_star += 1
                        if count_another_star > 1:
                            if not (is_comp or check):
                                print('Your turn is lost.')
                            return for_not_valid
                    elif lst_field[i][j] == opponent and figure[just_count_1][just_count_2] != '.':
                        if not (is_comp or check):
                            print('Your turn is lost.')
                        return for_not_valid
                    elif lst_field[i][j] == opponent and figure[just_count_1][just_count_2] == '.':
                        lst_field[i][j] = opponent
                    elif figure[just_count_1][just_count_2] != '.':
                        lst_field[i][j] = x_or_o
                    just_count_2 += 1
                just_count_1 += 1
        except IndexError:
            if not (is_comp or check):
                print('Your turn is lost.')
            return for_not_valid
            
        if is_comp and count_another_star == 0:
            return for_not_valid
        if is_comp or check:
            break
        else:
            if count_another_star == 0:
                print('Your turn is lost.')
                return for_not_valid
            if not (is_comp or check):
                print_field(lst_field)
                print('Are you sure?\n1 - Yes, 2 - No, choose again')
                choose = int(input())
                
    return lst_field

def check_possibility_accommodation(lst_field: list, lst_figures: list) -> bool:
    """
    Checks if any figure can be placed on the field.
    
    :param lst_field: The current game field.
    :param lst_figures: List of available figures.
    :return: True if at least one figure can be placed, False otherwise.
    
    >>> check_possibility_accommodation([['.', '.', '.']], [['*'], ['*', '*']])
    False
    """
    for figure in lst_figures:
        for i in range(len(lst_field) - len(figure)):
            for j in range(len(lst_field[0]) - len(figure[0])):
                fake_lst = deepcopy(lst_field)
                if lst_field != place_figure(fake_lst, figure, 'x', False, i, j, True):
                    return True
                fake_lst = deepcopy(lst_field)
                if lst_field != place_figure(fake_lst, figure, 'o', False, i, j, True):
                    return True
    return False

def game_for_two() -> None:
    """
    Starts a two-player game session.
    """
    all_fields = reading_files('field.txt')
    all_figures = reading_files('figures.txt')
    current_field, current_figures = choose_field_and_figures(all_fields, all_figures, int(input('Enter game level:\n1 - Easy, 2 - Average, 3 - Impossible\n')))
    print('Your field:')
    print_field(current_field)
    print('FIGURES NEED TO BE PLACED IN THE UPPER LEFT CORNER!!!')
    
    while True:
        local_figure_1 = choice(current_figures)
        print('Current figure for Player 1:')
        print_field(local_figure_1)
        current_field = place_figure(current_field, local_figure_1, 'x')
        print_field(current_field)
        
        local_figure_2 = choice(current_figures)
        print('Current figure for Player 2:')
        print_field(local_figure_2)
        current_field = place_figure(current_field, local_figure_2, 'o')
        print_field(current_field)
        
        if not check_possibility_accommodation(current_field, current_figures):
            count_1_player = sum(i.count('x') for i in current_field)
            count_2_player = sum(i.count('o') for i in current_field)
            if count_1_player > count_2_player:
                print('Player 1 wins!!')
            elif count_2_player > count_1_player:
                print('Player 2 wins!!')
            else:
                print('The game ended in a draw.')
            break

def game_for_one() -> None:
    """
    Starts a single-player game session against the computer.
    """
    all_fields = reading_files('field.txt')
    all_figures = reading_files('figures.txt')
    current_field, current_figures = choose_field_and_figures(all_fields, all_figures, int(input('Enter game level:\n1 - Easy, 2 - Average, 3 - Impossible\n')))
    print('Your field:')
    print_field(current_field)
    print('FIGURES NEED TO BE PLACED IN THE UPPER LEFT CORNER!!!')
    
    while True:
        local_figure_1 = choice(current_figures)
        print('Current figure for Player 1:')
        print_field(local_figure_1)
        current_field = place_figure(current_field, local_figure_1, 'x')
        print_field(current_field)
        
        local_figure_2 = choice(current_figures)
        print('Current figure for Computer:')
        print_field(local_figure_2)
        for i in range(len(current_field)):
            for j in range(len(current_field[0])):
                if current_field != place_figure(current_field, local_figure_2, 'o', True, i, j):
                    current_field = place_figure(current_field, local_figure_2, 'o', True, i, j)
                    break
                if i == len(current_field) - 1 and j == len(current_field[0]) - 1:
                    count_1_player = sum(i.count('x') for i in current_field)
                    count_2_player = sum(i.count('o') for i in current_field)
                    if count_1_player > count_2_player:
                        print('Player 1 wins!!')
                    elif count_2_player > count_1_player:
                        print('Computer wins!!')
                    else:
                        print('The game ended in a draw.')
                    return current_field
            else:
                continue
            break 
        
        print_field(current_field)
        if not check_possibility_accommodation(current_field, current_figures):
            count_1_player = sum(i.count('x') for i in current_field)
            count_2_player = sum(i.count('o') for i in current_field)
            if count_1_player > count_2_player:
                print('Player 1 wins!!')
            elif count_2_player > count_1_player:
                print('Computer wins!!')
            else:
                print('The game ended in a draw.')
            break

def main():
    """
    Main function to choose the opponent and start the game.
    """
    choose_opponent = int(input('Enter who you want to play with:\n1 - With a friend, 2 - With the computer\n'))
    if choose_opponent == 1:
        game_for_two()
    elif choose_opponent == 2:
        game_for_one()

main()
doctest.testmod()


# In[ ]:




