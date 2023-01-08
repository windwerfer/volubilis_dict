# volubilis_dict


unofficial dictionary (stardict/mdict) files for the volubilis project (https://belisan-volubilis.blogspot.com).<br>
- 103'406 entries thai-english<br>
- 101'915 entries english-thai<br>
- thai pronounciation for most words, eg. ม้า [máa] n. classifier: ตัว
- many expressions, like: ทิ้งไว้ [thíng wái] v. exp. leave behind ; leave undone<br><br><br>

<img  style='width:90%;max-width:1445px;'  src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_thai_lookup.png'><br>
the dictioanry is bilangual: Thai-English <br><br>

<img style='width:90%;max-width:1445px;' src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_english_lookup.png'>
and English-Thai has a Level to each word, judging how basic it is (B = basic, A1 = intermediate, A2 = advanced, s = special).<br><br><br>


<img  style='width:80%;max-width:1445px;'  src='https://github.com/windwerfer/volubilis_dict/blob/main/screenshot/example_pronouciation_search-dictbox_android.png'><br>
there is a pronounciation search. eg .maa (the sound of the thai word) would find มา, ม้า and หมา. almost every word has a pronuciation entry.<br><br><br>



this project converts the Volubilis Thai-English dictionary (released as spread sheat or pdf) to a standart dictionary format.<br><br><br>



Readable through <a href='http://www.huzheng.org/stardict/'>Stardict</a> (win/linux), <a href='https://www.mdict.cn/'>Mdict</a> (android/ios), <a href='http://goldendict.org/'>GoldenDict</a> (win/linux/android), <a href='https://www.google.co.th/url?sa=t&source=web&rct=j&url=https://play.google.com/store/apps/details%3Fid%3Dcom.grandsons.dictboxxth%26hl%3Den%26gl%3DUS%26referrer%3Dutm_source%253Dgoogle%2526utm_medium%253Dorganic%2526utm_term%253Ddict%2Bbox%2Bapp%2Bstore%26pcampaignid%3DAPPU_1_nfq6Y6nnDfOgz7sPt-CzqAU&ved=2ahUKEwjpqcaUvbj8AhVz0HMBHTfwDFUQ8oQBegQIChAB&usg=AOvVaw0SlLHjPWaRVXbk4INevGNt'>Dictbox</a> (android 4-9)<br><br><br><br>



<b>Install / use:</b>
to be able to use the dictionary files, you need to download one of the dictionary apps from above and than download the compiled <a href='https://github.com/windwerfer/volubilis_dict/blob/main/volubilis_stardict_2012-11-01.zip'>stardict</a> or <a href='https://github.com/windwerfer/volubilis_dict/blob/main/volubilis_mdict-mdx_2012-11-01.zip'>mdict</a> files</a> (.mdx for Mdict, stardict for all others) and after extracting, copy them into the dictionary folder.<br><br><br><br><br><br><br><br><br>



-----
for developers:<br><br>

If you want to create your own version of the dictionary files, i uploaded the converter scipt. it is written python and converts the spreadsheat into a tab separated txt file (one entry, one line). it also adds a reverse translation from English to Thai and a pronounciation search. eg .maa (the sound of the thai word) would find มา, ม้า and หมา<br><br><br>

the script was written without any thought of publishing it (bad coding, and lots of manual intervention, so just: for research purposes), but because i use the final product myself a lot, i thought i make it available.
