import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module(path: str):
    return ast.parse((ROOT / path).read_text(encoding='utf-8'))


def node_text(tree):
    return ast.get_source_segment((ROOT / 'main.py').read_text(encoding='utf-8'), tree) or ''


def test_main_ui_uses_http_client_not_db_or_exa():
    tree = load_module('main.py')
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or '')

    assert 'sqlite3' not in imports
    assert 'exa_py' not in imports
    assert any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == 'post'
        for node in ast.walk(tree)
    )


def test_processor_handles_cache_and_exa_logic():
    tree = load_module('processor.py')
    source = (ROOT / 'processor.py').read_text(encoding='utf-8')

    assert 'sqlite3.connect("cache.db")' in source
    assert 'SELECT response FROM search_cache' in source
    assert 'INSERT OR REPLACE INTO search_cache' in source
    assert 'process_search' in source
    assert 'Exa(' in source


def test_api_controller_exposes_search_endpoint():
    tree = load_module('app.py')
    source = (ROOT / 'app.py').read_text(encoding='utf-8')

    assert '@app.route("/api/search", methods=["POST"])' in source
    assert 'process_search(data)' in source
    assert 'jsonify' in source
