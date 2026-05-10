import shutil
import subprocess
import tempfile
from pathlib import Path
from uuid import uuid4
from app.interfaces.repo_manager import IRepoManager


class RepoManager(IRepoManager):
    def __init__(self, base_temp_dir: Path | None = None):
        self.base_temp_dir = base_temp_dir or Path(tempfile.gettempdir()) / "lintslayer"
        self.base_temp_dir.mkdir(parents=True, exist_ok=True)
    
    def getBaseTempDir(self) -> Path:
        return self.base_temp_dir

    def downloadRepo(self, owner: str, name: str, repo_url: str, timeout: int) -> Path:
        target_dir = self.base_temp_dir / owner / name
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        
        try:
            result = subprocess.run(
                ["git", "clone", "--depth", "1", repo_url, str(target_dir)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                text=True
            )

            if result.returncode != 0:
                raise RuntimeError(f"Git clone failed: {result.stderr}")

            return target_dir

        except subprocess.TimeoutExpired:
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
            raise TimeoutError(f"Cloning repo timed out after {timeout}s")

        except Exception:
            if target_dir.exists():
                shutil.rmtree(target_dir, ignore_errors=True)
            raise

    def saveTempFile(self, owner: str, name: str, ext: str, content: str) -> Path:
        file_dir = self.base_temp_dir / owner
        file_dir.mkdir(parents=True, exist_ok=True)
        file_path = file_dir / f"{name}.{ext.lstrip('.')}"
        
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def deleteRepo(self, path: Path):
        if not path.exists():
            return
        
        try:
            path = path.resolve()
            base = self.base_temp_dir.resolve()

            if not str(path).startswith(str(base)):
                raise ValueError("Attempt to delete path outside temp directory")

            shutil.rmtree(path, ignore_errors=True)

        except Exception as e:
            raise RuntimeError(f"Failed to delete repo: {e}")
