# LLM Agentic Workflow - Travel Agency App
To run the TravelAgent app, you need to set up your SerpAPI and OpenAI keys.

Copy the `flight_handler`, `hotel_handler` and `event_handler` python files into the same directory where you have the TravelAgent jupyter notebook.

You may have to mount your `/content/drive` to run the app.

## Setup MacOS

1. Install system dependencies

```bash

brew install zig rye graphviz direnv

```

2. Configure environment variables to be able to compile `graphviz`


Run `direnv edit` and add the following then `Esc` then `:wq`

```bash

## GraphViz
export CFLAGS="-I $(brew --prefix graphviz)/include -I $(python -c "import sys; print(f\"{sys.base_prefix}/include/python3.12\")")" # For Mac with Homebrew
export LDFLAGS="-L $(brew --prefix graphviz)/lib" # For Mac with Homebrew

## Zig CC
export CC="zig cc"
export CXX="zig c++"

```

3. Now you proceed with the installation for `pygraphviz`


```bash

rye add pygraphviz

```

