#!/usr/bin/env bash
# GitNexus Code Intelligence Hook — 3-Phase Architecture
# Phase 1: Refresh index with embeddings
# Phase 2: Run detection checks + allowlist filtering
# Phase 3: Deep investigation for actionable issues
set -euo pipefail

REPO_NAME="darktrace-sdk"
SECONDS=0

# Cleanup temp files on exit
trap 'rm -f /tmp/gn_*_$$' EXIT

# --- ANSI colors (disabled when piped) ---
if [ -t 1 ]; then
    RED='\033[0;31m'
    YELLOW='\033[0;33m'
    GREEN='\033[0;32m'
    CYAN='\033[0;36m'
    BOLD='\033[1m'
    DIM='\033[2m'
    RESET='\033[0m'
else
    RED=''
    YELLOW=''
    GREEN=''
    CYAN=''
    BOLD=''
    DIM=''
    RESET=''
fi

SEP="${BOLD}═══════════════════════════════════════════════════════${RESET}"

# --- Allowlist loading ---
ALLOWLIST_FILE=".gitnexus-allowlist"
declare -A ALLOWLIST_EXCLUSIONS

if [ -f "$ALLOWLIST_FILE" ]; then
    while IFS= read -r line; do
        [[ "$line" =~ ^[[:space:]]*# ]] && continue
        [[ -z "${line// }" ]] && continue
        local_sym=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $1); print tolower($1)}')
        local_check=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print tolower($2)}')
        if [ -n "$local_sym" ] && [ -n "$local_check" ]; then
            ALLOWLIST_EXCLUSIONS["${local_check}|${local_sym}"]=1
        fi
    done < "$ALLOWLIST_FILE"
fi

is_allowlisted() {
    local check_slug="$1"
    local symbol_name="$2"
    local key="${check_slug}|${symbol_name}"
    local all_key="all|${symbol_name}"
    [[ -n "${ALLOWLIST_EXCLUSIONS[$key]+x}" ]] && return 0
    [[ -n "${ALLOWLIST_EXCLUSIONS[$all_key]+x}" ]] && return 0
    return 1
}

# --- Helpers ---

# Run a cypher query and parse JSON result (from stderr)
run_cypher() {
    local query="$1"
    local result
    result=$(npx gitnexus cypher "$query" --repo "$REPO_NAME" 2>&1 1>/dev/null || echo '{"row_count": 0, "markdown": ""}')
    echo "$result"
}

# Extract row_count from cypher JSON
extract_count() {
    local json="$1"
    echo "$json" | jq -r 'if type == "array" then (.[0].row_count // 0) else (.row_count // 0) end' 2>/dev/null || echo "0"
}

# Extract markdown from cypher JSON
extract_markdown() {
    local json="$1"
    echo "$json" | jq -r 'if type == "array" then (.[0].markdown // "") else (.markdown // "") end' 2>/dev/null || echo ""
}

# Filter markdown table through allowlist.
# Writes: /tmp/gn_ack_$$ (acknowledged count), /tmp/gn_filtered_$$ (remaining rows as "name|filePath")
filter_allowlist() {
    local check_slug="$1"
    local raw_markdown="$2"
    local acknowledged=0
    local filtered_rows=""

    local seen_separator=false
    while IFS= read -r line; do
        if [[ "$line" =~ ^[[:space:]]*\|[[:space:]]*--+ ]]; then
            seen_separator=true
            continue
        fi
        if [[ "$line" == "|"*"|"* ]] && [ "$seen_separator" = true ]; then
            # Extract symbol name (2nd column, between 1st and 2nd |)
            sym=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print tolower($2)}')
            # Extract file path (3rd column)
            fpath=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $3); print $3}')
            fpath=$(echo "$fpath" | sed 's/^[ \t]*//;s/[ \t]*$//')
            if is_allowlisted "$check_slug" "$sym"; then
                acknowledged=$((acknowledged + 1))
            else
                # Store original-case name for deep investigation
                orig_name=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2}')
                orig_name=$(echo "$orig_name" | sed 's/^[ \t]*//;s/[ \t]*$//')
                filtered_rows="${filtered_rows}${orig_name}|${fpath}"$'\n'
            fi
        fi
    done <<< "$raw_markdown"

    echo "$acknowledged" > /tmp/gn_ack_$$
    printf '%s' "$filtered_rows" > /tmp/gn_filtered_$$
}

