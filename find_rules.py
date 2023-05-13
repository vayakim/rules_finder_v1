# -*- coding: utf-8 -*-
import os
import platform
import multiprocessing
import subprocess
import time

from tkinterdnd2 import *
from tkinter import ttk
from tkinter.messagebox import showinfo

try:
    from tkinter import *
except ImportError:
    from tkinter import *
    from tkinter.scrolledtext import ScrolledText

import pandas as pd

from data_infos import *
from pattern_infos import *
from format_data import *
from apriori_input_data import *
from decode_c_output import *
from context_manager import cd

from efficient_apriori import apriori



def ask_for_data_infos():
    """Return a frame to collect the data information inputs.
    """
    if has_content:
        data_infos_frame.generate_data_frame()
    else:
        msg = 'You need to add a valid file path'
        showinfo(title='Error_invalid_path',message=msg)

def ask_for_pattern_infos():
    """Return a frame to collect the pattern information inputs. bnjghnhjg
    """
    if has_content:
        pattern_infos_frame.generate_rules_frame()
    else:
        msg = 'You need to add a valid file path'
        showinfo(title='Error_invalid_path',message=msg)
         
def generate_rules():
    """Generates the association rules based on the dataset and the parameters.
        First, there is a filtering, then the data is set to be a proper input to the apriori algorithm, which retturns the rules.
        For Python it is already working, efforts are being put to make it work using a C++ call to a apriori algorithm function,
        with the objective of time reduction and system efficiency.
    """
    if has_content:
        if data_infos_frame.ended and pattern_infos_frame.ended:

            file_path = 'buckets_file.txt'
            outcome_file = '../rules.txt'

            dayfirst = data_infos_frame.dayfirst
            metadata = data_infos_frame.metadata
            antecedente = data_infos_frame.antecedente
            consequente = data_infos_frame.consequente
            min_rep = float(pattern_infos_frame.min_rep)
            confidence = float(pattern_infos_frame.confidence)
            period = pattern_infos_frame.period

            filtered_data = format_data(apriori_raw_data)
            filtered_data.select_columns(metadata, antecedente, consequente, dayfirst)
            filtered_data.apply_restrictions(min_rep)

            apriori_input = apriori_input_data(filtered_data.formated_data)
            buckets = apriori_input.generate_buckets(period, metadata)
            apriori_input.generate_cpp_input(file_path='bodon_apriori/buckets_file.txt')

            decoder = decode_c_file(output='rules.txt')

            decoder.set_dict(apriori_input.decoder_dict)
            sup_c = round(float(min_rep/len(buckets)), 2)
            confidence_c = round(float(confidence),2)

            start_c_time = time.time()
            with cd("bodon_apriori"):
                # we are in /bodon_apriori
                saida_C = subprocess.call("./apriori.exe %s %s %f %f" % (file_path ,outcome_file , sup_c , confidence_c))
           
            end_c_time_without_decode = time.time()
            decoder.decode()
            end_c_time_with_decode = time.time()

            c_apriori_time = end_c_time_without_decode - start_c_time
            c_py_apriori_time = end_c_time_with_decode - start_c_time
            if saida_C:
                print('ERRO!')
            decoder.generate_rules_csv()
            #TODO Tratamento de erros
            print('processando padrões...\n')

            start_py_time = time.time()
            itemset, rules = apriori(transactions = buckets, min_support=(min_rep/len(buckets)),  min_confidence=confidence)
            end_py_time = time.time()
            py_apriori_time = end_py_time - start_py_time

            print('C Apriori execution time:', c_apriori_time * 1000, 'miliseconds')
            print('C Apriori execution time + Decoder time:', c_py_apriori_time * 1000, 'miliseconds')
            print('Python Apriori execution time:', py_apriori_time * 1000, 'miliseconds')

            if not rules:
                msg = 'No rule found!'
                showinfo(title='No_rule',message=msg)
            else:
                print(f'Foram encontrados {len(rules)} padrões nos dados fornecidos.')
                for rule in rules:
                    print(f'O padrão {rule.lhs} -> {rule.rhs} se repete em {round(rule.support * len(apriori_input.buckets))} baldes e possui confiança de {"%.1f"%rule.confidence}\n')

        else:
            msg = 'Something went wrong! Please check the parameters'
            showinfo(title='Error_bad_parameters',message=msg)
    else:
        msg = 'You need to add a valid file path'
        showinfo(title='Error_invalid_path',message=msg)

