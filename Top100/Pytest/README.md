# Pytest Interview Questions and Answers (Top 100)

## Q1: What is pytest and why is it popular?
**A:** Pytest is a mature, feature-rich Python testing framework that supports simple unit tests and complex functional testing. It is popular for its concise assert statements, powerful fixtures, rich plugin ecosystem, and minimal boilerplate compared to unittest.

**Code:**
```python
def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
```

## Q2: How do you install pytest?
**A:** Install via pip: `pip install pytest`. For specific versions use `pip install pytest==8.0.0`.

**Code:**
```python
import pytest


def test_pytest_installed():
    assert pytest.__version__
```

## Q3: What is the minimum pytest version recommended today?
**A:** pytest 7.x and 8.x are current; pytest 8 drops Python 3.7 support and makes several long-deprecated features error. Target pytest 7/8 in modern projects.

**Code:**
```python
import pytest


def test_modern_pytest():
    major = int(pytest.__version__.split(".")[0])
    assert major >= 7
```

## Q4: How do you run all tests in a project?
**A:** Run `pytest` in the project root. It auto-discovers files matching `test_*.py` or `*_test.py` and functions/classes starting with `test`.

**Code:**
```python
# Any file named test_*.py picked up by plain `pytest`
def test_discovered():
    assert "pytest".startswith("py")
```

## Q5: What are pytest's default test discovery rules?
**A:** Files must match `test_*.py` or `*_test.py`; functions/classes must start with `test_` (classes may not have an `__init__`). Test methods inside classes must also start with `test_`.

**Code:**
```python
def test_function_matches():
    assert True


class TestClassWithoutInit:
    def test_method_matches(self):
        assert True
```

## Q6: How do you run a single test file?
**A:** `pytest tests/test_sample.py`.

**Code:**
```python
# tests/test_sample.py — run with: pytest tests/test_sample.py
def test_sample():
    assert 2 + 2 == 4
```

## Q7: How do you run a single test function?
**A:** `pytest tests/test_sample.py::test_function_name`.

**Code:**
```python
# Run with: pytest test_file.py::test_target
def test_target():
    assert 1 + 1 == 2


def test_not_selected():
    assert True
```

## Q8: What does `pytest -v` do?
**A:** `-v` (verbose) shows each test with its result (PASSED/FAILED) and an OK/FAIL indicator, giving more detail than the default dotted output.

**Code:**
```python
# Run with: pytest -v  ->  prints test name + PASSED/FAILED per line
def test_verbose_shows_result():
    assert [x * 2 for x in range(3)] == [0, 2, 4]
```

## Q9: What does `pytest -x` do?
**A:** `-x` stops the test session after the first failure, useful for quick feedback loops.

**Code:**
```python
def test_first_fails():
    assert 1 == 2  # pytest -x aborts the session here


def test_never_run():
    assert True
```

## Q10: What does `pytest --tb=short` (or `line`, `long`, `no`) do?
**A:** Controls traceback verbosity. `short` shows concise tracebacks, `line` shows one line per failure, `no` hides tracebacks, `long` is the most verbose.

**Code:**
```python
# Run with: pytest --tb=short / --tb=line / --tb=no
def test_failure_shows_traceback():
    payload = {"count": 3}
    assert payload["count"] == 5
```

## Q11: What does `pytest -s` do?
**A:** `-s` disables output capturing so `print()` statements appear in the terminal during the run.

**Code:**
```python
# Run with: pytest -s  -> the print below shows on screen
def test_with_print():
    print("keep this live log line")
    assert True
```

## Q12: What does `pytest -k` do?
**A:** `-k` selects tests by substring expression, e.g. `pytest -k "login or logout"` runs tests whose names contain "login" or "logout".

**Code:**
```python
# Run with: pytest -k "login or logout"
def test_login_success():
    assert True


def test_login_rejected():
    assert True


def test_logout():
    assert True


def test_registration():
    assert True  # not selected by -k "login or logout"
```

## Q13: What does `pytest -m` do?
**A:** `-m` runs tests marked with a given marker expression, e.g. `pytest -m "slow"` runs only tests marked slow.

**Code:**
```python
import pytest


@pytest.mark.slow
def test_slow():
    assert True


def test_fast():
    assert True  # skipped by `pytest -m slow`
```

## Q14: What is the purpose of `conftest.py`?
**A:** `conftest.py` holds fixtures, hooks, and plugin configuration shared across tests in its directory and subdirectories; it is auto-loaded by pytest.

**Code:**
```python
# conftest.py
import pytest


@pytest.fixture
def shared_url():
    return "http://api.example.com"
```

## Q15: How is `conftest.py` scoped?
**A:** A `conftest.py` applies to its own directory and all subdirectories. Multiple `conftest.py` files can exist at different levels, with deeper ones overriding/extending outer ones.

