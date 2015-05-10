#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_project
----------------------------------

Tests for `apub.model.project` module.
"""

import unittest
from apub.errors import MalformedProjectJsonError
from apub.metadata import Project


class TestProject(unittest.TestCase):

    def setUp(self):
        self.project = Project()
        pass

    def tearDown(self):
        pass

    def test_from_json_empty_string_raises_malformed_project_json_error(self):
        with self.assertRaises(MalformedProjectJsonError):
            Project.from_json('')

    def test_from_json_malformed_json_raises_malformed_project_json_error(self):
        with self.assertRaises(MalformedProjectJsonError):
            Project.from_json('{[}')

    def test_from_json_empty_json_object(self):
        project = Project.from_json('{}')

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.outputs, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_empty_dict(self):
        project = Project.from_dict({})

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.outputs, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_metadata_empty(self):
        metadata = {}
        dict_ = {
            'metadata': metadata
        }
        project = Project.from_dict(dict_)

        self.assertDictEqual(project.metadata, {})

        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.outputs, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_metadata(self):
        metadata = {
            'title': 'test'
        }
        dict_ = {
            'metadata': metadata
        }
        project = Project.from_dict(dict_)

        self.assertDictEqual(project.metadata, metadata)
        self.assertEqual(project.metadata['title'], 'test')

    def test_from_dict_chapters_empty(self):
        chapters = []
        dict_ = {
            'chapters': chapters
        }
        project = Project.from_dict(dict_)

        self.assertListEqual(project.chapters, [])

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.outputs, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_chapters_single(self):
        chapters = [{'title': 'test'}]
        dict_ = {
            'chapters': chapters
        }
        project = Project.from_dict(dict_)

        self.assertEqual(len(project.chapters), 1)
        self.assertEqual(project.chapters[0].title, 'test')

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.outputs, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_chapters_multiple(self):
        chapters = [
            {'title': 'first_chapter'},
            {'title': 'second_chapter'}
        ]
        dict_ = {
            'chapters': chapters
        }
        project = Project.from_dict(dict_)

        self.assertEqual(len(project.chapters), 2)

        # the order of the chapters *must* be preserved
        self.assertEqual(project.chapters[0].title, 'first_chapter')
        self.assertEqual(project.chapters[1].title, 'second_chapter')

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.outputs, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_outputs_empty(self):
        outputs = []
        dict_ = {
            'outputs': outputs
        }
        project = Project.from_dict(dict_)

        self.assertListEqual(project.outputs, [])

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_outputs_single(self):
        outputs = [{'type': 'html', 'name': 'test_output'}]
        dict_ = {
            'outputs': outputs
        }
        project = Project.from_dict(dict_)

        self.assertEqual(len(project.outputs), 1)
        self.assertEqual(project.outputs[0].name, 'test_output')

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_outputs_multiple(self):
        outputs = [
            {'type': 'html', 'name': 'first_output'},
            {'type': 'html', 'name': 'second_output'}
        ]
        dict_ = {
            'outputs': outputs
        }
        project = Project.from_dict(dict_)

        self.assertEqual(len(project.outputs), 2)
        self.assertEqual(project.outputs[0].name, 'first_output')
        self.assertEqual(project.outputs[1].name, 'second_output')

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.substitutions, [])

    def test_from_dict_substitutions_empty(self):
        substitutions = []
        dict_ = {
            'substitutions': substitutions
        }
        project = Project.from_dict(dict_)

        self.assertListEqual(project.substitutions, [])

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.outputs, [])

    def test_from_dict_substitutions_single(self):
        substitutions = [{'type': 'simple', 'find': 'a'}]
        dict_ = {
            'substitutions': substitutions
        }
        project = Project.from_dict(dict_)

        self.assertEqual(len(project.substitutions), 1)
        self.assertEqual(project.substitutions[0].find, 'a')

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.outputs, [])

    def test_from_dict_substitutions_multiple(self):
        substitutions = [
            {'type': 'simple', 'find': 'a'},
            {'type': 'simple', 'find': 'b'}
        ]
        dict_ = {
            'substitutions': substitutions
        }
        project = Project.from_dict(dict_)

        self.assertEqual(len(project.substitutions), 2)
        self.assertEqual(project.substitutions[0].find, 'a')
        self.assertEqual(project.substitutions[1].find, 'b')

        self.assertDictEqual(project.metadata, {})
        self.assertListEqual(project.chapters, [])
        self.assertListEqual(project.outputs, [])

    def test_from_dict(self):
        metadata = {'title': 'project_title'}
        chapters = [{'title': 'chapter_title'}]
        outputs = [{'type': 'html', 'name': 'test_output'}]
        substitutions = [{'type': 'simple', 'find': 'a'}]

        dict_ = {
            'metadata': metadata,
            'chapters': chapters,
            'outputs': outputs,
            'substitutions': substitutions
        }

        project = Project.from_dict(dict_)

        self.assertEqual(len(project.metadata), 1)
        self.assertEqual(project.metadata['title'], 'project_title')
        self.assertEqual(len(project.chapters), 1)
        self.assertEqual(project.chapters[0].title, 'chapter_title')
        self.assertEqual(len(project.outputs), 1)
        self.assertEqual(project.outputs[0].name, 'test_output')
        self.assertEqual(len(project.substitutions), 1)
        self.assertEqual(project.substitutions[0].find, 'a')



if __name__ == '__main__':
    unittest.main()
