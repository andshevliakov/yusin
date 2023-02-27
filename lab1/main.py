from menu.menu import vector_model, boolean_model
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Incorrect number of arguments")
        sys.exit(1)

    if sys.argv[1] == "--boolean":
        boolean_model()
    elif sys.argv[1] == "--vector":
        vector_model()
    else:
        print("Incorrect argument")
        sys.exit(1)


if __name__ == "__main__":
    main()
