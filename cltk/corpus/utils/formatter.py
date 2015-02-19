"""Process downloaded or local corpora from one format into another.
Some formatting can happen here, or invoke language-specific formatters in
other files.

#TODO: Add generic HTML stripper
"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Stephen Margheim <stephen.margheim@gmail.com>']
__license__ = 'MIT License. See LICENSE.'


from cltk.corpus.greek.beta_to_unicode import Replacer
from cltk.corpus.greek.tlg_index import TLG_INDEX
from cltk.corpus.greek.tlgu import TLGU
from cltk.corpus.utils.cltk_logger import logger
import os
import re
import sys


def remove_non_ascii(input_string):
    """remove non-ascii: http://stackoverflow.com/a/1342373"""
    no_ascii = "".join(i for i in input_string if ord(i) < 128)
    return no_ascii


def cleanup_tlg_txt(tlg_str):
    """"Remove all non–Greek characters from a TLG corpus."""
    # fix beta code transliteration problems
    tlg_str = re.sub(r'ι\+', 'ϊ', tlg_str)
    tlg_str = re.sub(r'ί\+', 'ΐ', tlg_str)
    tlg_str = re.sub(r'\\.', '.', tlg_str)
    # fix tlg markup
    tlg_str = re.sub(r'@1 \{1.+?\}1 @', '', tlg_str)  # rm book titles
    tlg_str = re.sub(r'\[.+?\]', '', tlg_str)  # rm words in square brackets
    tlg_str = re.sub(r'[0-9]', '', tlg_str)
    tlg_str = re.sub(r'@|%|\x00', '', tlg_str)
    tlg_str = re.sub('—', ' — ', tlg_str)
    return tlg_str


def build_corpus_index(corpus, authtab_path=None):
    """Build index for TLG or PHI5. ``authtab_path`` for testing only.
    TODO: Add a test flag argument and rm authtab_path
    :param corpus:
    :return: dict
    """
    if corpus == 'tlg':
        if not authtab_path:
            authtab_path = '~/cltk_data/originals/tlg/AUTHTAB.DIR'
        slice_start = 1
        slice_end = -6
        file_name_match = 'TLG[\d].{4}'
        pattern_author_regex = '&1|&l|l$|&|1$|\x83|\[2|\]2'
    elif corpus == 'phi5':
        if not authtab_path:
            authtab_path = '~/cltk_data/originals/phi5/AUTHTAB.DIR'
        slice_start = 1
        slice_end = -21
        file_name_match = 'LAT[\d].{4}'
        pattern_author_regex = '&1|&l|l$|&|1$|\x83'
    else:
        logger.warning("Corpus %s not available. Choose from 'tlg' or 'phi5'." % corpus)
        sys.exit(1)
    index_path = os.path.expanduser(authtab_path)
    if not os.path.isfile(index_path):
        logger.info("Failed to locate original %s index at '%s'. Please import first." % (corpus, index_path))
        sys.exit(1)
    with open(index_path, 'rb') as f:
        r = f.read()
    index_all = r.decode('latin-1').split('\xff')[slice_start:slice_end]
    index = [x for x in index_all if x]
    file_author = {}
    for x in index:
        # file name
        pattern_file = re.compile(file_name_match)
        m = pattern_file.match(x)
        file_name = m.group()[:-1]# + '.TXT'

        # author name
        author_name = pattern_file.split(x)[-1]
        pattern_author = re.compile(pattern_author_regex)
        author_name = pattern_author.sub('', author_name)
        pattern_comma = re.compile('\x80')
        author_name = pattern_comma.sub(', ', author_name)
        file_author[file_name] = author_name

    return file_author

def make_tlg_work_dict(author_dict):
    """ Lots to do here still. Pare characters around formats and clean all junk characters.
    Also find why returning only 1777; find rejected authors -- prob at a .split().
    :param author_dict:
    :return:
    """
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)

    final_dict = {}
    for file, author in file_index.items():
        a_id = {'id:': file[:-4]}
        idt_file = file[:-4] + '.IDT'
        author_index_path = os.path.join(orig_dir_path, idt_file)
        with open(author_index_path, 'rb') as a_ind_f:
            a_ind = a_ind_f.read()
        lat_list = a_ind.decode('latin-1').split('ÿ')
        ascii_list = [remove_non_ascii(x) for x in lat_list]

        works_list = []
        author_works = {}
        for possible_title in ascii_list:
            title_parts = possible_title.split('\x10', maxsplit=1)
            title_parts = [x for x in title_parts if x]
            for part in title_parts:
                try:
                    title_format = part.split('\x11', maxsplit=1)
                    title = title_format[0]
                    format = title_format[1]
                    author_works[title] = format
                    works_list.append(author_works)
                except:
                    pass
        author_vals = {'works': works_list, 'id': file[:-4]}
        final_dict[author] = author_vals
    #print(len(final_dict))  # 1777 this is missing ~100 files; find why

    return final_dict


