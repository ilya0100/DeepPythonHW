def filter_file(file, word_list):
    is_open = False
    if isinstance(file, str):
        file = open(file, "r", encoding="utf-8")
        is_open = True

    for line in file:
        words = line.lower().split()
        for word in word_list:
            if word.lower() in words:
                yield line
                break

    if is_open:
        file.close()
