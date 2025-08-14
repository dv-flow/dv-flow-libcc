import pytest
import os
from pytest_dfm import *

def test_shared_lib_c_only(tmp_path, dvflow):
    # Create a simple C source file
    src_file = tmp_path / "foo.c"
    src_file.write_text("int foo() { return 42; }\n")

    # Create FileSet task node
    fileset = dvflow.mkTask(
        "std.FileSet",
        name="c_files",
        base=".",
        type="cSource",
        include=[src_file.name],
        srcdir=str(tmp_path)
    )

    # Create SharedLib task node
    shared_lib = dvflow.mkTask(
        "cc.SharedLib",
        libname="testc",
        cc="gcc",
        cxx="g++",
        needs=[fileset],
        srcdir=str(tmp_path)
    )

    # Run the SharedLib task
    status, outputs = dvflow.runTask(shared_lib)
    assert status == 0
    out_fileset = outputs.output[0]
    out_lib = os.path.join(out_fileset.basedir, out_fileset.files[0])
    assert os.path.exists(out_lib)
    assert os.stat(out_lib).st_size > 0

def test_shared_lib_cpp_only(tmp_path, dvflow):
    # Create a simple C++ source file
    src_file = tmp_path / "bar.cpp"
    src_file.write_text("int bar() { return 99; }\n")

    fileset = dvflow.mkTask(
        "std.FileSet",
        name="cpp_files",
        base=".",
        type="cppSource",
        include=[src_file.name],
        srcdir=str(tmp_path)
    )

    shared_lib = dvflow.mkTask(
        "cc.SharedLib",
        libname="testcpp",
        cc="gcc",
        cxx="g++",
        needs=[fileset],
        srcdir=str(tmp_path)
    )

    status, outputs = dvflow.runTask(shared_lib)
    assert status == 0
    out_fileset = outputs.output[0]
    out_lib = os.path.join(out_fileset.basedir, out_fileset.files[0])
    assert os.path.exists(out_lib)
    assert os.stat(out_lib).st_size > 0

def test_shared_lib_c_and_cpp(tmp_path, dvflow):
    c_file = tmp_path / "foo.c"
    c_file.write_text("int foo() { return 1; }\n")
    cpp_file = tmp_path / "bar.cpp"
    cpp_file.write_text("int bar() { return 2; }\n")

    fileset_c = dvflow.mkTask(
        "std.FileSet",
        name="c_files",
        base=".",
        type="cSource",
        include=[c_file.name],
        srcdir=str(tmp_path)
    )
    fileset_cpp = dvflow.mkTask(
        "std.FileSet",
        name="cpp_files",
        base=".",
        type="cppSource",
        include=[cpp_file.name],
        srcdir=str(tmp_path)
    )

    shared_lib = dvflow.mkTask(
        "cc.SharedLib",
        libname="testmix",
        cc="gcc",
        cxx="g++",
        needs=[fileset_c, fileset_cpp],
        srcdir=str(tmp_path)
    )

    status, outputs = dvflow.runTask(shared_lib)
    assert status == 0
    out_fileset = outputs.output[0]
    out_lib = os.path.join(out_fileset.basedir, out_fileset.files[0])
    assert os.path.exists(out_lib)
    assert os.stat(out_lib).st_size > 0

def test_shared_lib_incdir_define(tmp_path, dvflow):
    incdir = tmp_path / "include"
    incdir.mkdir()
    header = incdir / "myhdr.h"
    header.write_text(
        "#ifndef MYHDR_H\n"
        "#define MYHDR_H\n"
        "#ifdef MYVAL\n"
        "#define VAL (MYVAL)\n"
        "#else\n"
        "#define VAL (0)\n"
        "#endif\n"
        "#endif\n"
    )

    src_file = tmp_path / "baz.c"
    src_file.write_text('#include "myhdr.h"\nint baz() { return VAL; }\n')

    fileset = dvflow.mkTask(
        "std.FileSet",
        name="c_files",
        base=".",
        type="cSource",
        include=[src_file.name],
        incdirs=[str(incdir)],
        defines=["MYVAL=123"],
        srcdir=str(tmp_path)
    )

    shared_lib = dvflow.mkTask(
        "cc.SharedLib",
        libname="testincdef",
        cc="gcc",
        cxx="g++",
        needs=[fileset],
        srcdir=str(tmp_path)
    )

    status, outputs = dvflow.runTask(shared_lib)
    assert status == 0
    out_fileset = outputs.output[0]
    out_lib = os.path.join(out_fileset.basedir, out_fileset.files[0])
    assert os.path.exists(out_lib)
    assert os.stat(out_lib).st_size > 0
