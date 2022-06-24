import argparse


class ValidateLimit(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        if 0 > int(value):
            raise argparse.ArgumentTypeError("--limit should be positive integer")
        setattr(namespace, self.dest, value)
