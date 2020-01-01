from argparse import ArgumentParser

from engorgio.parser import make_parser


def assert_parsed(cmdline, parser=make_parser(), **attrs):
    try:
        args = parser.parse_args(cmdline)
    except SystemExit:
        assert False, f"Parser didn't accept this cmdline {cmdline}"
    else:
        for name, expected in attrs.items():
            try:
                current = getattr(args, name)
            except AttributeError:
                assert False, f"Namespace does not contain {name}"
            else:
                assert current == expected, "Values doesn't match"


def test_generates_an_argumentparser():
    assert isinstance(make_parser(), ArgumentParser)


def test_parse_source_path():
    assert_parsed(['FOO'], source='FOO')
