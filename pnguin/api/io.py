"""A collection of io related helper methods.
"""


def read_csv_to_data(path: str, delimiter: str = ",", headers: list = []):
    """A zero-dependancy helper method to read a csv file

    Given the path to a csv file, read data row-wise. This data may be later converted to a dict of lists if needed (column-wise).

    Args:
        path (str): Path to csv file
        delimiter (str, optional): Delimiter to split the rows by. Defaults to ','
        headers: (list, optional): Given header list for a csv file. Defaults to an empty list, which results in the first row being used as a header.

    Returns:
        A list of dictionary values (list of rows) representing the file being read

    """
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
    """Helper method to print warnings

    Given a message, print it with the "Warning: " prefix as long as the to_warn flag is true

    Args:
        message (str): The message to print
        to_warn (bool): Whether warnings are turned on or not

    """
    if to_warn:
        print("Warning: {}".format(message))
