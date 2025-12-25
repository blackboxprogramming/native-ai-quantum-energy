#!/usr/bin/env bash

###############################################################################
# BlackRoad Traffic Light System
# Status tracking and workflow management for native-ai-quantum-energy
#
# Usage:
#   ./blackroad-traffic-light.sh init              # Initialize status database
#   ./blackroad-traffic-light.sh status            # Show current status
#   ./blackroad-traffic-light.sh set <color> [msg] # Set status (green|yellow|red)
#   ./blackroad-traffic-light.sh check             # Run automated checks
#   ./blackroad-traffic-light.sh history           # Show status history
#   ./blackroad-traffic-light.sh report            # Generate status report
###############################################################################

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATUS_DB="${REPO_ROOT}/.traffic-light-status.db"
STATUS_FILE="${REPO_ROOT}/.traffic-light-status"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

###############################################################################
# Initialize the status database
###############################################################################
init_status_db() {
    echo "Initializing BlackRoad Traffic Light System..."
    
    # Create simple status file
    cat > "${STATUS_FILE}" <<EOF
# BlackRoad Traffic Light Status
# Format: TIMESTAMP|STATUS|MESSAGE|AUTHOR
$(date -u +%Y-%m-%dT%H:%M:%SZ)|green|Initial status - Repository ready|System
EOF
    
    echo -e "${GREEN}✓${NC} Status tracking initialized"
    echo "Current status: GREEN (ready)"
}

###############################################################################
# Get current status
###############################################################################
get_current_status() {
    if [[ ! -f "${STATUS_FILE}" ]]; then
        echo "unknown"
        return
    fi
    
    # Get last non-comment line
    grep -v "^#" "${STATUS_FILE}" | tail -1 | cut -d'|' -f2
}

###############################################################################
# Show current status with details
###############################################################################
show_status() {
    if [[ ! -f "${STATUS_FILE}" ]]; then
        echo -e "${YELLOW}⚠${NC} Status not initialized. Run: $0 init"
        return 1
    fi
    
    local current_line=$(grep -v "^#" "${STATUS_FILE}" | tail -1)
    local timestamp=$(echo "${current_line}" | cut -d'|' -f1)
    local status=$(echo "${current_line}" | cut -d'|' -f2)
    local message=$(echo "${current_line}" | cut -d'|' -f3)
    local author=$(echo "${current_line}" | cut -d'|' -f4)
    
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo "  BlackRoad Traffic Light Status"
    echo "═══════════════════════════════════════════════════"
    echo ""
    
    case "${status}" in
        green)
            echo -e "  Status:  ${GREEN}🟢 GREENLIGHT${NC}"
            echo -e "  State:   ${GREEN}READY / SAFE TO PROCEED${NC}"
            echo ""
            echo -e "  ${GREEN}✓${NC} All systems operational"
            echo -e "  ${GREEN}✓${NC} Tests passing"
            echo -e "  ${GREEN}✓${NC} Ready for development"
            ;;
        yellow)
            echo -e "  Status:  ${YELLOW}🟡 YELLOWLIGHT${NC}"
            echo -e "  State:   ${YELLOW}CAUTION / REVIEW NEEDED${NC}"
            echo ""
            echo -e "  ${YELLOW}⚠${NC} Some issues require attention"
            echo -e "  ${YELLOW}⚠${NC} Proceed with caution"
            ;;
        red)
            echo -e "  Status:  ${RED}🔴 REDLIGHT${NC}"
            echo -e "  State:   ${RED}STOP / CRITICAL ISSUES${NC}"
            echo ""
            echo -e "  ${RED}✗${NC} Critical issues present"
            echo -e "  ${RED}✗${NC} DO NOT PROCEED"
            echo -e "  ${RED}✗${NC} Emergency fixes only"
            ;;
        *)
            echo -e "  Status:  ${BLUE}❓ UNKNOWN${NC}"
            ;;
    esac
    
    echo ""
    echo "  Message: ${message}"
    echo "  Updated: ${timestamp}"
    echo "  By:      ${author}"
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo ""
}

###############################################################################
# Set status
###############################################################################
set_status() {
    local new_status="$1"
    local message="${2:-Status changed to ${new_status}}"
    local author="${USER:-System}"
    
    if [[ ! -f "${STATUS_FILE}" ]]; then
        init_status_db
    fi
    
    # Validate status
    case "${new_status}" in
        green|yellow|red)
            ;;
        *)
            echo -e "${RED}✗${NC} Invalid status: ${new_status}"
            echo "Valid statuses: green, yellow, red"
            return 1
            ;;
    esac
    
    # Add new status entry
    local timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)
    echo "${timestamp}|${new_status}|${message}|${author}" >> "${STATUS_FILE}"
    
    case "${new_status}" in
        green)
            echo -e "${GREEN}✓${NC} Status set to: ${GREEN}GREENLIGHT${NC}"
            ;;
        yellow)
            echo -e "${YELLOW}⚠${NC} Status set to: ${YELLOW}YELLOWLIGHT${NC}"
            ;;
        red)
            echo -e "${RED}✗${NC} Status set to: ${RED}REDLIGHT${NC}"
            ;;
    esac
    
    echo "Message: ${message}"
}

