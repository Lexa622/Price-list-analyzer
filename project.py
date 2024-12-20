import csv
import os


class PriceMachine:

    def __init__(self):
        self.data = []
        self.result = []

    def load_prices(self, file_path='.'):
        files = [file_name for file_name in os.listdir(file_path) if "price" in file_name]
        for file_name in files:
            with (open(file_name, 'r', encoding='utf-8') as file):
                reader = csv.DictReader(file)  # загружаем csv-файл

                # находим требуемые столбцы
                headers = dict()
                headers["file"] = file_name
                for field in reader.fieldnames:
                    if field.lower() in ["название", "продукт", "товар", "наименование"]:
                        headers["name"] = field
                    elif field.lower() in ["цена", "розница"]:
                        headers["price"] = field
                    elif field.lower() in ["фасовка", "масса", "вес"]:
                        headers["weight"] = field

                # если файл не содержит нужных столбцов, он пропускается
                if len(headers) != 4:
                    print(f"WARNING: пропуск файла '{file_name}' из-за неверных "
                          f"имен заголовков: {reader.fieldnames}")
                    continue

                # чтение данных из файла
                count = 1  # номер текущей строки данных в файле
                for row in reader:
                    count += 1
                    row_d = dict()
                    row_d['name'] = row[headers['name']].lower()  # название товара
                    row_d['price'] = row[headers['price']]  # цена
                    row_d['weight'] = row[headers['weight']]  # вес в кг
                    row_d['file'] = headers["file"]  # название файла
                    # рассчитываем цену за килограмм
                    row_d['price_for_kg'] = round(float(row_d['price']) / float(row_d['weight']), 2)  # цена за кг
                    self.data.append(row_d)

        # сортируем данные по цене за килограмм
        self.data = sorted(self.data, key=lambda x: x['price_for_kg'])

    def show_found_result(self):
        if self.result:
            print(f'{"№":<5} {"Наименование":38} {"цена":>7} {"вес":>4} '
                  f'{"файл":^12} {"цена за кг.":<11}')
            count = 1
            for i in self.result:
                print(f'{count:<5} '
                      f'{self.data[i]["name"]:38} '
                      f'{self.data[i]["price"]:>7} '
                      f'{self.data[i]["weight"]:>4} '
                      f'{self.data[i]["file"]:>12}  '
                      f'{self.data[i]["price_for_kg"]:<11}')
                count += 1

    def export_to_html(self, fname='output.html'):
        result = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Позиции продуктов</title>
        </head>
        <body>
            <table>
                <tr>
                    <th>Номер</th>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Фасовка</th>
                    <th>Файл</th>
                    <th>Цена за кг.</th>
                </tr>
        """
        count = 1
        for i in self.result:
            result += "<tr>"
            result += f"<td>{count}</td>"
            result += f"<td>{self.data[i]['name']}</td>"
            result += f"<td>{self.data[i]['price']}</td>"
            result += f"<td>{self.data[i]['weight']}</td>"
            result += f"<td>{self.data[i]['file']}</td>"
            result += f"<td>{self.data[i]['price_for_kg']}</td>"
            result += "</tr>\n"
            count += 1
        result += "</tbody></table></body></html>"

        # сохранение HTML в файл
        with open(fname, mode="w", encoding="utf-8") as file:
            file.write(result)

    def find_text(self, text):
        self.result = []
        index = 0
        for row in self.data:
            if text in row["name"]:
                self.result.append(index)
            index += 1


if __name__ == "__main__":
    pm = PriceMachine()
    # загружаем данные из файлов
    pm.load_prices()
    prompt = "Введите название товара или exit для выхода: "
    command = input(prompt).lower()
    while command != 'exit':
        # поиск товара по введенному названию
        pm.find_text(command)
        if not pm.result:
            print(f"Данные по запросу '{command}' отсутствуют.")
        else:
            print()
            pm.show_found_result()  # отображение результатов поиска
            print('the end\n')
            answer = input("Сохранить результаты в HTML-формате (д/н)? ")
            if answer.lower() == "д":
                while True:
                    filename = input("Введите имя HTML-файла для сохранения или exit для выхода: ").strip()
                    # проверка на ввод имени файла
                    if not filename:
                        print("ERROR: вы не ввели имя файла.")
                        continue
                    elif filename == "exit":
                        exit(0)
                    # проверка существования файла
                    if os.path.isfile(filename):
                        answer = input(f"Файл '{filename}' существует. Перезаписать (д/н)? ")
                        if answer.lower() == "д":
                            break
                    else:
                        break
                # сохранение в HTML-файл
                pm.export_to_html(fname=filename)
                print(f"Файл '{filename}' успешно сохранен.")
        command = input(prompt).lower()
