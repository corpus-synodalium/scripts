rm -rf ./_output/*.xml
cd code
python3 main.py
cd -
zip -r output.zip _output -x "*.DS_Store"