###############################################################################
# Run automated checks
###############################################################################
run_checks() {
    echo "Running automated status checks..."
    echo ""
    
    local issues=0
    local warnings=0
    
    # Check if tests exist and run them
    if [[ -d "${REPO_ROOT}/tests" ]]; then
        echo -ne "Checking tests... "
        if command -v pytest &> /dev/null; then
            if pytest "${REPO_ROOT}/tests" -q --tb=no &> /dev/null; then
                echo -e "${GREEN}✓ PASS${NC}"
            else
                echo -e "${RED}✗ FAIL${NC}"
                ((issues++))
            fi
        else
            echo -e "${YELLOW}⚠ pytest not installed${NC}"
            ((warnings++))
        fi
    fi
    
    # Check for Python syntax errors
    echo -ne "Checking Python syntax... "
    if find "${REPO_ROOT}" -name "*.py" -exec python3 -m py_compile {} + 2>/dev/null; then
        echo -e "${GREEN}✓ PASS${NC}"
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((issues++))
    fi
    
    # Check for required files
    echo -ne "Checking required files... "
    local missing=0
    for file in README.md LICENSE; do
        if [[ ! -f "${REPO_ROOT}/${file}" ]]; then
            ((missing++))
        fi
    done
    if [[ ${missing} -eq 0 ]]; then
        echo -e "${GREEN}✓ PASS${NC}"
    else
        echo -e "${YELLOW}⚠ ${missing} file(s) missing${NC}"
        ((warnings++))
    fi
    
    echo ""
    echo "Check Results:"
    echo "  Issues:   ${issues}"
    echo "  Warnings: ${warnings}"
    echo ""
    
    # Determine recommended status
    if [[ ${issues} -gt 0 ]]; then
        echo -e "Recommended status: ${RED}REDLIGHT${NC}"
        echo "Run: $0 set red \"Automated checks failed\""
    elif [[ ${warnings} -gt 0 ]]; then
        echo -e "Recommended status: ${YELLOW}YELLOWLIGHT${NC}"
        echo "Run: $0 set yellow \"Automated checks show warnings\""
    else
        echo -e "Recommended status: ${GREEN}GREENLIGHT${NC}"
        echo "Run: $0 set green \"All automated checks passed\""
    fi
}

###############################################################################
# Show status history
###############################################################################
show_history() {
    if [[ ! -f "${STATUS_FILE}" ]]; then
        echo -e "${YELLOW}⚠${NC} No status history available"
        return 1
    fi
    
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo "  Status History"
    echo "═══════════════════════════════════════════════════"
    echo ""
    
    grep -v "^#" "${STATUS_FILE}" | while IFS='|' read -r timestamp status message author; do
        case "${status}" in
            green)
                echo -e "${GREEN}🟢${NC} ${timestamp} - ${message} (${author})"
                ;;
            yellow)
                echo -e "${YELLOW}🟡${NC} ${timestamp} - ${message} (${author})"
                ;;
            red)
                echo -e "${RED}🔴${NC} ${timestamp} - ${message} (${author})"
                ;;
        esac
    done
    
    echo ""
}

###############################################################################
# Generate status report
###############################################################################
generate_report() {
    local current_status=$(get_current_status)
    
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo "  BlackRoad Traffic Light Report"
    echo "  Repository: native-ai-quantum-energy"
    echo "  Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "═══════════════════════════════════════════════════"
    echo ""
    
    show_status
    
    echo ""
    echo "Recent History:"
    echo "───────────────────────────────────────────────────"
    grep -v "^#" "${STATUS_FILE}" | tail -5 | while IFS='|' read -r timestamp status message author; do
        echo "  ${timestamp}: ${status} - ${message}"
    done
    
    echo ""
    echo "Documentation:"
    echo "───────────────────────────────────────────────────"
    case "${current_status}" in
        green)
            echo "  See GREENLIGHT.md for full details"
            ;;
        yellow)
            echo "  See YELLOWLIGHT.md for action items"
            ;;
        red)
            echo "  See REDLIGHT.md for critical issues"
            ;;
    esac
    
    echo ""
    echo "  BlackRoad Codex: See BLACKROAD-CODEX.md"
    echo ""
}

###############################################################################
# Main
###############################################################################
main() {
    local cmd="${1:-status}"
    
    case "${cmd}" in
        init)
            init_status_db
            ;;
        status)
            show_status
            ;;
        set)
            if [[ $# -lt 2 ]]; then
                echo "Usage: $0 set <green|yellow|red> [message]"
                exit 1
            fi
            set_status "$2" "$3"
            ;;
        check)
            run_checks
            ;;
        history)
            show_history
            ;;
        report)
            generate_report
            ;;
        help|--help|-h)
            echo "BlackRoad Traffic Light System"
            echo ""
            echo "Usage:"
            echo "  $0 init              Initialize status tracking"
            echo "  $0 status            Show current status"
            echo "  $0 set <color> [msg] Set status (green|yellow|red)"
            echo "  $0 check             Run automated checks"
            echo "  $0 history           Show status history"
            echo "  $0 report            Generate status report"
            echo "  $0 help              Show this help"
            echo ""
            ;;
        *)
            echo -e "${RED}✗${NC} Unknown command: ${cmd}"
            echo "Run: $0 help"
            exit 1
            ;;
    esac
}

main "$@"
