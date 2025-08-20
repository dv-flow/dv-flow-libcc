import os
import logging
import shlex
import subprocess
from dv_flow.mgr import TaskDataResult, FileSet

_log = logging.getLogger("SharedLib")

async def Object(runner, input):
    """
    Builds a shared library from a set of FileSet objects.
    """
    # Gather parameters
    cc = getattr(input.params, "cc", "gcc")
    cxx = getattr(input.params, "cxx", "g++")
    objname = getattr(input.params, "objname")
    filename = getattr(input.params, "filename")
    rundir = input.rundir
    status = 0

    # Collect all files, include dirs, and defines
    src_files = []
    obj_files = []
    incdirs = set()
    defines = set()
    has_cpp = False

    for fs in input.inputs:
        filetype = getattr(fs, "filetype", None)
        basedir = getattr(fs, "basedir", "")
        files = getattr(fs, "files", [])
        fs_incdirs = getattr(fs, "incdirs", [])
        fs_defines = getattr(fs, "defines", [])

        # Collect include dirs and defines
        for inc in fs_incdirs:
            incdirs.add(inc)
        for define in fs_defines:
            defines.add(define)

        # Classify files
        for f in files:
            # If basedir is not absolute, make it relative to rundir's parent
            abs_basedir = basedir
            full_path = os.path.abspath(os.path.join(abs_basedir, f))
            if filetype == "cSource":
                src_files.append(full_path)
            elif filetype == "cppSource":
                src_files.append(full_path)
                has_cpp = True
            elif filetype == "objFile":
                obj_files.append(full_path)

    # Select compiler
    compiler = cxx if has_cpp else cc

    if filename != "":
        src_files.append(filename)

    if len(src_files) > 1:
        raise Exception("Only one source file is supported")
    
    if len(obj_files) > 0:
        raise Exception("Object files are not currently supported")

    if objname == "":
        objname = os.path.splitext(os.path.basename(src_files[0]))[0] + ".o"

    # Build output path
    # Place output in the parent of rundir (the test's tmp_path)
    out_obj = os.path.abspath(os.path.join(rundir, objname))

    # Build command
    cmd = [compiler, "-c", "-o", out_obj]
    for inc in sorted(incdirs):
        cmd.append(f"-I{inc}")
    for define in sorted(defines):
        cmd.append(f"-D{define}")
    cmd.extend(src_files)
    cmd.extend(obj_files)

    # Ensure rundir exists
    os.makedirs(os.path.dirname(out_obj), exist_ok=True)

    # Run the command
    try:
        status = await runner.exec(cmd, cwd=rundir)
        changed = True
    except Exception as e:
        _log.error(f"Failed to build shared library: {e}")
        raise


    output_fileset = FileSet(
        filetype="objFile",
        basedir=os.path.dirname(out_obj),
        files=[out_obj]
    )

    return TaskDataResult(
        status=status,
        changed=changed,
        output=[output_fileset]
    )
