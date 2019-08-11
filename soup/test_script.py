import os
import argparse
from os import path


if __name__ == "__main__":
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument('--test_dir', help='test dir', required=True)
	args = arg_parser.parse_args()

	assert path.exists(args.test_dir), '{} does not exist'.format(args.test_dir)
	test_dir = args.test_dir
	pascal_files = os.listdir(test_dir)
	pascal_files = [pascal_file for pascal_file in pascal_files if pascal_file.endswith('.pas')]
	for pascal_file in pascal_files:
		name, _ = path.splitext(pascal_file)
		os.system("./soup.py --input {} --output {}"
					.format(path.join(test_dir, pascal_file), path.join(test_dir, name + '.out')))
