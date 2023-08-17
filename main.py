import requests
import csv
from collections import defaultdict

# Extração
def extrair_dados(api_url):
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Erro na solicitação HTTP:", response.status_code)
        return None

api_url = "https://data.cdc.gov/resource/n8mc-b4w4.json"
raw_data = extrair_dados(api_url)

# Transformação
def transformar_dados(raw_data):
    transformed_data = []

    age_group_stats = defaultdict(lambda: {"count": 0, "deaths": 0})

    for entry in raw_data:
        if entry["current_status"] == "Laboratory-confirmed case":
            transformed_entry = {
                "case_month": entry["case_month"],
                "res_state": entry["res_state"],
                "res_county": entry["res_county"],
                "age_group": entry["age_group"],
                "sex": entry["sex"],
                "death_yn": entry["death_yn"]
            }
            transformed_data.append(transformed_entry)

            age_group = entry["age_group"]
            deaths = 1 if entry["death_yn"] == "Yes" else 0

            age_group_stats[age_group]["count"] += 1
            age_group_stats[age_group]["deaths"] += deaths

    return transformed_data, age_group_stats

transformed_data, age_group_stats = transformar_dados(raw_data)

# Carregar
def carregar_dados(age_group_stats, output_file):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Grupo Etário", "Total de Casos", "Óbitos", "Taxa de Óbito (%)"])

        for age_group, stats in age_group_stats.items():
            death_rate = stats["deaths"] / stats["count"] * 100
            writer.writerow([age_group, stats["count"], stats["deaths"], f"{death_rate:.2f}"])

stats_output_file = "resultado.csv"
carregar_dados(age_group_stats, stats_output_file)

# Imprimir estatísticas por grupo etário
print("Estatísticas por Grupo Etário:")
for age_group, stats in age_group_stats.items():
    death_rate = stats["deaths"] / stats["count"] * 100
    print(f"Grupo Etário: {age_group}, Total de Casos: {stats['count']}, Óbitos: {stats['deaths']}, Taxa de Óbito: {death_rate:.2f}%")
