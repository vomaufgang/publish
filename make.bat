@ECHO OFF

REM Command file for build automation

REM todo clean, lint, docs, dist (see Make.ps1)

if "%1" == "" goto help

if "%1" == "help" (
	:help
	echo.Please use `make ^<target^>` where ^<target^> is one of
	echo.  html       to make standalone HTML files
	goto end
)

if "%1" == "test" (
	python setup.py test
	goto end
)

if "%1" == "test-all" (
	tox
	goto end
)

if "%1" == "cover" (
	if "%2" == "show" (
	    pytest --cov-report html --cov=apub
        cd htmlcov
        index.html
        cd ..
        goto end
	)

	pytest --cov-report term-missing --cov=apub
	goto end
)

if "%1" == "docs" (
    REM Documentation: http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html
    sphinx-apidoc -o ./docs apub -e -f -T
    cd docs
    make clean
    make html
    cd ..
    goto end
)

:end