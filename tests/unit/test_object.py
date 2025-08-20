import pytest
import os
from pytest_dfm import *

def test_object_c_only(tmp_path, dvflow):
    # Create a simple C source file
    src_file = tmp_path / "foo.c"
    src_file.write_text("int foo() { return 42; }\n")

    fileset = dvflow.mkTask(
        "std.FileSet",
        name="c_files",
        base=".",
        type="cSource",
        include=[src_file.name],
        srcdir=str(tmp_path)
    )

    object_task = dvflow.mkTask(
        "cc.Object",
        objname="foo.o",
        cc="gcc",
        cxx="g++",
        needs=[fileset],
        srcdir=str(tmp_path)
    )

    status, outputs = dvflow.runTask(object_task)
    assert status == 0
    out_fileset = outputs.output[0]
    out_obj = os.path.join(out_fileset.basedir, out_fileset.files[0])
    assert os.path.exists(out_obj)
    assert os.stat(out_obj).st_size > 0

def test_object_multiple_sources_error(tmp_path, dvflow):
    # Create two C source files
    src_file1 = tmp_path / "foo.c"
    src_file2 = tmp_path / "bar.c"
    src_file1.write_text("int foo() { return 1; }\n")
    src_file2.write_text("int bar() { return 2; }\n")

    fileset = dvflow.mkTask(
        "std.FileSet",
        name="c_files",
        base=".",
        type="cSource",
        include=[src_file1.name, src_file2.name],
        srcdir=str(tmp_path)
    )

    object_task = dvflow.mkTask(
        "cc.Object",
        objname="multi.o",
        cc="gcc",
        cxx="g++",
        needs=[fileset],
        srcdir=str(tmp_path)
    )

    status, outputs = dvflow.runTask(object_task)
    assert status != 0
def test_object_incdir_define(tmp_path, dvflow):
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

    object_task = dvflow.mkTask(
        "cc.Object",
        objname="baz.o",
        cc="gcc",
        cxx="g++",
        needs=[fileset],
        srcdir=str(tmp_path)
    )

    status, outputs = dvflow.runTask(object_task)
    assert status == 0
    out_fileset = outputs.output[0]
    out_obj = os.path.join(out_fileset.basedir, out_fileset.files[0])
    assert os.path.exists(out_obj)
    assert os.stat(out_obj).st_size > 0

def test_object_cpp_only(tmp_path, dvflow):
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

    object_task = dvflow.mkTask(
        "cc.Object",
        objname="bar.o",
        cc="gcc",
        cxx="g++",
        needs=[fileset],
        srcdir=str(tmp_path)
    )

    status, outputs = dvflow.runTask(object_task)
    assert status == 0
    out_fileset = outputs.output[0]
    out_obj = os.path.join(out_fileset.basedir, out_fileset.files[0])
    assert os.path.exists(out_obj)
    assert os.stat(out_obj).st_size > 0

@pytest.mark.skip()
def test_foreach(tmp_path, dvflow):
    # Create three .c files: file1.c, file2.c, main.c
    (tmp_path / "file1.c").write_text("int file1_fn() { return 1; }\n")
    (tmp_path / "file2.c").write_text("int file2_fn() { return 2; }\n")
    (tmp_path / "main.c").write_text(
        "extern int file1_fn();\n"
        "extern int file2_fn();\n"
        "int main() { return file1_fn() + file2_fn(); }\n"
    )
    flow_dv = """
package:
    name: f1
    tasks:
    - name: CompileObjs
      strategy:
        matrix:
          src: ["file1.c", "file2.c", "main.c"]
      body:
      - name: Src
        uses: std.FileSet
        with:
          type: cSource
          include: ${{ matrix.src }}
      - name: mkObject
        uses: cc.Object
        needs: [Src]
    - name: Link
      uses: cc.Exe
      needs: [CompileObjs]
      with:
        exename: test_exe
"""

    with open(os.path.join(tmp_path, "flow.dv"), "w") as fp:
        fp.write(flow_dv)



    status = dvflow.runFlow(os.path.join(tmp_path, "flow.dv"), "f1.Link")

def test_graph_build(tmp_path, dvflow):
    # Create three .c files: file1.c, file2.c, main.c
    (tmp_path / "file1.c").write_text("int file1_fn() { return 1; }\n")
    (tmp_path / "file2.c").write_text("int file2_fn() { return 2; }\n")
    (tmp_path / "main.c").write_text(
        "extern int file1_fn();\n"
        "extern int file2_fn();\n"
        "int main() { return file1_fn() + file2_fn(); }\n"
    )
    flow_dv = """
package:
    name: f1
    tasks:
    - name: CompileMain
      strategy:
        generate:
          run: |
            cc_tasks = []
            for file in ("file1.c", "file2.c", "main.c"):
                cc_tasks.append(ctxt.addTask(ctxt.mkTaskNode(
                  "cc.Object",
                  name="compile_%s" % file,
                  filename=os.path.join(ctxt.srcdir, file))))
            ctxt.addTask(ctxt.mkTaskNode(
                "cc.Exe",
                name="link",
                needs=cc_tasks,
                exename="test_exe"))
"""

    with open(os.path.join(tmp_path, "flow.dv"), "w") as fp:
        fp.write(flow_dv)



    status = dvflow.runFlow(os.path.join(tmp_path, "flow.dv"), "f1.CompileMain")