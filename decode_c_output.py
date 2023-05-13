import pandas as pd

class decode_c_file:
    def __init__(self, output) -> None:
       self.file_path = output
       self.frequency_file = "frequence.txt"
        
    def set_dict(self,dict):
        self.decoder_dict = {v:k for k,v in dict.items()}

    def decode(self):
        cols_names = ['Antecedente', 'Consequente']
        df = pd.read_csv(self.file_path,delimiter=",", names=cols_names, header=None, dtype=str)

        for column in cols_names:
            df[column] = df[column].str.split(pat=' ')

        rules_c = []
        for index, row in df.iterrows():
            rules_c.append(tuple([row[cols_names[0]], row[cols_names[1]]]))

        term_part = []
        rule = []
        all_rules = []
        for regra in rules_c:
            for termos in regra:
                for y in termos:
                    x = self.decoder_dict.get(int(y))
                    term_part.append(x)
                if term_part:
                    rule.append(term_part)
                    term_part = []
            all_rules.append(rule)
            rule = []

        df = pd.DataFrame(all_rules, columns=cols_names)
        print("DECODED!")
        self.rules_decoded = df

    def generate_rules_csv(self):
        cols_names = ['Frequência de aparição', 'Confiança']
        self.frequency_df= pd.read_csv(self.frequency_file, delimiter=",", names=cols_names, header=None)
        outcome_csv = self.rules_decoded.join(self.frequency_df)
        outcome_csv.to_csv("rules_outcome.csv")

