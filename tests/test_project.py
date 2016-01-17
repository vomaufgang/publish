#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project
----------------------------------

Tests for `apub.model.project` module.
"""

import unittest
from apub.book import Book


class TestProject(unittest.TestCase):
    # todo: Write tests for mandatory properties

    def test_from_directory(self):
        pass
        # todo reuse this to test input.py read_project
        # import os
        # metadata = {
        #     'title': 'Once There Was A Test',
        #     'series': 'Testiliscious',
        #     'authors': 'Unit Test',
        #     'publisher': 'UT',
        #     'language': 'UND',
        #     'genre': '',
        #     'state': 'ongoing'
        # }
        #
        # script_path = os.path.dirname(os.path.abspath(__file__))
        # project_path = os.path.join(script_path, '../resources')
        #
        # project = Book.from_directory(project_path)
        #
        # # todo implement the missing assertions
        #
        # self.assertDictEqual(project.metadata, metadata)

    def test_from_file_file_does_not_exist(self):
        pass
        # todo reuse for input.py read_project
        # import os
        # this_file_should_not_exist = os.path.join(
        #    os.path.dirname(__file__),
        #    '../resources/nope.jpeg')

        # with self.assertRaises(FileNotFoundError):
        # Book.from_file(this_file_should_not_exist)

    def test_from_json_empty_string_raises_malformed_project_json_error(self):
        pass
        # todo reuse for input.py read_project
        # with self.assertRaises(MalformedProjectJsonError):
        #    Book.from_json('')

    def test_from_json_malformed_json_raises_malformed_project_json_error(self):
        pass
        # todo reuse for input.py read_project
        # with self.assertRaises(MalformedProjectJsonError):
        #    Book.from_json('{[}')

    def test_from_dict_empty_dict(self):
        project = Book.from_dict({})

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])

    def test_from_dict_metadata_empty(self):
        metadata = {}
        dict_ = {
            'metadata': metadata
        }
        book = Book.from_dict(dict_)

        self.assertDictEqual(book.metadata, {})
        self.assertListEqual(book.chapters, [])

    def test_from_dict_metadata(self):
        metadata = {
            'title': 'test'
        }
        dict_ = {
            'metadata': metadata
        }
        project = Book.from_dict(dict_)

        self.assertDictEqual(project.metadata, metadata)
        self.assertEqual(project.metadata['title'], 'test')

    def test_from_dict_chapters_empty(self):
        chapters = []
        dict_ = {
            'chapters': chapters
        }
        project = Book.from_dict(dict_)

        self.assertListEqual(project.chapters, [])

        self.assertDictEqual(project.metadata, {})

    def test_from_dict_chapters_single(self):
        chapters = [{'title': 'test', 'source': 'source'}]
        dict_ = {
            'chapters': chapters
        }
        project = Book.from_dict(dict_)

        self.assertEqual(len(project.chapters), 1)
        self.assertEqual(project.chapters[0].title, 'test')

        self.assertDictEqual(project.metadata, {})

    def test_from_dict_chapters_multiple(self):
        chapters = [
            {'title': 'first_chapter', 'source': 'source'},
            {'title': 'second_chapter', 'source': 'source'}
        ]
        dict_ = {
            'chapters': chapters
        }
        project = Book.from_dict(dict_)

        self.assertEqual(len(project.chapters), 2)

        # the order of the chapters *must* be preserved
        self.assertEqual(project.chapters[0].title, 'first_chapter')
        self.assertEqual(project.chapters[1].title, 'second_chapter')

        self.assertDictEqual(project.metadata, {})

    def test_from_dict_outputs_empty(self):
        pass
        # todo reuse for test_project
        # outputs = []
        # dict_ = {
        #     'outputs': outputs
        # }
        # project = Book.from_dict(dict_)
        #
        # self.assertListEqual(project.outputs, [])
        #
        # self.assertDictEqual(project.metadata, {})
        # self.assertListEqual(project.chapters, [])
        # self.assertListEqual(project.substitutions, [])

    def test_from_dict_outputs_single(self):
        pass
        # todo reuse for test_project
        # outputs = [{
        #         'type': 'html',
        #         'name': 'test_output',
        #         'path': 'output_path',
        #         'css': 'output_css'
        #     }]
        # dict_ = {
        #     'outputs': outputs
        # }
        # project = Book.from_dict(dict_)
        #
        # self.assertEqual(len(project.outputs), 1)
        # self.assertEqual(project.outputs[0].name, 'test_output')
        #
        # self.assertDictEqual(project.metadata, {})
        # self.assertListEqual(project.chapters, [])
        # self.assertListEqual(project.substitutions, [])

    def test_from_dict_outputs_multiple(self):
        pass
        # todo reuse for test_project
        # outputs = [
        #     {
        #         'type': 'html',
        #         'name': 'first_output',
        #         'path': 'output_path',
        #         'css': 'output_css'
        #     },
        #     {
        #         'type': 'html',
        #         'name': 'second_output',
        #         'path': 'output_path',
        #         'css': 'output_css'
        #     }
        # ]
        # dict_ = {
        #     'outputs': outputs
        # }
        # project = Book.from_dict(dict_)
        #
        # self.assertEqual(len(project.outputs), 2)
        # self.assertEqual(project.outputs[0].name, 'first_output')
        # self.assertEqual(project.outputs[1].name, 'second_output')
        #
        # self.assertDictEqual(project.metadata, {})
        # self.assertListEqual(project.chapters, [])
        # self.assertListEqual(project.substitutions, [])

    def test_from_dict_substitutions_empty(self):
        pass
        # todo reuse for test_project
        # substitutions = []
        # dict_ = {
        #     'substitutions': substitutions
        # }
        # project = Book.from_dict(dict_)
        #
        # self.assertListEqual(project.substitutions, [])
        #
        # self.assertDictEqual(project.metadata, {})
        # self.assertListEqual(project.chapters, [])
        # self.assertListEqual(project.outputs, [])

    def test_from_dict_substitutions_single(self):
        pass
        # todo reuse for test_project
        # substitutions = [{'type': 'simple', 'find': 'a'}]
        # dict_ = {
        #     'substitutions': substitutions
        # }
        # project = Book.from_dict(dict_)
        #
        # self.assertEqual(len(project.substitutions), 1)
        # self.assertEqual(project.substitutions[0].find, 'a')
        #
        # self.assertDictEqual(project.metadata, {})
        # self.assertListEqual(project.chapters, [])
        # self.assertListEqual(project.outputs, [])

    def test_from_dict_substitutions_multiple(self):
        pass
        # todo reuse for test_project
        # substitutions = [
        #     {'type': 'simple', 'find': 'a'},
        #     {'type': 'simple', 'find': 'b'}
        # ]
        # dict_ = {
        #     'substitutions': substitutions
        # }
        # project = Book.from_dict(dict_)
        #
        # self.assertEqual(len(project.substitutions), 2)
        # self.assertEqual(project.substitutions[0].find, 'a')
        # self.assertEqual(project.substitutions[1].find, 'b')
        #
        # self.assertDictEqual(project.metadata, {})
        # self.assertListEqual(project.chapters, [])
        # self.assertListEqual(project.outputs, [])

    def test_from_dict(self):
        metadata = {'title': 'project_title'}
        chapters = [{'title': 'chapter_title', 'source': 'chapter_source'}]
        outputs = [
            {
                'type': 'html',
                'name': 'test_output',
                'path': 'output_path',
                'css': 'output_css'
            }
        ]
        substitutions = [{'type': 'simple', 'find': 'a'}]

        dict_ = {
            'metadata': metadata,
            'chapters': chapters,
            'outputs': outputs,
            'substitutions': substitutions
        }

        project = Book.from_dict(dict_)

        self.assertEqual(len(project.metadata), 1)
        self.assertEqual(project.metadata['title'], 'project_title')
        self.assertEqual(len(project.chapters), 1)
        self.assertEqual(project.chapters[0].title, 'chapter_title')


if __name__ == '__main__':
    unittest.main()
