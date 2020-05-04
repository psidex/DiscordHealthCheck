Write-Host "Building /dist"
python setup.py sdist bdist_wheel

Pause

Write-Host "Uploading dist/* through twine"
twine upload dist/*
