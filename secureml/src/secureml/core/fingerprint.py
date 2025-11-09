"""
Advanced model fingerprinting using Merkle trees and multi-hash algorithms

Provides enhanced integrity verification beyond basic OpenSSF signing
with support for:
- Multiple hash algorithms (SHA-256, SHA-512, Blake2b)
- Merkle tree construction for large models
- Chunk-based hashing for distributed models
- Forensic analysis capabilities
"""

import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import json

from ..utils.logging import get_logger

logger = get_logger()


@dataclass
class HashResult:
    """Result of hashing operation"""
    algorithm: str
    digest: str
    file_size: int
    chunk_count: Optional[int] = None


@dataclass
class ModelFingerprint:
    """
    Complete fingerprint of a model

    Includes multiple hash algorithms and optional Merkle tree
    for enhanced verification and tamper detection.
    """
    model_path: Path
    hashes: Dict[str, HashResult] = field(default_factory=dict)
    merkle_root: Optional[str] = None
    merkle_tree: Optional[List[str]] = None
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        model_path: Path,
        algorithms: Optional[List[str]] = None,
        enable_merkle: bool = False,
        chunk_size: int = 1024 * 1024,  # 1MB chunks
    ) -> "ModelFingerprint":
        """
        Create fingerprint for a model

        Args:
            model_path: Path to model file
            algorithms: Hash algorithms to use (default: ["sha256"])
            enable_merkle: Build Merkle tree for verification
            chunk_size: Chunk size for hashing (bytes)

        Returns:
            ModelFingerprint instance

        Example:
            >>> fp = ModelFingerprint.create(
            ...     Path("model.pkl"),
            ...     algorithms=["sha256", "sha512"],
            ...     enable_merkle=True
            ... )
            >>> print(fp.hashes["sha256"].digest)
        """
        from datetime import datetime

        if algorithms is None:
            algorithms = ["sha256"]

        logger.info(f"Creating fingerprint for: {model_path}")

        fingerprint = cls(model_path=model_path)
        fingerprint.timestamp = datetime.now().isoformat()

        # Calculate hashes
        for algorithm in algorithms:
            hash_result = cls._hash_file(model_path, algorithm, chunk_size)
            fingerprint.hashes[algorithm] = hash_result

        # Build Merkle tree if requested
        if enable_merkle:
            merkle_root, merkle_tree = cls._build_merkle_tree(
                model_path, chunk_size
            )
            fingerprint.merkle_root = merkle_root
            fingerprint.merkle_tree = merkle_tree

        logger.info(f"Fingerprint created with {len(algorithms)} algorithms")
        return fingerprint

    @staticmethod
    def _hash_file(
        path: Path,
        algorithm: str,
        chunk_size: int
    ) -> HashResult:
        """Hash file using specified algorithm"""
        logger.debug(f"Hashing {path} with {algorithm}")

        # Create hasher
        hasher = hashlib.new(algorithm)

        file_size = path.stat().st_size
        chunk_count = 0

        # Read and hash in chunks
        with open(path, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
                chunk_count += 1

        return HashResult(
            algorithm=algorithm,
            digest=hasher.hexdigest(),
            file_size=file_size,
            chunk_count=chunk_count,
        )

    @staticmethod
    def _build_merkle_tree(
        path: Path,
        chunk_size: int
    ) -> Tuple[str, List[str]]:
        """
        Build Merkle tree for file chunks

        Returns:
            Tuple of (merkle_root, tree_nodes)
        """
        logger.debug(f"Building Merkle tree for: {path}")

        # Read file in chunks and hash each chunk
        chunk_hashes = []
        with open(path, "rb") as f:
            while chunk := f.read(chunk_size):
                chunk_hash = hashlib.sha256(chunk).hexdigest()
                chunk_hashes.append(chunk_hash)

        if not chunk_hashes:
            return ("", [])

        # Build Merkle tree from chunk hashes
        tree_levels = [chunk_hashes]

        while len(tree_levels[-1]) > 1:
            current_level = tree_levels[-1]
            next_level = []

            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    # Hash pair of nodes
                    combined = current_level[i] + current_level[i + 1]
                    parent_hash = hashlib.sha256(combined.encode()).hexdigest()
                else:
                    # Odd node, promote as-is
                    parent_hash = current_level[i]

                next_level.append(parent_hash)

            tree_levels.append(next_level)

        merkle_root = tree_levels[-1][0]
        logger.debug(f"Merkle root: {merkle_root}")

        return merkle_root, chunk_hashes

    def verify(
        self,
        algorithm: str = "sha256",
        verify_merkle: bool = False,
    ) -> bool:
        """
        Verify fingerprint against current model state

        Args:
            algorithm: Hash algorithm to use for verification
            verify_merkle: Also verify Merkle tree

        Returns:
            True if verification passes

        Example:
            >>> fp = ModelFingerprint.create(Path("model.pkl"))
            >>> # ... model file might be modified ...
            >>> is_valid = fp.verify()
            >>> if not is_valid:
            ...     print("Model has been tampered with!")
        """
        logger.info(f"Verifying fingerprint for: {self.model_path}")

        if algorithm not in self.hashes:
            logger.error(f"No hash found for algorithm: {algorithm}")
            return False

        # Recompute hash
        current_hash = self._hash_file(
            self.model_path,
            algorithm,
            chunk_size=1024 * 1024
        )

        # Compare
        original_hash = self.hashes[algorithm]
        match = current_hash.digest == original_hash.digest

        if not match:
            logger.warning(
                f"Hash mismatch! Original: {original_hash.digest[:16]}... "
                f"Current: {current_hash.digest[:16]}..."
            )
            return False

        # Verify Merkle tree if requested
        if verify_merkle and self.merkle_root:
            current_root, _ = self._build_merkle_tree(
                self.model_path,
                chunk_size=1024 * 1024
            )
            if current_root != self.merkle_root:
                logger.warning("Merkle tree verification failed!")
                return False

        logger.info("Fingerprint verification passed")
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert fingerprint to dictionary"""
        return {
            "model_path": str(self.model_path),
            "hashes": {
                algo: {
                    "algorithm": result.algorithm,
                    "digest": result.digest,
                    "file_size": result.file_size,
                    "chunk_count": result.chunk_count,
                }
                for algo, result in self.hashes.items()
            },
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
        }

    def to_json(self, path: Optional[Path] = None) -> str:
        """
        Serialize fingerprint to JSON

        Args:
            path: Optional path to save JSON file

        Returns:
            JSON string
        """
        json_str = json.dumps(self.to_dict(), indent=2)

        if path:
            with open(path, "w") as f:
                f.write(json_str)
            logger.info(f"Fingerprint saved to: {path}")

        return json_str

    @classmethod
    def from_json(cls, json_str_or_path: Union[str, Path]) -> "ModelFingerprint":
        """Load fingerprint from JSON string or file"""
        # Load JSON
        if isinstance(json_str_or_path, Path) or Path(json_str_or_path).exists():
            with open(json_str_or_path, "r") as f:
                data = json.load(f)
        else:
            data = json.loads(json_str_or_path)

        # Reconstruct fingerprint
        fp = cls(model_path=Path(data["model_path"]))
        fp.merkle_root = data.get("merkle_root")
        fp.timestamp = data.get("timestamp")
        fp.metadata = data.get("metadata", {})

        # Reconstruct hash results
        for algo, hash_data in data.get("hashes", {}).items():
            fp.hashes[algo] = HashResult(**hash_data)

        return fp
