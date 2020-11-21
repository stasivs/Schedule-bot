import json

from openpyxl import load_workbook


def convert_directory(dir):
    return "json"


def convert_file(file):
    wb = load_workbook(file)
    ws = wb.active
    columns = []
    sign_of_temp_schedule = False

    for col in ws.iter_cols(min_row=3):
        cells = []
        for cell in col:
            cells.append(cell.value)

        if cells[0] or cells[1]:
            if not cells[1]:
                cells[1] = "1 группа"
            columns.append(cells)

        if "уч.нед." in str(cells[2]) or "уч.нед." in str(cells[3]):
            sign_of_temp_schedule = True

    day_of_the_week = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница"]

    pr = None
    groups = dict()
    for col in range(len(columns)):
        if columns[col][0]:
            pr = columns[col][0]
        else:
            columns[col][0] = pr

        daily_schedule = dict()

        for cel in range(1, len(columns[col]), 2):
            if columns[col][cel - 1] and not columns[col][cel]:
                columns[col][cel] = columns[col][cel - 1]

        for i in range(1, 6):
            if sign_of_temp_schedule:
                daily_schedule.update({day_of_the_week[i - 1]: columns[col][i * 12 - 9: i * 12 + 3]})
            else:
                daily_schedule.update({day_of_the_week[i - 1]: columns[col][i * 12 - 10: i * 12 + 2]})

        if columns[col][0] in groups:
            groups[columns[col][0]] += [daily_schedule]
        else:
            groups[columns[col][0]] = [daily_schedule]

    return groups


if __name__ == "__main__":
    res = convert_file("Расписания/ISA 2 1-20 jr.xlsx")

    with open("data.json", "w", encoding="utf8") as file:
        json.dump(res, file)

    print(res["ИСА 2 курс 01 группа (Б) (оч.ф.о., 08.03.01)"][0]["Четверг"])
    print(res["ИСА 2 курс 01 группа (Б) (оч.ф.о., 08.03.01)"][1]["Четверг"])