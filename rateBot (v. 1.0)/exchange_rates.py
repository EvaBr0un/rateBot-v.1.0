import requests
import lxml.html

def get_rate(code_ind):
    
    url = "https://cbr.ru/currency_base/daily/"

    code_ind += 2

    try:
        html_text = requests.get(url).text
    except:
        print("Error connecting to database!")

    tree = lxml.html.document_fromstring(html_text)

    tr_rate = tree.xpath("/html/body/main/div/div/div/div[3]/div/table/tbody/tr[{ind}]/td[5]".format(ind = code_ind))
    rate = tr_rate[0].text_content() 

    return rate

