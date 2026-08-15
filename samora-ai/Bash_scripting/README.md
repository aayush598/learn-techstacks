# Bash Scripting Interview Questions and Answers (Top 100)

## Q1: What is the shebang line and why is it important?
**A:** The shebang `#!/usr/bin/env bash` tells the OS which interpreter to use. Using `/usr/bin/env bash` is portable because it finds bash via PATH rather than a hardcoded path.

## Q2: How do you define and use a variable in bash?
**A:** Assign without spaces: `name="value"`, then reference with `$name` or `${name}`. Bash variables are untyped and stored as strings by default.

## Q3: What is the difference between single and double quotes?
**A:** Single quotes preserve literal text with no expansion. Double quotes allow variable and command substitution: `"$HOME"` expands but `'$HOME'` does not.

## Q4: What is command substitution and the preferred syntax?
**A:** It captures command output into a variable. Prefer `$(...)` over backticks because it is nestable and more readable: `files=$(ls)`.

## Q5: What is the difference between backticks and $()?
**A:** Both do command substitution, but `$( )` is nestable (`$(echo $(date))`) and easier to read, while backticks require escaping inside nested commands.

## Q6: What are $0, $1, $#, $@, and $*?
**A:** `$0` is the script name, `$1` the first arg, `$#` the arg count, `$@` all args (each quoted), `$*` all args as one string. Use `"$@"` to preserve individual arguments.

## Q7: What is the difference between $@ and $*?
**A:** In double quotes, `"$@"` expands to separate quoted words (`"$1" "$2"`), while `"$*"` expands to a single string joined by IFS (`"$1c$2"`).

## Q8: How does the shift command work?
**A:** `shift` discards `$1` and shifts remaining args down (`$2` becomes `$1`). `shift N` shifts N positions; useful for parsing options in a loop.

## Q9: What does $? represent?
**A:** `$?` holds the exit status of the last executed command: 0 means success, non-zero indicates an error.

## Q10: How do you set a default value for a variable?
**A:** Use `${var:-default}` to substitute default if unset/empty, or `${var:=default}` to also assign it: `port=${PORT:-8080}`.

## Q11: What is the difference between ${var:-x} and ${var:=x}?
**A:** `${var:-x}` returns `x` if `var` is unset/empty but does not assign it. `${var:=x}` assigns `x` to `var` and returns it.

## Q12: How do you check if a variable is set?
**A:** Use `${var:+value}` (returns value if set and non-empty) or parameter tests: `if [ -z "${var:-}" ]; then ...` checks unset/empty.

## Q13: What is the purpose of ${var:?error}?
**A:** It prints `error` to stderr and exits the script if `var` is unset or empty, useful for mandatory configuration checks.

## Q14: How do you get the length of a string in bash?
**A:** Use `${#var}`: `name="bash"; echo ${#name}` prints 4.

## Q15: How do you extract a substring in bash?
**A:** Use `${var:offset:length}`: `echo ${name:0:2}` returns the first two characters.

## Q16: How do you replace text in a string?
**A:** Use `${var/pattern/repl}` for first match, `${var//pattern/repl}` for all: `echo ${path/foo/bar}`.

## Q17: How do you remove a prefix or suffix from a string?
**A:** Use `${var#prefix}` (shortest prefix), `${var##prefix}` (longest), `${var%suffix}` and `${var%%suffix}` for suffixes.

## Q18: What is the difference between [ ] and [[ ]]?
**A:** `[[ ]]` is a bash keyword with no word-splitting, supports `&&`, `||`, `=~` regex, and `>` without escaping. `[ ]` is the `test` command, requires quoted vars and `-a`/`-o`.

## Q19: How do you compare strings in bash?
**A:** In `[[ ]]`: `if [[ "$a" == "$b" ]]`. In `[ ]`: `if [ "$a" = "$b" ]`. Use `!=` for inequality and `-z`/`-n` for empty checks.

