from main import DFAFilter

def test_W():
    org_txt = "E:/hh/1.txt "
    word_txt = "E:/hh/2.txt "
    ans_txt = "E:/hh/3.txt"
    compare_txt = "E:/hh/compare.txt"
    gfw = DFAFilter()
    gfw.parse(word_txt)
    gfw.filter(org_txt, ans_txt, word_txt)
    with open(ans_txt, "r", encoding="utf8") as f:
        out_list = f.read().splitlines()
    with open(compare_txt, "r", encoding="utf8") as f:
        compare_list = f.read().splitlines()
    for i in range(len(compare_list)):
        assert out_list[i] == compare_list[i]