from yaml import load, Loader
from pprint import pprint

source = load(open('../files/source.yaml'), Loader=Loader)

dict_counter = 0
list_counter = 0
obj_counter = 0

mermaid = ""
indent = 4
list_item = ""


def levels(data):
    global mermaid, dict_counter, list_counter, obj_counter, indent, list_item
    data_type = type(data)

    if data_type is dict:
        for key in data.keys():
            mermaid += f"{' ' * indent}dict{dict_counter}({key})\n"
            mermaid += f"{' ' * indent}subgraph dict{dict_counter}[{key}]\n"
            mermaid += f"{' ' * indent}  direction LR\n"
            dict_counter += 1
            indent += 2
            levels(data[key])
            indent -= 2
            mermaid += f"{' ' * indent}end\n"
        return

    if data_type is list:
        counter = 0
        while counter < len(data) - 1:
            list_item = "first"
            levels(data[counter])
            list_item = "second"
            levels(data[counter + 1])
            list_item = ""
            counter += 1
        return

    if not data or data == '':
        label = "''"
    else:
        label = data
    if list_item == "first":
        mermaid += f"{' ' * indent}obj{obj_counter}({label})"
        obj_counter += 1
    elif list_item == "second":
        mermaid += f" --> obj{obj_counter + 1}({label})\n"
    else:
        mermaid += f"{' ' * indent}obj{obj_counter}({label})\n"
        obj_counter += 1
    return


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
</html>
"""


def write_mermaid():
    global mermaid
    mermaid = get_mermaid_header() + mermaid + get_mermaid_footer()
    with open('../files/mermaid.html', 'w') as f:
        f.write(mermaid)


if __name__ == '__main__':
    levels(source)
    write_mermaid()
