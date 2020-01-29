







'''
===========================main==============================
===========================main==============================
===========================main==============================
'''
import read_apt_file
import op

apt_txt = read_apt_file.txt_temp

pch_txt = op.main(apt_txt)



filename_out = read_apt_file.apt_filename + '.pch'
file_out = open(filename_out, mode='w', encoding='utf-8')
for i in pch_txt:
    file_out.write(i + '\n')
file_out.close
