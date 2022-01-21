class Adder:
    def add(self, a=0, b=0):
        a, b, err = self.__sanitize(a, b)
        return a + b if not err else err

    def prompt(self):
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
            return None, None, '*** Error: Both entries must be integers! ***'


def main():
    adder = Adder()
    adder.prompt()

if __name__ == '__main__':
    main()