**Code:**
```python
# tests/conftest.py -> visible from tests/ and every subdirectory
import pytest


@pytest.fixture
def base_token():
    return "token-root"


# tests/auth/conftest.py -> only visible inside tests/auth/
@pytest.fixture
def auth_token(base_token):
    return base_token + "-auth"
```

## Q16: What is a pytest fixture?
**A:** A fixture is a function decorated with `@pytest.fixture` that provides a fixed baseline (data, state, resources) to tests via dependency injection by name.

**Code:**
```python
import pytest


@pytest.fixture
def db():
    return {"connected": True}


def test_db_ready(db):
    assert db["connected"]
```

## Q17: How do you use a fixture in a test?
**A:** Declare it as a test function argument with the same name: `def test_a(my_fixture): assert my_fixture == 1`.

**Code:**
```python
import pytest


@pytest.fixture
def my_fixture():
    return 1


def test_uses_fixture(my_fixture):
    assert my_fixture == 1
```

## Q18: What are fixture scopes?
**A:** Scopes are `function` (default), `class`, `module`, `package`, and `session`, controlling how often the fixture is set up/ torn down.

**Code:**
```python
import pytest


@pytest.fixture(scope="module")
def module_state():
    return {"data": "loaded once per module"}


@pytest.fixture(scope="session")
def session_state():
    return "created once for the whole run"
```

## Q19: What is the default fixture scope?
**A:** `function`—the fixture is created and destroyed for each test function.

**Code:**
```python
import pytest


@pytest.fixture  # scope="function" by default
def counter():
    return []


def test_first(counter):
    counter.append(1)
    assert counter == [1]


def test_second(counter):
    assert counter == []  # fresh instance per test
```

## Q20: How do you set a fixture scope?
**A:** Use `@pytest.fixture(scope="session")`; valid values: `function`, `class`, `module`, `package`, `session`.

**Code:**
```python
import pytest


@pytest.fixture(scope="session")
def one_time_setup():
    return {"expensive": "computed once"}
```

## Q21: How do you implement fixture teardown?
**A:** Use `yield` instead of `return`; code after `yield` runs as teardown: `yield resource` then `resource.close()`.

**Code:**
```python
import pytest


@pytest.fixture
def resource():
    print("setup", end=" ")
    yield {"open": True}
    print("teardown", end=" ")  # runs after the test


def test_resource(resource):
    assert resource["open"]
```

## Q22: What is fixture finalization with `addfinalizer`?
**A:** `request.addfinalizer(func)` registers cleanup that runs even if the fixture setup fails, unlike `yield` which only tears down after successful setup.

**Code:**
```python
import pytest


@pytest.fixture
def session(request):
    request.addfinalizer(lambda: print("finalized", end=" "))
    return "established"


def test_session(session):
    assert session == "established"
```

## Q23: What is an `autouse` fixture?
**A:** A fixture with `@pytest.fixture(autouse=True)` is applied automatically to all tests in its scope without needing to be requested as an argument.

**Code:**
```python
import pytest


@pytest.fixture(autouse=True)
def always_runs():
    print("setup for every test", end=" ")


def test_example_one():
    assert True


def test_example_two():
    assert True
```

## Q24: How do you parametrize a fixture?
**A:** Use `@pytest.fixture(params=[1,2,3])`; the fixture receives `request` and returns `request.param`, running the test once per param.

**Code:**
```python
import pytest


@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param


def test_receives_each_param(number):
    assert number in (1, 2, 3)
```

## Q25: What does `@pytest.mark.parametrize` do?
**A:** It runs a test multiple times with different arguments: `@pytest.mark.parametrize("a,b,expected",[(1,2,3),(2,3,5)])`.

**Code:**
```python
import pytest


@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (2, 3, 5)])
def test_add(a, b, expected):
    assert a + b == expected
```

## Q26: How do you give readable IDs to parametrized tests?
**A:** Pass `ids=["case1","case2"]` or use `ids=str`/`ids=lambda x: f"v{x}"` to customize test IDs in reports.

**Code:**
```python
import pytest


@pytest.mark.parametrize("value", [1, 2], ids=["one", "two"])
def test_ids(value):
    assert value > 0


@pytest.mark.parametrize("n", [10, 11], ids=lambda x: f"value-{x}")
def test_lambda_ids(n):
    assert n >= 10
```

## Q27: Can you parametrize with multiple arguments?
**A:** Yes: `@pytest.mark.parametrize("x,y",[(1,2),(3,4)])` injects `x` and `y` into the test.

**Code:**
```python
import pytest


@pytest.mark.parametrize("x,y", [(1, 2), (3, 4)])
def test_multi_args(x, y):
    assert y == x + 1
```

