# Pytest Interview Questions and Answers (Top 100)

## Q1: What is pytest and why is it popular?
**A:** Pytest is a mature, feature-rich Python testing framework that supports simple unit tests and complex functional testing. It is popular for its concise assert statements, powerful fixtures, rich plugin ecosystem, and minimal boilerplate compared to unittest.

## Q2: How do you install pytest?
**A:** Install via pip: `pip install pytest`. For specific versions use `pip install pytest==8.0.0`.

## Q3: What is the minimum pytest version recommended today?
**A:** pytest 7.x and 8.x are current; pytest 8 drops Python 3.7 support and makes several long-deprecated features error. Target pytest 7/8 in modern projects.

## Q4: How do you run all tests in a project?
**A:** Run `pytest` in the project root. It auto-discovers files matching `test_*.py` or `*_test.py` and functions/classes starting with `test`.

## Q5: What are pytest's default test discovery rules?
**A:** Files must match `test_*.py` or `*_test.py`; functions/classes must start with `test_` (classes may not have an `__init__`). Test methods inside classes must also start with `test_`.

## Q6: How do you run a single test file?
**A:** `pytest tests/test_sample.py`.

## Q7: How do you run a single test function?
**A:** `pytest tests/test_sample.py::test_function_name`.

## Q8: What does `pytest -v` do?
**A:** `-v` (verbose) shows each test with its result (PASSED/FAILED) and an OK/FAIL indicator, giving more detail than the default dotted output.

## Q9: What does `pytest -x` do?
**A:** `-x` stops the test session after the first failure, useful for quick feedback loops.

## Q10: What does `pytest --tb=short` (or `line`, `long`, `no`) do?
**A:** Controls traceback verbosity. `short` shows concise tracebacks, `line` shows one line per failure, `no` hides tracebacks, `long` is the most verbose.

## Q11: What does `pytest -s` do?
**A:** `-s` disables output capturing so `print()` statements appear in the terminal during the run.

## Q12: What does `pytest -k` do?
**A:** `-k` selects tests by substring expression, e.g. `pytest -k "login or logout"` runs tests whose names contain "login" or "logout".

## Q13: What does `pytest -m` do?
**A:** `-m` runs tests marked with a given marker expression, e.g. `pytest -m "slow"` runs only tests marked slow.

## Q14: What is the purpose of `conftest.py`?
**A:** `conftest.py` holds fixtures, hooks, and plugin configuration shared across tests in its directory and subdirectories; it is auto-loaded by pytest.

## Q15: How is `conftest.py` scoped?
**A:** A `conftest.py` applies to its own directory and all subdirectories. Multiple `conftest.py` files can exist at different levels, with deeper ones overriding/extending outer ones.

## Q16: What is a pytest fixture?
**A:** A fixture is a function decorated with `@pytest.fixture` that provides a fixed baseline (data, state, resources) to tests via dependency injection by name.

## Q17: How do you use a fixture in a test?
**A:** Declare it as a test function argument with the same name: `def test_a(my_fixture): assert my_fixture == 1`.

## Q18: What are fixture scopes?
**A:** Scopes are `function` (default), `class`, `module`, `package`, and `session`, controlling how often the fixture is set up/ torn down.

## Q19: What is the default fixture scope?
**A:** `function`—the fixture is created and destroyed for each test function.

## Q20: How do you set a fixture scope?
**A:** Use `@pytest.fixture(scope="session")`; valid values: `function`, `class`, `module`, `package`, `session`.

## Q21: How do you implement fixture teardown?
**A:** Use `yield` instead of `return`; code after `yield` runs as teardown: `yield resource` then `resource.close()`.

## Q22: What is fixture finalization with `addfinalizer`?
**A:** `request.addfinalizer(func)` registers cleanup that runs even if the fixture setup fails, unlike `yield` which only tears down after successful setup.

## Q23: What is an `autouse` fixture?
**A:** A fixture with `@pytest.fixture(autouse=True)` is applied automatically to all tests in its scope without needing to be requested as an argument.

## Q24: How do you parametrize a fixture?
**A:** Use `@pytest.fixture(params=[1,2,3])`; the fixture receives `request` and returns `request.param`, running the test once per param.

## Q25: What does `@pytest.mark.parametrize` do?
**A:** It runs a test multiple times with different arguments: `@pytest.mark.parametrize("a,b,expected",[(1,2,3),(2,3,5)])`.

