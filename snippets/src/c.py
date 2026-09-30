"""C (C11) snippets: control flow, memory, files, timing and file templates."""

FAMILY = dict(key="c", vscode="c", sublime="source.c")

SNIPPETS = [
    ("inc", "Standard includes", r"""
// ---- Standard library headers (C11) ----
#include <stdio.h>    // printf, fprintf, fopen, fgets
#include <stdlib.h>   // malloc, free, exit, EXIT_SUCCESS / EXIT_FAILURE
#include <string.h>   // strlen, strncpy, strcmp, memset
#include <stdbool.h>  // bool, true, false
#include <stdint.h>   // fixed-width integers: int32_t, uint8_t
#include <errno.h>    // errno is set by failing library calls
«0»
"""),
    ("main", "main function", r"""
// Entry point. argc = number of arguments, argv[0] = program name.
int main(int argc, char *argv[])
{
    if (argc < «1:2») {
        fprintf(stderr, "usage: %s «2:<arg>»\n", argv[0]);
        return EXIT_FAILURE;   // non-zero exit tells the shell it failed
    }
    «0»
    return EXIT_SUCCESS;
}
"""),
    ("cfile", "C program file", r"""
/*
 * «1:program».c
 * Purpose: «2:one line on what this program does»
 * Build:   gcc -std=c11 -Wall -Wextra -O2 -o «1» «1».c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// ---- Prototypes: declare before main so main reads top-down ----
static void «3:run»(void);

int main(void)
{
    «3»();
    return EXIT_SUCCESS;
}

// ---- Definitions ----
static void «3»(void)
{
    «0»
}
""", {"template": True}),
    ("header", "Header file with include guard", r"""
// Include guard: stops this header being pasted twice into one translation unit
#ifndef «1:MODULE»_H
#define «1»_H

#include <stddef.h>

// Public API of «1»: only declarations here, definitions live in the .c file
«0»

#endif // «1»_H
""", {"template": True}),
    ("if", "if statement", r"""
// if: run the block only when the condition is non-zero (true)
if («1:condition») {
    «0»
}
"""),
    ("ife", "if / else", r"""
// if / else: exactly one of the two blocks runs
if («1:condition») {
    «2»
} else {
    «0»
}
"""),
    ("elif", "else-if chain", r"""
// else-if chain: tested top to bottom, first true branch wins
if («1:score» >= «2:90») {
    «3»
} else if («1» >= «4:75») {
    «5»
} else {
    «0»
}
"""),
    ("ifn", "Nested if with early-return alternative", r"""
// Nested if: the inner check only runs when the outer one passed
if («1:ptr» != NULL) {
    if («2:ptr->count > 0») {
        «0»
    }
}
// Tip: deep nesting reads badly. Prefer guard clauses:
// if (ptr == NULL) return; if (!(ptr->count > 0)) return;
"""),
    ("tern", "Ternary operator", r"""
// ternary: condition ? value_if_true : value_if_false (an expression, not a statement)
«1:int» «2:result» = («3:a > b») ? «4:a» : «5:b»;«0»
"""),
    ("sw", "switch statement", r"""
// switch on an integer or enum. Each case needs `break` or it falls through.
switch («1:value») {
    case «2:1»:
        «3»
        break;
    case «4:2»:
        «5»
        break;
    default:   // runs when no case matches: handle the unexpected here
        «0»
        break;
}
"""),
    ("for", "for loop", r"""
// for: init; condition checked before each pass; step after each pass
for (size_t «1:i» = 0; «1» < «2:count»; «1»++) {
    «0»
}
"""),
    ("forr", "reverse for loop", r"""
// Reverse loop with size_t: count down using i-- > 0 because size_t never goes negative
for (size_t «1:i» = «2:count»; «1»-- > 0; ) {
    «0»
}
"""),
    ("while", "while loop", r"""
// while: checks the condition first, so the body may run zero times
while («1:condition») {
    «0»
}
"""),
    ("dowhile", "do-while loop", r"""
// do-while: body always runs at least once, condition checked after
do {
    «0»
} while («1:condition»);
"""),
    ("fn", "function with doc comment", r"""
/**
 * «2:What the function does in one sentence.»
 * @param «3:value» «4:meaning of the parameter»
 * @return «5:what is returned, and what signals an error»
 */
«1:int» «6:function_name»(«7:int» «3»)
{
    «0»
}
"""),
    ("struct", "typedef struct", r"""
// typedef struct: lets you write `«1:Item»` instead of `struct «1»`
typedef struct «1» {
    «2:int id;»
    «3:char name[64];»
} «1»;«0»
"""),
    ("enum", "typedef enum", r"""
// Named integer constants: clearer than magic numbers in a switch
typedef enum {
    «1:STATE_IDLE»,
    «2:STATE_RUNNING»,
    «3:STATE_DONE»
} «4:State»;«0»
"""),
    ("malloc", "malloc with NULL check", r"""
// malloc can fail: always check for NULL, and free exactly once when done
«1:int» *«2:buffer» = malloc(«3:count» * sizeof *«2»);
if («2» == NULL) {
    perror("malloc");
    return EXIT_FAILURE;
}
«0»
free(«2»);
«2» = NULL;   // avoid a dangling pointer being used after free
"""),
    ("fopen", "open a file safely", r"""
// fopen returns NULL on failure; perror prints the reason from errno
FILE *«1:fp» = fopen(«2:"data.txt"», «3:"r"»);
if («1» == NULL) {
    perror(«2»);
    return EXIT_FAILURE;
}

char «4:line»[256];
while (fgets(«4», sizeof «4», «1») != NULL) {   // fgets is bounded, unlike gets
    «0»
}

fclose(«1»);
"""),
    ("readint", "read an integer safely", r"""
// Read a whole line with fgets, then parse it. Safer than scanf("%d") on bad input.
char «1:buf»[64];
long «2:number» = 0;
if (fgets(«1», sizeof «1», stdin) != NULL) {
    char *end = NULL;
    errno = 0;
    «2» = strtol(«1», &end, 10);
    if (errno != 0 || end == «1») {
        fprintf(stderr, "not a number\n");
    }
}«0»
"""),
    ("timer", "measure elapsed time", r"""
#include <time.h>
// clock() measures CPU time used by this process (not wall-clock time)
clock_t «1:start» = clock();

«0»

double «2:elapsed_ms» = (double)(clock() - «1») * 1000.0 / CLOCKS_PER_SEC;
printf("elapsed: %.3f ms\n", «2»);
"""),
    ("arrlen", "array length macro", r"""
// Only works on real arrays, not on pointers passed into a function
#define ARRAY_LEN(a) (sizeof(a) / sizeof((a)[0]))«0»
"""),
    ("printf", "printf with format guide", r"""
// %d int, %ld long, %zu size_t, %f double, %s string, %c char, %p pointer
printf("«1:%s»\n", «2:value»);«0»
"""),
]
