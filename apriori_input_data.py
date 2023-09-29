import pandas as pd
from datetime import datetime
import csv

class apriori_input_data:
    def __init__(self, data):
        self.original_data = data
        self.apriori_input = pd.DataFrame()

    def generate_buckets(self, period, metadata):
        """Generates the buckets based on a time span provided by the user as a parameter, the buckets are yet fixed, but there is a plan to make the 
           time window dynamic, preventing rules associations to not be found

        Args:
            period (dict): A dict containing the days, hours and minutes equivalents of the period.
            metadata (str): The column value of the data metadata

        Returns:
            The buckets as a list of tuples, where which tuple corresponds to one bucket.
        """
        dates = pd.DatetimeIndex(self.original_data.loc[:, metadata])
        index = list(range(0, len(dates)))
        data = pd.Series(dates, index=index)
        fc = pd.Timedelta(days=float(period['days']), hours=float(period['hours']), minutes=float(period['minutes']))
        i=0
        limit = 0

        lst_copy = self.original_data.copy()
        lst_copy.drop(metadata, inplace=True, axis=1)
        buckets = []
        slice = []
        if len(lst_copy) > 1:
            while i < len(index):
                if data[i] - data[limit] < fc:
                    slice.append(tuple(lst_copy.iloc[i].values.flatten().tolist()))
                else:
                    if slice:
                        buckets.append(slice)
                    slice = []
                    slice.append(tuple(lst_copy.iloc[i].values.flatten().tolist()))
                    limit = i+1
                i+=1

        self.buckets = buckets
        return buckets

    def generate_cpp_input(self, file_path):
        """Generates a file with the data as the input required for the C++ apriori algorithm function developed by Ferenc Bodon.
        """
        #cada transação precisa ter um codigo unico
        #cada linha do arquivo de saida precisa conter todas as transaçoes de um balde
        #o conjunto de baldes possui varios baldes individuais contendo n transações
        transacoes_por_balde = []
        todos_baldes = []
        baldes = pd.Series(self.buckets)

        baldes_list_list = []
        baldes_list = []

        #make each transaction have a unique code
        for row in baldes:
            baldes_list_list.append(row)

        for list in baldes_list_list:
            for balde in list:
                baldes_list.append(str(balde))
        
        baldes_dict = dict.fromkeys(baldes_list)

        unique_value = 1
        for key in baldes_dict.keys():
            baldes_dict[key] = unique_value
            unique_value+=1
        #-------------------------------------------#
        
        for balde in baldes:
            for transacao in balde:
                transacoes_por_balde.append(baldes_dict[str(transacao)])
            todos_baldes.append(tuple(transacoes_por_balde))
            transacoes_por_balde = []

        with open(file_path, "w") as the_file:
            csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
            writer = csv.writer(the_file, dialect="custom")
            for balde in todos_baldes:
                writer.writerow(balde)
            the_file.close()

        self.decoder_dict = baldes_dict
        return todos_baldes
    
    
        

        

    
        
        
