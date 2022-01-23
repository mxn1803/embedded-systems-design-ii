"""Adds two numbers provided by the user.

A command line utility that prompts the user for two numbers and prints their
sum. Core functionality may also be hooked into by an external module.
"""

__version__ = '1.0.0'
__author__ = 'Mike Nystoriak'
__credits__ = ['Mike Nystoriak']

class Adder:
    """Performs the addition of two numbers."""

    def add(self, a=0, b=0):
        """Hook into the core functionality of an Adder.

        Args:
            a (int): The first number, default is 0.
            b (int): The second number, default is 0.

        Returns:
            int|str: The sum of the two numbers. If an error occured, this will
            be a string containing the error message.
        """

        a, b, err = self.__sanitize(a, b)
        return a + b if not err else err

    def prompt(self):
        """Runs a small command line interface."""

        a = raw_input('Please enter a number: ')
        b = raw_input('Please enter another number: ')
        a, b, err = self.__sanitize(a, b)

        # if an entry is not an integer
        if err:
            print('\n{}\n'.format(err))
        else:
            print('\n{} + {} = {}\n'.format(a, b, self.add(a, b)))

    def __sanitize(self, a, b):
        try:
            return int(a), int(b), None
        except ValueError:
            return (
                None,
                None,
                '*** Error: Both entries must be integers! ***'
            )

def main():
    adder = Adder()
    adder.prompt()

if __name__ == '__main__':
    main()
