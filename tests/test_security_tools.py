from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts import build_jobs, check_repo, package_release


class JobDataSecurityTests(unittest.TestCase):
    def test_canonical_snapshot_validates(self) -> None:
        data = build_jobs.load_data()
        self.assertEqual(data["snapshot_date"], "2026-08-03")

    def test_non_https_url_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_jobs.validate_https("http://example.com/job", field="test.url")

    def test_credentials_in_url_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_jobs.validate_https("https://user:pass" + "@" + "example.com/job", field="test.url")

    def test_contact_data_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_jobs.safe_text("name" + "@" + "example.com", field="test.summary")
        with self.assertRaises(ValueError):
            build_jobs.safe_text("010" + "-1234" + "-5678", field="test.summary")

    def test_control_character_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            build_jobs.safe_text("safe\x00unsafe", field="test.summary")


class RepositorySecurityTests(unittest.TestCase):
    def test_github_slug_matches_local_headings(self) -> None:
        self.assertEqual(check_repo.github_slug("보안·무결성 기준"), "보안무결성-기준")

    def test_package_file_list_contains_no_symlink(self) -> None:
        for path in package_release.files_for_package():
            self.assertFalse(path.is_symlink())

    def test_zip_path_policy_example(self) -> None:
        from pathlib import PurePosixPath

        safe = PurePosixPath("engineering-path-review/docs/01-PATH.md")
        unsafe = PurePosixPath("engineering-path-review/../secret")
        self.assertNotIn("..", safe.parts)
        self.assertIn("..", unsafe.parts)

    def test_manifest_format_is_stable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.txt"
            path.write_text("sample\n", encoding="utf-8")
            digest = package_release.sha256(path)
            self.assertRegex(digest, r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
