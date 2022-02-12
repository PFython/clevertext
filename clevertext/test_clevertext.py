# Tests for clevertext
import pytest
from .clevertext import *

class Test_Initialisation:
    def test_init(self):
        ct = CleverText("some text$$$some more text")
        assert ct.initial == ct.history[0] == 'some text$$$some more text'
        assert ct.final == ct.history[0] == 'some text$$$some more text'
        assert ct.final == ct.history[1] == 'some text$$$some more text'
        assert repr(ct) == str(ct) == 'some text$$$some more text'
        assert ct.__eq__() == 'some text$$$some more text'

class Test_Core_Functions:
    def test_format_bytes(self):
        assert format_bytes(1,"b") == '8 b'
        assert format_bytes(1,"bits") == '8 bits'
        assert format_bytes(1024, "kilobyte") == "1 Kilobyte"
        assert format_bytes(1024, "kB") == "1 KB"
        assert format_bytes(7141000, "mb") == '54 Mb'
        assert format_bytes(7141000, "mib") == '54 Mib'
        assert format_bytes(7141000, "Mb") == '54 Mb'
        assert format_bytes(7141000, "MB") == '7 MB'
        assert format_bytes(7141000, "mebibytes") == '7 Mebibytes'
        assert format_bytes(7141000, "gb") == '0 Gb'
        assert format_bytes(1000000, "kB") == '977 KB'
        assert format_bytes(1000000, "kB", SI=True) == '1,000 KB'
        assert format_bytes(1000000, "kb") == '7,812 Kb'
        assert format_bytes(1000000, "kb", SI=True) == '8,000 Kb'
        assert format_bytes(125000, "kb") == '977 Kb'
        assert format_bytes(125000, "kb", SI=True) == '1,000 Kb'
        assert format_bytes(125*1024, "kb") == '1,000 Kb'
        assert format_bytes(125*1024, "kb", SI=True) == '1,024 Kb'

    def test_ruud_tests(self):
        ct = CleverText("initial")
        ct.update("final")
        assert ct.initial == ct.history[0] == "initial"
        assert ct.final == ct.history[1] == "final"
        assert str(ct) == "final"
        assert ct == "final"
        assert "".join(c for c in ct) == "final"
        assert ct.upper() == "FINAL"
        assert ct > "2"
        assert CleverText("12").isdecimal()
        assert "ina" in ct
        assert "ini" not in ct
        assert 2 * ct == "finalfinal"
        assert len(ct) == 5
        assert ct[1:4] == "ina"
        assert ct + "2" == "final2"
        assert repr(ct) == "CleverText('initial', 'final')"
        ct += "2"
        assert repr(ct) == "CleverText('initial', 'final', 'final2')"
        ct.final = "final3"
        assert repr(ct) == "CleverText('initial', 'final', 'final2', 'final3')"
        try:
            CleverText()
            raise AssertionError("should not have passed")
        except TypeError:
            pass
        c1 = CleverText("%02d")
        assert repr(c1 % 4) == "'04'"
        assert isinstance(ct, str)
        assert "/".join(c for c in ct) == "f/i/n/a/l"
        assert ct.join("1 2 3".split()) == "1final2final3"
        assert CleverText("1 2 3").split() == ["1", "2", "3"]

    def test_grammar_checker(self):
        payload = "The benefits of life insurance is obvious"
        text = correct_grammar(payload)
        expected = "The benefits of life insurance are obvious."
        assert "is obvious" not in text
        assert "are obvious" in text
        assert text.endswith(".")

    def test_checksum_and_actions(self):
        self = e = CleverText(EXAMPLES[0]+test_marker)
        assert e.checksum == [('init', 13790)]
        e.clean_unwanted_tags()
        assert e.checksum == [('init', 13790), ('clean', 13634)]
        e.delete_empty_pattern()
        assert e.actions == ['init', 'clean', 'dep']
        assert e.checksum == [('init', 13790), ('clean', 13634), ('dep', 13634)]
        e.delete_whole_lines()
        assert e.checksum[-1] == ('dmt', 13569)
        e.delete_empty_pattreplace_h1_h2_h3_except_titleern()
        assert e.checksum[-1] == ('h3', 13569)

    def test_save_AB(self):
        e.save_AB("CleverText_1")
        assert Path("CleverText_1_A.txt").is_file()
        assert Path("CleverText_1_B.txt").is_file()
        Path("CleverText_1_A.txt").unlink()
        Path("CleverText_1_B.txt").unlink()
        assert not Path("CleverText_1_A.txt").is_file()
        assert not Path("CleverText_1_B.txt").is_file()

    def test_shortcuts(self):
        #TODO: Add recently added methods
        self = e = CleverText(EXAMPLES[0]+test_marker)
        assert e.checksum == [('init', 12727)]
        e.apply('clean')
        assert e.checksum == [('init', 12727), ('clean', 11554)]
        e.apply('dep')
        assert e.actions == ['init', 'clean', 'dep']
        assert e.checksum == [('init', 12727), ('clean', 11554), ('dep', 11554)]
        e.apply('dmt')
        assert e.checksum[-1] == ('dmt', 11203)
        e.apply("h3")
        assert e.checksum[-1] == ('h3', 11203)

class Test_Edge_Cases:
    def test_something(self):
        """ Something should happen when you run something() """
        assert something() == something_else
