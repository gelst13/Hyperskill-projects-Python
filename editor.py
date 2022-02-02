# write your code here

formatters = ['plain', 'bold', 'italic', 'header', 'link', 'inline-code', 'ordered-list',
              'unordered-list', 'new-line']
markdown = []
formatter =''


def plain():
    user_text = input('Text: > ')
    markdown_text = user_text
    # print(markdown_text)
    markdown.append(markdown_text)


def bold():
    user_text = input('Text: > ')
    markdown_text = "**" + user_text + "**"
    # print(markdown_text)
    markdown.append(markdown_text)


def italic():
    user_text = input('Text: > ')
    markdown_text = "*" + user_text + "*"
    # print(markdown_text)
    markdown.append(markdown_text)


def header():
    heading_level = input('Level: > ')
    while True:
        try:
            if int(heading_level) not in (1, 2, 3, 4, 5, 6):
                print('The level should be within the range of 1 to 6')
                header()
            else:
                user_text = input('Text: > ')
                markdown_text = int(heading_level) * '#' + ' ' + user_text + "\n"
                # print(markdown_text)
                markdown.append(markdown_text)
                break
        except ValueError:
            print('The level should be within the range of 1 to 6')
            header()


def link():
    label = input('Label: > ')
    url = input('URL: > ')
    markdown_text = '[' + label + ']' + '(' + url + ')'
    # print(markdown_text)
    markdown.append(markdown_text)


def inline_code():
    user_text = input('Text: > ')
    markdown_text = "`" + user_text + "`"
    markdown.append(markdown_text)


def new_line():
    markdown_text = '\n'
    # print(markdown_text)
    markdown.append(markdown_text)


def special_list():
    global formatter
    try:
        rows = int(input('Number of rows: '))
        if rows > 0:
            for number in range(rows):
                row = input(f'Row  # {number + 1}: ')
                if formatter == 'ordered-list':
                    markdown_text = f"{number + 1}. {row}\n"
                else:
                    markdown_text = f"* {row}\n"
                markdown.append(markdown_text)
        else:
            print('The number of rows should be greater than zero')
            special_list()
    except ValueError:
        print('The number of rows should be greater than zero')
        special_list()


# def unordered_list():
#     try:
#         rows = int(input('Number of rows: '))
#         if rows > 0:
#             for number in range(rows):
#                 row = input(f'Row  # {number + 1}: ') + '\n'
#                 markdown_text = "* " + row
#                 markdown.append(markdown_text)
#         else:
#             print('The number of rows should be greater than zero')
#             unordered_list()
#     except ValueError:
#         print('The number of rows should be greater than zero')
#         unordered_list()


methods = {'plain': plain, 'bold': bold, 'italic': italic, 'header': header, 'link': link,
           'inline-code': inline_code, 'new-line': new_line,
           'ordered-list': special_list, 'unordered-list': special_list}


def done():
    try:
        file = open("output.md", "w")
        for item in markdown:
            file.write(item)
        file.close()
    except FileExistsError:
        print("Failed to save file.")
    quit()


def check_input():
    global formatter
    if formatter == '!done':
        done()
    elif formatter == '!help':
        print("""Available formatters: plain bold italic header link inline-code new-line
        ordered-list, unordered-list
                Special commands: !help !done""")
    elif formatter in formatters:
        return 'Ok'
    else:
        print('Unknown formatting type or command')


def print_markdown():
    print(*markdown, sep="")


def format_editor():
    global formatter
    formatter = input('Choose a formatter: ')
    if check_input() == 'Ok':
        methods[formatter]()
    print_markdown()
    format_editor()


format_editor()
