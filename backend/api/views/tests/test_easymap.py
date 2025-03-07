import easymap
import pytest

@pytest.mark.skip(reason="No valid token and may be useless feature.")
def test_get_land_number():
    # 120.1074406, 23.2353021
    # 臺南市北門區 溪底寮段三寮灣小段 (5404) 1681地號
    result = easymap.get_land_number(120.1074406, 23.2353021)
    assert result["City"] == "D"
    assert result["Area"] == "臺南市北門區"
    assert result["sectno"] == "5404"
    assert result["sectName"] == "溪底寮段三寮灣小段"
    assert result["landno"] == "1681"
