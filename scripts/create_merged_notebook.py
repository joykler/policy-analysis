import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from pathlib import Path

SRC = Path(r"c:\Users\Home\policy-analysis\Dictionary_discovery_v3_COMPLETE.ipynb")
DST = Path(r"c:\Users\Home\policy-analysis\Dictionary_discovery_v3_COMPLETE_merged.ipynb")

def normalize_source(src):
    if isinstance(src, list):
        # join list into single string then split by lines
        s = "".join(src)
    else:
        s = str(src)
    # remove accidental export header lines like "// filepath: ..."
    lines = s.splitlines()
    if lines and lines[0].lstrip().startswith("// filepath:"):
        lines = lines[1:]
    # strip leading/trailing blank lines
    while lines and lines[0].strip() == "":
        lines = lines[1:]
    while lines and lines[-1].strip() == "":
        lines = lines[:-1]
    return "\n".join(lines)


def main():
    nb = nbformat.read(str(SRC), as_version=4)

    seen = set()
    out_cells = []

    for cell in nb.get("cells", []):
        src_str = normalize_source(cell.get("source", ""))
        key = (cell.get("cell_type"), src_str.strip())
        if key in seen:
            continue
        seen.add(key)

        # Prepare metadata and move top-level id into metadata.id if present
        meta = dict(cell.get("metadata", {}) or {})
        top_id = cell.get("id")
        if top_id and "id" not in meta:
            meta["id"] = top_id

        # ensure language meta exists
        if "language" not in meta:
            meta["language"] = "python" if cell.get("cell_type") == "code" else "markdown"

        # Build new cell
        if cell.get("cell_type") == "code":
            new = new_code_cell(source=src_str.splitlines(), metadata=meta)
            # preserve outputs/execution_count where possible
            new["outputs"] = cell.get("outputs", [])
            new["execution_count"] = cell.get("execution_count", None)
        else:
            new = new_markdown_cell(source=src_str.splitlines(), metadata=meta)

        out_cells.append(new)

    nb_out = new_notebook(cells=out_cells)
    nb_out["metadata"] = {
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"}
    }
    nb_out["nbformat"] = 4
    nb_out["nbformat_minor"] = 5

    nbformat.write(nb_out, str(DST))
    print(f"✓ Merged notebook written: {DST}")


if __name__ == '__main__':
    main()