## Q20: How do you compare numbers in bash?
**A:** Use `[ "$a" -eq "$b" ]` (`-ne -gt -lt -ge -le`) or the arithmetic `(( a == b ))` which supports C-like operators.

## Q21: How do you check if a file exists?
**A:** Use `[ -f "$file" ]` for a regular file or `[ -e "$file" ]` for any file. Always quote the variable to avoid word splitting.

## Q22: How do you test file properties like readable/writable/executable?
**A:** Use `-r`, `-w`, `-x`: `if [ -r "$file" ] && [ -w "$file" ]; then ...`. `-d` tests a directory, `-L` a symlink.

## Q23: How do you write an if statement in bash?
**A:**
```bash
if [[ condition ]]; then
  echo "yes"
elif [[ other ]]; then
  echo "maybe"
else
  echo "no"
fi
```

## Q24: What is the test command and how is it related to [ ]?
**A:** `test` evaluates expressions and returns exit status. `[ ]` is a synonym for `test` with a required trailing `]`; both are builtins in bash.

## Q25: How do you write a for loop?
**A:**
```bash
for i in 1 2 3; do
  echo "$i"
done
```
Also `for f in *.txt` to iterate over files.

## Q26: How do you write a C-style for loop?
**A:**
```bash
for ((i=0; i<10; i++)); do
  echo "$i"
done
```

## Q27: How do you write a while loop?
**A:**
```bash
while [[ $n -gt 0 ]]; do
  echo "$n"
  ((n--))
done
```

## Q28: What is the until loop?
**A:** `until` runs until the condition is true (opposite of while): `until [[ -f done ]]; do sleep 1; done`.

## Q29: How do you read a file line by line?
**A:**
```bash
while IFS= read -r line; do
  echo "$line"
done < file.txt
```
`IFS=` keeps leading spaces; `-r` prevents backslash interpretation.

## Q30: What is a case statement and when do you use it?
**A:**
```bash
case "$var" in
  start) echo "starting" ;;
  stop)  echo "stopping" ;;
  *)     echo "usage: start|stop" ;;
esac
```
Use it for pattern-based branching instead of long if chains.

## Q31: How do you define a function in bash?
**A:**
```bash
myfunc() {
  echo "arg1: $1"
}
```
Or `function myfunc { ... }`. Call with `myfunc arg`.

## Q32: How do functions return values?
**A:** Use `return N` to set the exit status (0-255), accessible via `$?`. For data, echo to stdout and capture with `$(myfunc)`, or use a global/nameref variable.

## Q33: How do you declare a local variable inside a function?
**A:** Use `local var="value"` so it does not leak into the parent scope. Without `local`, variables are global.

## Q34: How do you define an indexed array?
**A:**
```bash
arr=(one two three)
arr[3]="four"
echo "${arr[0]}"      # one
echo "${arr[@]}"      # all elements
echo "${#arr[@]}"     # count
```

## Q35: How do you define an associative array?
**A:**
```bash
declare -A map
map[name]="bob"
map[age]=30
echo "${map[name]}"
```
Requires `declare -A` before use.

## Q36: How do you iterate over an array?
**A:**
```bash
for item in "${arr[@]}"; do
  echo "$item"
done
```

## Q37: How do you iterate over associative array keys?
**A:**
```bash
for key in "${!map[@]}"; do
  echo "$key = ${map[$key]}"
done
```

## Q38: What is arithmetic evaluation in bash?
**A:** Use `$(( ))` or `(( ))`: `sum=$((a + b))`, `((count++))`. Variables need not be prefixed with `$` inside `(( ))`.

## Q39: What is the difference between (( )) and let?
**A:** Both do arithmetic; `(( ))` is preferred and returns non-zero if the expression is 0 (useful in if). `let "a = b + 1"` is older syntax.

## Q40: How does redirection with > and >> work?
**A:** `>` overwrites a file, `>>` appends. Both create the file if missing: `echo hi > out.txt`.

## Q41: What does 2> redirect and what is 2>&1?
**A:** `2>` redirects stderr. `2>&1` sends stderr to the same place as stdout; order matters: `cmd >out 2>&1`.

