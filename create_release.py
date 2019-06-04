from subprocess import run, PIPE, CompletedProcess
from sys import platform, exit
from os import environ


python = "python" if platform == "win32" else "python3",


def main() -> int:
    # Prompt for version
    print("\n"
          "Did you increment the software version in `setup.py`?")
    input("Press ENTER to continue or CTRL+C to exit now...\n")

    # Check environmental variables || Automatically picked up by twine
    username = environ.get("TWINE_USERNAME", "")
    password = environ.get("TWINE_PASSWORD", "")
    if not (username and password):
        print("ERROR! Missing environmental variables.\n"
              "Please set the following environmental variables:\n"
              "  * TWINE_USERNAME\n"
              "  * TWINE_PASSWORD\n"
              )

    # Create sdist, bdist_wheel
    cmd_create_package = [
        python,
        "setup.py",
        "sdist",
        "bdist_wheel"
    ]
    proc_create_package: CompletedProcess = run(cmd_create_package, shell=True, stdout=PIPE, stderr=PIPE)
    if proc_create_package.stderr:
        print("ERROR:", proc_create_package.stderr)
        return 1

    # Upload to PyPi
    cmd_upload_to_pypi = [
        python,
        "-m",
        "twine",
        "upload",
        "dist/*"
    ]
    proc_upload_package: CompletedProcess = run(cmd_upload_to_pypi, shell=True, stdout=PIPE, stderr=PIPE)
    print("proc_upload_package stdout", proc_upload_package.stdout)
    print("proc_upload_package stderr", proc_upload_package.stderr)
    if proc_upload_package.stderr:
        print("ERROR:", proc_upload_package.stderr)
        return 1
    return 0


if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
