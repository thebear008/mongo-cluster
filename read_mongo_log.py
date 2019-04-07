# coding: utf-8
import re



pattern = r"\[(conn[0-9]+)\].* as principal ([^ ]+) on"

my_dict_connections = {}
with open('mongod.log', 'r') as my_f:
    for line in my_f.readlines():
        if "ACCESS" in line:
            match = re.search(pattern, line)
            if match:
                print(match.group(1))
                print(match.group(2))
                my_dict_connections[match.group(1)] = match.group(2)
            else:
                print("KO")

with open('mongod.log', 'r') as my_f:
    for line in my_f.readlines():
        if "COMMAND" in line:
            for connection in my_dict_connections:
                pattern_command = r"^([^ ]+) .* \[{}\] command ([^ ]+) ".format(connection)
                match = re.search(pattern_command, line)
                if match:
                    print(connection)
                    print(match.group(1))
                    print(match.group(2))
