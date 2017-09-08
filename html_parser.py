class Parser:
    
    def __init__(self, raw_content):
        self.raw_content = raw_content
        

    def get_columns_name_and_threshold(self, section_list, sec_no = 1):
        columns = []
        thresholds = []
        for line in section_list[sec_no].split('\n'): #Read each line
            if '<b>' in line:
                columns.append(line.split('<b>')[1].split('<br>')[0])
                thresholds.append(line.split(':')[1].split('<')[0])
        return (columns, thresholds)


     
    def get_values(self, section):
        #The elements in the following dictionary are (distance_from_acc, sequence, value)
        result = []
        chunks = section.split('<tr>')
        for c in chunks:            
            lines = c.split('\n')

            if len(lines) == 6:
#                lines = c.split('\n')
                #print(lines)
                dis_from_acc = lines[1].split('>')[2].split('(')[0]
                seq = lines[2].split('>')[2].split('<')[0]
                value = lines[3].split('>')[2].split('<')[0]
                #print(lines, '\n', dis_from_acc, seq, value, '\n')
                result.append((dis_from_acc, seq, value))
        return result


    
    def pars_html(self):
        result = {}
        sections = self.raw_content.split('style=\"border-collapse: collapse')
        (columns, thresholds) = self.get_columns_name_and_threshold(sections, 1)
        for i in range(2, len(sections)-1):
            values = self.get_values(sections[i])
            result[(columns[i-2], thresholds[i-2])] = values
        return result