## Q28: What is the difference between fixture `params` and `@pytest.mark.parametrize`?
**A:** `params` on a fixture parametrizes the fixture (and any test using it), while `parametrize` parametrizes the specific test function directly.

**Code:**
```python
import pytest


@pytest.fixture(params=[10, 20])
def base(request):
    return request.param  # every test using `base` runs twice


@pytest.mark.parametrize("increment", [1, 5])
def test_only_this_test(increment, base):
    assert base + increment > 10
```

## Q29: How do you mark a test as expected to fail?
**A:** Use `@pytest.mark.xfail` to mark a test that should fail; pytest reports XFAIL if it fails and XPASS if it unexpectedly passes.

**Code:**
```python
import pytest


@pytest.mark.xfail(reason="known bug in legacy path")
def test_known_bug():
    assert 1 == 2  # reported as XFAIL
```

## Q30: What is the difference between `skip` and `xfail`?
**A:** `skip` omits the test entirely (reported SKIPPED); `xfail` runs it and reports XFAIL/XPASS depending on outcome.

**Code:**
```python
import pytest


@pytest.mark.skip(reason="not ready")
def test_skipped():
    assert True


@pytest.mark.xfail(reason="bug not fixed yet")
def test_xfail_runs_anyway():
    assert 1 == 2
```

## Q31: How do you skip a test conditionally?
**A:** Use `@pytest.mark.skipif(sys.version_info < (3,8), reason="needs py3.8+")` or `pytest.skip(msg)` inside the test.

**Code:**
```python
import sys

import pytest


@pytest.mark.skipif(sys.version_info < (3, 9), reason="needs py3.9+")
def test_py39_feature():
    assert True


def test_skip_inside():
    if sys.platform == "win32":
        pytest.skip("unsupported on windows")
    assert True
```

## Q32: How do you skip a test unconditionally?
**A:** `@pytest.mark.skip(reason="not implemented yet")`.

**Code:**
```python
import pytest


@pytest.mark.skip(reason="not implemented yet")
def test_todo():
    raise NotImplementedError
```

## Q33: What are custom markers and how do you register them?
**A:** Define markers like `@pytest.mark.slow` and register them in `pytest.ini`/`pyproject.toml` under `[pytest] markers = slow: marks slow tests` to avoid warnings.

**Code:**
```python
# pytest.ini
# [pytest]
# markers =
#     slow: marks tests as slow

import pytest


@pytest.mark.slow
def test_heavy():
    assert True
```

## Q34: What is `strict` markers mode?
**A:** With `filterwarnings`/`--strict-markers`, pytest errors on unregistered markers, preventing typos in marker names.

**Code:**
```python
# Run with: pytest --strict-markers
import pytest


@pytest.mark.slwo  # typo -> collection error under --strict-markers
def test_typo_marker():
    assert True
```

## Q35: How does assert rewriting work in pytest?
**A:** pytest rewrites the bytecode of assert statements to provide detailed introspection of values on failure (showing left/right operands), instead of just "AssertionError".

**Code:**
```python
def test_introspection():
    expected = {"user": "ada"}
    actual = {"user": "bob"}
    assert actual == expected  # failure prints full diff
```

## Q36: How do you compare floats with pytest?
**A:** Use `pytest.approx`: `assert 0.1 + 0.2 == pytest.approx(0.3)` for tolerant floating-point comparison.

**Code:**
```python
import pytest


def test_floats():
    assert 0.1 + 0.2 == pytest.approx(0.3)
    assert 10.0 / 3.0 == pytest.approx(3.333, rel=1e-3)
```

## Q37: How do you test that an exception is raised?
**A:** Use `with pytest.raises(ValueError): func()`; you can also inspect `excinfo`: `with pytest.raises(ValueError) as ei: ...`.

**Code:**
```python
import pytest


def parse_int(text):
    return int(text)


def test_raises():
    with pytest.raises(ValueError):
        parse_int("not-a-number")


def test_inspect_exception():
    with pytest.raises(ValueError) as excinfo:
        parse_int("abc")
    assert isinstance(excinfo.value, ValueError)
```

## Q38: How do you check the exception message with `pytest.raises`?
**A:** Use `match`: `with pytest.raises(ValueError, match="invalid"): ...` (regex match against the message).

**Code:**
```python
import pytest


def validate(age):
    if age < 0:
        raise ValueError("invalid age value")
    return age


def test_message():
    with pytest.raises(ValueError, match="invalid"):
        validate(-1)
```

## Q39: What is `tmp_path`?
**A:** `tmp_path` is a session-scoped fixture providing a `pathlib.Path` to a unique temporary directory per test function.

**Code:**
```python
def test_writes_file(tmp_path):
    target = tmp_path / "data.txt"
    target.write_text("hello")
    assert target.read_text() == "hello"
```

