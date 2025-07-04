import requests
from bs4 import BeautifulSoup
import numpy as np

salarios = []

# A USA TODAY usa paginação: page/1, page/2, ... até o fim (~25 páginas)
for page in range(1, 48):
    url = f"https://databases.usatoday.com/major-league-baseball-salaries-2025/page/{page}/"
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Encontra linhas no formato "Player. Team. Position. Salary. ..."
    rows = soup.select("table tr")
    if not rows:
        break  # sem mais tabelas, encerra
    for tr in rows:
        cols = tr.get_text(separator="|").split("|")
        # O campo Salary geralmente aparece como "$XX,YYY,YYY"
        for part in cols:
            if part.startswith("$"):
                text = part.replace("$","").replace(",","")
                try:
                    salarios.append(float(text))
                except:
                    pass

print(f"Total de salários coletados: {len(salarios)}")

arr = np.array(salarios)
print(f"Média: US$ {arr.mean():,.2f}")
print(f"Mediana: US$ {np.median(arr):,.2f}")
