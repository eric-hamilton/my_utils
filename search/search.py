import csv
import sys
import os
import re
import io


def get_args(query):
    find = {
        "lower":[],
        "case_sensitive":[]
    }
    
    exclude = {
        "lower":[],
        "case_sensitive":[]
    }
    
    quotes = ['"', "'"]
    for x in query.split(" "):
        if len(x) >=2:
            if x[0]=="!":
                if len(x) >= 3:
                    if x[1] in quotes and x[-1] == x[1]:
                        exclude["case_sensitive"].append(x[2:-1])
                    else:
                        exclude["lower"].append(x[1:].lower())
                        
                else:
                    exclude["lower"].append(x[1:].lower())
            
            else:
                if len(x) >=2:
                    if x[0] in quotes and x[-1] == x[0]:
                        find["case_sensitive"].append(x[1:-1])
                    else:
                        find["lower"].append(x.lower())
                else:
                    find["lower"].append(x.lower())
                    
    
    print("find", find)
    print("exclude", exclude)
    return find, exclude

def search_text(file_path, find, exclude):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_lower = line.lower()
            if all(term in line for term in find["case_sensitive"] + find["lower"]) and \
               not any(ex_term in line for ex_term in exclude["case_sensitive"] + exclude["lower"]):
                results.append(line.rstrip('\n'))
    return results

def search_csv(file_path, find, exclude):
    results = []
    pre_exclude = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if all(any(term in cell.lower() for cell in row) for term in find["lower"]):
                if all(any(term in cell for cell in row) for term in find["case_sensitive"]):
                    pre_exclude.append(list(row)) 
    
    for item in pre_exclude:
        add = True
        if any(term in x for x in item for term in exclude["case_sensitive"]):
            add = False
        if any(term in x.lower() for x in item for term in exclude["lower"]):
            add = False
            
        if add:
            results.append(item)
            
    return results    

def determine_file_type(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == '.txt':
        return 'text'
    elif file_extension.lower() == '.csv':
        return 'csv'
    else:
        return None

def write_output_text(results, output_name):
    with open(output_name, "w") as outfile:
        for result in results:
            outfile.write(result + '\n')
            
def write_output_csv(results, output_name):
    with open(output_name, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(results)
 
def dump_seeds_to_console(results):
    hash_pattern = re.compile(r'\b[0-9a-fA-F]{40}\b')
    seeds = hash_pattern.findall(results)
    for seed in seeds:
        print(seed)

def main(): 
    csv_header = None
    file_path = None
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = input("type a filename\n")
    filename = os.path.basename(file_path)    

    while True:
        query = input(f"enter search query for {filename}. (Enter nothing to exit)\n")
        if not query:
            sys.exit()
        
        find, exclude = get_args(query)
        
        file_type = determine_file_type(file_path)
        search_results = []

        try:
            if file_type == "text":
                search_results = search_text(file_path, find, exclude)
            elif file_type == "csv":
                search_results = search_csv(file_path, find, exclude)
        except Exception as e:
            print(e)

        print(f"Found {len(search_results)} results.")
        
        # Limit output to 100 searches
        if len(search_results) > 100:
            choice = input("There are a lot of results. Do you want to print to console? y/n\n").lower()
            if choice in ["y", "yes"]:
                for result in search_results:
                    if isinstance(result, list):
                        print(" ".join(result))
                    else:
                        print(result)
            else:
                print()
        else:
            for result in search_results:
                if isinstance(result, list):
                    print(" ".join(result))
                else:
                    print(result)

        if search_results:
            choice = input("Write to file? y/n\n").lower()
            if choice in ["y", "yes"]:
                if file_type == "text":
                    output_name = f"{filename}_{query}.txt"
                    write_output_text(search_results, output_name)
                elif file_type == "csv":
                    output_name = f"{filename}_{query}.csv"
                    write_output_csv(search_results, output_name)

            elif choice in ["s", "seeds"]:
                if file_type == "csv":
                    output = io.StringIO()
                    writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
                    writer.writerow(search_results)
                    search_results = output.getvalue()
                dump_seeds_to_console(search_results)
        print("")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input("Press Enter to Exit")