## Q40: What is `tmpdir` and how does it differ from `tmp_path`?
**A:** `tmpdir` provides a `py.path.local` object (legacy API); `tmp_path` (preferred) provides a modern `pathlib.Path`.

**Code:**
```python
def test_with_tmpdir(tmpdir):
    f = tmpdir.join("note.txt")
    f.write("legacy api")
    assert f.read() == "legacy api"


def test_with_tmp_path(tmp_path):
    f = tmp_path / "note.txt"
    f.write_text("modern api")
    assert f.read_text() == "modern api"
```

## Q41: How do you capture stdout/stderr in tests?
**A:** Use `capsys` fixture: `def test(capsys): print("hi"); assert capsys.readouterr().out == "hi\n"`.

**Code:**
```python
def test_capture(capsys):
    print("hi")
    captured = capsys.readouterr()
    assert captured.out == "hi\n"
```

## Q42: What is the difference between `capsys` and `capfd`?
**A:** `capsys` captures Python-level stdout/stderr (sys.stdout); `capfd` captures at file-descriptor level, also catching output from subprocesses.

**Code:**
```python
import subprocess


def test_capsys_python_level(capsys):
    print("python-level")
    assert "python-level" in capsys.readouterr().out


def test_capfd_fd_level(capfd):
    subprocess.run(["echo", "from-subprocess"], check=True)
    captured = capfd.readouterr()
    assert "from-subprocess" in captured.out
```

## Q43: What is `monkeypatch`?
**A:** The `monkeypatch` fixture temporarily modifies attributes, environment variables, or dict items, automatically reverting after the test.

**Code:**
```python
import os


def test_env_variable(monkeypatch):
    monkeypatch.setenv("API_KEY", "secret-test")
    assert os.environ["API_KEY"] == "secret-test"


def test_env_not_leaking():
    assert "API_KEY" not in os.environ  # reverted automatically
```

## Q44: How do you mock with `monkeypatch`?
**A:** `monkeypatch.setattr(module, "func", lambda: 42)` replaces `module.func` for the test duration.

**Code:**
```python
import os


def test_replaces_attribute(monkeypatch):
    monkeypatch.setattr(os, "getcwd", lambda: "/mocked/path")
    assert os.getcwd() == "/mocked/path"
```

## Q45: What is the difference between `monkeypatch` and `unittest.mock`?
**A:** `monkeypatch` is pytest-native and auto-reverts via fixture; `unittest.mock` (Mock/Patch) is stdlib-based and more flexible for complex mocking but requires manual cleanup or context managers.

**Code:**
```python
from unittest import mock


def test_monkeypatch_auto_revert(monkeypatch):
    monkeypatch.setattr("os.getcwd", lambda: "/monkey")
    assert os.getcwd() == "/monkey"


def test_unittest_mock_block():
    with mock.patch("os.getcwd", return_value="/mock"):
        assert os.getcwd() == "/mock"
```

## Q46: What is `pytest-mock`?
**A:** A plugin providing the `mocker` fixture wrapping `unittest.mock`, offering `mocker.patch`, `mocker.Mock`, etc., with auto-cleanup.

**Code:**
```python
def test_decorate(mocker):
    fake = mocker.patch("os.getcwd", return_value="/virtual")
    assert os.getcwd() == "/virtual"
    fake.assert_called_once()
```

## Q47: How do you use the `mocker` fixture?
**A:** `def test(mocker): m = mocker.patch("module.fn", return_value=5); assert module.fn() == 5`.

**Code:**
```python
import os


def test_uses_mocker(mocker):
    mocked = mocker.patch("os.getenv", return_value="token")
    assert os.getenv("API_KEY") == "token"
    mocked.assert_called_once_with("API_KEY")
```

## Q48: What is `pytest-cov`?
**A:** A plugin integrating coverage.py; run `pytest --cov=myapp` to report code coverage alongside tests.

**Code:**
```python
# Run with: pytest --cov=calculator
def calculator_add(a, b):
    return a + b


def test_add():
    assert calculator_add(2, 3) == 5
```

## Q49: How do you generate an HTML coverage report?
**A:** `pytest --cov=myapp --cov-report=html` produces an `htmlcov/` directory with a browsable report.

**Code:**
```python
# Run with: pytest --cov=. --cov-report=html  -> opens ./htmlcov/index.html
def covered():
    return True


def test_covered():
    assert covered()
```

## Q50: What is `pytest-xdist`?
**A:** A plugin for parallel test execution using `pytest -n 4` (or `-n auto`) to run tests across multiple CPUs.

**Code:**
```python
# Run with: pytest -n 4  (or pytest -n auto)
def test_parallel_one():
    assert 1 + 1 == 2


def test_parallel_two():
    assert 2 + 2 == 4
```

