import subprocess


def prepublish():
    # test
    subprocess.call(["pytest"])
    # type checking
    subprocess.call(["mypy", "-p", "terra_sdk"])
    # isort before black
    subprocess.call(["isort", "terra_sdk"])
    subprocess.call(["black", "terra_sdk"])
