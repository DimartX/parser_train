#!/usr/bin/env bash

INPUT_NAME="out.html"
SOLVED_COST=1.0
UPSOLVED_COST=0.3
FINAL_COST=2.0
NUMBER_OF_FINAL_CONTEST=12
COEFFICIENT=0.019354

echo "Parsing result table..."
./parser_calculate.py --name $INPUT_NAME --solved-cost=$SOLVED_COST --upsolved-cost=$UPSOLVED_COST --final-cost=$FINAL_COST --final-contest=$NUMBER_OF_FINAL_CONTEST --coefficient=$COEFFICIENT > table.csv
echo "Parsing as original table..."
./parser_html_to_csv.py --name $INPUT_NAME > sub_table.csv
echo "Pasting original table in right of result table"
paste -d ' , '  table.csv sub_table.csv > mega_table.csv
echo "mega_table.csv created!"
(head -n 2 mega_table.csv && tail -n +3 mega_table.csv | sort -r -k2 -n -t, ) > final_table.csv
echo "final_table.csv sorted!"
rm table.csv sub_table.csv mega_table.csv