## Q51: How does `pytest-xdist` affect fixtures?
**A:** Each worker gets its own process, so `session`-scoped fixtures run separately per worker; avoid shared mutable global state.

**Code:**
```python
import pytest


@pytest.fixture(scope="session")
def worker_local():
    return []  # fresh instance inside every xdist worker process


def test_appends(worker_local):
    worker_local.append(1)
    assert worker_local == [1]
```

## Q52: What is `pytest-html`?
**A:** A plugin generating a self-contained HTML report of test results via `pytest --html=report.html`.

**Code:**
```python
# Run with: pytest --html=report.html  -> opens ./report.html
def test_passes():
    assert True
```

## Q53: What is `pytest-asyncio`?
**A:** A plugin enabling async test functions; mark with `@pytest.mark.asyncio` and use `async def test_...(...)`.

**Code:**
```python
import pytest


async def fetch_value():
    return 42


@pytest.mark.asyncio
async def test_async_fn():
    assert await fetch_value() == 42
```

## Q54: How do you configure `pytest-asyncio` mode?
**A:** Set `asyncio_mode = auto` in config to run async tests without the marker, or use `strict` (default) with explicit markers.

**Code:**
```python
# pyproject.toml
# [tool.pytest.ini_options]
# asyncio_mode = "auto"

async def test_no_marker_needed():
    assert True
```

## Q55: What are pytest hooks?
**A:** Hooks are callable functions (e.g., `pytest_collection_modifyitems`, `pytest_runtest_setup`) you implement in `conftest.py` to customize the test lifecycle.

**Code:**
```python
# conftest.py
def pytest_runtest_setup(item):
    print(f"setting up {item.name}", end=" ")
```

## Q56: What is `pytest_configure`?
**A:** A hook called after command-line options are parsed; used to register markers, plugins, or customize config.

**Code:**
```python
# conftest.py
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")
```

## Q57: What is `pytest_collection_modifyitems`?
**A:** A hook to modify collected items, e.g., auto-adding markers: `def pytest_collection_modifyitems(items): for i in items: i.add_marker(...)`.

**Code:**
```python
# conftest.py
def pytest_collection_modifyitems(items):
    for item in items:
        if "integration" in item.nodeid:
            item.add_marker("slow")
```

## Q58: What is `pytest_runtest_protocol`?
**A:** A hook defining the runtest protocol (setup, call, teardown) for a single test item; rarely overridden.

**Code:**
```python
# conftest.py
def pytest_runtest_protocol(item, nextitem):
    if nextitem is None:
        pass  # this is the last test in the session
    return None  # None -> let pytest run the default protocol
```

## Q59: What is the `pytest_addoption` hook used for?
**A:** To add custom command-line options: `def pytest_addoption(parser): parser.addoption("--env", action="store", default="dev")`.

**Code:**
```python
# conftest.py
def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="dev")
```

## Q60: How do you access a custom CLI option in a fixture?
**A:** `request.config.getoption("--env")` inside a fixture that takes `request`.

**Code:**
```python
import pytest


@pytest.fixture
def env(request):
    return request.config.getoption("--env")


# Run with: pytest --env staging
def test_env(env):
    assert env in ("dev", "staging", "prod")
```

## Q61: What is `pytest_generate_tests`?
**A:** A hook letting you parametrize tests dynamically based on the test item or CLI options, implementing custom parametrization logic.

**Code:**
```python
# conftest.py
def pytest_generate_tests(metafunc):
    if "value" in metafunc.fixturenames:
        metafunc.parametrize("value", dynamic_cases())


def dynamic_cases():
    return [1, 2, 3]
```

## Q62: How do you implement custom parametrization with `pytest_generate_tests`?
**A:** `def pytest_generate_tests(metafunc): if "data" in metafunc.fixturenames: metafunc.parametrize("data", load_cases())`.

**Code:**
```python
# conftest.py
def load_cases():
    return [(1, 2), (3, 4)]


def pytest_generate_tests(metafunc):
    if "pair" in metafunc.fixturenames:
        metafunc.parametrize("pair", load_cases())


# test_case.py
def test_pairs(pair):
    a, b = pair
    assert b == a + 1
```

## Q63: What is `metafunc`?
**A:** The object passed to `pytest_generate_tests` providing access to the test function's fixtures (`fixturenames`) and methods like `parametrize`.

**Code:**
```python
# conftest.py
def pytest_generate_tests(metafunc):
    if "param" in metafunc.fixturenames:  # fixturenames -> which args to fill
        metafunc.parametrize("param", ["a", "b"])


# test_param.py
def test_param(param):
    assert param in ("a", "b")
```

## Q64: What is the `request` fixture?
**A:** A built-in fixture giving access to the requesting test context: `request.param`, `request.config`, `request.node`, `request.addfinalizer`.