# Sanitize a symbol name for safe Cypher injection (alphanumeric + underscore only)
sanitize_sym() {
    echo "$1" | tr -cd '[:alnum:]_'
}

# ═══════════════════════════════════════════════════════
# PHASE 1: Index Refresh
# ═══════════════════════════════════════════════════════
echo -e "$SEP"
echo -e "${CYAN}${BOLD}Phase 1/3: Index Refresh${RESET}"
echo -e "$SEP"

if [ "${SKIP_GITNEXUS_REFRESH:-0}" = "1" ]; then
    echo -e "${DIM}Skipping index refresh (SKIP_GITNEXUS_REFRESH=1)${RESET}"
else
    echo "Refreshing GitNexus index with embeddings..."
    refresh_start=$SECONDS
    if npx gitnexus analyze --embeddings 2>/dev/null; then
        refresh_dur=$(( SECONDS - refresh_start ))
        # Parse stats from status
        status_line=$(npx gitnexus status 2>/dev/null | grep -i "symbol\|relationship" || true)
        echo -e "${GREEN}✅${RESET} Index refreshed${status_line:+ ($status_line)} [${refresh_dur}s]"
    else
        echo -e "${YELLOW}WARNING${RESET}: Index refresh failed, using cached index"
    fi
fi
echo ""

# ═══════════════════════════════════════════════════════
# PHASE 2: Detection + Allowlist Filtering
# ═══════════════════════════════════════════════════════
echo -e "$SEP"
echo -e "${CYAN}${BOLD}Phase 2/3: Code Intelligence Detection${RESET}"
echo -e "$SEP"

# Track actionable issues for Phase 3
# Format per line: "check_slug|symbol_name|file_path"
ACTIONABLE_ISSUES=""
TOTAL_ACTIONABLE=0

# --- Check runner ---
run_check() {
    local description="$1"
    local query="$2"
    local check_slug="${3:-none}"

    local json markdown count acknowledged=0
    json=$(run_cypher "$query")
    count=$(extract_count "$json")
    markdown=$(extract_markdown "$json")

    local actionable=0
    if [ "$count" -gt 0 ] && [ "${#ALLOWLIST_EXCLUSIONS[@]}" -gt 0 ]; then
        filter_allowlist "$check_slug" "$markdown"
        acknowledged=$(cat /tmp/gn_ack_$$)
        # Count remaining (non-allowlisted) rows
        if [ -f /tmp/gn_filtered_$$ ]; then
            actionable=$(grep -c . /tmp/gn_filtered_$$ 2>/dev/null || echo "0")
            # Trim trailing newline can cause off-by-one
            actionable=$(cat /tmp/gn_filtered_$$ | sed '/^$/d' | wc -l | tr -d ' ')
        fi

        # Collect actionable issue details for Phase 3
        if [ "$actionable" -gt 0 ] && [ -f /tmp/gn_filtered_$$ ]; then
            while IFS='|' read -r sym_name sym_path; do
                [ -z "$sym_name" ] && continue
                ACTIONABLE_ISSUES="${ACTIONABLE_ISSUES}${check_slug}|${sym_name}|${sym_path}"$'\n'
            done < /tmp/gn_filtered_$$
        fi
    else
        actionable=$count
        # No allowlist filtering needed but still collect actionable issues
        if [ "$count" -gt 0 ]; then
            # Parse markdown table directly
            local seen_sep=false
            while IFS= read -r line; do
                if [[ "$line" =~ ^[[:space:]]*\|[[:space:]]*--+ ]]; then
                    seen_sep=true
                    continue
                fi
                if [[ "$line" == "|"*"|"* ]] && [ "$seen_sep" = true ]; then
                    sym_name=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2}')
                    sym_path=$(echo "$line" | awk -F'|' '{gsub(/^[ \t]+|[ \t]+$/, "", $3); print $3}')
                    sym_name=$(echo "$sym_name" | sed 's/^[ \t]*//;s/[ \t]*$//')
                    sym_path=$(echo "$sym_path" | sed 's/^[ \t]*//;s/[ \t]*$//')
                    [ -n "$sym_name" ] && ACTIONABLE_ISSUES="${ACTIONABLE_ISSUES}${check_slug}|${sym_name}|${sym_path}"$'\n'
                fi
            done <<< "$markdown"
        fi
    fi

    # Output status line
    if [ "$actionable" -gt 0 ]; then
        local suffix=""
        [ "$acknowledged" -gt 0 ] && suffix=", $acknowledged acknowledged"
        echo -e "${YELLOW}WARNING${RESET} $description: ${count} found${suffix} → ${BOLD}${actionable} actionable${RESET}"
        TOTAL_ACTIONABLE=$((TOTAL_ACTIONABLE + actionable))
    else
        if [ "$acknowledged" -gt 0 ]; then
            echo -e "${GREEN}OK      ${RESET}$description: $count found, $acknowledged acknowledged → 0 actionable"
        else
            echo -e "${GREEN}OK      ${RESET}$description: $count"
        fi
    fi
}

