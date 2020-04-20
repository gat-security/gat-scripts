import sys

from integration import openvas

tools = {
    'openvas': openvas
}

if __name__ == '__main__':
    if(len(sys.argv) == 1):
        print('Specify the tool you want to use.')
        sys.exit(1)
    tool = sys.argv[1]
    if(len(sys.argv) == 3):
        filename = sys.argv[2]
        tools[tool].main(filename)
    else:
        tools[tool].main()