**Code:**
```python
import pytest


@pytest.fixture(params=[5, 10])
def scaled(request):
    assert request.config  # config access
    return request.param * 2


def test_scaled(scaled):
    assert scaled in (10, 20)
```

## Q65: What is `request.node`?
**A:** The test item object; `request.node.name` gives the test name, useful in fixtures and hooks.

**Code:**
```python
import pytest


@pytest.fixture
def test_name(request):
    return request.node.name


def test_current(test_name):
    assert test_name == "test_current"
```

## Q66: How do you order fixtures / control fixture execution?
**A:** Fixtures execute in order of dependency (by argument name); use `pytest-ordering` plugin or explicit dependencies; pytest runs fixtures based on the test's requested arguments.

**Code:**
```python
import pytest


@pytest.fixture
def inner():
    return {"ready": True}


@pytest.fixture
def outer(inner):  # inner set up before outer
    return {"child": inner}


def test_ordered(outer):
    assert outer["child"]["ready"]
```

## Q67: Can fixtures depend on other fixtures?
**A:** Yes, a fixture can request another fixture as an argument: `@pytest.fixture def db(app): ...` where `app` is a fixture.

**Code:**
```python
import pytest


@pytest.fixture
def app():
    return {"name": "blog"}


@pytest.fixture
def db(app):
    return {"app_name": app["name"]}


def test_db_knows_app(db):
    assert db["app_name"] == "blog"
```

## Q68: What is a factory fixture?
**A:** A fixture that returns a function creating resources, allowing the test to create multiple instances: `def factory(): return Client()` returned from the fixture.

**Code:**
```python
import pytest


@pytest.fixture
def make_user():
    users = []

    def _make(name):
        user = {"name": name}
        users.append(user)
        return user

    return _make


def test_factory(make_user):
    alice = make_user("alice")
    bob = make_user("bob")
    assert alice["name"] != bob["name"]
```

## Q69: Should a fixture `return` or `yield`?
**A:** Use `return` to provide a value; use `yield` when you also need teardown code to run after the test.

**Code:**
```python
import pytest


@pytest.fixture
def plain_value():
    return 42  # no teardown needed


@pytest.fixture
def opened_file(tmp_path, monkeypatch):
    f = tmp_path / "log.txt"
    f.write_text("start")
    yield f  # teardown below
    f.unlink()
```

## Q70: How do you share fixtures across multiple test files?
**A:** Put them in a `conftest.py` (at an appropriate directory level) or a shared module imported via `pytest_plugins` in `conftest.py`.

**Code:**
```python
# conftest.py (project root) -> visible to every test file
import pytest


@pytest.fixture
def shared_config():
    return {"debug": False}


# tests/test_one.py and tests/test_two.py can both request shared_config
def test_reads_shared(shared_config):
    assert shared_config["debug"] is False
```

## Q71: What is `pytest_plugins`?
**A:** A variable in `conftest.py` listing module names to import as plugins: `pytest_plugins = ["tests.fixtures.common"]`.

**Code:**
```python
# conftest.py
pytest_plugins = ["tests.fixtures.common"]


# tests/fixtures/common.py
import pytest


@pytest.fixture
def shared_fixture():
    return "loaded from plugin module"
```

## Q72: How do you test `print` output without `capsys`?
**A:** Prefer `capsys`; alternatively redirect `sys.stdout` manually, but `capsys` is cleaner and auto-restores.

**Code:**
```python
import io
import sys


def test_manual_redirect():
    buffer = io.StringIO()
    old = sys.stdout
    sys.stdout = buffer
    try:
        print("captured")
    finally:
        sys.stdout = old
    assert buffer.getvalue() == "captured\n"
```

## Q73: What is doctest integration in pytest?
**A:** Use `--doctest-modules` to run doctests in `.py` files, or `--doctest-glob="*.txt"`; pytest collects and reports doctest failures as tests.

**Code:**
```python
def add(a, b):
    """Return a + b.

    >>> add(2, 3)
    5
    """
    return a + b
```

## Q74: How do you run doctests with pytest?
**A:** `pytest --doctest-modules mymodule.py` executes the examples in docstrings as tests.

**Code:**
```python
# Run with: pytest --doctest-modules math_utils.py
def square(x):
    """Return x squared.

    >>> square(4)
    16
    """
    return x * x
```

## Q75: How do you configure pytest via `pytest.ini`?
**A:** Create `pytest.ini` with `[pytest]` section: `addopts = -v`, `testpaths = tests`, `markers = slow: ...`.

**Code:**
```python
# pytest.ini
# [pytest]
# addopts = -v
# testpaths = tests
# markers = slow: marks tests as slow
```

