import json

def transform_json(input_data):
    output_data = []
    pk = 1
    for item in input_data:
        new_item = {
            "model": "compatability.compatability",
            "pk": pk,  # Всегда присваиваем новое значение pk
            "fields": {
                "zodiac_female": item.get("zodiac_from") or (item.get("fields") or {}).get("zodiac_from"),
                "zodiac_male": item.get("zodiac_to") or (item.get("fields") or {}).get("zodiac_to"),
                "compatability": item.get("compatability") or (item.get("fields") or {}).get("compatability")
            }
        }
        output_data.append(new_item)
        pk += 1
    return output_data

try:
    with open('input.json', 'r', encoding='utf-8') as f:
        input_json = json.load(f)

    transformed_json = transform_json(input_json)

    with open('output.json', 'w', encoding='utf-8') as outfile:
        json.dump(transformed_json, outfile, indent=2, ensure_ascii=False)

    print("JSON успешно преобразован и сохранен в файл output.json")

except FileNotFoundError:
    print("Файл input.json не найден.")
except json.JSONDecodeError as e:
    print(f"Ошибка декодирования JSON: {e}")
except Exception as e:
    print(f"Произошла ошибка: {e}")