# Check 1: Deprecated code
run_check "Deprecated functions (warnings.warn)" \
    "MATCH (f:Function) WHERE f.content CONTAINS 'warnings.warn' AND f.content CONTAINS 'DeprecationWarning' AND NOT f.filePath CONTAINS 'test' RETURN f.name, f.filePath ORDER BY f.filePath" \
    "deprecated"

# Check 2: Bare except Exception
run_check "Bare 'except Exception' handlers" \
    "MATCH (f:Function) WHERE f.content CONTAINS 'except Exception' AND NOT f.filePath CONTAINS 'test' AND NOT f.filePath CONTAINS 'examples' RETURN f.name, f.filePath ORDER BY f.filePath" \
    "except-exception"

# Check 3: Orphaned classes
run_check "Orphaned classes (no importers)" \
    "MATCH (c:Class) WHERE NOT ()-[:CodeRelation {type: 'IMPORTS'}]->(c) AND NOT c.filePath CONTAINS 'test' AND NOT c.filePath CONTAINS '__init__' AND NOT c.name STARTS WITH '_' RETURN c.name, c.filePath ORDER BY c.filePath" \
    "orphaned-classes"

# Check 4: Unused private functions
run_check "Unused private functions" \
    "MATCH (f:Function) WHERE NOT ()-[:CodeRelation {type: 'CALLS'}]->(f) AND f.name STARTS WITH '_' AND NOT f.name STARTS WITH '__' AND NOT f.filePath CONTAINS 'test' AND NOT f.filePath CONTAINS 'dt_utils' RETURN f.name, f.filePath ORDER BY f.filePath" \
    "unused-private"

echo ""

# ═══════════════════════════════════════════════════════
# PHASE 3: Deep Investigation (only for actionable issues)
# ═══════════════════════════════════════════════════════
PHASE3_OUTPUT=""

