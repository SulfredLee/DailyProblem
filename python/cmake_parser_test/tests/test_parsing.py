# Copyright 2015 Open Source Robotics Foundation, Inc.
# Copyright 2013 Willow Garage, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import parse_cmake.parsing

from parse_cmake.parsing import (
    File, Command, Comment, BlankLine, Arg, parse, FormattingOptions)


def prettify(src):
    opts = FormattingOptions()
    opts.indent = '    '
    return parse_cmake.parsing.prettify(src, opts)


class ParsingTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_parse_empty_raises_exception(self):
        self.assertEqual(File([]), parse(''))

    def test_parse_nonempty1(self):
        input = 'FIND_PACKAGE(ITK REQUIRED)'
        output = parse(input)
        expected = File([Command('FIND_PACKAGE', [Arg('ITK'), Arg('REQUIRED')])])
        msg = '\nexpected\n%s\ngot\n%s' % (repr(expected), repr(output))
        self.assertEqual(expected, output, msg)

    def test_parse_nonempty2(self):
        input = '''\
# Top level comment
FIND_PACKAGE(ITK REQUIRED)
INCLUDE(${ITK_USE_FILE})
ADD_EXECUTABLE(CastImageFilter CastImageFilter.cxx)
TARGET_LINK_LIBRARIES(CastImageFilter # inline comment 1
vtkHybrid   #inline comment 2
ITKIO ITKBasicFilters ITKCommon
)
        '''

        output = parse(input)

        expected = File([
            Comment('# Top level comment'),
            Command('FIND_PACKAGE', [Arg('ITK'), Arg('REQUIRED')]),
            Command('INCLUDE', [Arg('${ITK_USE_FILE}')]),
            BlankLine(),
            Command('ADD_EXECUTABLE', [Arg('CastImageFilter'), Arg('CastImageFilter.cxx')]),
            Command('TARGET_LINK_LIBRARIES', [
                Arg('CastImageFilter', comments=['# inline comment 1']),
                Arg('vtkHybrid', comments=['#inline comment 2']),
                Arg('ITKIO'),
                Arg('ITKBasicFilters'),
                Arg('ITKCommon'),
            ])
        ])
        msg = '\nexpected\n%s\ngot\n%s' % (expected, output)
        self.assertEqual(expected, output, msg)

    def test_idempotency_of_parsing_and_unparsing(self):
        input = '''\
# Top level comment
FIND_PACKAGE(ITK REQUIRED)
INCLUDE(${ITK_USE_FILE})
'''
        round_trip = lambda s: str(parse(s))
        self.assertEqual(round_trip(input), round_trip(round_trip(input)))

    def test_invalid_format_raises_an_exception(self):
        input = 'FIND_PACKAGE('
        self.assertRaises(Exception, parse, input)

    def test_line_numbers_in_exceptions(self):
        input = '''\
FIND_PACKAGE(ITK)
INCLUDE(
'''
        try:
            parse(input)
            self.fail('Expected an exception, but none was raised.')
        except Exception as e:
            self.assertTrue('line 2' in str(e))

    def test_arg_with_a_slash(self):
        tree = parse('include_directories (${HELLO_SOURCE_DIR}/Hello)')
        expected = File([
            Command('include_directories', [Arg('${HELLO_SOURCE_DIR}/Hello')])
        ])
        self.assertEqual(expected, tree)

    def test_command_with_no_args(self):
        tree = parse('cmd()')
        expected = File([Command('cmd', [])])
        self.assertEqual(expected, tree)

    def assertStringEqualIgnoreSpace(self, a, b):
        a2 = ''.join(a.split())
        b2 = ''.join(b.split())
        msg = '\nExpected\n%s\ngot\n%s\n(ignoring whitespace details)' % (a, b)
        self.assertEqual(a2, b2, msg)

    def test_arg_comments_preserved(self):
        input = '''
some_command(x  # inline comment about x
    )
'''
        self.assertMultiLineEqual(input, prettify(input))

    def test_comments_preserved(self):
        input = '''\
# file comment
# more about the file
# comment above Command1
command1(VERSION 2.6) # inline comment for Command1
command2(x  # inline comment about x
    "y"  # inline comment about a quoted string "y"
    ) # inline comment for Command2
'''
        self.assertMultiLineEqual(input, prettify(input))

    def test_multiline_string(self):
        s = '''
string containing
newlines
'''
        input = '''\
set (MY_STRING "%s")
''' % s
        tree = parse(input)
        expected = File([Command('set', [Arg('MY_STRING'),
                                         Arg('"' + s + '"')])])
        self.assertEqual(expected, tree)

    # TODO: test macros and functions
    def test_ifs_indented(self):
        input = '''
if(a)
    if(b)
        set(X 1)
    endif()
elseif(a)
    if(foo)
        set(Z 3)
    endif()
else(a)
    if(c)
        set(Y 2)
    endif(c)
endif(a)
'''
        self.assertMultiLineEqual(input, prettify(input))

    def test_macros_indented(self):
        input = '''
macro(hello MESSAGE)
    message(${MESSAGE})
endmacro(hello) # call the macro with the string "hello world"
hello("hello world")
'''
        self.assertUnchangedByPrettyPrinting(input)

    def test_functions_indented(self):
        input = '''
function(hello MESSAGE)
    message(${MESSAGE})
endfunction(hello) # call the macro with the string "hello world"
hello("hello world")
'''
        self.assertUnchangedByPrettyPrinting(input)

    def test_loops_indented(self):
        input = '''
foreach(var ${LIST})
    command(var)
endforeach()
while(cond)
    command(var)
endwhile()
'''
        self.assertUnchangedByPrettyPrinting(input)

    def test_breaks_commands_at_parameter_names(self):
        input = '''
set_source_files_properties(source_file.cpp
    PROPERTIES
    COMPILE_FLAGS "-Wsome-error -Wanother-error -fsome-flag")
'''
        self.assertMultiLineEqual(input, prettify(input))

    def assertUnchangedByPrettyPrinting(self, input):
        self.assertMultiLineEqual(input, prettify(input))

if __name__ == '__main__':
    unittest.main()
