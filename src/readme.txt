
requirements:
pip install pyglossary regex openpyxl mdict-utils
apt install dictzip (linux)
   or
apt install dictd (on android/termux)


1) download the 'volubilis mundo.xlsx' (all languages, max wordcount) to the project folder from https://belisan-volubilis.blogspot.com
2) open main__excel_extract_columns_to_txt-v10.py. almost at the end, set first argunent of the function call 'import_excel_file' to the filename of the downloaded file.
3) run $ python main__excel_extract_columns_to_txt-v10.py

this should create the ifo files for stardict and a txt file. the txt file can be converted to a mdx convertable txt file with $ python convert_tabTxt_to_mdxTxt.py <name.txt>.
and with $ mdict -a <name_mdx.txt> create the .mdx file (needs mdict-utils installed 'pip install mdict-utils')


eg:
python convert_tabTxt_to_mdxTxt.py vol_mundo/d_en-th.txt
python convert_tabTxt_to_mdxTxt.py vol_mundo/d_th-en.txt
python convert_tabTxt_to_mdxTxt.py 'vol_mundo/d_th(dot+pr)-en.txt'
python convert_tabTxt_to_mdxTxt.py 'vol_mundo/d_th(pr)-en.txt'
cd vol_mundo
mdict -a d_en-th_mdx.txt volubilis_en-th_06-2023.mdx
mdict -a 'd_th(dot+pr)-en_mdx.txt' volubilis_th_Dpr-en_06-2023.mdx
mdict -a 'd_th(pr)-en_mdx.txt' volubilis_th_pr-en_06-2023.mdx
mdict -a d_th-en_mdx.txt volubilis_th-en_06-2023.mdx