## Q42: What is a heredoc and how do you use it?
**A:**
```bash
cat <<EOF
line with $variable
EOF
```
Use `<<'EOF'` to disable expansion inside the heredoc.

## Q43: What is a here-string (<<<)?
**A:** `<<<` feeds a string to a command's stdin: `grep foo <<<"some text"`. Equivalent to `echo "some text" | grep foo`.

## Q44: What is process substitution?
**A:** `<(cmd)` and `>(cmd)` let a command's output act as a file: `diff <(sort a) <(sort b)`. Works where a filename is expected.

## Q45: How do you use pipes?
**A:** `|` sends stdout of one command to stdin of the next: `cat file | grep error | wc -l`. Avoid unnecessary `cat` (useless cat).

## Q46: What is the difference between globbing and regex?
**A:** Globbing (`*.txt`) matches filenames in the shell and is not regex. Regex (`[[ $x =~ ^a.*z$ ]]`) matches text patterns inside commands like grep or `=~`.

## Q47: How do you match a regex in bash?
**A:**
```bash
if [[ $email =~ ^[^@]+@[^@]+\.[^@]+$ ]]; then
  echo "valid"
fi
```
The right side is an unquoted extended regex.

## Q48: How do you use grep basics?
**A:** `grep "pattern" file` searches lines. Use `-i` case-insensitive, `-r` recursive, `-v` invert, `-n` line numbers, `-E` for extended regex.

## Q49: How do you use sed basics?
**A:** `sed 's/old/new/' file` replaces first match per line; `s/old/new/g` all. Use `-i` to edit in place. Sed streams text transformations.

## Q50: How do you use awk basics?
**A:** `awk '{print $1}' file` prints the first field. `awk -F, '{print $2}'` uses comma delimiter. Awk is great for column processing and sums.

## Q51: How do you find files with find?
**A:** `find . -name "*.log" -mtime +7` finds logs older than 7 days. Use `-type f`, `-size`, `-exec` to act on results.

## Q52: What is xargs and why use it?
**A:** `xargs` builds command lines from stdin: `find . -name "*.txt" | xargs rm`. Use `-0` with `find -print0` to handle spaces safely.

## Q53: How does read work and what are common options?
**A:** `read var` reads a line into `var`. `read -p "Name: " name` prompts; `read -a arr` into array; `read -s` hides input for passwords.

## Q54: How do you prompt a user for input?
**A:**
```bash
read -r -p "Enter name: " name
echo "Hello $name"
```

## Q55: What does set -e do?
**A:** `set -e` exits the script immediately if any command returns non-zero. It is part of strict mode but can surprise with commands expected to fail.

## Q56: What does set -u do?
**A:** `set -u` treats referencing an unset variable as an error, catching typos. Combine with `${var:-}` when a default is acceptable.

## Q57: What does set -x do?
**A:** `set -x` prints each command and its expanded arguments before executing, useful for debugging. Disable with `set +x`.

## Q58: What does set -o pipefail do?
**A:** With pipefail, a pipeline returns the rightmost non-zero exit status if any command fails, instead of only the last command's status.

## Q59: What is a recommended "strict mode" header?
**A:**
```bash
set -euo pipefail
IFS=$'\n\t'
```
This catches unset vars, errors, and pipe failures early.

## Q60: What is the difference between sourcing and executing a script?
**A:** `. script.sh` or `source script.sh` runs in the current shell (vars/functions persist). `./script.sh` runs in a subshell so changes don't affect the parent.

## Q61: How do you export an environment variable?
**A:** `export VAR="value"` makes it available to child processes. `env` lists all environment variables.

## Q62: What is the difference between an environment variable and a shell variable?
**A:** A shell variable is local to the shell; an environment variable is exported (`export`) and inherited by child processes.

## Q63: What is a subshell and when is it created?
**A:** A subshell is a child bash that inherits a copy of the environment. Created by `()`, pipes, or `(cmd)`, and changes inside do not affect the parent.

