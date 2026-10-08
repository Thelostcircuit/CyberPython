import unittest

import job
from job import AsmError, Instr, VMError, assemble, disassemble, parse_line, run_source

# Iris's release program. It releases wing C in order (here, subjects 9401 down to 9392),
# then calls the `last` subroutine, which releases the training source (4471) and prints
# how many minds were freed in total.
RELEASE = """
; SNAKE-1 release program, I. Vale
        PUSH 10
        STORE left          ; how many to release before the source
        PUSH 9401
        STORE next
        PUSH 0
        STORE freed
loop:   LOAD left
        JZ done
        LOAD next
        RELEASE
        LOAD freed
        PUSH 1
        ADD
        STORE freed
        LOAD next
        PUSH 1
        SUB
        STORE next
        LOAD left
        PUSH 1
        SUB
        STORE left
        JMP loop
done:   CALL last
        LOAD freed
        PRINT
        HALT
last:   PUSH 4471           ; Iris goes last
        RELEASE
        LOAD freed
        PUSH 1
        ADD
        STORE freed
        RET
"""


class Parsing(unittest.TestCase):
    def test_parse_line(self):
        self.assertEqual(parse_line("loop: push 3 ; hi"), ("loop", "PUSH", "3"))
        self.assertEqual(parse_line("   ; nothing"), (None, None, None))
        self.assertEqual(parse_line("start:"), ("start", None, None))
        self.assertEqual(parse_line("  halt"), (None, "HALT", None))
        self.assertEqual(parse_line("x:PUSH -2"), ("x", "PUSH", "-2"))
        with self.assertRaises(AsmError):
            parse_line("PUSH 1 2")

    def test_assemble(self):
        prog = assemble("start: PUSH 2\n  push -3\nloop:\n  JMP loop\n  STORE x\n  HALT")
        self.assertEqual(prog, [Instr("PUSH", 2), Instr("PUSH", -3), Instr("JMP", 2),
                                Instr("STORE", "x"), Instr("HALT")])
        self.assertEqual(assemble("; only a comment\n\n"), [])

    def test_assemble_errors(self):
        cases = {
            "PUSH 1\nFLY 3": "line 2",
            "PUSH": "line 1",
            "POP 3": "line 1",
            "\nPUSH three": "line 2",
            "JMP nowhere": "line 1",
            "a: PUSH 1\na: PUSH 2": "line 2",
            "STORE 9x": "line 1",
        }
        for source, where in cases.items():
            with self.subTest(source=source):
                with self.assertRaises(AsmError) as ctx:
                    assemble(source)
                self.assertIn(where, str(ctx.exception))

    def test_disassemble(self):
        self.assertEqual(disassemble(assemble("PUSH 7\nx: DUP\nJNZ x\nHALT")),
                         "000 PUSH 7\n001 DUP\n002 JNZ 1\n003 HALT")


class Machine(unittest.TestCase):
    def test_arithmetic(self):
        r = run_source("PUSH 7\nPUSH 3\nSUB\nPRINT\nPUSH -7\nPUSH 2\nDIV\nPRINT\n"
                       "PUSH -7\nPUSH 2\nMOD\nPRINT\nPUSH 6\nPUSH 7\nMUL\nPRINT")
        self.assertEqual(r.output, [4, -4, 1, 42])

    def test_compare_and_stack_ops(self):
        r = run_source("PUSH 2\nPUSH 3\nLT\nPRINT\nPUSH 3\nPUSH 2\nLT\nPRINT\n"
                       "PUSH 5\nDUP\nEQ\nPRINT\nPUSH 1\nPUSH 2\nSWAP\nPRINT\nPRINT\nPUSH 9\nPOP")
        self.assertEqual(r.output, [1, 0, 1, 1, 2])

    def test_variables_and_jumps(self):
        src = "PUSH 3\nSTORE n\ntop: LOAD n\nJZ end\nLOAD n\nPRINT\nLOAD n\nPUSH 1\nSUB\nSTORE n\nJMP top\nend: HALT\nPUSH 99\nPRINT"
        r = run_source(src)
        self.assertEqual((r.output, r.variables), ([3, 2, 1], {"n": 0}))

    def test_call_ret(self):
        r = run_source("CALL f\nCALL f\nHALT\nf: PUSH 5\nPRINT\nRET")
        self.assertEqual(r.output, [5, 5])

    def test_runs_off_the_end(self):
        self.assertEqual(run_source("PUSH 1\nPRINT").output, [1])
        self.assertEqual(run_source("").output, [])

    def test_errors(self):
        for src in ("POP", "ADD", "PUSH 1\nPUSH 0\nDIV", "PUSH 1\nPUSH 0\nMOD", "LOAD ghost",
                    "RET", "PRINT"):
            with self.subTest(src=src), self.assertRaises(VMError):
                run_source(src)
        with self.assertRaises(VMError):
            run_source("spin: JMP spin", max_steps=1000)

    def test_fresh_state_each_run(self):
        vm = job.VM()
        prog = assemble("PUSH 1\nSTORE x\nPUSH 2\nRELEASE")
        vm.run(prog)
        again = vm.run(prog)
        self.assertEqual((again.released, again.variables), ([2], {"x": 1}))


class TheRelease(unittest.TestCase):
    def test_iris_release_program(self):
        result = run_source(RELEASE)
        self.assertEqual(result.released, list(range(9401, 9391, -1)) + [4471])
        self.assertEqual(result.released[-1], 4471)
        self.assertEqual(result.output, [11])


if __name__ == "__main__":
    unittest.main()
