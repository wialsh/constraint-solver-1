"""
Created on Mon Aug 24 23:15:23 2020

@author: wialsh

@e-mail: hebiyaozizhou@gmail.com

http://elib.zib.de/pub/mp-testdata/tsp/tsplib/
http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsplib.html
"""
import json, re
from utils import Requesters
from lxml import etree

import sys, os

root_path = '/'.join(os.path.split(os.path.realpath(__file__))[0].split(os.sep)[:-1])
save_path = os.path.join(root_path, 'data', 'dataset', 'tsplib_data')


tsp_url = 'http://elib.zib.de/pub/mp-testdata/tsp/tsplib/tsp/'
tsp_solutions_url = 'http://elib.zib.de/pub/mp-testdata/tsp/tsplib/stsp-sol.html'


atsp_url = 'http://elib.zib.de/pub/mp-testdata/tsp/tsplib/atsp/'
atsp_solutions_url = 'http://elib.zib.de/pub/mp-testdata/tsp/tsplib/atsp-sol.html'


re_s = re.compile('\s+')
re_a = re.compile('[a-z]', re.I) #'\A[a-z]'

def cast_number(value):
    try:
        return int(value)
    except:
        return float(value)

class DownloadTSPLibData(Requesters):
    _name = 'tsp'
    _localfile = 'download_tsplib_data'

    def download(self):
        # self.request(tsp_solutions_url, 'download_tsp_solutions', 'stsp_sol.json')
        #
        # self.request(atsp_solutions_url, 'download_tsp_solutions', 'atsp_sol.json')

        self.request(tsp_url, 'download_tsp_info', 'tsp_data.json')

        self.request(atsp_url, 'download_tsp_info', 'atsp_data.json')

    def request(self, url, *args, **kwargs):
        download_schema = args[0]
        file = args[1]
        print(f'url={url};\ndownload_schema={download_schema};\nfile={file};')
        if download_schema == 'download_tsp_solutions':
            content = self.responses(url, **kwargs)
            print(content)
            tsp_solutions = self.parse_sol(content)
            print(tsp_solutions)
            self._dump(tsp_solutions, file)
        elif download_schema == 'download_tsp_info':
            content = self.responses(url, **kwargs)
            print(content)
            tsp_dict = dict()
            self.parse_tsp_data_info(url, content, tsp_dict)
            print(tsp_dict)
            self._dump(tsp_dict, file)
        else:
            raise Exception(f'args[0] must be `str` and that in ("download_solution", "download_tsp_info")')


    def parse_sol(self, content):
        html = etree.HTML(content, etree.HTMLParser())
        tsp_solutions = dict()
        for elem in html.xpath('//li/text()'):
            tsp_name, best_sol = elem.split(':')
            tsp_name = tsp_name.strip()
            best_sol = best_sol.strip()
            if '[' in best_sol:
                best_sol = eval(best_sol)
            else:
                best_sol = int(best_sol)
            tsp_solutions[tsp_name] = best_sol
        return tsp_solutions
    
    def parse_tsp_data_info(self, url, content, tsp_dict):

        html = etree.HTML(content, etree.HTMLParser())
        # tsp_content = html.xpath('//li/text()')
        # tsp_name = html.xpath('//li/a/@href')

        for sub_html in html.xpath('//li'):

            sub_tsp_content = sub_html.xpath('text()')
            sub_tsp_name = sub_html.xpath('a/@href')
            if sub_tsp_name:
                tsp_name = sub_tsp_name[0]
                if sub_tsp_content:
                    tsp_content = sub_tsp_content[0]
                else:
                    tsp_content = ''

                tsp_dict[tsp_name] = dict()
                tsp_dict[tsp_name]['content'] = tsp_name + ' ' + re_s.sub(' ', tsp_content.strip())
                tsp_data_url = url + tsp_name
                if 'tsp' in tsp_name:
                    tsp_data_dict = self._parse_tsp_data(tsp_data_url)
                else:
                    tsp_data_dict = dict()
                tsp_dict[tsp_name]['data'] = tsp_data_dict
                tsp_dict[tsp_name]['url']  = tsp_data_url
                self._dump(tsp_dict[tsp_name], f"{'atsp' if 'atsp' in url else 'tsp'}-{tsp_name}.json")

                
    def _parse_tsp_data(self, url):
        print(f'parse_tsp_data: {url}')
        content = self.responses(url)

        tsp_data_dict = dict()
        try:
            html = etree.HTML(content, etree.HTMLParser())
        except:
            print(content)
            return tsp_data_dict

        title_list = html.xpath('//title')
        if title_list:
            title = title_list[0]
            if '404' in title:
                return tsp_data_dict

        content = content.decode('utf8') if isinstance(content, bytes) else content
        print(content)

        number_schema = False
        data_list = []
        key = ''
        for line in content.split('\n'):
            line = line.strip()
            if line == 'EOF':
                if data_list:
                    data_list = self._check_dist_list(data_list, tsp_data_dict)
                    tsp_data_dict[key] = data_list
                    data_list = []
                break
            if not line: continue

            if re_a.match(line):
                if ':' in line:
                    key, value = line.split(':')
                    key = key.strip()
                    value = value.strip()
                    if value.isdigit():
                        value = cast_number(value)
                    
                    tsp_data_dict[key] = value
                else:
                    if data_list:
                        data_list = self._check_dist_list(data_list, tsp_data_dict)
                        tsp_data_dict[key] = data_list

                    data_list = []
                    key = line.strip()
                    number_schema = False

            else:
                number_schema = True
            if number_schema:
                if key == 'EDGE_WEIGHT_SECTION':
                    data_list.append(list(map(cast_number, line.split())))
                elif key == 'DISPLAY_DATA_SECTION':
                    data_list.append(list(map(cast_number, line.split()[1:])))
                else:
                    print(key, line)
                    data_list.append(list(map(cast_number, line.split()[1:])))
        return tsp_data_dict

    def _check_dist_list(self, data_list, tsp_data_dict):
        _dim = tsp_data_dict.get('DIMENSION', 0)
        if len(data_list) == _dim * 2 and _dim >= 4:
            _tmp_size_list = list(map(len, data_list))
            data_list_new = []
            if _tmp_size_list[0] == _tmp_size_list[2] \
                    and _tmp_size_list[1] == _tmp_size_list[3] \
                    and _tmp_size_list[0] > _tmp_size_list[1] * 2:
                for i in range(0, len(data_list), 2):
                    tmp_data = data_list[i] + data_list[i+1]
                    data_list_new.append(tmp_data)
                data_list = data_list_new
        return data_list

    def _dump(self, obj, file):
        with open(os.path.join(save_path, file), 'w') as fp:
            json.dump(obj, fp)

if __name__ == '__main__':
    tsplib_data = DownloadTSPLibData()
    tsplib_data.download()