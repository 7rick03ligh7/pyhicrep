def read_txt_results(path: list) -> dict:
    data = dict()
    data['data'] = dict()
    with open(path, 'r') as f:
        for line in f:
            line = line[:-1]
            if line[0] == "@":
                chromnames = line.split(" ")[1:]
                data['chromnames'] = chromnames
            elif line[0] == "#":
                filenames = line[2:]
            else:
                scores = [float(score) for score in line.split(", ")]
                data['data'][filenames] = scores
    return data