## Q26: How do you give readable IDs to parametrized tests?
**A:** Pass `ids=["case1","case2"]` or use `ids=str`/`ids=lambda x: f"v{x}"` to customize test IDs in reports.

## Q27: Can you parametrize with multiple arguments?
**A:** Yes: `@pytest.mark.parametrize("x,y",[(1,2),(3,4)])` injects `x` and `y` into the test.

## Q28: What is the difference between fixture `params` and `@pytest.mark.parametrize`?
**A:** `params` on a fixture parametrizes the fixture (and any test using it), while `parametrize` parametrizes the specific test function directly.

## Q29: How do you mark a test as expected to fail?
**A:** Use `@pytest.mark.xfail` to mark a test that should fail; pytest reports XFAIL if it fails and XPASS if it unexpectedly passes.

## Q30: What is the difference between `skip` and `xfail`?
**A:** `skip` omits the test entirely (reported SKIPPED); `xfail` runs it and reports XFAIL/XPASS depending on outcome.

## Q31: How do you skip a test conditionally?
**A:** Use `@pytest.mark.skipif(sys.version_info < (3,8), reason="needs py3.8+")` or `pytest.skip(msg)` inside the test.

## Q32: How do you skip a test unconditionally?
**A:** `@pytest.mark.skip(reason="not implemented yet")`.

## Q33: What are custom markers and how do you register them?
**A:** Define markers like `@pytest.mark.slow` and register them in `pytest.ini`/`pyproject.toml` under `[pytest] markers = slow: marks slow tests` to avoid warnings.

## Q34: What is `strict` markers mode?
**A:** With `filterwarnings`/`--strict-markers`, pytest errors on unregistered markers, preventing typos in marker names.

## Q35: How does assert rewriting work in pytest?
**A:** pytest rewrites the bytecode of assert statements to provide detailed introspection of values on failure (showing left/right operands), instead of just "AssertionError".

## Q36: How do you compare floats with pytest?
**A:** Use `pytest.approx`: `assert 0.1 + 0.2 == pytest.approx(0.3)` for tolerant floating-point comparison.

## Q37: How do you test that an exception is raised?
**A:** Use `with pytest.raises(ValueError): func()`; you can also inspect `excinfo`: `with pytest.raises(ValueError) as ei: ...`.

## Q38: How do you check the exception message with `pytest.raises`?
**A:** Use `match`: `with pytest.raises(ValueError, match="invalid"): ...` (regex match against the message).

## Q39: What is `tmp_path`?
**A:** `tmp_path` is a session-scoped fixture providing a `pathlib.Path` to a unique temporary directory per test function.

## Q40: What is `tmpdir` and how does it differ from `tmp_path`?
**A:** `tmpdir` provides a `py.path.local` object (legacy API); `tmp_path` (preferred) provides a modern `pathlib.Path`.

## Q41: How do you capture stdout/stderr in tests?
**A:** Use `capsys` fixture: `def test(capsys): print("hi"); assert capsys.readouterr().out == "hi\n"`.

## Q42: What is the difference between `capsys` and `capfd`?
**A:** `capsys` captures Python-level stdout/stderr (sys.stdout); `capfd` captures at file-descriptor level, also catching output from subprocesses.

## Q43: What is `monkeypatch`?
**A:** The `monkeypatch` fixture temporarily modifies attributes, environment variables, or dict items, automatically reverting after the test.

## Q44: How do you mock with `monkeypatch`?
**A:** `monkeypatch.setattr(module, "func", lambda: 42)` replaces `module.func` for the test duration.

## Q45: What is the difference between `monkeypatch` and `unittest.mock`?
**A:** `monkeypatch` is pytest-native and auto-reverts via fixture; `unittest.mock` (Mock/Patch) is stdlib-based and more flexible for complex mocking but requires manual cleanup or context managers.

## Q46: What is `pytest-mock`?
**A:** A plugin providing the `mocker` fixture wrapping `unittest.mock`, offering `mocker.patch`, `mocker.Mock`, etc., with auto-cleanup.

## Q47: How do you use the `mocker` fixture?
**A:** `def test(mocker): m = mocker.patch("module.fn", return_value=5); assert module.fn() == 5`.

## Q48: What is `pytest-cov`?
**A:** A plugin integrating coverage.py; run `pytest --cov=myapp` to report code coverage alongside tests.

## Q49: How do you generate an HTML coverage report?
**A:** `pytest --cov=myapp --cov-report=html` produces an `htmlcov/` directory with a browsable report.

