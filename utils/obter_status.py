import requests
from bs4 import BeautifulSoup
import json
import os

URL = "https://servizipst.giustizia.it/PST/it/pst_2_6_1.wp?actionPath=/ExtStr2/do/consultazionepubblica/sicid/contenzioso/detail.action&currentFrame=10&idfascicolo=200492369&numeroregistro=00015726&annoregistro=2023&regioneRicerca=5&ufficioRicerca=0370060094&registroRicerca=CC"
ARQUIVO_STATUS = "data/status_atual.json"

def obter_status():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")

    h3 = soup.find("h3", string=lambda text: "Elenco delle righe di storico" in text)
    ul = h3.find_next_sibling("ul") if h3 else None
    itens = ul.find_all("li") if ul else []

    status = [li.get_text(strip=True).replace('\xa0', ' ') for li in itens]

    if status:
        with open(ARQUIVO_STATUS, "w") as f:
            json.dump(status, f, indent=2, ensure_ascii=False)
        print("✅ Status salvos em:", ARQUIVO_STATUS)
    else:
        print("⚠️ Nenhum status encontrado.")

    return status

if __name__ == "__main__":
    obter_status()