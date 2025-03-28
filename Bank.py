from collections import defaultdict

list1 = [
    "Page 18 : Row-27, Row-28", "Page 19 : Row-51, Row-52", "Page 20 : Row-56",
    "Page 1 : Row-2, Row-3, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-22, Row-23, Row-24, Row-25",
    "Page 2 : Row-27, Row-28, Row-29, Row-30, Row-31, Row-32, Row-33, Row-34, Row-35, Row-36, Row-40, Row-41, Row-42, Row-43, Row-44, Row-45, Row-46, Row-47",
    "Page 3 : Row-19, Row-20, Row-21, Row-22, Row-23, Row-24",
    "Page 4 : Row-28, Row-46, Row-47, Row-49, Row-50", "Page 5 : Row-55, Row-56",
    "Page 6 : Row-2, Row-3, Row-4, Row-5, Row-6, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-21, Row-22, Row-23, Row-24, Row-25",
    "Page 7 : Row-26, Row-27, Row-28, Row-29, Row-30, Row-31, Row-32, Row-33, Row-34, Row-35, Row-36, Row-37",
    "Page 10 : Row-18, Row-20", "Page 11 : Row-4, Row-5",
    "Page 12 : Row-21, Row-22", "Page 13 : Row-44, Row-45",
    "Page 14 : Row-13, Row-27", "Page 15 : Row-46, Row-47",
    "Page 16 : Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-17, Row-20, Row-21, Row-22",
    "Page 17 : Row-27, Row-28, Row-37, Row-41, Row-42, Row-44, Row-45"
]

list2 = [
    "Page 18 : Row-27, Row-28", "Page 19 : Row-51, Row-52", "Page 20 : Row-56",
    "Page 1 : Row-2, Row-3, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-22, Row-23, Row-24, Row-25",
    "Page 2 : Row-27, Row-28, Row-29, Row-30, Row-31, Row-32, Row-33, Row-34, Row-35, Row-36, Row-40, Row-41, Row-42, Row-43, Row-44, Row-45, Row-46, Row-47",
    "Page 3 : Row-19, Row-20, Row-21, Row-22, Row-23, Row-24",
    "Page 4 : Row-28, Row-46, Row-47, Row-49, Row-50", "Page 5 : Row-55, Row-56",
    "Page 6 : Row-2, Row-3, Row-4, Row-5, Row-6, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-21, Row-22, Row-23, Row-24, Row-25",
    "Page 7 : Row-29, Row-30", "Page 10 : Row-18, Row-20",
    "Page 11 : Row-4, Row-5", "Page 12 : Row-2, Row-3, Row-21, Row-22",
    "Page 13 : Row-44, Row-45", "Page 14 : Row-13, Row-27",
    "Page 15 : Row-46, Row-47",
    "Page 16 : Row-2, Row-3, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-17, Row-20, Row-21, Row-22",
    "Page 17 : Row-27, Row-28, Row-37, Row-41, Row-42, Row-43, Row-44, Row-45"
]

def parse_list(data):
    """Parses the list into a dictionary with page numbers as keys and sets of rows as values."""
    parsed_data = defaultdict(set)
    for item in data:
        page, rows = item.split(" : ")
        parsed_data[page] = set(rows.split(", "))
    return parsed_data

def find_differences(list1, list2):
    """Finds missing rows for each page in list2 compared to list1 and extra rows in list2."""
    data1 = parse_list(list1)
    data2 = parse_list(list2)

    difference = []
    
    for page in data1:
        if page in data2:
            missing_rows = data1[page] - data2[page]  # Rows in list1 but not in list2
            if missing_rows:
                difference.append(f"{page} : {', '.join(sorted(missing_rows, key=lambda x: int(x.split('-')[1])))}")
        else:
            difference.append(f"{page} : {', '.join(sorted(data1[page], key=lambda x: int(x.split('-')[1])))}")

    # Check for extra rows in list2 that don't exist in list1
    for page in data2:
        if page in data1:
            extra_rows = data2[page] - data1[page]  # Rows in list2 but not in list1
            if extra_rows:
                difference.append(f"{page} : {', '.join(sorted(extra_rows, key=lambda x: int(x.split('-')[1])))}")

    return difference

difference = find_differences(list1, list2)
print(difference)