## Q50: What is `pytest-xdist`?
**A:** A plugin for parallel test execution using `pytest -n 4` (or `-n auto`) to run tests across multiple CPUs.

## Q51: How does `pytest-xdist` affect fixtures?
**A:** Each worker gets its own process, so `session`-scoped fixtures run separately per worker; avoid shared mutable global state.

## Q52: What is `pytest-html`?
**A:** A plugin generating a self-contained HTML report of test results via `pytest --html=report.html`.

## Q53: What is `pytest-asyncio`?
**A:** A plugin enabling async test functions; mark with `@pytest.mark.asyncio` and use `async def test_...(...)`.

## Q54: How do you configure `pytest-asyncio` mode?
**A:** Set `asyncio_mode = auto` in config to run async tests without the marker, or use `strict` (default) with explicit markers.

## Q55: What are pytest hooks?
**A:** Hooks are callable functions (e.g., `pytest_collection_modifyitems`, `pytest_runtest_setup`) you implement in `conftest.py` to customize the test lifecycle.

## Q56: What is `pytest_configure`?
**A:** A hook called after command-line options are parsed; used to register markers, plugins, or customize config.

## Q57: What is `pytest_collection_modifyitems`?
**A:** A hook to modify collected items, e.g., auto-adding markers: `def pytest_collection_modifyitems(items): for i in items: i.add_marker(...)`.

## Q58: What is `pytest_runtest_protocol`?
**A:** A hook defining the runtest protocol (setup, call, teardown) for a single test item; rarely overridden.

## Q59: What is the `pytest_addoption` hook used for?
**A:** To add custom command-line options: `def pytest_addoption(parser): parser.addoption("--env", action="store", default="dev")`.

## Q60: How do you access a custom CLI option in a fixture?
**A:** `request.config.getoption("--env")` inside a fixture that takes `request`.

## Q61: What is `pytest_generate_tests`?
**A:** A hook letting you parametrize tests dynamically based on the test item or CLI options, implementing custom parametrization logic.

## Q62: How do you implement custom parametrization with `pytest_generate_tests`?
**A:** `def pytest_generate_tests(metafunc): if "data" in metafunc.fixturenames: metafunc.parametrize("data", load_cases())`.

## Q63: What is `metafunc`?
**A:** The object passed to `pytest_generate_tests` providing access to the test function's fixtures (`fixturenames`) and methods like `parametrize`.

## Q64: What is the `request` fixture?
**A:** A built-in fixture giving access to the requesting test context: `request.param`, `request.config`, `request.node`, `request.addfinalizer`.

## Q65: What is `request.node`?
**A:** The test item object; `request.node.name` gives the test name, useful in fixtures and hooks.

## Q66: How do you order fixtures / control fixture execution?
**A:** Fixtures execute in order of dependency (by argument name); use `pytest-ordering` plugin or explicit dependencies; pytest runs fixtures based on the test's requested arguments.

## Q67: Can fixtures depend on other fixtures?
**A:** Yes, a fixture can request another fixture as an argument: `@pytest.fixture def db(app): ...` where `app` is a fixture.

## Q68: What is a factory fixture?
**A:** A fixture that returns a function creating resources, allowing the test to create multiple instances: `def factory(): return Client()` returned from the fixture.

## Q69: Should a fixture `return` or `yield`?
**A:** Use `return` to provide a value; use `yield` when you also need teardown code to run after the test.

## Q70: How do you share fixtures across multiple test files?
**A:** Put them in a `conftest.py` (at an appropriate directory level) or a shared module imported via `pytest_plugins` in `conftest.py`.

## Q71: What is `pytest_plugins`?
**A:** A variable in `conftest.py` listing module names to import as plugins: `pytest_plugins = ["tests.fixtures.common"]`.

## Q72: How do you test `print` output without `capsys`?
**A:** Prefer `capsys`; alternatively redirect `sys.stdout` manually, but `capsys` is cleaner and auto-restores.

## Q73: What is doctest integration in pytest?
**A:** Use `--doctest-modules` to run doctests in `.py` files, or `--doctest-glob="*.txt"`; pytest collects and reports doctest failures as tests.

## Q74: How do you run doctests with pytest?
**A:** `pytest --doctest-modules mymodule.py` executes the examples in docstrings as tests.

## Q75: How do you configure pytest via `pytest.ini`?
**A:** Create `pytest.ini` with `[pytest]` section: `addopts = -v`, `testpaths = tests`, `markers = slow: ...`.

