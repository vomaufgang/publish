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
	nosetests
	goto end
)

if "%1" == "test-all" (
	tox
	goto end
)

if "%1" == "cover" (
	nosetests && coverage html
	if "%2" == "show" (
        cd htmlcov
        index.html
        cd ..
	)
	goto end
)

if "%1" == "docs" (
    del docs\apub.rst
    del docs\modules.rst
    sphinx-apidoc -o ./docs apub
    cd docs
    make html
    cd ..
    goto end
)

:end