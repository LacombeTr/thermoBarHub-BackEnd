# conftest.py
def pytest_runtest_logreport(report):
    if report.when == "call":  # On s'intéresse à l'exécution des tests
        if report.passed:
            print(f"\033[92mPassed\033[0m - {report.nodeid}\n")
        elif report.failed:
            print(f"\033[91mFailed\033[0m - {report.nodeid}\n")