## Q76: How do you configure pytest via `pyproject.toml`?
**A:** Use `[tool.pytest.ini_options]` table: `testpaths = ["tests"]`, `addopts = ["-ra", "-q"]`, `markers = ["slow: ..."]`.

**Code:**
```python
# pyproject.toml
# [tool.pytest.ini_options]
# testpaths = ["tests"]
# addopts = ["-ra", "-q"]
# markers = ["slow: marks tests as slow"]
```

## Q77: What is `addopts` in pytest config?
**A:** `addopts` specifies default CLI options added to every invocation, e.g. `addopts = -ra -q --cov`.

**Code:**
```python
# pytest.ini
# [pytest]
# addopts = -ra -q --cov=src
```

## Q78: What is `testpaths`?
**A:** A list of directories/files to search for tests by default, speeding up collection: `testpaths = tests`.

**Code:**
```python
# pytest.ini
# [pytest]
# testpaths = tests
```

## Q79: How do you set a minimum pytest version in config?
**A:** `minversion = 7.0` in `[pytest]` ensures the test run requires at least that version.

**Code:**
```python
# pytest.ini
# [pytest]
# minversion = 7.0
```

## Q80: How do you ignore certain paths during collection?
**A:** Use `norecursedirs = .git build dist` in config to prevent descending into those directories.

**Code:**
```python
# pytest.ini
# [pytest]
# norecursedirs = .git build dist venv
```

## Q81: What is `pytest.raises` versus `pytest.warns`?
**A:** `pytest.raises` checks an exception is raised; `pytest.warns(Warning)` checks a warning is emitted.

**Code:**
```python
import warnings

import pytest


def raises_error():
    raise ValueError("bad")


def emits_warning():
    warnings.warn("old API", DeprecationWarning)


def test_raises():
    with pytest.raises(ValueError):
        raises_error()


def test_warns():
    with pytest.warns(DeprecationWarning):
        emits_warning()
```

## Q82: How do you test warnings?
**A:** `with pytest.warns(DeprecationWarning): legacy_func()` asserts the warning is triggered.

**Code:**
```python
import warnings

import pytest


def legacy_func():
    warnings.warn("use new_func()", DeprecationWarning)


def test_warns_deprecation():
    with pytest.warns(DeprecationWarning):
        legacy_func()
```

## Q83: What is `assert` vs `pytest.fail`?
**A:** `assert` checks a condition with detailed output; `pytest.fail("reason")` immediately fails the test unconditionally.

**Code:**
```python
import pytest


def test_assert_style():
    result = expensive_check()
    assert result == "ok"

def expensive_check():
    return "ok"


def test_fail_style():
    if not condition_met():
        pytest.fail("required precondition was not met")

def condition_met():
    return False
```

## Q84: How do you run only failed tests from last run?
**A:** `pytest --lf` (last-failed) reruns only tests that failed previously; `--ff` runs failures first then the rest.

**Code:**
```python
# Run with: pytest --lf   (only rerun the failing test below)
def test_the_flaky_failure():
    assert True


def test_always_passes():
    assert True
```

## Q85: What does `pytest --pdb` do?
**A:** Drops into the Python debugger (pdb) on failures, letting you inspect state interactively.

**Code:**
```python
# Run with: pytest --pdb  -> lands in pdb on the failing line below
def test_inspect_on_failure():
    value = {"count": 3}
    assert value["count"] == 5
```

## Q86: How do you set up a database fixture for tests?
**A:** Use a session/module-scoped fixture that creates a test DB in setup and drops it in teardown (after `yield`), e.g., with `yield engine` then `engine.dispose()`.

**Code:**
```python
import pytest


@pytest.fixture(scope="session")
def engine():
    engine = create_test_engine()
    yield engine
    engine.dispose()  # teardown drops the test database


def create_test_engine():
    return {"disposed": False}


def test_db_up(engine):
    assert engine["disposed"] is False
```

## Q87: How do you avoid tests affecting each other (isolation)?
**A:** Use function-scoped fixtures for state, rely on `tmp_path` for files, and avoid module-level mutable globals.

**Code:**
```python
import pytest


@pytest.fixture  # function scope: fresh state per test
def store():
    return []


def test_first(store):
    store.append(1)
    assert store == [1]


def test_second(store, tmp_path):
    assert store == []  # isolated
    f = tmp_path / "x.txt"
    f.write_text("unique")
    assert f.exists()
```

## Q88: What are best practices for naming tests?
**A:** Name test files `test_*.py`, functions `test_*`, and describe behavior: `test_login_fails_with_wrong_password`.

**Code:**
```python
def test_login_fails_with_wrong_password():
    assert login("admin", "wrong") is None


def login(user, password):
    return user if password == "correct" else None
```

