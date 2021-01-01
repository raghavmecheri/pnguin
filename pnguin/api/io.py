def read_csv_to_data(path: str, delimiter: str = ",", headers: list = []):
    data = []
    with open(path, "r") as f:
        header = headers
        if len(headers) == 0:
            header = f.readline().split(",")
        for line in f:
            entry = {}
            for i, value in enumerate(line.split(",")):
                entry[header[i].strip()] = value.strip()
            data.append(entry)
    return data


def print_warning(message, to_warn):
    if to_warn:
        print("Warning: {}".format(message))
