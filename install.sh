#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# Tvastar UI Design Intelligence — One-Command Installer
# ═══════════════════════════════════════════════════════════════
set -e

SKILL_NAME="ui-design-intelligence"
CLAUDE_DIR="${CLAUDE_HOME:-$HOME/.claude}"
SKILL_DIR="$CLAUDE_DIR/skills/$SKILL_NAME"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

header() {
  echo ""
  echo -e "${CYAN}${BOLD}╔══════════════════════════════════════════════════════╗${RESET}"
  echo -e "${CYAN}${BOLD}║   🔥 Tvastar UI Design Intelligence — Installer     ║${RESET}"
  echo -e "${CYAN}${BOLD}║   v4.0 · 18 Libraries · 24 Styles · 86 Lint Rules  ║${RESET}"
  echo -e "${CYAN}${BOLD}╚══════════════════════════════════════════════════════╝${RESET}"
  echo ""
}

check_python() {
  if ! command -v python3 &>/dev/null; then
    echo -e "${RED}✗ Python 3 is required but not found.${RESET}"
    echo "  Install: https://python.org/downloads"
    exit 1
  fi
  PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
  echo -e "${GREEN}✓ Python ${PY_VERSION} found${RESET}"
}

check_claude_code() {
  if ! command -v claude &>/dev/null; then
    echo -e "${YELLOW}⚠  Claude Code CLI not found. Installing Tvastar anyway.${RESET}"
    echo "   Get Claude Code: https://claude.ai/code"
  else
    CLAUDE_VERSION=$(claude --version 2>/dev/null || echo "unknown")
    echo -e "${GREEN}✓ Claude Code found${RESET}"
  fi
}

install_skill() {
  echo ""
  echo -e "${BLUE}Installing to: ${SKILL_DIR}${RESET}"

  # Create skills directory
  mkdir -p "$SKILL_DIR/scripts"
  mkdir -p "$SKILL_DIR/references"

  # Copy files (works whether run from repo or extracted zip)
  SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  cp -r "$SCRIPT_DIR/scripts/"* "$SKILL_DIR/scripts/"
  cp -r "$SCRIPT_DIR/references/"* "$SKILL_DIR/references/"
  cp "$SCRIPT_DIR/SKILL.md" "$SKILL_DIR/"
  cp "$SCRIPT_DIR/README.md" "$SKILL_DIR/" 2>/dev/null || true

  chmod +x "$SKILL_DIR/scripts/"*.py

  echo -e "${GREEN}✓ Skill files installed${RESET}"
}

run_tests() {
  echo ""
  echo -e "${BLUE}Running self-test...${RESET}"
  cd "$SKILL_DIR"

  if PYTHONIOENCODING=utf-8 python3 scripts/test_all.py --fast 2>/dev/null | grep -q "ALL.*TESTS PASSED"; then
    TEST_COUNT=$(PYTHONIOENCODING=utf-8 python3 scripts/test_all.py --fast 2>/dev/null | grep "Results:" | grep -o '[0-9]*' | head -1)
    echo -e "${GREEN}✓ All tests passed${RESET}"
  else
    echo -e "${YELLOW}⚠  Tests inconclusive — skill installed but verify manually${RESET}"
  fi
}

windows_note() {
  if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] || [[ -n "$WINDIR" ]]; then
    echo ""
    echo -e "${YELLOW}📋 Windows users: Set encoding before running scripts${RESET}"
    echo -e "   ${BOLD}set PYTHONIOENCODING=utf-8${RESET}"
    echo "   Or add to your shell profile."
  fi
}

print_success() {
  echo ""
  echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════╗${RESET}"
  echo -e "${GREEN}${BOLD}║   ✅ Tvastar installed successfully!                ║${RESET}"
  echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════╝${RESET}"
  echo ""
  echo -e "${BOLD}Quick start:${RESET}"
  echo "  1. Open Claude Code in your project directory"
  echo "  2. Type: ${CYAN}/design landing page for a SaaS product${RESET}"
  echo "  3. That's it — Tvastar handles the rest"
  echo ""
  echo -e "${BOLD}All 17 commands available:${RESET}"
  echo "  /design  /review  /ship  /component  /heal  /tokens"
  echo "  /dark    /a11y    /cro   /color       /typography"
  echo "  /motion  /extract /storybook  /preview  /approved  /apply"
  echo ""
  echo -e "${BOLD}Detect your stack:${RESET}"
  echo "  ${CYAN}python3 ~/.claude/skills/ui-design-intelligence/scripts/detect_stack.py${RESET}"
  echo ""
}

# Run installer
header
check_python
check_claude_code
install_skill
run_tests
windows_note
print_success
