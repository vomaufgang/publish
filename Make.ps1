function clean-build(){
    Remove-Item .\build -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item .\dist -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item .\*.egg-info -Recurse -Force -ErrorAction SilentlyContinue
}

function clean-pyc(){
    Remove-Item .\*.pyc -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item .\*.pyo -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item .\*~ -Recurse -Force -ErrorAction SilentlyContinue
}

function clean(){
    clean-build
    clean-pyc
    Remove-Item .\htmlcov -Recurse -Force -ErrorAction SilentlyContinue
}

function get-coverage(){
    &nosetests --with-coverage --cover-html --cover-html-dir=htmlcov
    Invoke-Item .\htmlcov\index.html
}

function lint(){
    &pylint apub tests
}

function test(){
    &python setup.py test
}

function test-all(){
    &tox
}

function docs(){
	Remove-Item .\docs\apub.rst
	Remove-Item .\docs\apub.*.rst
    Remove-Item .\docs\modules.rst
    &sphinx-apidoc -o docs/ apub
    Push-Location .\docs
    &.\make.bat clean
    &.\make.bat html
    Pop-Location
    Invoke-Item docs/_build/html/index.html
}

function dist(){
    clean
    &python setup.py sdist
    &python setup.py bdist_wheel
    Get-ChildItem .\dist
}

$action = $args[0]

if ($action -eq "coverage"){
    $action = "get-coverage"
}

Invoke-Expression "$action"