FROM mcr.microsoft.com/devcontainers/base:ubuntu

USER vscode
ENV UV_PYTHON_CACHE_DIR=/home/vscode/.cache/uv
ENV FNM_PATH=/home/vscode/.local/share/fnm

RUN <<EOF
##
## Installing UV: https://docs.astral.sh/uv/getting-started/installation/
##
curl -LsSf https://astral.sh/uv/0.11.8/install.sh | sh
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc
echo 'eval "$(uvx --generate-shell-completion bash)"' >> ~/.bashrc

##
## Installing fnm (node version manager): https://github.com/schniz/fnm
##
curl -fsSL https://fnm.vercel.app/install | bash -s -- --skip-shell
# adding fnm to bashrc
cat <<'NESTED_EOF' >> ~/.bashrc
# fnm
if [ -d "$FNM_PATH" ]; then
	export PATH="$FNM_PATH:$PATH"
	eval "$(fnm env --use-on-cd --shell bash)"
fi
NESTED_EOF

##
## General apt deps
##

sudo apt update && sudo apt install -y graphviz

EOF



# persist directories between rebuilds
RUN <<EOF
mkdir -p /home/vscode/.cache/uv			# uv cache dir: https://docs.astral.sh/uv/guides/integration/docker/#caching
mkdir -p /home/vscode/.local/share/fnm	# cache fnm installation: https://github.com/schniz/fnm#parameters
EOF
# RUN mkdir -p /workspaces/DeepLearning/.venv
VOLUME ["/home/vscode/.cache/uv", "/home/vscode/.local/share/fnm"]


# TODO: cache /workspace/.venv