#Each output file corresponding to an exon shold be named as (or contain): "exonX-Y.txt", where X is
#the number os exon and Y is the number of HotSpot output for the same exon 
#Similarly, for oligoes the file should be named as (or contain): "exonX_oligoY-Z.txt", where X and Y
#are the numbers of the exon and oligo respectively, and Z is the number of HotSpot output for the 
#same pair of exon and oligo

import os
import requests
import json
import html_parser


def get_body(seq, seq_no):
    body = {'process': 'search',
          'db' : 'SRProteins',
          'check_sf2' : 'ON',
          'threshold_sf2' : '1.956',
          'check_sf2_igm_brca1' : 'ON',
          'threshold_sf2_igm_brca1' : '1.867',
          'check_sc35' : 'ON',
          'threshold_sc35' : '2.383',
          'check_srp40' : 'ON',
          'threshold_srp40' : '2.67',
          'check_srp55' : 'ON',
          'threshold_srp55' : '2.676',
          'seq' :'>exon|' +\
           str(seq_no) + '\n' + seq,
           'upload' : '',
           'report_max_only' : 'ON',
           'report_all_score' : 'ON',
           'email' : '',
           'submit' : 'Send'}
    return body



def save(result, output_addr):
    keys = list(result)
    max_len = 0
    for k in keys:
        if max_len < len(result[k]):
            max_len = len(result[k])
    buff = ['' for i in range(max_len)]
    f = open(output_addr, "w")
    for key in result:
        f.write('\t' + key[0] + '_threshold' + key[1] + '\t')
    f.write('\ndistance_from_acc\t' + 'sequence_chunk\tvalue\t'*5 + '\n')
    for key in result:
        rows = result[key]
        for i in range(len(result[key])):
            value = rows[i]
            buff[i] = buff[i] + value[1] + '\t' + value[2] + '\t'
    for i in range(len(buff)):
        f.write(str(i) + '\t' + buff[i] + '\n')
    f.flush()
    f.close()        



def get_files(path):
    f = []
    for (dirpath, dirnames, filesname) in os.walk(path):
        f.extend(filesname)
        #Enable, only if you want the files in the top directory
        #break #Enable, only if you want the files in the top directory
    return f



def find_coresponding_files(input_dir, keywords_list, unwanted_keywords_list):
    fnames = get_files(input_dir)
    files_addr = []
    for name in fnames:
        valid = True
        for k in keywords_list:
            if k not in name:
                valid = False
                break
        for u in unwanted_keywords_list:
            if u in name:
                valid = False
                break
        
        if valid:
            files_addr.append(name)
    return files_addr



def get_all_seq(input_dir):
    seq_list = []
    seen = []
    only_exon = find_coresponding_files(input_dir, ["exon"], ["oligo"])
    for name in only_exon:
        if name in seen:
            continue;
        addr = input_dir + "/" + name
        f = open(addr, "r")
        sequence = f.readline().strip()
        f.close()
        seq_list.append((name, sequence))
        seen.append(name)
    return seq_list



def post_request(url, seq, seq_no):
    body = get_body(seq, seq_no)
    r = requests.post(url, data = body)
    #print("Request status: ", r.status_code, r.reason)
    p = html_parser.Parser(r.text)
    result  = p.pars_html()
    return result



def submit_seq(url, seq_list):
    parsed_responses = []
    for name, seq in seq_list:
        response = post_request(url, seq, name)
        parsed_responses.append((name, response))
    return parsed_responses
        

if __name__ == "__main__":
    input_dir = '/home/seyedmah/Desktop/1_hotspot_input_30mer' 
    url = 'http://krainer01.cshl.edu/cgi-bin/tools/ESE3/esefinder.cgi' #Destination URL
    output_dir = './'    

    seq_list = get_all_seq(input_dir)
    print('Submitting sequences . . .')
    results =  submit_seq(url, seq_list)
    
    for name, response in results:
        print('Saving " + name + " response.')
        output_addr = output_dir + 'ESE_finder_' + name[:-4] + '.xlsx' #Removed ".txt"
        save(response, output_addr)
        print('Done!')

    
