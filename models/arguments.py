from argparse import Namespace


class ArgumentModel:
    def __init__(self, source_args: Namespace):
        self.api_key = source_args.api_key
        self.stock = source_args.stock
        self.alpha_function = source_args.alpha_function