## Q64: How do you run a command in the background?
**A:** Append `&`: `long_task &` runs it in background, returning a job and PID. Use `wait` to block until it finishes.

## Q65: How do you manage background jobs?
**A:** `jobs` lists active jobs, `fg %1` brings job 1 to foreground, `bg %1` resumes it in background. `wait %1` blocks for a specific job.

## Q66: What is the wait command?
**A:** `wait` blocks until all/all-specified background jobs finish; `wait $PID` waits for a PID. It returns the exit status of the last waited job.

## Q67: How do you handle signals with trap?
**A:** `trap 'echo bye' EXIT` runs cleanup on exit; `trap 'rm -f "$tmp"' INT TERM` handles interrupts. Useful for temp file cleanup.

## Q68: What is trap on ERR?
**A:** `trap 'handler' ERR` runs a command when a command returns non-zero (with `set -e` it fires before exit). Good for error logging.

## Q69: How do you parse options with getopts?
**A:**
```bash
while getopts ":f:o:v" opt; do
  case $opt in
    f) file=$OPTARG ;;
    o) out=$OPTARG ;;
    v) verbose=1 ;;
    *) echo "bad opt" ;;
  esac
done
```
`:f:o:v` means f and o take arguments.

## Q70: What is the difference between getopts and getopt?
**A:** `getopts` is a builtin handling short options only and is portable. `getopt` (external) supports long options (`--long`) but varies by platform.

## Q71: How do you debug a bash script?
**A:** Run `bash -x script.sh` to trace, `bash -n script.sh` to check syntax without executing, or use `set -x` inside. `declare -p var` inspects variables.

## Q72: How do you check a script's syntax without running it?
**A:** Use `bash -n script.sh` (or `set -n`) to parse and report syntax errors only, without executing commands.

## Q73: What is the difference between bash and sh?
**A:** `sh` is the POSIX shell with a minimal feature set; `bash` adds arrays, `[[ ]]`, `(( ))`, process substitution, and more. Scripts starting with `#!/bin/sh` should avoid bashisms.

## Q74: How does bash differ from zsh?
**A:** Zsh has better globbing, arrays starting at 1, associative arrays by default, and `setopt` options. Bash is more universally available; both share most basic syntax.

## Q75: How do you make a script portable across shells?
**A:** Use only POSIX features (stick to `[ ]`, no arrays/`[[ ]]`), use `#!/bin/sh`, quote variables, and avoid bashisms. Test under `dash` or `sh`.

## Q76: What are common pitfalls with unquoted variables?
**A:** Unquoted `$var` undergoes word splitting and globbing, breaking on spaces or `*`; `rm $file` can delete multiple files. Always quote: `"$var"`.

## Q77: Why is `if [ $var = "x" ]` dangerous?
**A:** If `var` is empty or unset, it becomes `if [ = "x" ]` causing a syntax error. Quote it: `if [ "$var" = "x" ]`, or use `[[ ]]`.

## Q78: What is a common mistake with for loops over files?
**A:** `for f in $(ls)` breaks on filenames with spaces. Instead use `for f in *.txt` or `while IFS= read -r f; do ... done < <(find ...)`.

## Q79: What is the `:` null command used for?
**A:** `:` is a builtin that does nothing and returns 0. Used as a placeholder, in `while :` infinite loops, or `: "${var:=default}"` to set defaults.

## Q80: How do you trim whitespace from a string?
**A:** Use parameter expansion: `trim=${var#"${var%%[![:space:]]*}"}; trim=${trim%"${trim##*[![:space:]]}"}` removes leading/trailing spaces.

## Q81: How do you print colored output in bash?
**A:**
```bash
echo -e "\e[31mRed text\e[0m"
```
Use ANSI codes; `\e[31m` sets red, `\e[0m` resets. `printf` is more portable than `echo -e`.

