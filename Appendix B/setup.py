import cx_Freeze

executables = [cx_Freeze.Executable("ants_game.py")]

cx_Freeze.setup(
    name="Ant Game",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["ant.png","leaf.png","spider.png",'gameobjects']}},
    executables = executables

    )