if [ "$TOTAL_ACTIONABLE" -gt 0 ]; then
    echo -e "$SEP"
    echo -e "${CYAN}${BOLD}Phase 3/3: Deep Investigation${RESET}"
    echo -e "$SEP"
    echo ""

    issue_num=0
    # Deduplicate: process each unique actionable issue
    while IFS='|' read -r check_slug sym_name sym_path; do
        [ -z "$check_slug" ] && continue
        issue_num=$((issue_num + 1))

        safe_name=$(sanitize_sym "$sym_name")
        safe_path=$(sanitize_sym "$sym_path")

        echo -e "${BOLD}--- Issue ${issue_num}: ${sym_name} (${check_slug}) ---${RESET}"
        echo "Location: ${sym_path}"

        case "$check_slug" in
            deprecated)
                # Callers
                echo "Callers:"
                q="MATCH (caller:Function)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: '${safe_name}'}) RETURN caller.name, caller.filePath, caller.startLine"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none)"
                fi

                # Callees
                echo "Callees:"
                q="MATCH (f:Function {name: '${safe_name}'})-[:CodeRelation {type: 'CALLS'}]->(callee:Function) RETURN callee.name, callee.filePath"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none)"
                fi

                # Processes
                echo "Processes:"
                q="MATCH (f:Function {name: '${safe_name}'})-[:CodeRelation {type: 'STEP_IN_PROCESS'}]->(p:Process) RETURN p.label, p.processType, p.stepCount"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none)"
                fi
                ;;

            except-exception)
                # Callees — what could throw
                echo "Callees (potential exception sources):"
                q="MATCH (f:Function {name: '${safe_name}', filePath: '${sym_path}'})-[:CodeRelation {type: 'CALLS'}]->(callee:Function) RETURN callee.name, callee.filePath"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none)"
                fi

                # Callers — blast radius
                echo "Callers (blast radius):"
                q="MATCH (caller:Function)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: '${safe_name}'}) RETURN caller.name, caller.filePath"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none)"
                fi
                ;;

            unused-private)
                # Sibling functions in same file
                echo "Sibling functions in same file:"
                q="MATCH (file:File)-[:CodeRelation {type: 'DEFINES'}]->(f:Function {name: '${safe_name}'}) MATCH (file)-[:CodeRelation {type: 'DEFINES'}]->(sibling:Function) RETURN sibling.name, sibling.startLine"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none)"
                fi
                ;;

            orphaned-classes)
                # Extends
                echo "Extends:"
                q="MATCH (c:Class {name: '${safe_name}'})-[:CodeRelation {type: 'EXTENDS'}]->(parent:Class) RETURN parent.name"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none found)"
                fi

                # Member functions
                echo "Member functions:"
                q="MATCH (file:File)-[:CodeRelation {type: 'DEFINES'}]->(c:Class {name: '${safe_name}'}) MATCH (file)-[:CodeRelation {type: 'DEFINES'}]->(f:Function) WHERE f.startLine > c.startLine AND f.endLine < c.endLine RETURN f.name, f.startLine"
                result=$(run_cypher "$q")
                md=$(extract_markdown "$result")
                cnt=$(extract_count "$result")
                if [ "$cnt" -gt 0 ] && [ -n "$md" ]; then
                    echo "$md"
                else
                    echo "  (none)"
                fi
                ;;

            *)
                echo "  (no deep investigation defined for check type: $check_slug)"
                ;;
        esac

        echo ""
    done <<< "$(echo -n "$ACTIONABLE_ISSUES" | sed '/^$/d' | sort -u)"

    # ═══════════════════════════════════════════════════════
    # RESULT: Summary + LLM Action
    # ═══════════════════════════════════════════════════════
    echo -e "$SEP"
    echo -e "${RED}${BOLD}RESULT: ${TOTAL_ACTIONABLE} actionable issue(s) found${RESET} [${SECONDS}s]"
    echo -e "$SEP"
    echo ""
    echo "## LLM Action Required"
    echo ""
    echo "Review each issue above with its investigation context. For simple fixes,"
    echo "resolve directly. For complex issues, invoke Sisyphus with Ultrawork Mode:"
    echo ""
    echo -e "  ${CYAN}task(${RESET}"
    echo -e "    ${CYAN}category=\"deep\",${RESET}"
    echo -e "    ${CYAN}load_skills=[\"gitnexus-exploring\", \"gitnexus-impact-analysis\", \"gitnexus-refactoring\"],${RESET}"
    echo -e "    ${CYAN}run_in_background=false,${RESET}"
    echo -e "    ${CYAN}prompt=\"ulw mode\\n\\nAnalyze and fix the following code intelligence issues found by GitNexus:\\n<paste Phase 2 + Phase 3 output from above>\\n\\nResearch the codebase, assess impact, implement fixes, and verify all tests pass.\"${RESET}"
    echo -e "  ${CYAN})${RESET}"
    echo ""
    echo "Ultrawork mode triggers autonomous, thorough problem-solving — the agent"
    echo "will research the codebase, assess blast radius, implement fixes, and"
    echo "verify everything works end-to-end without further hand-holding."
    echo ""
    echo -e "${DIM}To skip: git commit --no-verify${RESET}"
    exit 1
else
    echo -e "$SEP"
    echo -e "${GREEN}${BOLD}RESULT: All checks passed${RESET} [${SECONDS}s]"
    echo -e "$SEP"
    exit 0
fi
