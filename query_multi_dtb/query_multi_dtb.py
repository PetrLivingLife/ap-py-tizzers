# TODO udelat to nezavisle na typu prenasenych hodnot - string / int na vstupu druheho dotazu - zkusit vsechno jako
# string
import cx_Oracle as Cxo


class Database(object):
    def __init__(self, username, password, server, database, query, column):
        pass


class Config(object):
    def __init__(self):
        self._file = r".\query_multi_dtb_conf.txt"
        with open(self._file, encoding='utf8') as fin:
            self._conf = {key.strip(): value.strip() for key, value in
                          [tuple(line.split("=", 1)) for line in fin.read().splitlines() if  # jen 1. "=" kvuli vzorcum
                           line.strip() and not line.startswith("#")]}
            # ignoruj radky s #, ktere oznacuji casti
            # ignoruj prazdne radky line.strip() => 0 = False
            # takhle jednodussi, ale neumi strip:
            # conf = {tuple(line.split("=")) for line in fin.read().splitlines() if not line.startswith("#")}

        # Database 1 - results from this will be used in query for database 2
        self.one_user = self._conf["one_user"]
        self.one_password = self._conf["one_password"]
        self.one_server = self._conf["one_server"]
        self.one_database = self._conf["one_database"]
        self.one_query = self._conf["one_query"]
        self.one_results_column = self._conf["one_results_column"]

        # Database 2 - takes input results from Database 1
        self.two_user = self._conf["two_user"]
        self.two_password = self._conf["two_password"]
        self.two_server = self._conf["two_server"]
        self.two_database = self._conf["two_database"]
        self.two_query = self._conf["two_query"]
        self.two_input_column = self._conf["two_input_column"]


cfg = Config()
dtb_one = Database(username=cfg.one_user, password=cfg.one_password, server=cfg.one_server, database=cfg.one_database,
                   query=cfg.one_query)
dtb_two = Database(username=cfg.two_user, password=cfg.two_password, server=cfg.two_server, database=cfg.two_database,
                   query=cfg.two_query)

username = "x0556520"
password = "w443_AXPj"
at = "@"
server = "ocsxpptdb01r-scan.ux.to2cz.cz"
database = "COCRMR"
con = Cxo.connect(username + password + at + server + database)
cur = con.cursor()
query = 'select * from onecrm.pc_product_master pcm where pcm.product_master_id = 2415'
# list of results
results = [result for result in cur.execute(query)]

cur.close()
con.close()
