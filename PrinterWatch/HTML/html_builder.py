
class HTMLCreator(object):
    def __init__(self):
        self.address = '172.20.12.179/'
        self.insert_dict = {'*icon_insert*': self.insert_logo(),
                            '*navbar_insert*': self.insert_navbar(),
                            '*content_insert*': self.insert_content()}
        self.insert_keys = list(self.insert_dict.keys())
        self.basecode = self.create_base()

    def create_base(self):
        html_code = []
        with open(r'A:\Raze VorteX\Documents\PrinterWatch\PrinterWatch\HTML\basecode', 'r') as file:
            for line in file.readlines():
                line = line.strip()
                for key in self.insert_dict.keys():
                    if key in line:
                        line = line.replace(key, self.insert_dict[key])

                html_code.append(line)
        return html_code

    def insert_logo(self, local=False):
        if local:
            return r'../PrinterWatch.ico'
        else:
            return r'https://photos.google.com/album/AF1QipPfQXwp0iAMJm8ZKSYWzyoSpSOyv44nUMrPwGpH/photo/AF1QipPiMDKuY8CJrOjF2aKarBI8J1nc7o7viMPqDuhY'

    def insert_navbar(self, local=True):
        if local:
            return r'../navbar.html'
        else:
            return 'https://docs.google.com/document/d/1at3UO-Na0iMZ-OvByI4msX2QDSWZDvlqVzvaN0Ur6nQ/edit?usp=sharing'

    def insert_content(self, local=False):
        if local:
            return 'nan'
        else:
            return r'https://docs.google.com/spreadsheets/d/1lSXBP5OPtdYT9VPXkcwKnn5nrwIv1dCh/edit?usp=sharing&ouid=102357389013742688623&rtpof=true&sd=true'

if __name__ == "__main__":
    test = HTMLCreator()
    print(test.basecode)