"""C++ (C++17/20) snippets: control flow, classes, STL, RAII, timing, templates."""

FAMILY = dict(key="cpp", vscode="cpp", sublime="source.c++")

SNIPPETS = [
    ("inc", "Common includes", r"""
// ---- Standard library headers ----
#include <iostream>       // std::cout, std::cerr
#include <string>         // std::string
#include <vector>         // std::vector (dynamic array)
#include <unordered_map>  // hash map, average O(1) lookup
#include <memory>         // std::unique_ptr, std::make_unique
#include <algorithm>      // std::sort, std::find_if, std::transform
#include <stdexcept>      // std::runtime_error, std::invalid_argument
«0»
"""),
    ("main", "main function", r"""
// Entry point. Return 0 on success; exceptions escaping main terminate the program.
int main(int argc, char* argv[])
{
    try {
        «0»
    } catch (const std::exception& e) {
        std::cerr << "error: " << e.what() << '\n';
        return 1;
    }
    return 0;
}
"""),
    ("cppfile", "C++ program file", r"""
// «1:main».cpp
// Purpose: «2:one line on what this program does»
// Build:   g++ -std=c++20 -Wall -Wextra -O2 -o «1» «1».cpp
#include <iostream>
#include <string>
#include <vector>

int main()
{
    «0»
    return 0;
}
""", {"template": True}),
    ("classh", "Class header (.hpp)", r"""
// #pragma once: include guard supported by every major compiler
#pragma once

#include <string>

// «1:Account»: «2:what this type represents»
class «1» {
public:
    explicit «1»(std::string «3:name»);   // explicit: no silent conversions from string

    // Accessors are const: they promise not to modify the object
    [[nodiscard]] const std::string& «3»() const noexcept { return «3»_; }

private:
    std::string «3»_;   // trailing underscore marks a member variable
};
«0»
""", {"template": True}),
    ("if", "if statement", r"""
// if: run the block only when the condition is true
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
// else-if chain: evaluated top to bottom, first match wins
if («1:value» < «2:0») {
    «3»
} else if («1» == «4:0») {
    «5»
} else {
    «0»
}
"""),
    ("ifn", "Nested if / if-with-initializer", r"""
// C++17 if-with-initializer keeps `it` scoped to the if/else only
if (auto it = «1:map».find(«2:key»); it != «1».end()) {
    if («3:it->second > 0») {   // nested: only checked when the key exists
        «0»
    }
}
"""),
    ("tern", "Ternary operator", r"""
// ternary: condition ? if_true : if_false (both branches should be the same type)
auto «1:result» = («2:a > b») ? «3:a» : «4:b»;«0»
"""),
    ("sw", "switch statement", r"""
// switch on an integral or enum value. [[fallthrough]] documents intentional fall-through.
switch («1:value») {
    case «2:1»:
        «3»
        break;
    case «4:2»:
        «5»
        break;
    default:
        «0»
        break;
}
"""),
    ("for", "index for loop", r"""
// Index loop: use when you need the position, otherwise prefer range-for
for (std::size_t «1:i» = 0; «1» < «2:items».size(); ++«1») {
    «0»
}
"""),
    ("forr", "range-based for loop", r"""
// Range-for: const& avoids copying each element; drop const to modify in place
for (const auto& «1:item» : «2:items») {
    «0»
}
"""),
    ("while", "while loop", r"""
// while: condition checked before each iteration (body may run zero times)
while («1:condition») {
    «0»
}
"""),
    ("dowhile", "do-while loop", r"""
// do-while: body runs at least once
do {
    «0»
} while («1:condition»);
"""),
    ("try", "try / catch", r"""
// Catch by const reference; most specific exception types first
try {
    «1»
} catch (const std::invalid_argument& e) {
    std::cerr << "bad input: " << e.what() << '\n';
} catch (const std::exception& e) {
    std::cerr << "error: " << e.what() << '\n';
}«0»
"""),
    ("cls", "class (rule of zero)", r"""
// Rule of zero: members manage their own resources, so no custom copy/move/dtor needed
class «1:Name» {
public:
    «1»() = default;
    explicit «1»(«2:int» «3:value») : «3»_{«3»} {}

    [[nodiscard]] «2» «3»() const noexcept { return «3»_; }
    void set_«3»(«2» v) { «3»_ = v; }

private:
    «2» «3»_{};   // brace-init guarantees a value, never garbage
};«0»
"""),
    ("iface", "abstract interface", r"""
// Abstract base: pure virtual methods + virtual destructor for safe polymorphic delete
class «1:Shape» {
public:
    virtual ~«1»() = default;
    [[nodiscard]] virtual double «2:area»() const = 0;
};

class «3:Circle» final : public «1» {
public:
    explicit «3»(double r) : r_{r} {}
    [[nodiscard]] double «2»() const override { return 3.14159265358979 * r_ * r_; }

private:
    double r_;
};«0»
"""),
    ("uptr", "unique_ptr ownership", r"""
// unique_ptr: single owner, freed automatically when it goes out of scope (RAII)
auto «1:obj» = std::make_unique<«2:Type»>(«3»);
«0»
// Transfer ownership with std::move(«1»); never call delete yourself
"""),
    ("sort", "sort with lambda comparator", r"""
// std::sort with a lambda: return true when a should come before b
std::sort(«1:items».begin(), «1».end(), [](const auto& a, const auto& b) {
    return a.«2:score» > b.«2»;   // > sorts descending
});«0»
"""),
    ("findif", "find_if", r"""
// find_if returns end() when nothing matches: always compare before dereferencing
auto it = std::find_if(«1:items».begin(), «1».end(), [&](const auto& x) {
    return x.«2:id» == «3:target»;
});
if (it != «1».end()) {
    «0»
}
"""),
    ("umap", "unordered_map usage", r"""
// unordered_map: hash map. operator[] inserts a default value if the key is missing.
std::unordered_map<«1:std::string», «2:int»> «3:counts»;
«3»[«4:key»]++;                       // insert-or-increment
if (auto it = «3».find(«4»); it != «3».end()) {   // lookup without inserting
    «0»
}
"""),
    ("lambda", "lambda", r"""
// [captures](params) -> return_type { body }. [&] captures by reference, [=] by copy.
auto «1:fn» = [«2:&»](«3:int x») {
    «0»
};
"""),
    ("timer", "chrono scoped timer", r"""
#include <chrono>
// steady_clock never jumps backwards, so it is the right clock for measuring durations
const auto «1:start» = std::chrono::steady_clock::now();

«0»

const auto «2:ms» = std::chrono::duration_cast<std::chrono::milliseconds>(
    std::chrono::steady_clock::now() - «1»).count();
std::cout << "elapsed: " << «2» << " ms\n";
"""),
    ("tmpl", "function template", r"""
// Function template: the compiler generates one version per type used
template <typename T>
[[nodiscard]] T «1:clamp_value»(T v, T lo, T hi)
{
    return v < lo ? lo : (hi < v ? hi : v);
}«0»
"""),
]
