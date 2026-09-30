"""PHP (8.1+) snippets: strict types, classes, enums, control flow incl. match,
PDO prepared statements, a JSON/AJAX endpoint, CSRF, escaping, sessions."""

FAMILY = dict(key="php", vscode="php", sublime="embedding.php, source.php")

SNIPPETS = [
    ("phpclass", "PHP class file", r"""
<?php

declare(strict_types=1);   // no silent type juggling: '5' is not accepted where int is expected

namespace «1:App\Service»;

use «2:App\Repository\UserRepository»;

/**
 * «3:What this class is responsible for.»
 */
final class «4:UserService»
{
    public function __construct(
        private readonly «5:UserRepository» $«6:users»,   // constructor property promotion
    ) {
    }
    «0»
}
""", {"template": True}),
    ("cls", "class with promoted properties", r"""
final class «1:Product»
{
    // PHP 8: declare, type and assign properties straight from the constructor
    public function __construct(
        public readonly int $id,
        public readonly string $«2:name»,
        private float $«3:price» = 0.0,
    ) {
    }

    public function «3»(): float
    {
        return $this->«3»;
    }
    «0»
}
"""),
    ("enum", "backed enum", r"""
// Backed enum (8.1+): a fixed set of values, safer than string constants
enum «1:Status»: string
{
    case «2:Active» = '«3:active»';
    case «4:Closed» = '«5:closed»';

    public function label(): string
    {
        return ucfirst($this->value);
    }
}
// «1»::from('active') throws on bad input; «1»::tryFrom() returns null instead«0»
"""),
    ("if", "if statement", r"""
// if: runs when the condition is truthy. Use === to compare type and value.
if («1:$condition») {
    «0»
}
"""),
    ("ife", "if / else", r"""
// if / else: exactly one branch runs
if («1:$condition») {
    «2»
} else {
    «0»
}
"""),
    ("elif", "if / elseif / else", r"""
// elseif chain (one word in PHP): first true branch wins
if («1:$score» >= «2:90») {
    «3»
} elseif («1» >= «4:75») {
    «5»
} else {
    «0»
}
"""),
    ("ifn", "Nested if / nullsafe", r"""
// Nested if: the inner check only runs when the outer one passed
if («1:$user» !== null) {
    if («1»->«2:isActive»()) {
        «0»
    }
}
// PHP 8 nullsafe alternative: if («1»?->«2»()) { ... }
"""),
    ("tern", "Ternary / null coalescing", r"""
// ternary: condition ? if_true : if_false
$«1:label» = «2:$count > 0» ? '«3:has items»' : '«4:empty»';
// ?? returns the right side when the left is null OR undefined (no notice raised)
$«5:page» = (int) ($_GET['«6:page»'] ?? 1);«0»
"""),
    ("sw", "switch statement", r"""
// switch uses loose comparison (==); prefer match below for strict comparison
switch («1:$action») {
    case '«2:create»':
        «3»
        break;
    case '«4:delete»':
        «5»
        break;
    default:
        «0»
        break;
}
"""),
    ("match", "match expression", r"""
// match (PHP 8): strict (===), returns a value, no fall-through, throws if nothing matches
$«1:message» = match («2:$status») {
    «3:200», «4:201» => 'OK',
    «5:404» => 'Not found',
    default => 'Error',
};«0»
"""),
    ("for", "for loop", r"""
// for: use when you need the index
for ($«1:i» = 0; $«1» < «2:count($items)»; $«1»++) {
    «0»
}
"""),
    ("fore", "foreach loop", r"""
// foreach: iterate arrays (key => value). Use &$value only if you must modify in place.
foreach («1:$items» as «2:$key» => «3:$value») {
    «0»
}
"""),
    ("while", "while loop", r"""
// while: checks the condition before each pass
while («1:$row = $stmt->fetch()») {
    «0»
}
"""),
    ("dowhile", "do-while loop", r"""
// do-while: body runs at least once
do {
    «0»
} while («1:$condition»);
"""),
    ("try", "try / catch / finally", r"""
// Catch specific exceptions first; \Throwable catches everything including Errors
try {
    «1»
} catch («2:\PDOException» $e) {
    error_log($e->getMessage());   // log details, never echo them to the user
} finally {
    «0»
}
"""),
    ("fn", "typed function with docblock", r"""
/**
 * «2:What the function does.»
 */
function «1:name»(«3:int» $«4:value»): «5:bool»
{
    «0»
}
"""),
    ("pdo", "PDO connection", r"""
// PDO works with MySQL, SQLite, PostgreSQL... Configure it once, reuse the object.
$pdo = new PDO(
    «1:'mysql:host=127.0.0.1;dbname=app;charset=utf8mb4'»,   // or 'sqlite:' . __DIR__ . '/app.db'
    «2:getenv('DB_USER') ?: 'root'»,
    «3:getenv('DB_PASS') ?: ''»,
    [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,        // throw on SQL errors
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,   // rows as ['column' => value]
        PDO::ATTR_EMULATE_PREPARES => false,                // real prepared statements
    ],
);«0»
"""),
    ("pdoq", "PDO prepared query", r"""
// Prepared statements keep data separate from SQL: this is what prevents SQL injection.
// NEVER concatenate user input into a query string.
$stmt = $pdo->prepare('SELECT «1:id, name» FROM «2:users» WHERE «3:email» = :«3» LIMIT 1');
$stmt->execute(['«3»' => $«4:email»]);
$«5:user» = $stmt->fetch();   // false when no row matched«0»
"""),
    ("json", "AJAX: JSON API endpoint", r"""
<?php
// api/«1:items».php: a JSON endpoint called by fetch() / $.ajax from the front end
declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');

function respond(int $status, array $payload): never
{
    http_response_code($status);
    echo json_encode($payload, JSON_THROW_ON_ERROR);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== '«2:POST»') {
    respond(405, ['error' => 'Method not allowed']);
}

// fetch() sends JSON in the body, which $_POST does not parse
$input = json_decode(file_get_contents('php://input') ?: '', true);
if (!is_array($input) || trim((string) ($input['«3:name»'] ?? '')) === '') {
    respond(422, ['error' => '«3» is required']);
}
«0»
respond(201, ['ok' => true]);
""", {"template": True}),
    ("csrf", "CSRF token", r"""
// CSRF protection: every state-changing form carries a secret token tied to the session
session_start();
$_SESSION['csrf'] ??= bin2hex(random_bytes(32));

// In the form:  <input type="hidden" name="csrf" value="<?= e($_SESSION['csrf']) ?>">
// On submit: hash_equals is a constant-time compare (resists timing attacks)
if (!hash_equals($_SESSION['csrf'], (string) ($_POST['csrf'] ?? ''))) {
    http_response_code(403);
    exit('Invalid CSRF token');
}«0»
"""),
    ("esc", "HTML escape helper", r"""
// Escape everything you echo into HTML: this is what prevents XSS
function e(?string $value): string
{
    return htmlspecialchars($value ?? '', ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}
// <p><?= e($«1:comment») ?></p>«0»
"""),
    ("sess", "secure session start", r"""
// Harden the session cookie before starting the session
session_set_cookie_params([
    'lifetime' => 0,
    'path' => '/',
    'secure' => «1:true»,     // HTTPS only
    'httponly' => true,       // JavaScript cannot read it (limits XSS damage)
    'samesite' => 'Lax',      // basic CSRF protection
]);
session_start();
// After login: session_regenerate_id(true); to prevent session fixation«0»
"""),
    ("input", "read request input safely", r"""
// filter_input validates/normalises instead of reading $_GET/$_POST raw
$«1:id» = filter_input(INPUT_GET, '«1»', FILTER_VALIDATE_INT, ['options' => ['min_range' => 1]]);
if ($«1» === false || $«1» === null) {
    http_response_code(400);
    exit('Invalid «1»');
}«0»
"""),
    ("timer", "measure elapsed time", r"""
// hrtime(true): monotonic nanoseconds, the right clock for durations
$«1:start» = hrtime(true);
«0»
$ms = (hrtime(true) - $«1») / 1e6;
error_log(sprintf('elapsed: %.2f ms', $ms));
"""),
    ("phpunit", "PHPUnit test class", r"""
<?php

declare(strict_types=1);

namespace «1:Tests»;

use PHPUnit\Framework\TestCase;

final class «2:CalculatorTest» extends TestCase
{
    public function test«3:AddsTwoNumbers»(): void
    {
        // Arrange, act, assert
        $sut = new «4:\App\Calculator»();
        self::assertSame(5, $sut->add(2, 3));
    }
    «0»
}
""", {"template": True}),
]
