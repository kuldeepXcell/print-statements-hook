from print_statement_hook.hook import check_file_for_prints, is_excluded, get_all_python_files

def test_detects_print(tmp_path):
    p = tmp_path / "has_print.py"
    p.write_text("print('hello')")
    assert len(check_file_for_prints(str(p))) > 0

def test_detects_multiple_prints(tmp_path):
    p = tmp_path / "multiple_prints.py"
    p.write_text("print('one')\nprint('two')")
    findings = check_file_for_prints(str(p))
    assert len(findings) == 2

def test_no_print(tmp_path):
    p = tmp_path / "no_print.py"
    p.write_text("x = 1 + 1\n# print('commented')")
    assert len(check_file_for_prints(str(p))) == 0

def test_is_excluded(tmp_path):
    f = tmp_path / "test.py"
    d = tmp_path / "subdir"
    d.mkdir()
    f2 = d / "inner.py"
    
    exclude_list = [str(f), str(d)]
    
    assert is_excluded(str(f), exclude_list) is True
    assert is_excluded(str(f2), exclude_list) is True
    assert is_excluded(str(tmp_path / "other.py"), exclude_list) is False

def test_get_all_python_files(tmp_path):
    (tmp_path / "a.py").write_text("print('a')")
    (tmp_path / "b.txt").write_text("not python")
    sd = tmp_path / "sub"
    sd.mkdir()
    (sd / "c.py").write_text("print('c')")
    
    files = get_all_python_files(str(tmp_path), [])
    assert len(files) == 2
    assert any("a.py" in f for f in files)
    assert any("c.py" in f for f in files)

def test_get_all_python_files_with_exclude(tmp_path):
    (tmp_path / "a.py").write_text("print('a')")
    sd = tmp_path / "sub"
    sd.mkdir()
    (sd / "c.py").write_text("print('c')")
    
    files = get_all_python_files(str(tmp_path), [str(sd)])
    assert len(files) == 1
    assert "a.py" in files[0]
