
__author__ = "Nir Moshe (nirmo)"

import dataclasses
import logging
import os
import re
import sqlite3
from typing import Optional, Iterator, Dict

_logger = logging.getLogger(__name__)


@dataclasses.dataclass
class IOCCCWinnerEntry:
    name: str
    year: str
    prog_location: str
    hint_location: Optional[str]
    spoiler: Optional[str]

    def prog(self) -> bytes:
        with open(self.prog_location, "rb") as _prog:
            return _prog.read()

    def hint(self) -> Optional[str]:
        if not self.hint_location:
            return None

        try:
            # TODO: Make it work with `latin-1` encoding. (for example see 2001/ollinger).
            with open(self.hint_location) as _hint:
                return _hint.read()
        except UnicodeDecodeError:
            _logger.warning(f"Can't get the hint for {self.year}/{self.name}, the encoding isn't utf-8!")
            return None


class IOCCCWinnersDB:
    def __init__(self, ioccc_winners_dir):
        self.entries: Dict[(str, str), IOCCCWinnerEntry] = IOCCCWinnersDB.build_db_entries(ioccc_winners_dir)

    def get_entry(self, year, name) -> IOCCCWinnerEntry:
        return self.entries.get((year, name))

    def get_all_entries(self) -> Iterator[IOCCCWinnerEntry]:
        return iter(self.entries.values())

    @staticmethod
    def build_db_entries(ioccc_winners_dir):
        entries = {}
        spoilers = IOCCCWinnersDB._get_spoilers(spoilers_file=os.path.join(ioccc_winners_dir, "all", "summary.txt"))
        for dirpath, dirnames, filenames in os.walk(top=ioccc_winners_dir):
            if "prog.c" in filenames:
                # In this case we got only one program in the directory.
                entry = IOCCCWinnersDB._build_entry_from_path(dirpath, "prog.c", spoilers)
                if entry:
                    entries[(entry.year, entry.name)] = entry
            else:
                # In this case we got many programs in the directory.
                # if it's not *.c file then skip it...
                for prog in (f for f in filenames if f[-2:] == ".c"):
                    entry = IOCCCWinnersDB._build_entry_from_path(dirpath, prog, spoilers)
                    if entry:
                        entries[(entry.year, entry.name)] = entry

        return entries

    @staticmethod
    def _build_entry_from_path(dirpath: str, c_filename: str, spoilers: Dict) -> Optional[IOCCCWinnerEntry]:
        entry_details = IOCCCWinnersDB._get_entry_details_from_path(dirpath)
        author = entry_details.author
        if not author:
            author = c_filename[:-2]

        spoiler = spoilers.get((entry_details.year, author))
        hint_location = IOCCCWinnersDB._locate_hint_location_by_name(dirpath, author)
        if not hint_location:
            _logger.warning(f"Can't find hint and spoiler for {os.path.join(dirpath, c_filename)}, ignoring it.")
            return None

        return IOCCCWinnerEntry(
            name=author,
            year=entry_details.year,
            prog_location=os.path.join(dirpath, c_filename),
            hint_location=hint_location,
            spoiler=spoiler
        )

    @staticmethod
    def _get_entry_details_from_path(path: str):
        """
        return `EntryDetails` from a given path. The path might contain the author name and the year of submission.

        For example:
            ioccc-db/winner/2011/dlowe -> EntryDetails(2011, dlowe)
            ioccc-db/winner/1991 -> EntryDetails(1991, None)
        """
        pattern = re.compile(r".*/(\d{4}).(\w+)|.*/(\d{4})")
        result = re.search(pattern, path)
        if result.group(3):
            return IOCCCWinnersDB._EntryDetails(year=result.group(3), author=None)

        return IOCCCWinnersDB._EntryDetails(year=result.group(1), author=result.group(2))

    @staticmethod
    def _locate_hint_location_by_name(dirpath, name) -> Optional[str]:
        hint_candidates = {
            os.path.join(dirpath, name) + ".text",
            os.path.join(dirpath, "hint.text"),
            os.path.join(dirpath, name) + ".hint"
        }
        for hint_candidate in hint_candidates:
            if os.path.exists(hint_candidate):
                return hint_candidate

        return None

    @staticmethod
    def _get_spoilers(spoilers_file):
        spoiler_line_pattern = re.compile(r"(\d{4}) ([\w.-]+)\s+(.*)")
        spoilers_dict = {}

        with open(spoilers_file) as spoilers:
            for spoiler in spoilers:
                spoiler = spoiler.strip()
                if spoiler and not spoiler.startswith("#"):
                    results = re.search(spoiler_line_pattern, spoiler)
                    year, author, spoiler = results.groups()
                    spoilers_dict[(year, author)] = spoiler

        return spoilers_dict

    @dataclasses.dataclass
    class _EntryDetails:
        author: Optional[str]
        year: str


def build_sqllite_db(entries: Iterator[IOCCCWinnerEntry], output_file: str):
    with sqlite3.connect(output_file) as conn:
        # Create the "winners" table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS winners (
                name TEXT,
                year INTEGER,
                spoiler TEXT,
                prog BLOB,
                hint TEXT
            )
        """)

        for entry in entries:
            _logger.debug(f"Writing to DB {entry.year}/{entry.name}")
            hint = entry.hint()
            if not hint:
                hint = ""

            conn.execute(
                """
                INSERT INTO winners (name, year, spoiler, prog, hint)
                VALUES (?, ?, ?, ?, ?)
                """,
                (entry.name, entry.year, entry.spoiler, entry.prog(), hint)
            )
