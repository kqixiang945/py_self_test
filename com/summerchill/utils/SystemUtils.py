import pkg_resources

"""
get local machine python installed modules
"""
def getLocalMachineModules():
    installed_packages = {d.project_name: d.version for d in pkg_resources.working_set}
    print(installed_packages)
    # or
    print(help('modules package'))


if __name__ == "__main__":
    getLocalMachineModules()
