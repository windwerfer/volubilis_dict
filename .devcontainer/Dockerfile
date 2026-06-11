FROM mcr.microsoft.com/devcontainers/python:3.12-trixie

# Best way in Docker: copy the pre-built binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

ARG USERNAME=vscode

USER $USERNAME
WORKDIR /workspace

# additional PATH var - just in case
ENV PATH="/root/.local/bin:/home/vscode/.local/bin:/home/vscode/.opencode/bin:${PATH}"

# Ensure zsh is the default shell for the vscode user
RUN sudo chsh -s /usr/bin/zsh vscode

# Add useful aliases
RUN cat >> /home/$USERNAME/.zshrc << 'EOF'

# === useful aliases ===
alias ll='ls -alF'
alias la='ls -A'
alias ..='cd ..'
alias ...='cd ../..'
alias gs='git status'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push'
alias gl='git log --oneline --graph --decorate'

EOF
