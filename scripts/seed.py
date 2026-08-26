from sqlmodel import Session

from release_tracker.database import get_engine
from release_tracker.models import Project


def seed() -> None:
    # 1. Create a Session using the engine
    with Session(get_engine()) as session:
        # 2. Instantiate three Project objects
        frontend = Project(name="Frontend Redesign", slug="frontend-redesign")
        backend = Project(name="Backend Redesign", slug="backend-redesign")
        ml = Project(name="Machine Learning", slug="machine-learning")
        # 3. Add them to the session
        session.add(frontend)
        session.add(backend)
        session.add(ml)
        # 4. Commit the transaction to save them to the database
        session.commit()

        print("Loaded sample data for 3 projects.")


if __name__ == "__main__":
    seed()
