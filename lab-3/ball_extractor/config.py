class ConfigParser:
    def parse(self, args):
        self.__handle_help(args)
        arg_dict, err = self.__build_arg_dict(args)
        if err: return None, err

        # override defaults
        defaults = {'files': [], 'directories': [], 'output': './results'}
        config = defaults.copy()
        directory_handled = False
        schema_handled = False

        for flag, values in arg_dict.iteritems():
            if flag == '-f' or flag == '--file':
                config['files'] = config['files'] + values
            elif flag == '-d' or flag == '--directory':
                if not directory_handled:
                    config['directories'] = values
                    directory_handled = True
                else:
                    config['directories'] = config['directories'] + values
            elif flag == '-o' or flag == '--output':
                if not output_handled:
                    config['output'] = values
                else:
                    err = '*** Error: Invalid number of arguments! ***'
                    return None, err
            else:
                err = '*** Error: Invalid argument `{}`! ***'
                return None, err.format(flag)
        return config, None

    def usage(self):
        return ('Usage: python ball_extractor.py [options]'
                '\n'
                '\n    options: -f, --file      FILE         The path to a'
                '\n                                          single image file'
                '\n                                          (JPG format only).'
                '\n                                          Many single image'
                '\n                                          flags can be'
                '\n                                          passed in'
                '\n                                          succession for'
                '\n                                          processing.'
                '\n'
                '\n             -d, --directory DIRECTORY    Directory with'
                '\n                                          image files (JPG'
                '\n                                          format only). This'
                '\n                                          flag gives the'
                '\n                                          user the ability'
                '\n                                          to funnel many'
                '\n                                          images into the'
                '\n                                          processor at once'
                '\n                                          with one flag.'
                '\n'
                '\n             -o, --output    PATH         Path to the'
                '\n                                          directory that'
                '\n                                          should be'
                '\n                                          populated with the'
                '\n                                          resulting images.'
                '\n                                          If the directory'
                '\n                                          does not exist, it'
                '\n                                          will be made to'
                '\n                                          create it.'
                '\n'
                '\n             -h, --help                   Show this help'
                '\n                                          message and exit.')

    def __handle_help(self, args):
        # if no arguments provided, print usage
        if len(args) == 0:
            print('\n{}\n'.format(self.usage()))
            exit(0)

        # see if `-h` or `--help` was invoked first
        for arg in args:
            if arg == '-h' or arg == '--help':
                print('\n{}\n'.format(self.usage()))
                exit(0)

    def __build_arg_dict(self, args):
        # extract configuration
        flags = []
        values = []
        for i in range(len(args)):
            if i % 2 == 0:
                flags.append(args[i])
            else:
                values.append(args[i])

        # should have one key per one value
        if len(flags) != len(values):
            return (
                None,
                '*** Error: Invalid number of arguments! ***'
            )

        arg_dict = dict.fromkeys(flags)
        for i in range(len(flags)):
            key = flags[i]
            value = values[i]
            if not arg_dict[key]:
                arg_dict[key] = []
            arg_dict[key].append(value)
        return arg_dict, None
