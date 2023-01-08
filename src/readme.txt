
requirements:
pip install pyglossary regex openpyxl mdict-utils
apt install dictzip (linux)
   or
apt install dictd (on android/termux)


1) download the 'volubilis mundo.xlsx' (all languages, max wordcount) to the project folder from <a href='https://belisan-volubilis.blogspot.com/'>belisan-volubilis.blogspot.com</a>
2) open main__excel_extract_columns_to_txt-v10.py. almost at the end, set first argunent of the function call 'import_excel_file' to the filename of the downloaded file.
3) run $ python main__excel_extract_columns_to_txt-v10.py

this should create the ifo files for stardict and a txt file. the txt file can be converted to a mdx convertable txt file with $ python convert_tabTxt_to_mdxTxt.py <name.txt>.
and with $ mdict -a <name_mdx.txt> create the .mdx file
