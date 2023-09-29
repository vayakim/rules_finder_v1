from tkinter import *
from tkinter.messagebox import showinfo
import pandas as pd

class format_data:
    def __init__(self, data) -> None:
        self.original_data = pd.DataFrame(data)
        self.ordered_data = pd.DataFrame()
        
    def select_columns(self, metadata, antecedente, consequente, dayfirstx, yearfirstx):
        self.metadata = metadata
        self.antecedente = antecedente
        self.consequente = consequente

        self.ordered_data = self.original_data[[metadata, antecedente, consequente]]
        self.ordered_data.loc[:,metadata] = pd.to_datetime(self.ordered_data[metadata], dayfirst=dayfirstx, yearfirst=yearfirstx, errors='coerce')
        self.ordered_data.sort_values(by=metadata, inplace=True, ignore_index=True)

    def apply_restrictions(self, min_rep):
        count = 'counts'
        self.formated_data = self.ordered_data.copy()

        occur = self.formated_data.groupby([self.antecedente]).size().reset_index(name=count)
        occur = occur[occur[count] > min_rep]
        self.formated_data = self.formated_data[self.formated_data[self.antecedente].isin(list(occur[self.antecedente]))]

        occur = self.formated_data.groupby([self.consequente]).size().reset_index(name=count)
        occur = occur[occur[count] > min_rep]
        self.formated_data = self.formated_data[self.formated_data[self.consequente].isin(list(occur[self.consequente]))]

        