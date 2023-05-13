from tkinter import *
from tkinter.messagebox import showinfo

class data_infos:
    def __init__(self):
        self.dayfirst = True
        self.metadata = StringVar()
        self.antecedente = StringVar()
        self.consequente = StringVar()
        self.ended = False

    def generate_data_frame(self):
        """Basic tkinter usage to create a frame asking for information about the data inputs.
        """
        informations_frame = Tk()

        def confirm_data_infos():
            self.metadata = metadata_entry.get()
            self.antecedente = antecedente_entry.get()
            self.consequente = consequente_entry.get()
            informations_frame.destroy()
            if self.metadata and self.antecedente and self.consequente:
                self.ended = True
                msg = 'Information added'
                showinfo(title='Information',message=msg)

        informations_frame.grid_rowconfigure(1, weight=1, minsize=50)
        informations_frame.grid_rowconfigure(2, weight=1, minsize=50)
        informations_frame.grid_rowconfigure(3, weight=1, minsize=50)

        informations_frame.grid_columnconfigure(0, weight=1, minsize=300)
        informations_frame.grid_columnconfigure(1, weight=1, minsize=300)
        informations_frame.focus()
        # metadata
        metadata_label = Label(informations_frame, text="Metadata attribute (Unique):")
        metadata_label.grid(row=1, column=0, padx=5, pady=1)

        metadata_entry = Entry(informations_frame, textvariable=self.metadata)
        metadata_entry.grid(row=1, column=1, padx=5, pady=1)
        metadata_entry.focus()

        # target attributes
        #antecedente
        antecedente_label = Label(informations_frame, text="Atributo de origem:")
        antecedente_label.grid(row=2, column=0, padx=5, pady=1)

        antecedente_entry = Entry(informations_frame, textvariable=self.antecedente)
        antecedente_entry.grid(row=2, column=1, padx=5, pady=1)

        #consequente
        consequente_label = Label(informations_frame, text="Atributo de destino:")
        consequente_label.grid(row=3, column=0, padx=5, pady=1)

        consequente_entry = Entry(informations_frame, textvariable=self.consequente)
        consequente_entry.grid(row=3, column=1, padx=5, pady=1)


        # confirm button
        confirm_button = Button(informations_frame, text="Confirm", command=confirm_data_infos)
        confirm_button.grid(row=4, column=1, padx=5, pady=10)

        #dayfirst button
        dayfirst_button = Checkbutton(informations_frame, text='day first format', width= 20,variable=self.dayfirst,onvalue=True,offvalue=False)
        dayfirst_button.grid(row=4, column=0, padx=5, pady=10)
    

    def reset(self):
        self.ended = False


    