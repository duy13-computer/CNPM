from domain.models.iwatch_repository import IWatchRepository
from domain.models.watch import Watch
from infrastructure.databases import Base
from domain.models.watch import Watch
from typing import List, Optional
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config
from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.mssql import session
from sqlalchemy.orm import Session

load_dotenv()

class WatchRepository(IWatchRepository):
    def __init__(self, session: Session = session):
        db_url = os.getenv("DATABASE_URI", Config.DATABASE_URI)
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add(self, watch: Watch) -> Watch:
        session = self.Session()
        session.add(watch)
        session.commit()
        session.refresh(watch)
        session.close()
        return watch

    def get_by_id(self, watch_id: int) -> Optional[Watch]:
        session = self.Session()
        watch = session.query(Watch).filter(Watch.id == watch_id).first()
        session.close()
        return watch

    def list(self) -> List[Watch]:
        session = self.Session()
        watches = session.query(Watch).all()
        session.close()
        return watches

    #def update(self, watch: Watch) -> Course:
    #    pass

    def delete(self, watch_id: int) -> None:
        session = self.Session()
        watch = session.query(Watch).filter(Watch.id == watch_id).first()
        if watch:
            session.delete(watch)
            session.commit()
        session.close()

#class WatchRepository(IWatchRepository):
#    def __init__(self):
#       self._watch = []
 #       self._id_counter = 1
#
 #   def add(self, watch: Watch) -> Watch:
  #      watch.id = self._id_counter
   #     self._id_counter += 1
    #    self._todos.append(watch)
     #   return watch
##   def get_by_id(self, course_id: int) -> Optional[Course]:
  #      for course in self._courses:
   #         if course.id == course_id:
    #            return course
     #   return None
#
 #   def list(self) -> List[Course]:
  #      return self._courses
#
 ##      for idx, t in enumerate(self._courses):
   ##            self._courses[idx] = course
     #           return course
      #  raise ValueError('course not found')
#
 ##      self._courses = [t for t in self._courses if t.id != course_id] 

