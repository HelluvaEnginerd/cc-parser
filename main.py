import csv
import re
import os

# chase statements key
# row[key] = <>
# 0 = Transaction Date
# 1 = Post Date
# 2 = Description
# 3 = Category
# 4 = Type
# 5 = Amount
# 6 = Memo (mostly unused)

# planned output
# Date | Place | Amount | Category | Notes

statement_dir = 'statements'

# set up output file
with open('auto_budget.csv', 'a+') as outfile:
    outfile_field_names = ['Date', 'Place', 'Amount', 'Category', 'Notes']
    writer = csv.DictWriter(outfile, fieldnames = outfile_field_names)
    writer.writeheader()
    # parse statements
    for filename in os.listdir(statement_dir):
        # ignore hidden files
        if not filename.startswith('.'):
            with open(os.path.join(statement_dir, filename)) as statement:
                print(f"parsing {filename} now")
                reader = csv.DictReader(statement, delimiter=',')
                for input_row in reader:
                    if len(input_row) == 0:
                        print("empty row, skipping")
                    elif input_row['Type'] != 'Payment':
                        notes = ""
                        # TODO - put in regex map or similar matcher with format [regex|options|here : matching category]
                        # [amazon|amzn|amazon marketplace : Amazon]
                        if re.match('amazon|amzn', input_row['Description'], re.IGNORECASE):
                            print(f"Amazon order from {input_row['Post Date']} for amount ${input_row['Amount']}.")
                            # TODO, only respect first comma and catch error if no comma
                            fin_category, notes = input("categorize as: ").split(',')
                        else:
                            fin_category = input_row['Category']
                        writer.writerow({'Date': input_row['Post Date'], 'Place': input_row['Description'], 'Amount': input_row['Amount'], 'Category': fin_category, 'Notes': notes})
                    else:
                        print(f"---\npayment posted on {input_row['Transaction Date']} for amount ${input_row['Amount']}. Not categorizing\n---")
                outfile.close
            statement.close