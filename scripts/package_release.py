from pathlib import Path
import hashlib, zipfile
root=Path(__file__).resolve().parents[1]
out=root.parent/(root.name+".zip")
with zipfile.ZipFile(out,"w",zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and ".git" not in p.parts:
            z.write(p,p.relative_to(root.parent))
h=hashlib.sha256(out.read_bytes()).hexdigest()
(out.with_suffix(out.suffix+".sha256")).write_text(f"{h}  {out.name}\n")
print(out)
print(h)
