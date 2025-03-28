def parse_list(data):
    """Parses the list into a dictionary with page numbers as keys and sets of rows as values."""
    parsed_data = {}
    for item in data:
        page, rows = item.split(" : ")
        parsed_data[page] = set(rows.split(", "))
    return parsed_data

def find_differences(list1, list2):
    """Finds differences where:
       1. Pages in list2 do not exist in list1.
       2. Pages exist in both lists but have extra rows in list2.
    """
    data1 = parse_list(list1)
    data2 = parse_list(list2)

    difference = []

    for page, rows in data2.items():
        if page not in data1:  
            # Entire page is missing in list1
            difference.append(f"{page} : {', '.join(sorted(rows, key=lambda x: int(x.split('-')[1])))}")
        else:
            # Check for extra rows in list2 for the same page
            extra_rows = rows - data1[page]  
            if extra_rows:
                difference.append(f"{page} : {', '.join(sorted(extra_rows, key=lambda x: int(x.split('-')[1])))}")

    return difference

list1 = [
    'Page 1 : Row-1', 'Page 7 : Row-62', 'Page 8 : Row-1', 'Page 15 : Row-77', 
    'Page 16 : Row-1', 'Page 24 : Row-83', 'Page 25 : Row-1', 'Page 34 : Row-94', 
    'Page 35 : Row-1', 'Page 43 : Row-89', 'Page 44 : Row-1', 'Page 52 : Row-84', 
    'Page 53 : Row-1', 'Page 59 : Row-61'
]

list2 = [
    'Page 1 : Row-1', 'Page 4 : Row-31', 'Page 7 : Row-62', 'Page 8 : Row-1', 
    'Page 15 : Row-77', 'Page 16 : Row-1', 'Page 24 : Row-83', 'Page 25 : Row-1', 
    'Page 34 : Row-94', 'Page 35 : Row-1', 'Page 39 : Row-42', 'Page 43 : Row-89', 
    'Page 44 : Row-1', 'Page 52 : Row-84', 'Page 53 : Row-1', 'Page 59 : Row-61'
]

difference = find_differences(list1, list2)
print(difference)