## Q82: What is the difference between echo and printf?
**A:** `printf` is POSIX-portable, gives precise formatting (`printf "%.2f\n" 3.1`), and no auto-newline. `echo` varies (`-e`, `-n`) across shells/implementations.

## Q83: How do you write a simple backup script?
**A:**
```bash
src="$1"; dst="/backup/$(date +%F)"
mkdir -p "$dst"
cp -a "$src" "$dst/"
```
Use `tar -czf` or `rsync -a` for efficient backups.

## Q84: How do you write a log rotation script?
**A:**
```bash
for f in /var/log/app/*.log; do
  mv "$f" "$f.$(date +%s)"
done
find /var/log/app -name '*.log.*' -mtime +30 -delete
```

## Q85: How do you parse a CSV file in bash?
**A:**
```bash
while IFS=, read -r col1 col2; do
  echo "first=$col1 second=$col2"
done < data.csv
```
For quoted fields use `awk` or a real CSV parser.

## Q86: How do you parse JSON in bash?
**A:** Bash has no native JSON parser. Use `jq`: `name=$(jq -r '.name' file.json)`. Avoid fragile `grep`/`sed` parsing of JSON.

## Q87: How do you run multiple commands conditionally?
**A:** Use `cmd1 && cmd2` (run cmd2 only if cmd1 succeeds) and `cmd1 || cmd2` (run cmd2 if cmd1 fails). `cmd1; cmd2` runs both unconditionally.

## Q88: What does `command || true` accomplish with set -e?
**A:** It prevents a failing command from aborting the script under `set -e`, allowing expected failures: `grep q file || true`.

## Q89: How do you capture both stdout and stderr?
**A:** `out=$(cmd 2>&1)` captures combined output into a variable, or `cmd > all.log 2>&1` to a file. Use `&>` as a bash shortcut (`cmd &> all.log`).

## Q90: What is the purpose of `exec` in a script?
**A:** `exec` replaces the shell process with the given command (no subshell, no return). Often used to redirect all output: `exec >log 2>&1`.

## Q91: How do you measure elapsed time of a command?
**A:** `time cmd` prints real/user/sys. Or use `start=$(date +%s); cmd; end=$(date +%s); echo $((end-start))` seconds.

## Q92: How do you limit a loop to N parallel background jobs?
**A:**
```bash
for i in {1..20}; do
  (( $(jobs -r | wc -l) >= 4 )) && wait -n
  task "$i" &
done
wait
```

## Q93: What is word splitting and how do you avoid it?
**A:** Word splitting breaks unquoted expansions on IFS into multiple arguments. Avoid by double-quoting: `"$var"`. `mapfile`/`read -a` also help.

## Q94: How do you read a file into an array?
**A:** `mapfile -t lines < file.txt` (or `readarray`) reads each line into the array `lines`. Then iterate `"${lines[@]}"`.

## Q95: How do you check if a command exists?
**A:** Use `command -v git >/dev/null 2>&1` (POSIX, reliable) or `type -P git`. Avoid `which` which has inconsistent exit codes.

## Q96: How do you get the directory of the current script?
**A:** `script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)`. Robust against symlinks and relative invocation.

## Q97: What are nameref variables (declare -n)?
**A:** `declare -n ref=var` makes `ref` an alias to `var`; assigning `ref=5` sets `var`. Useful for passing variables by reference to functions.

## Q98: How do you make a script print usage and exit on bad args?
**A:**
```bash
usage() { echo "Usage: $0 [-f file] [-v]" >&2; exit 1; }
[[ $# -eq 0 ]] && usage
```

## Q99: How do you ensure a script runs with bash even if called as sh?
**A:** Start with `#!/usr/bin/env bash` and re-exec if needed:
```bash
if [ -z "${BASH_VERSION:-}" ]; then exec bash "$0" "$@"; fi
```

## Q100: What are key bash best practices?
**A:** Use a strict header (`set -euo pipefail`), quote all variables, prefer `[[ ]]` and `$(( ))`, use `$( )`, avoid `ls` parsing, validate input, and clean up with `trap`.
