import requests
import lxml.html
import ssl
from urllib3 import poolmanager

class TLSAdapter(requests.adapters.HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLS,
                ssl_context=ctx)

def get_rate(code_ind):
    
    url = "https://cbr.ru/currency_base/daily/"

    code_ind += 2

    try:
        session = requests.session()
        session.mount('https://', TLSAdapter())
        html_text = session.get(url).text
    except:
        print("Connection error!")

    tree = lxml.html.document_fromstring(html_text)

    tr_rate = tree.xpath("/html/body/main/div/div/div/div[3]/div/table/tbody/tr[{ind}]/td[5]".format(ind = code_ind))
    rate = tr_rate[0].text_content() 

    return rate

