from yaml import load, Loader
from pprint import pprint

source = load(open('../files/source.yaml'), Loader=Loader)

mermaid = ""
indent = 4
dict_counter = 0
list_counter = 0
obj_counter = 0
parent_type = ""
parent_key = ""
box_color = "#fff"


# Recursive function to traverse the yaml data structure and generate mermaid code
# List items are identified by a comment in the mermaid code for later reprocessing
def traverse_yaml(data):
    global mermaid, indent, dict_counter, list_counter, obj_counter, parent_type, child_key
    data_type = type(data)

    if data_type is dict:
        for key in data.keys():
            new_dict = type(data[key]) == dict or type(data[key]) == list
            add_end = False
            if new_dict:
                mermaid += f"{' ' * indent}dict{dict_counter}({key})\n"
                mermaid += f"{' ' * indent}style dict{dict_counter} fill:{get_color()}\n"
                mermaid += f"{' ' * indent}subgraph dict{dict_counter}[{key}]\n"
                mermaid += f"{' ' * indent}  direction LR\n"
                dict_counter += 1
                indent += 2
                add_end = True
            parent_type = data_type
            child_key = key
            traverse_yaml(data[key])
            if add_end:
                indent -= 2
                mermaid += f"{' ' * indent}end\n"
        return

    if data_type is list:
        list_counter += 1
        add_end = False
        if parent_type is list:
            mermaid += f"{' ' * indent}list{list_counter}\n"
            mermaid += f"{' ' * indent}subgraph list{list_counter}\n"
            mermaid += f"{' ' * indent}  direction LR\n"
            indent += 2
            add_end = True
        for item in data:
            mermaid += f"#list_item {list_counter}\n"
            parent_type = data_type
            if parent_type is list:
                child_key = ""
            traverse_yaml(item)
        if add_end:
            indent -= 2
            mermaid += f"{' ' * indent}end\n"
        return

    value = '""'
    if data:
        value = data
    annotation = ""
    if child_key:
        annotation = f"{child_key}: {value}"
    else:
        annotation = f"{value}"
    mermaid += f"{' ' * indent}obj{obj_counter}({annotation})\n"
    obj_counter += 1


def get_color():
    global box_color
    colors = ["#fff", "#ff0", "#f0f", "#0ff", "#f06", "#06F", "#0f6"]
    box_color = colors[dict_counter % len(colors)]
    return box_color


# Replaces the list items with the correct mermaid code
def get_mermaid_list():
    global mermaid
    mermaid_list = ""
    mermaid_lines = mermaid.splitlines()
    lists = {}
    for i, line in enumerate(mermaid_lines):
        if line.startswith('#'):
            list_count = line.split(' ')[1]
            if list_count not in lists:
                lists[list_count] = []
            next_line = mermaid_lines[i + 1] if i + 1 < len(mermaid_lines) else ''
            lists[list_count].append(next_line)
    for key in lists:
        count = 0
        while count < len(lists[key]) - 1:
            item = lists[key][count]
            next_item = lists[key][count + 1]
            mermaid_list += f"    {item.strip()} --> {next_item.strip()}\n"
            count += 1
    return mermaid_list


def clean_mermaid():
    global mermaid
    result = ""
    mermaid_lines = mermaid.splitlines()
    for line in mermaid_lines:
        if not line.startswith('#'):
            result += line + '\n'
    mermaid = result


def get_mermaid_header():
    return """
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>mermaid.initialize({startOnLoad:true});</script>
</head>
<body>
  <div class="mermaid">
  flowchart LR
"""


def get_mermaid_footer():
    return """
  </div>
</body>
</html>"""


def write_mermaid():
    global mermaid
    mermaid_list = get_mermaid_list()
    clean_mermaid()
    mermaid += mermaid_list
    print(mermaid)
    mermaid = get_mermaid_header() + mermaid + get_mermaid_footer()
    with open('../files/mermaid.html', 'w') as f:
        f.write(mermaid)


if __name__ == '__main__':
    traverse_yaml(source)
    write_mermaid()