def make_tlg_work_dict2(author_dict):

    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)

    final_dict = {}
    for file, author in file_index.items():
        works = []
        idt_file = file[:-4] + '.IDT'
        author_index_path = os.path.join(orig_dir_path, idt_file)
        with open(author_index_path, 'rb') as a_ind_f:
            a_ind = a_ind_f.read()
        lat_list = a_ind.decode('latin-1').split('ÿ')
        ascii_list = [remove_non_ascii(x) for x in lat_list]
        for possible_title in ascii_list:
            title_parts = possible_title.split('\x10', maxsplit=1)
            title_parts = [x for x in title_parts if x]
            for part in title_parts:
                title_format = part.split('\x11', maxsplit=1)
                if len(title_format) == 2:  # Note: nothing with len(title_format) > 2
                    work_title = title_format[0]
                    work_format = title_format[1]

                    # clean work title
                    work_title = remove_non_ascii(work_title)
                    work_title = work_title.replace('	', '').strip()
                    work_title = work_title

                    # clean format info
    return final_dict


def bad_idts():
    l = ['TLG2212.TXT', 'TLG2466.TXT', 'TLG0288.TXT', 'TLG1225.TXT', 'TLG4347.TXT', 'TLG1917.TXT', 'TLG1843.TXT', 'TLG4346.TXT', 'TLG1263.TXT', 'TLG1318.TXT', 'TLG0413.TXT', 'TLG1123.TXT', 'TLG0635.TXT', 'TLG2319.TXT', 'TLG1326.TXT', 'TLG0595.TXT', 'TLG2186.TXT', 'TLG9020.TXT', 'TLG1324.TXT', 'TLG4391.TXT', 'TLG0613.TXT', 'TLG2482.TXT', 'TLG2314.TXT', 'TLG4344.TXT', 'TLG2587.TXT', 'TLG1941.TXT', 'TLG0069.TXT', 'TLG2681.TXT', 'TLG1319.TXT', 'TLG1678.TXT', 'TLG0023.TXT', 'TLG2475.TXT', 'TLG2423.TXT', 'TLG0085.TXT', 'TLG1138.TXT', 'TLG1320.TXT', 'TLG2696.TXT', 'TLG0538.TXT', 'TLG1414.TXT', 'TLG4157.TXT', 'TLG1429.TXT', 'TLG1192.TXT', 'TLG4345.TXT', 'TLG2354.TXT', 'TLG0380.TXT', 'TLG2307.TXT']
    #l = ['TLG0003.TXT']
    l = [str(x[:-4] + '.IDT') for x in l]
    #print(l)
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)

    tmp = []
    for idt_file in l:
        author_index_path = os.path.join(orig_dir_path, idt_file)
        with open(author_index_path, 'rb') as f:
            r = f.read()
        lat_list = r.decode('latin-1').split('ÿ')
        ascii_list = [remove_non_ascii(x) for x in lat_list]
        for possible_title in ascii_list:
            title_parts = possible_title.split('\x10', maxsplit=1)
            title_parts = [x for x in title_parts if x]
            for part in title_parts:
                title_format = part.split('\x11', maxsplit=1)
                if len(title_format) == 2:
                    #print('what', len(title_format), title_format)
                    tmp.append(idt_file)
                elif len(title_format) > 2:
                    print('what', len(title_format), title_format)
    print(len(set(idt_file)))


def tlgu_break_works():
    """Use the work-breaking option for TLGU.
    TODO: This should be added to ``tlgu.py`` to allow bulk corpus converting with work-breaking."""
    t = TLGU()
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    tlg_files = os.listdir(orig_dir_path)
    texts = [x for x in tlg_files if x.endswith('.TXT') and x.startswith('TLG')]

    for file in texts:
        orig_file_path = os.path.join(orig_dir_path, file)
        works_dir_rel = '~/cltk_data/greek/text/tlg/individual_works'
        works_dir = os.path.expanduser(works_dir_rel)
        if not os.path.isdir(works_dir):
            os.makedirs(works_dir)
        new_file_path = os.path.join(works_dir_rel, file)

        orig_file_rel = os.path.join(orig_dir_path_rel, file)
        print(orig_file_rel)
        print(new_file_path)
        t.convert(orig_file_rel, new_file_path, divide_works=True)


