from argparse import Namespace


class ArgumentModel:
    def __init__(self, source_args: Namespace):
        self.api_key = source_args.api_key
        self.symbol = source_args.symbol
        self.function = source_args.function

        # Extended argument
        self.alpha_vantage_function = self.function
