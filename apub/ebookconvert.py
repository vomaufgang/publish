__author__ = 'Christopher'


def convert(input_file, output_file, options=None):
    if not input_file:
        raise AttributeError('input_file')

    if not output_file:
        raise AttributeError('output_file')

    # if not options:
    #     if '.epub' in output_file


__format_exclusive_options = {
    'epub': [
        'input-encoding'
    ]
}
