__author__ = 'Christopher'

if __name__ == "__main__":
    import sys
    import os
    # The following assumes the script is in the top level of the package
    # directory.  We use dirname() to help get the parent directory to add to
    # sys.path, so that we can import the current package.  This is necessary
    # since when invoked directly, the 'current' package is not automatically
    # imported.
    #
    # credit: http://stackoverflow.com/questions/2943847
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(1, parent_dir)
    import apub
    __package__ = 'apub'
    import apub.cli
    apub.cli.main()
