rm -rf ./_output/*.xml
rm -f output_norm.zip
cd code
python3 main.py -n
cd -
zip -r -q output_norm.zip _output -x "*.DS_Store"
