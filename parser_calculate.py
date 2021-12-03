#!/usr/bin/env python3
from bs4 import *
import bs4
import argparse

coefficient = 2.0 / (103 + 1 / 3)

def print_info(human, solved_cost, upsolved_cost, final_cost, final_contest, coefficient):
    name = human.td.next_sibling.next_sibling

    final = 0
    solved = 0
    upsolved = 0

    tasks = name.next_sibling.next_sibling

    cnt_contests = 0

    lst_contests = []
    for task in tasks.next_siblings:
        if task is None or type(task) is bs4.element.NavigableString:
            continue

        if task["class"][0] == "_OverallCustomRatingFrame_delimiter":
            cnt_contests += 1
            lst_contests.append((solved, upsolved, final))

            solved = 0
            upsolved = 0
            continue

        if "overall-custom-rating-contestant" in task["class"] and "+" in task.text:
            if cnt_contests == final_contest:
                final += 1
            else:
                solved += 1
        elif "overall-custom-rating-practice" in task["class"] and "+" in task.text:
            upsolved += 1
    lst_contests.append((solved, upsolved, final))

    final = 0
    solved = 0
    upsolved = 0

    for contest in lst_contests:
        solved += contest[0]
        upsolved += contest[1]
        final += contest[2]

    cnt_tasks = final + solved + upsolved # сколько всего решено
    points = final * final_cost + solved * solved_cost + upsolved * upsolved_cost

    opencup = 0
    # Здесь можно навалить ифов типо
    # if name.text.strip() == "Белоусов Егор Владимирович 105":
    #     opencup = 20

    points += opencup

    # базовая информация, без опенкапов
    str_points = f'{points:.{1}f}' # округление до одного знака
    print(name.text.strip(), str_points, solved, upsolved, final, cnt_tasks, sep = ',', end = ',')

    # по опенкапам + итоговый балл на экзамен
    str_result = f'{points * coefficient:.{6}f}'
    if opencup:
        print(f'{opencup:.{1}f}', str_result, "", sep = ',')
    else:
        print('', str_result, "", sep = ',')

    if (solved == 0 and upsolved == 0):
        return 1

    return 0

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True, help='Name of .html file with codeforces rating table')
    parser.add_argument('--solved-cost', type=float, required=True, help='Cost of solved problem (1)')
    parser.add_argument('--upsolved-cost', type=float, required=True, help='Cost of upsolved problem (0.3)')
    parser.add_argument('--final-cost', type=float, required=True, help='Cost of final contest problem (0.3)')
    parser.add_argument('--coefficient', type=float, required=True, help='Coefficient to calculate final grade')
    parser.add_argument('--final-contest', type=int, required=True, help='Print the number of final contest (10-12)')
    return parser.parse_args()

def main():
    args = parse_args()

    print(",,,,,,,,,")
    print("ФИО",
          "Баллы",
          "Решено {}".format(args.solved_cost),
          "Дорешено {}".format(args.upsolved_cost),
          "Реш. финал {}".format(args.final_cost),
          "Всего задач",
          "Опенкапы,,", sep = ',')

    with open(args.name, "r") as page:
        contents = page.read()

        soup = BeautifulSoup(contents, "lxml")

        table = soup.tbody

        i = 0
        for human in table.children:
            if type(human) is bs4.element.NavigableString:
                continue
            i += 1

            if print_info(
                    human,
                    args.solved_cost,
                    args.upsolved_cost,
                    args.final_cost,
                    args.final_contest,
                    args.coefficient
            ):
                break


if __name__ == "__main__":
    main()
