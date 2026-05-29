#!/bin/bash
# eCommerce BI — Universal Installer
# Usage: bash scripts/install.sh [hermes|claude-code|cursor|copilot|opencode|windsurf|aider|all]

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
PLATFORM="${1:-}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

show_usage() {
    echo "eCommerce BI — Universal Installer"
    echo "Usage: bash scripts/install.sh <platform>"
    echo ""
    echo "Platforms: hermes, claude-code, cursor, copilot, opencode, windsurf, aider, all"
    exit 0
}

install_hermes() {
    echo -e "${CYAN}Installing for Hermes Agent...${NC}"
    local dest="$HOME/.hermes/skills/ecommerce-bi"
    mkdir -p "$dest"
    cp "$REPO_ROOT/platforms/hermes/SKILL.md" "$dest/"
    cp -r "$REPO_ROOT/references" "$dest/"
    cp "$REPO_ROOT/scripts/bi_analysis.py" "$dest/"
    echo -e "${GREEN}✓ Hermes skill installed to $dest${NC}"
}

install_claude_code() {
    echo -e "${CYAN}Installing for Claude Code...${NC}"
    local dest=".claude/skills/ecommerce-bi"
    mkdir -p "$dest"
    cp "$REPO_ROOT/platforms/claude-code/SKILL.md" "$dest/"
    cp -r "$REPO_ROOT/references" "$dest/"
    cp "$REPO_ROOT/scripts/bi_analysis.py" "$dest/"
    echo -e "${GREEN}✓ Claude Code skill installed to $dest${NC}"
}

install_cursor() {
    echo -e "${CYAN}Installing for Cursor...${NC}"
    mkdir -p .cursor/rules
    cp "$REPO_ROOT/platforms/cursor/ecommerce-bi.mdc" .cursor/rules/
    echo -e "${GREEN}✓ Cursor rules installed${NC}"
}

install_copilot() {
    echo -e "${CYAN}Installing for GitHub Copilot...${NC}"
    mkdir -p .github
    cp "$REPO_ROOT/platforms/copilot/copilot-instructions.md" .github/
    echo -e "${GREEN}✓ Copilot instructions installed${NC}"
}

install_opencode() {
    echo -e "${CYAN}Installing for OpenCode...${NC}"
    local dest="$HOME/.opencode/skills/ecommerce-bi"
    mkdir -p "$dest"
    cp "$REPO_ROOT/platforms/opencode/SKILL.md" "$dest/"
    cp -r "$REPO_ROOT/references" "$dest/"
    cp "$REPO_ROOT/scripts/bi_analysis.py" "$dest/"
    echo -e "${GREEN}✓ OpenCode skill installed to $dest${NC}"
}

install_windsurf() {
    echo -e "${CYAN}Installing for Windsurf...${NC}"
    cp "$REPO_ROOT/platforms/windsurf/.windsurfrules" .windsurfrules
    echo -e "${GREEN}✓ Windsurf rules installed${NC}"
}

install_aider() {
    echo -e "${CYAN}Installing for Aider...${NC}"
    cp "$REPO_ROOT/platforms/aider/.aider.rules" .aider.rules
    echo -e "${GREEN}✓ Aider rules installed${NC}"
}

[ -z "$PLATFORM" ] && show_usage

case "$PLATFORM" in
    hermes) install_hermes ;;
    claude-code) install_claude_code ;;
    cursor) install_cursor ;;
    copilot) install_copilot ;;
    opencode) install_opencode ;;
    windsurf) install_windsurf ;;
    aider) install_aider ;;
    all)
        echo -e "${YELLOW}Installing for all platforms...${NC}\n"
        install_hermes; install_claude_code; install_cursor
        install_copilot; install_opencode; install_windsurf; install_aider ;;
    -h|--help|help) show_usage ;;
    *) echo -e "${RED}Unknown: $PLATFORM${NC}"; show_usage ;;
esac

echo -e "\n${GREEN}Done!${NC}"
echo "Requirements: pip3 install pandas numpy"
