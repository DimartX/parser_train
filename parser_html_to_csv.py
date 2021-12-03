#!/usr/bin/env python3
from bs4 import *
import bs4
import argparse

def print_info(human):
    name = human.td.next_sibling.next_sibling

    tasks = name.next_sibling.next_sibling
    print(name.text.strip(), ", ", tasks.text.strip(), end = ",")
    for task in tasks.next_siblings:
        if task is None or type(task) is bs4.element.NavigableString:
            continue
        
        if task["class"][0] == "_OverallCustomRatingFrame_delimiter":
            continue

        if "overall-custom-rating-contestant" in task["class"]:
            print("s", task.text.strip(), end = ",") # solved
        elif "overall-custom-rating-practice" in task["class"]:
            print("u", task.text.strip(), end = ",") # upsolved
        else:
            print(end = ",")
    print()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True, help='Print name of .html file with codeforces rating table')
    return parser.parse_args()

def main():
    args = parse_args()

    with open(args.name, "r") as page:
        contents = page.read()

        soup = BeautifulSoup(contents, "lxml")

        head = soup.tr
        head_bottom = head.next_sibling.next_sibling

        task = head_bottom.th
        i = 0
        for contest in head.children:
            if contest is None or type(contest) is not bs4.element.Tag or contest.text.strip() == "":
                continue
            print(contest.text.strip(), end = ',')

            i += 1
            if i < 3:
                continue
            task = task.next_sibling
            while task:
                task = task.next_sibling
                if task is None or type(task) is not bs4.element.Tag:
                    continue
                if task.text == "" and task["class"][0] == "_OverallCustomRatingFrame_delimiter":
                    task = task.next_sibling
                    break
                print(end = ",")
                
                
        print()

        head_bottom = head.next_sibling.next_sibling
        print(", ,", end = "")
        for task in head_bottom.children:
            if task is None or type(task) is not bs4.element.Tag or task.text.strip() == "":
                continue
            print(task.text.strip(), end = ',')
        print()

        
        table = soup.tbody

        for human in table.children:
            if type(human) is bs4.element.NavigableString:
                continue

            print_info(human)
                

if __name__ == "__main__":
    main()
