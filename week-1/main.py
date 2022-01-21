def main():
    try:
        a = int(raw_input('Please enter a number: '))
        b = int(raw_input('Please enter another number: '))
        print('\n{} + {} = {}'.format(a, b, a + b))
    except ValueError:
        print('\n*** ERROR: Both entries must be a valid number. ***\n')
        print('Exiting...')

if __name__ == '__main__':
    main()