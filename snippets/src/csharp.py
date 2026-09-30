"""C# (.NET 8/10) snippets: control flow, types, async, LINQ, ASP.NET Core."""

FAMILY = dict(key="csharp", vscode="csharp", sublime="source.cs")

SNIPPETS = [
    ("usings", "Common usings", r"""
// .NET 6+ projects enable ImplicitUsings (System, System.Linq, System.Collections.Generic,
// System.Threading.Tasks ...). Add only what is not already implicit:
using System.Diagnostics;        // Stopwatch, Debug
using System.Text.Json;          // JsonSerializer
using System.ComponentModel.DataAnnotations;  // [Required], [Range] validation attributes
«0»
"""),
    ("csfile", "C# class file", r"""
namespace «1:MyApp.Services»;   // file-scoped namespace (C# 10+): one less indent level

/// <summary>
/// «2:What this class is responsible for.»
/// </summary>
public sealed class «3:MyService»
{
    «0»
}
""", {"template": True}),
    ("if", "if statement", r"""
// if: run the block only when the condition is true
if («1:condition»)
{
    «0»
}
"""),
    ("ife", "if / else", r"""
// if / else: exactly one of the two blocks runs
if («1:condition»)
{
    «2»
}
else
{
    «0»
}
"""),
    ("elif", "else-if chain", r"""
// else-if chain: first true branch wins
if («1:score» >= «2:90»)
{
    «3»
}
else if («1» >= «4:75»)
{
    «5»
}
else
{
    «0»
}
"""),
    ("ifn", "Nested if with pattern matching", r"""
// Pattern matching null-check + type test in one step, then a nested condition
if («1:input» is «2:Order» «3:order»)
{
    if («3».«4:Total» > «5:0»)
    {
        «0»
    }
}
"""),
    ("tern", "Ternary and null-coalescing", r"""
// ternary: condition ? if_true : if_false
var «1:label» = «2:count» > 0 ? "«3:has items»" : "«4:empty»";
// ?? picks the right side when the left is null; ??= assigns only if null
var «5:name» = «6:input» ?? "«7:default»";«0»
"""),
    ("sw", "switch statement", r"""
// switch statement: each section must end with break, return or throw
switch («1:value»)
{
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
    ("swe", "switch expression", r"""
// Switch expression (C# 8+): returns a value; `_` is the catch-all
var «1:result» = «2:status» switch
{
    «3:Status.Active» => «4:"active"»,
    «5:Status.Closed» => «6:"closed"»,
    _ => throw new ArgumentOutOfRangeException(nameof(«2»), «2», null)
};«0»
"""),
    ("for", "for loop", r"""
// for: use when you need the index
for (var «1:i» = 0; «1» < «2:items».«3:Count»; «1»++)
{
    «0»
}
"""),
    ("fore", "foreach loop", r"""
// foreach: read-only iteration over any IEnumerable
foreach (var «1:item» in «2:items»)
{
    «0»
}
"""),
    ("while", "while loop", r"""
// while: condition checked before each pass
while («1:condition»)
{
    «0»
}
"""),
    ("dowhile", "do-while loop", r"""
// do-while: body runs at least once
do
{
    «0»
} while («1:condition»);
"""),
    ("try", "try / catch / finally", r"""
// Catch specific exceptions first; finally always runs (cleanup)
try
{
    «1»
}
catch («2:InvalidOperationException» ex)
{
    «3:logger».LogWarning(ex, "«4:Operation failed»");
}
finally
{
    «0»
}
"""),
    ("cls", "class with properties", r"""
/// <summary>«2:What this type represents.»</summary>
public class «1:Customer»
{
    public int Id { get; init; }                     // init: settable only when constructing
    public required string «3:Name» { get; set; }    // required: must be set by the caller
    public DateTime CreatedAt { get; } = DateTime.UtcNow;
    «0»
}
"""),
    ("rec", "record type", r"""
// record: immutable data type with value equality and a ToString for free
public sealed record «1:ProductDto»(int Id, string «2:Name», decimal «3:Price»);«0»
"""),
    ("iface", "interface", r"""
// Interface: the contract a class promises to fulfil (great for testing with fakes)
public interface I«1:Repository»<T>
{
    Task<T?> GetByIdAsync(int id, CancellationToken ct = default);
    Task<IReadOnlyList<T>> ListAsync(CancellationToken ct = default);
    «0»
}
"""),
    ("async", "async method", r"""
// async Task: always accept a CancellationToken and pass it down
public async Task<«1:string»> «2:LoadAsync»(«3:int id», CancellationToken ct = default)
{
    «0»
    await Task.Delay(10, ct);
    return default!;
}
"""),
    ("linq", "LINQ query chain", r"""
// LINQ is lazy: nothing runs until ToList / First / Count / foreach
var «1:result» = «2:orders»
    .Where(o => o.«3:Total» > «4:100»)
    .OrderByDescending(o => o.«3»)
    .Select(o => new { o.Id, o.«3» })
    .ToList();«0»
"""),
    ("guard", "argument guard clauses", r"""
// Guard clauses: fail fast with a clear exception instead of a NullReference later
ArgumentNullException.ThrowIfNull(«1:input»);
ArgumentException.ThrowIfNullOrWhiteSpace(«2:name»);
ArgumentOutOfRangeException.ThrowIfNegative(«3:count»);«0»
"""),
    ("timer", "Stopwatch timing", r"""
// Stopwatch: high-resolution elapsed time for measuring code
var «1:sw» = System.Diagnostics.Stopwatch.StartNew();
«0»
«1».Stop();
Console.WriteLine($"elapsed: {«1».ElapsedMilliseconds} ms");
"""),
    ("ptimer", "PeriodicTimer loop", r"""
// PeriodicTimer (.NET 6+): async-friendly repeating timer, stops with the token
using var «1:timer» = new PeriodicTimer(TimeSpan.FromSeconds(«2:5»));
while (await «1».WaitForNextTickAsync(«3:ct»))
{
    «0»
}
"""),
    ("minapi", "ASP.NET Core minimal API", r"""
// Program.cs: ASP.NET Core minimal API
var builder = WebApplication.CreateBuilder(args);

builder.Services.AddEndpointsApiExplorer();
builder.Services.AddProblemDetails();   // RFC 7807 error responses

var app = builder.Build();
app.UseExceptionHandler();

// Group related endpoints under one prefix
var «1:items» = app.MapGroup("/api/«1»");
«1».MapGet("/", () => Results.Ok(Array.Empty<object>()));
«1».MapGet("/{id:int}", (int id) => Results.NotFound());
«1».MapPost("/", (object body) => Results.Created($"/api/«1»/1", body));
«0»
app.Run();

public partial class Program;   // lets integration tests reference the app
""", {"template": True}),
    ("xunit", "xUnit test class", r"""
namespace «1:MyApp.Tests»;

public class «2:CalculatorTests»
{
    [Fact]
    public void «3:Add_ReturnsSum»()
    {
        // Arrange - Act - Assert keeps every test readable
        var sut = new «4:Calculator»();

        var result = sut.«5:Add»(2, 3);

        Assert.Equal(5, result);
    }«0»
}
""", {"template": True}),
]
