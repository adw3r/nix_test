from src import parser, utils


def main():
    args = utils.create_args()
    input_data = utils.get_data(args.file)
    repo_hrefs = parser.retrieve_info(input_data)
    print(repo_hrefs)


if __name__ == '__main__':
    main()
