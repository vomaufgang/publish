TODO
====

.. todo:: switch from .py project files to a .apub, .git like json metadata
          file or folder. Use http://www.diveintopython3.net/serializing.html
          for (de-)serialization.
          Each folder can only contain one apub project - adjust the data
          structures and classes accordingly, i.e. the Output class
          loses its project property. The project will be passed to the
          make() method as a parameter instead.

IDEAS
=====

.. todo:: Connect apub to apub-server instances via
          apub-push [*|1-5|1,3,5]

.. todo:: transfer Markdown inside JSON, let the server parse it via
          http://parsedown.org/




"""
apub make --outputs=1,2,5
apub make --outputs=1
apub make --outputs=1
apub make --outputs=1

"""


        # todo: parser for output ranges
        # everything - outputs everything in a single file using the project
        # metadata
        # books:a - outputs the book in a single file, the book metadata
        #  overrides the project metadata
        # chapters:1,2,3,4 - outputs the selected chapters into a single file
        #  using the project metadata where it applies
        # chapters:1-15
        # chapters:1-4,7,9-15
        # chapters:slug-a,slug-b
        # chapter slugs must be unique for the project
        # books:a,b,c

        # html output gets an additional parameter: output every chapter into
        #  a separate file for easy inspection

        # todo: chapters are defined @project level, books use ranges, just like outputs

        # todo resolve chapter range

        # todo redo and rethink the metadata structure - project, book, chapter
        #  for example: title and subtitle should be inherited from project
        #  to book, unless the book defines its own title or subtitle