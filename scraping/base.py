class Scrapping:
    def __init__(self, cid, name, url, output_type):
        self.cid = cid
        self.name = name
        self.url = url
        self.output_type = output_type
        self.data = {}

    def process(self):
        self.data["description"] = self.get_description()
        self.data["contacts"] = self.get_contacts()
        self.data["news"] = self.get_news()
        self.data["clients"] = self.get_clients()
        #print(self.data)

    def get_description(self):
        return []

    def get_contacts(self):
        return []

    def get_news(self):
        return []

    def get_clients(self):
        return []
