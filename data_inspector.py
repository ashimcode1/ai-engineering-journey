import json
import csv

def get_rows(filepath):
    rows=[]
    with open(filepath,"r") as file:
        reader=csv.DictReader(file)
        for row in reader:
            rows.append(row)
    
    return rows

def get_columns(rows):
    return (rows[0].keys())

def count_rows(rows):
    return len(rows)

def stats(rows,column):
    values=[float(row[column]) for row in rows]
    stats={
        "min":min(values),
        "max":max(values),
        "average":round(sum(values)/len(values),4)
    }
    return stats

def inspect(filepath):
    print(f"\n loading:{filepath}")
    rows=get_rows(filepath)

    print(f"rows in the file")
    print(f"columns in the rows are:{get_columns(rows)}")

    print(f"number of columns:{count_rows(rows)}")
    
    print(f"stats are:{stats(rows,"tokens_used")}")

inspect('data.csv')