def drop_enter(event):
    event.widget.focus_force()
    return event.action

def drop_position(event):
    return event.action

def drop_leave(event):
    return event.action

def drop(event):
    global apriori_raw_data
    global has_content
    if event.data:
        print('Dropped data:\n', event.data)
        if event.widget == listbox:
            files = listbox.tk.splitlist(event.data)
            for f in files:
                if os.path.exists(f):
                    print('Dropped file: "%s"' % f)
                    listbox.insert('end', f)
                    try:
                        apriori_raw_data = pd.read_excel(f)
                        has_content = True
                    except:
                        try:
                            apriori_raw_data = pd.read_csv(f)
                            has_content = True
                        except FileNotFoundError as error:
                            print(error)

                else:
                    print('Not dropping file "%s": file does not exist.' % f)
        else:
                    print('Not dropping file "%s": file does not exist.' % f)

    return event.action

# define drag callbacks
def drag_init_listbox(event):
    # use a tuple as file list, this should hopefully be handled gracefully
    # by tkdnd and the drop targets like file managers or text editors
    data_path = ()
    if listbox.curselection():
        data_path = tuple([listbox.get(i) for i in listbox.curselection()])
        print('Dragging :', data_path)
    # tuples can also be used to specify possible alternatives for
    # action type and DnD type:
    return ((ASK, COPY), (DND_FILES, DND_TEXT), data_path)

root = TkinterDnD.Tk()
root.withdraw()
root.title('RULE_FINDER')
root.grid_rowconfigure(2, weight=1, minsize=250)
root.grid_columnconfigure(0, weight=1, minsize=150)
root.grid_columnconfigure(1, weight=1, minsize=150)

apriori_raw_data = pd.DataFrame()
apriori_input = pd.DataFrame()
data_infos_frame = data_infos()
pattern_infos_frame = pattern_infos()
has_content = False

Label(root, text='Welcome to Pattern Finder!').grid(row=0, column=0, columnspan=2, padx=10, pady=5)
Label(root, text='To start, drag and drop a file path here:').grid(row=1, column=0, columnspan=2, padx=10, pady=5)

buttonbox_set_data_info = Frame(root)
buttonbox_set_data_info.grid(row=3, column=0, pady=5)
Button(buttonbox_set_data_info, text='Select data columns', command=ask_for_data_infos).pack(padx=5)


buttonbox_set_pattern_info = Frame(root)
buttonbox_set_pattern_info.grid(row=3, column=1, pady=5)
Button(buttonbox_set_pattern_info, text='Configure pattern restrictions', command=ask_for_pattern_infos).pack(padx=5)


buttonbox_generate_rules = Frame(root)
buttonbox_generate_rules.grid(row=4, column=0, columnspan=2 ,pady=5)
Button(buttonbox_generate_rules, text='Generate Rules!', command=generate_rules).pack(side=BOTTOM)

#############################################################################
##                                                                         ##     
#                     drag & drop files interface                           #
##                                                                         ##
#############################################################################
listbox = Listbox(root, name='dnd_demo_listbox',
                    selectmode='extended', width=1, height=1)
listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='news')

#listbox.insert(END, os.path.abspath(__file__))

# now make the Listbox and Text drop targets
listbox.drop_target_register(DND_FILES)

listbox.dnd_bind('<<DropEnter>>', drop_enter)
listbox.dnd_bind('<<DropPosition>>', drop_position)
listbox.dnd_bind('<<DropLeave>>', drop_leave)
listbox.dnd_bind('<<Drop>>', drop)


listbox.drag_source_register(1, DND_FILES)

listbox.dnd_bind('<<DragInitCmd>>', drag_init_listbox)


root.update_idletasks()
root.deiconify()
root.mainloop()