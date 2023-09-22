content_st = """
#!/bin/bash

BUILD_FOLDER="../debug"
COVERAGE_FOLDER="../test_coverage"

if [ ! -d "$COVERAGE_FOLDER" ];
then
    mkdir $COVERAGE_FOLDER
fi

echo "How to view test coverage? You need to run the test first"

cd ${BUILD_FOLDER}
./test/{{ project_name }}_Test
cd -

lcov --directory ${BUILD_FOLDER} --capture --output-file ${COVERAGE_FOLDER}/code_coverage.info -rc lcov_branch_coverage=1
genhtml ${COVERAGE_FOLDER}/code_coverage.info --branch-coverage --output-directory ${COVERAGE_FOLDER}/
"""
