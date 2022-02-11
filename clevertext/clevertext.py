#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# clevertext
# Author: Peter Fison
import re
import requests
from lxml.html.clean import clean_html, Cleaner
import csv
import difflib

class CleverText(str):
    """A string which also contain its own version history and record of
    actions.  Intended for comparing different states of a string as various
    transformations (replacements, deletions, validation, parsing) are applied
    to it.  Methods of this class are then readily available for future ETL
    style processing.

    .history : a sequential list of string states
    .initial : shortcut to the initial string supplied
    .final : shortcut to the latest version of the string
    .actions : a sequential list of functional transformations applied
    .transformers : a mapping of shortcuts to tranformation methods
    .checksum : quick comparison of string lengths across .history

    Use self.history += [] and self.actions += [] to update output
    and action log after every transformation.

    TODO: make setter function
    TODO: make .transformers/.apply class methods?
    TODO: diff
    """
    shortcuts = '{"dep": self.delete_empty_pattern, "clean": self.clean_unwanted_tags, "dmt": self.delete_whole_lines, "h3": self.replace_h1_h2_h3_except_title, "div": self.remove_surrounding_div, "b1": self.format_brackets_1, "rp": self.remove_punctuation, "html1": self.final_html_filters, "h3h3": self.remove_empty_h3, "sai": self.strip_aida_inputs, "rs": self.remove_spaces, "rn": self.remove_noise, "cg": self.correct_grammar, "rt": self.replace_tags, "rie": self.remove_incomplete_ending, "rdl": self.remove_double_linespaces, "frh": self.force_remove_http, "aes": self.add_end_sequence}'

    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.history = [str(text)]
        self.actions = ["initial"]
        self.transformers = eval(CleverText.shortcuts)

    @property
    def initial(self):
        return self.history[0]

    @property
    def final(self):
        return self.history[-1]

    # @final.setter
    # def final(self, value):
    # If already initialised, add to .history and .actions
    #     self.history += [value]

    @property
    def checksum(self):
        """Returns a list of tuples based on .actions and .history length"""
        return list(zip(self.actions, [len(x) for x in self.history]))

    def apply(self, shortcut):
        """Helper method to apply a given method to .final based on shortcuts"""
        transform_function = self.transformers.get(shortcut)
        if not transform_function:
            return
        result = transform_function()
        return result

    def pretty(self, **kwargs):
        from textwrap import wrap
        width = kwargs.get("width") or 100
        for action in self.actions:
            x = [f"{action}:"]
            x += wrap(f"{summary.by_shortcut(action)[0]}\n", width=width, **kwargs)
            for item in x:
                print(item)
            print()

    @staticmethod
    def apply_to_csv(shortcut_list, filepath=None, column=None):
        """Imports a CSV and applies transformation functions before re-saving creating a comparison column and saving as a new file.

        Arguments
        ---------

        shortcut_list (list or str):
            Short function codes for transformations indexed in
            CleverText.shortcuts

        filepath (str):
            Full or relative file path to the input CSV file.

        column (str):
            Optional. Specific column to use for initial transformation.

        For further details, import and use the info() function from CleverText.

        """
        if type(shortcut_list) == str:
            shortcut_list = [shortcut_list]
        if filepath is None:
            filepath = "CleverText_output.csv"
        print(f"\nⓘ  Using input CSV:\n{filepath}\n")
        # TODO: replace with csv variant, not pandas
        df = pd.read_csv(filepath, encoding="utf-8")
        valid_shortcuts = eval(CleverText.shortcuts.replace("self","CleverText")).keys()
        for shortcut in shortcut_list:
            if shortcut not in valid_shortcuts:
                print(f"\n⚠ Shortcut '{shortcut}' not found.\n")
                continue
            text_column = column or df.columns[-1]
            df[shortcut] = df[text_column].map(lambda x: CleverText(x).apply(shortcut))
            filepath = filepath.replace(".csv", f"_{shortcut}.csv")
            df.to_csv(filepath, encoding='utf-8', index=False)
            print(f"✓ {df.shape[0]} rows and {len(df.columns)} columns {list(df.columns)} saved to:\n{filepath}")
        return df

    def update(self, new_string, action="n/a"):
        self.history += [str(new_string)]  # In case CleverText object received
        self.actions += [action]

    def _replace(self):
        pass
        #TODO: Create wrapped functions (.update) for existing string methods


    def save_AB(self, prefix="CleverText"):
        """Saves two files for comparison based on .initial and .final"""
        for text in [self.initial, self.final]:
            filename = f'{prefix}_{"A" if text==self.initial else "B"}.txt'
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(text)

    def final_html_filters(self):
        """Common final processing filters e.g. for AIDA and BlogSpinner"""
        self.delete_empty_pattern()
        self.clean_unwanted_tags()
        self.delete_whole_lines()
        self.replace_h1_h2_h3_except_title()
        self.remove_surrounding_div()
        self.replace_tags()
        self.remove_empty_h3()
        self.remove_incomplete_ending()
        self.remove_double_linespaces()
        self.force_remove_http()
        self.add_end_sequence()
        return self.final

    def remove_double_linespaces(self):
        self.history += [self.final.replace("\n\n", "\n")]
        self.actions += ["rdl"]
        return self.final

    def remove_incomplete_ending(self):
        lines = self.final.splitlines()
        last_line = []
        while not last_line:
            # Find last non-empty line
            last_line = lines[-1].split(" ")
            lines = lines[:-1]
        if "<" in last_line[-1]:
            end_tag = f'<{"".join(last_line[-1].split("<")[1:])}'
            last_line = last_line[:-1]
        else:
            end_tag = ""
        def matches():
            try:
                return [
                    "." in last_line[-1],
                    "?" in last_line[-1],
                    "!" in last_line[-1],
                    "<" in last_line[-1] and ">" in last_line[-1],
                    ]
            except IndexError:
                return [True]
        while not any(matches()):
            last_line = last_line[:-1]
        lines += [" ".join(last_line) + end_tag]
        self.history += ["\n".join(lines)]
        self.actions += ["rie"]
        return self.final

    def replace_html_tags(self):
        replacements = {
            "li>": "p>",
            }
        text = self.final
        for old, new in replacements.items():
            text.replace(old, new)
        self.history += [text]
        self.actions += ["rt"]
        return self.final

    def correct_grammar(self, HUGGINGFACE_TOKEN):
        headers = {"Authorization": HUGGINGFACE_TOKEN}
        payload = {"inputs": self.final}
        url = "https://api-inference.huggingface.co/models/prithivida/grammar_error_correcter_v1"
        response = requests.post(url, headers=headers, json=payload)
        try:
            self.history += [response.json()[0]["generated_text"]]
        except:
            self.history += [f"\n⚠ ERROR [{response.status_code}"]
        self.actions += ["cg"]
        return self.final

    def clean_unwanted_tags(self, tags=None):
        tags = tags or ['img', 'a', 'ul', 'ol', 'br']
        # cleaner = Cleaner(scripts=True, embedded=True, meta=True, page_structure=True, links=True, style=True, remove_tags = ['img', 'a'])
        # cleaner = Cleaner(scripts=True, embedded=True, meta=True, page_structure=True, links=True, style=True, kill_tags = ['img', 'a'])
        cleaner = Cleaner(kill_tags = kill_tags)
        self.history += [cleaner.clean_html(self.final)]
        self.actions += ["clean"]
        return self.final


    def force_remove_http(self):
        """Disregard HTML tags and remove every http/https occurrence"""
        self.history += [re.sub(r'^https?:\/\/.*[\r\n]*', '', self.final, flags=re.MULTILINE)]
        self.actions += ["frh"]
        return self.final

    def nuke(self):
        """Removes lines with both meeting specific criteria

        NB if you want ALL possible case permutations:

        import itertools
        t = "fox"
        list(''.join(x) for x in itertools.product(*zip(t.upper(), t.lower()))))"""
        newlines = []
        for line in self.final.splitlines():
            conditions = ['class="' in line,
                          '[img]' in line and '[/img]' in line,
                          '[Image]' in line,
                          '[Link]' in line,
                          'www.' in line,
                          "$" in line,
                          "€" in line,
                          "£"in line,
                          ".com" in line,
                          ]
            if any(conditions):
                continue
            else:
                newlines += [line]
        self.history += ["\n".join(newlines)]
        self.actions += ["dmt"]
        return self.final

    def replace_h1_h2_h3_except_title(self):
        """Replace all h2 tags except the title with h3.
        Recorded as two distinct actions on h1 and h2 respectively."""
        for tags in [("<h1>", "</h1>"), ("<h2>", "</h2>")]:
            first_match_found = False
            # mark first tag pair for protection
            text = self.final.replace(tags[0][-3:],"**>", 2)
            # replace all others
            text = text.replace(tags[0][-3:],"h3>", 2)
            # restore first tag pair
            text = text.replace("**>", tags[0][-3:])
            self.history += [text]
            self.actions += [f"h3:{tags[0]}"]
        return self.final

    def remove_empty_h3(self):
        """Removes an h3 title line if there's no <p> content between it and the
        next h3 title"""
        newlines = []
        h3 = "<h3>"
        lines = self.final.splitlines()
        for index, line in enumerate(lines):
            if h3 in line and index == len(lines) -1:
                continue
            if h3 in line and h3 in lines[index+1]:
                continue
            else:
                newlines += [line]
        self.history += ["\n".join(newlines)]
        self.actions += ["h3h3"]
        return self.final

    def remove_punctuation(self):
        """Removes spurious punctuation in title, or converts to spaces"""
        spaces = " - ,®,™,�".split(",")
        singletons = [x for x in ",•_|;·Ââ*{}◆/✔()✦[]"]
        multiples = "】,【,『,』,''','',Product Features:,product features:,Product features:,Q:,:Q,Features:".split(",")
        # TODO: Move phrases to strip_aida_inputs?
        text = self.final
        for replacement in spaces + singletons + multiples:
            text = str(text).replace(replacement, " " if replacement in spaces else " ")
        self.history += [text]
        self.actions += ["rp"]
        return self.final

    def replace(self, *args, **kwargs):
        """Model for wrapping inherited methods"""
        #TODO: Extend to all other str methods
        #TODO: Extend to operators e.g. += which current convert CleverText object back to simple string!
        self.history += [super().replace(*args, **kwargs)]
        self.actions += [f"replace {args}"]
        return self.final

    def __repr__(self):
        return self.final

    def __str__(self):
        return self.final

    def by_shortcut(self, shortcut):
        """
        Return a list of all .history result with action code matching shortcut.
        """
        index_list = [i for i,x in enumerate(self.actions) if x==shortcut]
        return [self.history[i] for i in index_list]

    def diff(self, index_a=0, index_b=None, print_only=True):
        """
        Print or return a colour-coded diff of two items in a list of strings.  Default: Compare first and last strings; print the output; return None.
        """
        index_b = index_b or len(self.history) -1
        green = '\x1b[38;5;16;48;5;2m'
        red = '\x1b[38;5;16;48;5;1m'
        end = '\x1b[0m'
        output = []
        string_a = self.history[index_a]
        string_b = self.history[index_b]
        matcher = difflib.SequenceMatcher(None, string_a, string_b)
        for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
            if opcode == "equal":
                output += [string_a[a0:a1]]
            elif opcode == "insert":
                output += [green + string_b[b0:b1] + end]
            elif opcode == "delete":
                output += [red + string_a[a0:a1] + end]
            elif opcode == "replace":
                output += [green + string_b[b0:b1] + end]
                output += [red + string_a[a0:a1] + end]
        output = "".join(output)
        if not print_only:
            return output
        print(f"\n{output}\n")

def info():
    message = "\nCleverText.shortcuts:\n"
    message += CleverText.shortcuts.replace("self","CleverText").replace("{","\n").replace("}","\n").replace(', "', '\n"')
    message += "\nSee also clevertext_readme.md"
    print(message)