## Q76: How do you configure pytest via `pyproject.toml`?
**A:** Use `[tool.pytest.ini_options]` table: `testpaths = ["tests"]`, `addopts = ["-ra", "-q"]`, `markers = ["slow: ..."]`.

## Q77: What is `addopts` in pytest config?
**A:** `addopts` specifies default CLI options added to every invocation, e.g. `addopts = -ra -q --cov`.

## Q78: What is `testpaths`?
**A:** A list of directories/files to search for tests by default, speeding up collection: `testpaths = tests`.

## Q79: How do you set a minimum pytest version in config?
**A:** `minversion = 7.0` in `[pytest]` ensures the test run requires at least that version.

## Q80: How do you ignore certain paths during collection?
**A:** Use `norecursedirs = .git build dist` in config to prevent descending into those directories.

## Q81: What is `pytest.raises` versus `pytest.warns`?
**A:** `pytest.raises` checks an exception is raised; `pytest.warns(Warning)` checks a warning is emitted.

## Q82: How do you test warnings?
**A:** `with pytest.warns(DeprecationWarning): legacy_func()` asserts the warning is triggered.

## Q83: What is `assert` vs `pytest.fail`?
**A:** `assert` checks a condition with detailed output; `pytest.fail("reason")` immediately fails the test unconditionally.

## Q84: How do you run only failed tests from last run?
**A:** `pytest --lf` (last-failed) reruns only tests that failed previously; `--ff` runs failures first then the rest.

## Q85: What does `pytest --pdb` do?
**A:** Drops into the Python debugger (pdb) on failures, letting you inspect state interactively.

## Q86: How do you set up a database fixture for tests?
**A:** Use a session/module-scoped fixture that creates a test DB in setup and drops it in teardown (after `yield`), e.g., with `yield engine` then `engine.dispose()`.

## Q87: How do you avoid tests affecting each other (isolation)?
**A:** Use function-scoped fixtures for state, rely on `tmp_path` for files, and avoid module-level mutable globals.

## Q88: What are best practices for naming tests?
**A:** Name test files `test_*.py`, functions `test_*`, and describe behavior: `test_login_fails_with_wrong_password`.

## Q89: Should you import unittest in pytest?
**A:** Not required; pytest supports plain functions. You can still run unittest-based tests, but pytest-style asserts are preferred.

## Q90: How does pytest compare to unittest?
**A:** pytest needs less boilerplate (no `TestCase` subclasses/`self.assert*` methods), has fixtures and rich plugins, while unittest is stdlib-only with xUnit style.

## Q91: Can pytest run unittest tests?
**A:** Yes, pytest discovers and runs `unittest.TestCase` classes, though some unittest-specific features behave slightly differently.

## Q92: What is the difference between a mock and a fixture?
**A:** A fixture provides test context/resources; a mock replaces a dependency with a test double. Mocks are often used inside fixtures or tests to isolate units.

## Q93: How do you mock an environment variable?
**A:** `monkeypatch.setenv("API_KEY", "test")` or `mocker.patch.dict(os.environ, {"KEY":"VAL"})`.

## Q94: How do you test code that calls `time`/`datetime`?
**A:** Use `mocker.patch("module.datetime")` or `freezegun` library; monkeypatch `time.time` to return a fixed value.

## Q95: What is `pytest.fixture` `name` parameter?
**A:** `@pytest.fixture(name="db")` lets you request the fixture under a different name than the function name.

## Q96: How do you debug why a fixture isn't found?
**A:** Ensure the fixture is in `conftest.py` or imported via `pytest_plugins`, and that its name matches the test argument; check scope/visibility by directory.

## Q97: What is the `cache` fixture?
**A:** `request.config.cache` (or `cache` fixture) stores cross-run data via `cache.set/get`, used by `--lf` and custom persistence.

## Q98: How do you integrate pytest with CI (e.g., GitHub Actions)?
**A:** Add a step running `pytest` (often with `--junitxml=report.xml` for results) and install deps; ensure exit codes propagate failures.

## Q99: What does `--junitxml` do?
**A:** Writes a JUnit-style XML report (`pytest --junitxml=report.xml`) consumable by CI systems for test result display.

## Q100: What are common pytest pitfalls to avoid?
**A:** Forgetting to register markers, using module-level mutable state, relying on test execution order, naming files incorrectly so they aren't collected, and not using `yield` for teardown (causing resource leaks).
