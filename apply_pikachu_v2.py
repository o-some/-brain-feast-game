from pathlib import Path
import base64

parts = [f"pika_patch_{i}.b64" for i in range(1, 5)]
payload = "".join(Path(name).read_text() for name in parts)
code = base64.b64decode(payload).decode("utf-8")
exec(compile(code, "<pikachu-electric-patch>", "exec"), {"__name__": "__main__"})
for name in parts:
    Path(name).unlink()
