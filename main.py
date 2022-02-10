import csv
import re
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

with open('freedom_statement.csv') as sapphire:
    with open('auto_budget.csv', 'w+') as outfile:
        reader = csv.DictReader(sapphire, delimiter=',')
        outfile_field_names = ['Date', 'Place', 'Amount', 'Category', 'Notes']
        writer = csv.DictWriter(outfile, fieldnames = outfile_field_names) 
        writer.writeheader()
        for input_row in reader: 
            if input_row['Type'] != 'Payment':
                # TODO - notes logic
                notes = "fill this in"
                # TODO - put in map or similar matcher
                if re.match('amazon|amzn', input_row['Description'], re.IGNORECASE):
                    print(f"Amazon order from {input_row['Post Date']} for amount ${input_row['Amount']}.")
                    # todo, comma separate for category + notes
                    fin_category = input("categorize as: ")
                    print(fin_category)
                else:
                    fin_category = input_row['Category']
                writer.writerow({'Date': input_row['Post Date'], 'Place': input_row['Description'], 'Amount': input_row['Amount'], 'Category': fin_category, 'Notes': notes})
            else: 
                print(f"---\npayment posted on {input_row['Transaction Date']} for amount ${input_row['Amount']}. Not categorizing\n---")
        outfile.close
    sapphire.close