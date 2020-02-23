# coding: utf-8
import os
import re
import copy
import treetaggerwrapper as ttw

tagger = ttw.TreeTagger(TAGLANG='en', TAGDIR='/Users/hamaike/src/words_for_developers/TreeTagger')

files_path = ['docs/drf_requests.txt', 'docs/drf_responses.txt']
ROOT_PATH = '/Users/hamaike/src/words_for_developers/docs'


def make_recursive_file_path(path, path_list):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            make_recursive_file_path(path + "/" + file, path_list)
    else:
        path_list.append(path)

    return path_list


def make_context(str_data, context):
    tags = tagger.TagText(str_data)
    for tag in tags:
        details = tag.split("\t")
        new_key = details[0].lower()
        new_key = new_key.replace('.', '')
        new_key = new_key.replace('^', '')
        if new_key in context.keys():
            context[new_key].append(tag)
        else:
            context.update({new_key: []})
            context[new_key].append(tag)
    return context


def get_str_data(path):
    with open(path) as f:
        s = f.read()
    return s


def remove_fuck_keys(context):
    keys = copy.deepcopy(list(context.keys()))
    for key in keys:
        result_a = re.fullmatch(r'^<.*>', key)
        result_b = '_' in key
        result_c = '-' in key
        result_d = True
        result_e = len(key) == 1

        try:
            int(key)
        except Exception:
            result_d = False

        if result_a or result_b or result_c or result_d or result_e:
            context.pop(key)
    return context


def main():
    context = {}
    path_list = []
    path_list = make_recursive_file_path(ROOT_PATH, path_list)

    for path in path_list:
        str_data = get_str_data(path)
        context = make_context(str_data, context)

    context = remove_fuck_keys(context)
    sorted(context, key=lambda k: len(context[k]))
    # key_list = context.keys()
    # sorted_context = list(context.keys()).sort(key=lambda x: len(x), reverse=True)
    import pdb;
    pdb.set_trace()


if __name__ == '__main__':
    main()
