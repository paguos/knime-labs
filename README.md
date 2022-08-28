# knime-labs
Experiments with KNIME Python nodes.

## Nodes

- **penguin**: A simple node that fetches penguin data in the palmer archipelago.

## Requirements

- [Mini Conda](https://docs.conda.io/en/latest/miniconda.html)
- [KNIME Analytics Platform v4.6.1](https://www.knime.com/downloads)

## Development

Each node in this repository has its own independent conda enviroment.


### Run tests

Create the node's conda environment:

```bash
make create/conda
```
To run both lint and unit tests:

```bash
make tests
```

### Build node

Create knime's building conda environment:

```bash
make create/builder
```

To build a given node:

```bash
make build
```
