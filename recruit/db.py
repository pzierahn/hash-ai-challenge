import json
import os
from typing import Iterator

import requests
from tqdm import tqdm


class CandidatesDB:
    people: dict[int, dict] = {}

    def __init__(self, db_path: str = "../spi/coresignal/employee_multi_source"):
        self.db_path = db_path
        self.people = self.load_people()

    def load_people(self) -> dict[int, dict]:
        files = os.listdir(self.db_path)

        for file in files:
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(self.db_path, file)
            with open(file_path, "r") as f:
                person = json.load(f)
                self.people[person["id"]] = person

        return self.people

    def get(self, person_id: int) -> dict | None:
        return self.people.get(person_id)

    def contains(self, person_id: int) -> bool:
        return person_id in self.people

    def store(self, person: dict) -> None:
        person_id = person["id"]
        self.people[person_id] = person

        # Write the response to a JSON file
        clean_name = (
            person.get("full_name", "")
            .replace("/", "_")
            .replace("\\", "_")
            .strip()
            .replace(".", "")
            .replace(" ", "_")
            .strip("_")
        ) or f"person_{person_id}"

        file_path = os.path.join(self.db_path, f"{clean_name}.json")
        with open(file_path, "w") as f:
            json.dump(person, f, indent=4)


class Candidates:
    def __init__(self, db_path: str = "../spi/coresignal/employee_multi_source"):
        self.db = CandidatesDB(db_path)

    def _fetch_person(self, person_id: int) -> dict | None:
        url = f"https://api.coresignal.com/cdapi/v2/employee_multi_source/collect/{person_id}"

        headers = {
            "Content-Type": "application/json",
            "apikey": os.environ["CORESIGNAL_API_KEY"],
        }

        response = requests.request(
            "GET",
            url,
            headers=headers,
        ).json()

        self.db.store(response)

        return response

    def get_person(self, person_id: int) -> dict | None:
        if self.db.contains(person_id):
            return self.db.get(person_id)

        return self._fetch_person(person_id)

    def get_persons(self, person_ids: list[int]) -> list[dict]:
        persons = []
        for person_id in tqdm(person_ids, desc="Fetching persons"):
            person = self.get_person(person_id)
            if person:
                persons.append(person)

        return persons

    def __iter__(self) -> Iterator[dict]:
        for person in self.db.people.values():
            yield person
