import importlib
import time
import os


path = os.getcwd()
dir_typ = None
# Linux and mac like to use '/' in their directory names, but for some reason
# windows likes '\' so I made the program adaptable. Probably using a very
# stupid fix, but hey whatever.
if '/' in path:
    dir_typ = '/'
else:
    dir_typ = '\\'

def block_writer(block: int) -> str:
    """
    creates python files containing a certain range of even num checkers. Each
    file can check a block of 250,000
    block1 is 0 - 250,000
    block2 is 250,001 - 500,000

    precondition: block >= 1
    """
    num_end = 2000000 * block + 1
    num_start = num_end - 2000000 - 1
    even_nums = [x for x in range(num_start, num_end) if x % 2 == 0]
    with open(path + f'{dir_typ}locks{dir_typ}lock{block}.py', 'w') as f:
        f.write(f'def even_block(num: int) -> bool:')
        f.write(''.join(f'\n    if num == {i}:\n        return True\n'
                        for i in even_nums))
        f.write('    return False\n')
    with open(path + f'{dir_typ}locks.txt', 'a') as made:
        made.write(f'{block}\n')
    return f'{block}'


class EvenNum:
    """
    A very inefficient even number checker.

    Instance Atributes:
    blocks: a dictionary containing what blocks(ranges of numbers are available)
            Keys being ints, and values being the directories for the
            corresponding block. Each block will be a size of 5000 integers that
            can be checked (i.e. block 1 will be from 0-4999).
    num: the number to check, must be an int.
    """
    blocks: list
    num: int

    def __init__(self, num: int) -> None:
        """
        Initializes an even num_object
        """
        self.num = num
        self.blocks = []
        with open(path + f'{dir_typ}locks.txt', 'r') as blo:
            self.blocks.extend(blo.readlines())
            #self.blocks = avail.split()
        x = 0

    # maybe add multiprocessing to make it go faster.
    def check_even(self) -> bool:
        """checks whether num is even"""
        block_need = self.num // 2000000

        if block_need == 0 and self.blocks == []:
            directory = block_writer(1)
            self.blocks[1] = directory
        # if the necessary block is not available, it creates all of them.
        elif block_need + 1 not in self.blocks:
            for i in range(block_need + 1):
                directory = block_writer(i + 1)
                self.blocks.append(directory)

        if block_need + 1 == 1 and str(block_need + 1) in self.blocks:
            x = importlib.import_module(f'locks.lock{1}')
            return x.even_block(self.num)

        elif str(block_need + 1) in self.blocks:
            for i in range(1, block_need + 2):
                x = importlib.import_module(f'locks.lock{block_need + 1}')
                if i != block_need + 1:
                    x.even_block(self.num)
                else:
                    return x.even_block(self.num)


if __name__ == '__main__':
    import PySimpleGUI as sg

    #sg.theme('DarkAmber')   # Add a touch of color
    # All the stuff inside your window.
    layout = [ [sg.Text('Are you in a rush?')],
                [sg.Text('Enter yes or no (or y/n)'), sg.InputText()],
                [sg.Button('Ok'), sg.Button('Cancel')]]
    valids = ['y', 'Y', 'yes', 'YES', 'Yes', 'n', 'N', 'No', 'NO', 'no']
    # Create the Window
    window = sg.Window('Da-Even Number Checker', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    val = True
    while val:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            val = False
            break
        elif values[0] in valids:
            break
        print('You entered ', values[0])
    ty = values[0]
    window.close()

    layout2 = [[],
               [sg.Text('Enter A Number'), sg.InputText()],
               [sg.Button('Ok'), sg.Button('Cancel')]]
    if val:
        window = sg.Window('Da-Even Number Checker', layout2)
        while True:
            event2, values2 = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel' or values2[0].isnumeric()\
                    or event2 == sg.WIN_CLOSED or event2 == 'Cancel': # if user closes window or clicks cancel
                break
        num = values2[0]
        window.close()

        if ty in valids[5:]:
            start = time.time()
            to_check = EvenNum(int(num))
            out = to_check.check_even()
            end = time.time() - start

            if out:
                layout2 = [[sg.Text(f'\t\t\t{int(num)} is an EVEN number.')],
                           [sg.Text(f'\t\t\tIt took {end} seconds to check.\t\t\t')]]

                window = sg.Window('Da-Even Number Checker', layout2)
                while True:
                    event, values2 = window.read()
                    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                        break
            else:
                layout2 = [[sg.Text(f'\t\t\t{int(num)} is an ODD number.\t\t\t')],
                           [sg.Text(f'\t\t\tIt took {end} seconds to check.\t\t\t')]]
                window = sg.Window('Da-Even Number Checker', layout2)
                while True:
                    event, values2 = window.read()
                    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                        break
            window.close()

        else:
            if int(num) % 2 == 0:
                layout2 = [[sg.Text(f'\t\t\t{int(num)} is an EVEN number.\t\t\t')]]
                window = sg.Window('Da-Even Number Checker', layout2)
                while True:
                    event, values2 = window.read()
                    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                        break
            else:
                layout2 = [[sg.Text(f'\t\t\t{int(num)} is an ODD number.\t\t\t')]]
                window = sg.Window('Da-Even Number Checker', layout2)
                while True:
                    event, values2 = window.read()
                    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                        break
            window.close()