## Q89: Should you import unittest in pytest?
**A:** Not required; pytest supports plain functions. You can still run unittest-based tests, but pytest-style asserts are preferred.

**Code:**
```python
# No `import unittest` needed — plain functions work
def test_plain_pytest_style():
    result = 2 + 2
    assert result == 4
```

## Q90: How does pytest compare to unittest?
**A:** pytest needs less boilerplate (no `TestCase` subclasses/`self.assert*` methods), has fixtures and rich plugins, while unittest is stdlib-only with xUnit style.

**Code:**
```python
# pytest: no class, no self.assert* — a bare function with assert
def test_concise():
    assert len("pytest") == 6
```

## Q91: Can pytest run unittest tests?
**A:** Yes, pytest discovers and runs `unittest.TestCase` classes, though some unittest-specific features behave slightly differently.

**Code:**
```python
import unittest


class TestLegacy(unittest.TestCase):
    def test_unittest_ran_by_pytest(self):
        self.assertEqual(2 + 2, 4)
```

## Q92: What is the difference between a mock and a fixture?
**A:** A fixture provides test context/resources; a mock replaces a dependency with a test double. Mocks are often used inside fixtures or tests to isolate units.

**Code:**
```python
import pytest


@pytest.fixture
def client():
    return {"base_url": "https://api.example.com"}  # context


def test_with_fixture_and_mock(client, mocker):
    fake = mocker.patch("os.getcwd", return_value="/vfs")
    assert client["base_url"] == "https://api.example.com"
    assert os.getcwd() == "/vfs"
    fake.assert_called_once()
```

## Q93: How do you mock an environment variable?
**A:** `monkeypatch.setenv("API_KEY", "test")` or `mocker.patch.dict(os.environ, {"KEY":"VAL"})`.

**Code:**
```python
import os
import pytest


def test_monkeypatch_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test")
    assert os.environ["API_KEY"] == "test"


def test_mocker_patch_dict(mocker):
    mocker.patch.dict(os.environ, {"FLAG": "on"})
    assert os.environ["FLAG"] == "on"
```

## Q94: How do you test code that calls `time`/`datetime`?
**A:** Use `mocker.patch("module.datetime")` or `freezegun` library; monkeypatch `time.time` to return a fixed value.

**Code:**
```python
import time


def epoch_hour():
    return int(time.time()) // 3600


def test_fixed_time(monkeypatch):
    monkeypatch.setattr(time, "time", lambda: 3600.0)
    assert epoch_hour() == 1
```

## Q95: What is `pytest.fixture` `name` parameter?
**A:** `@pytest.fixture(name="db")` lets you request the fixture under a different name than the function name.

**Code:**
```python
import pytest


@pytest.fixture(name="db")
def database_connection():
    return {"connected": True}


def test_reads_db(db):  # requested as `db`, not `database_connection`
    assert db["connected"]
```

## Q96: How do you debug why a fixture isn't found?
**A:** Ensure the fixture is in `conftest.py` or imported via `pytest_plugins`, and that its name matches the test argument; check scope/visibility by directory.

**Code:**
```python
# conftest.py
import pytest


@pytest.fixture
def avail_fixture():
    return "here"


# test_foo.py — the argument name must match exactly
def test_asks(avail_fixture):
    assert avail_fixture == "here"
```

## Q97: What is the `cache` fixture?
**A:** `request.config.cache` (or `cache` fixture) stores cross-run data via `cache.set/get`, used by `--lf` and custom persistence.

**Code:**
```python
def test_store_and_read(cache):
    cache.set("env/name", "staging")
    assert cache.get("env/name", None) == "staging"
```

## Q98: How do you integrate pytest with CI (e.g., GitHub Actions)?
**A:** Add a step running `pytest` (often with `--junitxml=report.xml` for results) and install deps; ensure exit codes propagate failures.

**Code:**
```python
# .github/workflows/ci.yml (excerpt)
# - run: pip install -r requirements-dev.txt
# - run: pytest --junitxml=report.xml

def test_ci_safe():
    assert True
```

## Q99: What does `--junitxml` do?
**A:** Writes a JUnit-style XML report (`pytest --junitxml=report.xml`) consumable by CI systems for test result display.

**Code:**
```python
# Run with: pytest --junitxml=report.xml  -> produces report.xml
def test_passes():
    assert True
```

## Q100: What are common pytest pitfalls to avoid?
**A:** Forgetting to register markers, using module-level mutable state, relying on test execution order, naming files incorrectly so they aren't collected, and not using `yield` for teardown (causing resource leaks).

**Code:**
```python
import pytest


@pytest.mark.slow  # register `slow` in config to avoid warnings
def test_registered_marker():
    assert True


@pytest.fixture
def handle():
    f = {"open": True}
    yield f  # teardown prevents resource leaks
    f["open"] = False
```