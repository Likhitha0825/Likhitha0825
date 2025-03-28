from collections import defaultdict

# Function to parse the list into a dictionary
def parse_list(lst):
    page_dict = defaultdict(set)
    for entry in lst:
        page, rows = entry.split(' : ')
        row_numbers = set(rows.replace("Row-", "").split(", "))
        page_dict[page] = row_numbers
    return page_dict

# Given lists
list1 = [
    'Page 18 : Row-27, Row-28', 'Page 19 : Row-51, Row-52', 'Page 20 : Row-56', 
    'Page 1 : Row-2, Row-3, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-22, Row-23, Row-24, Row-25', 
    'Page 2 : Row-27, Row-28, Row-29, Row-30, Row-31, Row-32, Row-33, Row-34, Row-35, Row-36, Row-40, Row-41, Row-42, Row-43, Row-44, Row-45, Row-46, Row-47', 
    'Page 3 : Row-19, Row-20, Row-21, Row-22, Row-23, Row-24', 'Page 4 : Row-28, Row-46, Row-47, Row-49, Row-50', 
    'Page 5 : Row-55, Row-56', 'Page 6 : Row-2, Row-3, Row-4, Row-5, Row-6, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-21, Row-22, Row-23, Row-24, Row-25', 
    'Page 7 : Row-26, Row-27, Row-28, Row-29, Row-30, Row-31, Row-32, Row-33, Row-34, Row-35, Row-36, Row-37', 
    'Page 10 : Row-18, Row-20', 'Page 11 : Row-4, Row-5', 'Page 12 : Row-21, Row-22', 
    'Page 13 : Row-44, Row-45', 'Page 14 : Row-13, Row-27', 'Page 15 : Row-46, Row-47', 
    'Page 16 : Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-17, Row-20, Row-21, Row-22', 
    'Page 17 : Row-27, Row-28, Row-37, Row-41, Row-42, Row-44, Row-45'
]

list2 = [
    'Page 18 : Row-27, Row-28', 'Page 19 : Row-51, Row-52', 'Page 20 : Row-56', 
    'Page 1 : Row-2, Row-3, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-22, Row-23, Row-24, Row-25', 
    'Page 2 : Row-27, Row-28, Row-29, Row-30, Row-31, Row-32, Row-33, Row-34, Row-35, Row-36, Row-40, Row-41, Row-42, Row-43, Row-44, Row-45, Row-46, Row-47', 
    'Page 3 : Row-19, Row-20, Row-21, Row-22, Row-23, Row-24', 'Page 4 : Row-28, Row-46, Row-47, Row-49, Row-50', 
    'Page 5 : Row-55, Row-56', 'Page 6 : Row-2, Row-3, Row-4, Row-5, Row-6, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-16, Row-17, Row-18, Row-19, Row-20, Row-21, Row-22, Row-23, Row-24, Row-25', 
    'Page 7 : Row-29, Row-30', 'Page 10 : Row-18, Row-20', 'Page 11 : Row-4, Row-5', 
    'Page 12 : Row-2, Row-3, Row-21, Row-22', 'Page 13 : Row-44, Row-45', 'Page 14 : Row-13, Row-27', 
    'Page 15 : Row-46, Row-47', 'Page 16 : Row-2, Row-3, Row-7, Row-8, Row-9, Row-10, Row-11, Row-12, Row-13, Row-14, Row-15, Row-17, Row-20, Row-21, Row-22', 
    'Page 17 : Row-27, Row-28, Row-37, Row-41, Row-42, Row-43, Row-44, Row-45'
]

# Parse both lists
dict1 = parse_list(list1)
dict2 = parse_list(list2)

# Compare list2 against list1 and find differences
difference_from_before = []
for page, rows in dict2.items():
    if page in dict1:
        new_rows = rows - dict1[page]
        if new_rows:
            difference_from_before.append(f"{page} : " + ", ".join(sorted(f"Row-{row}" for row in new_rows)))
    else:
        difference_from_before.append(f"{page} : " + ", ".join(sorted(f"Row-{row}" for row in rows)))

# Print final difference list
print(difference_from_before)