def find_works_in_texts(author_dict):
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    comp_title = re.compile('\{1(.+?)\}1')
    author_works = {}
    replacer = Replacer()
    for file, auth in author_dict.items():
        author_file_path = os.path.join(orig_dir_path, file)
        with open(author_file_path, 'rb') as auth_file:
            auth_read = auth_file.read()
        auth_read = auth_read.decode('latin-1')
        titles = comp_title.findall(auth_read)
        unicode_titles = []
        for title in titles:
            title = remove_non_ascii(title)
            unicode_title = replacer.beta_code(title)
            unicode_titles.append(unicode_title)
        titles_in_file = {'titles_in_file': unicode_titles}
        author_works[auth] = titles_in_file
        print(author_works)
        input()


# was doing something with parsing the individually divided works
''''
individual_work_dir_rel = '~/cltk_data/greek/text/tlg/individual_works/'
individual_work_dir = os.path.expanduser(individual_work_dir_rel)
individual_work = os.path.join(individual_work_dir, 'TLG0007.TXT-007.txt')
if not os.path.isfile(individual_work):
    tlgu_break_works()
for file, author in TLG_INDEX.items():
    file_base = os.path.join(individual_work_dir, file)
    print(file_base)
    input()
'''


def read_tlg_idts():
    """Read TLG IDT files from the directory. These should later be checked against the TLG_INDEX."""
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    return [os.path.join(orig_dir_path, x) for x in os.listdir(orig_dir_path) if x.endswith('.IDT') and x.startswith('TLG')]


def open_idt(idt_path):
    #print(idt_path)
    with open(idt_path, 'rb') as opened_idt:
        return opened_idt.read()


def cleanup_author(author_text):
    comp_clean_author = re.compile('&|\[2|\]2|1')
    author = comp_clean_author.sub('', author_text)

    # super ugly. replace name if 1 of 3 which has Greek in name
    greek_name = {'Dialexeis ($*DISSOI\\ LO/GOI)': 'Dialexeis Δισσοὶ λόγοι',
                  'Dionysius $*METAQE/MENOS Phil.': 'Dionysius Μεταθέμενος Phil.',
                  'Lexicon $AI(MWDEI=N': 'Lexicon αἱμωδεῖν'}
    if author in greek_name:
        author = greek_name[author]

    # same as above. damn ugly. replace name w/ dict value if name is one we
    # know to have a diaresis in it
    diaresis_authors = {'Danai+s vel Danai+des': 'Danaïs vel Danaïdes',
                       'Ae+tius Doxogr.': 'Aëtius Doxogr.',
                       'Aglai+s Poet. Med.': 'Aglaïs Poet. Med.',
                       'Ae+tius Med.': 'Aëtius Med.',
                       'Thebai+s': 'Thebaïs',
                       'Boi+das Phil.': 'Boïdas Phil.'
    }
    if author in diaresis_authors:
        author = diaresis_authors[author]

    return author

def match_idt_author_name(idt_binary):
    idt_text = idt_binary.decode('latin-1')
    comp_name = re.compile('&1(.+?)\x02')
    author = comp_name.findall(idt_text)
    return author[0]

def match_idt_titles(idt_binary):
    #idt_text = idt_binary.decode('latin-1')
    comp_post_name = re.compile(b'\x02')
    post_name = comp_post_name.split(idt_binary, 1)
    comp_pre_first_title = re.compile(b'\xff\x10')
    pre_first_title = comp_pre_first_title.split(post_name[1])
    print(pre_first_title[1:])  #! This is good! Each element of the list is a work + its index method
    input()
    return ''

def author_names_from_idts():
    """There are 1823 TLG*.IDT files, but the authors in them are only 1773
    unique. That is 50 IDT files give an author name identical to one in
    another file. OIPOPOI!
    """
    orig_dir_path_rel = '~/cltk_data/originals/tlg'
    orig_dir_path = os.path.expanduser(orig_dir_path_rel)
    #return [os.path.join(orig_dir_path, x) for x in os.listdir(orig_dir_path) if x.endswith('.IDT') and x.startswith('TLG')]

    author_dict = {}

    for tlg_id, dir_name in TLG_INDEX.items():
        idt_path = os.path.join(orig_dir_path, tlg_id + '.IDT')

        idt_binary = open_idt(idt_path)
        author_ugly = match_idt_author_name(idt_binary)
        author = cleanup_author(author_ugly)

        author_names = {'name_idt': author,
                        'name_authtab': dir_name
                        }
        author_dict[tlg_id] = author_names

    # here add parsing of works in .idt file
    for tlg_id, dir_name in TLG_INDEX.items():
        idt_path = os.path.join(orig_dir_path, tlg_id + '.IDT')
        idt_binary = open_idt(idt_path)
        titles_ugly = match_idt_titles(idt_binary)

    return author_dict


if __name__ == '__main__':
    author_dict = author_names_from_idts()

    '''
    with open('cltk/corpus/greek/tlg_master_index.py', 'w') as f:
        f.write('TLG_MASTER_INDEX = ' + str(author_dict))
    '''

