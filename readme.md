#Universal Machine implementation

This is my implementation of the [2006 ICFP Programming Contest](http://www.boundvariable.org/task.shtml).

The first part of the contest is to write a Universal Machine according to the specifications in `um-spec.txt`. You can use `sandmark.umz` to test your implementation. Finally you can load `codex.umz` and continue from there. For more information, have a look at the [contest page](http://www.boundvariable.org/task.shtml).

##How to run the code

Here's how you can run my implementation.

###Python
You can use the native Python interpreter, but it will take a *long* time. Running the sandmark takes about 2 hours and 42 minutes on my machine.

    python machine.py sandmark.umz
    python machine.py codex.umz

Using `pypy` will speed things up *a lot*. Running the sandmark takes about 5 minutes and 6 seconds on my machine.

    pypy machine.py sandmark.umz
    pypy machine.py codex.umz

You can use `test_machine.py` to run some unit tests.

    py.test test_machine.py


###C&#35;
You can run this on OS X or Linux using `mono`. First you need to compile it to an exe-file.

    mcs machine.cs

Then you can run the exe-file. Running the sandmark takes about 3 minutes and 15 seconds on my machine.

    mono machine.exe sandmark.umz
    mono machine.exe codex.umz
