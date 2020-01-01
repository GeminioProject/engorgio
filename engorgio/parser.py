from argparse import ArgumentParser


def make_parser():
    parser = ArgumentParser()
    parser.add_argument('source')
    return parser
