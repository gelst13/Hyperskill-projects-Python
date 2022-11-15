# supporting module for $Memorization Tool Stage 4

from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy import Column, Integer, String
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

db_name = 'flashcard.db'
engine = create_engine(f'sqlite:///{db_name}?check_same_thread=False')
engine.connect()
Base = declarative_base()


class FlashCard(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def get_cards():
    """Return list of all entries from table 'flashCard'
    (FlashCard objects)"""
    return session.query(FlashCard).all()


def get_card_by_id(id_num):
    # workaround:
    # for card in session.query(FlashCard).all():
    #     if card.id == id_num:
    #         return card
    # variant 2
    return session.query(FlashCard).filter(FlashCard.id == id_num).first()
    # Get by Primary Key variant:
    # return session.get(FlashCard, id_num)


def store_card(question, answer, box):
    session.add(FlashCard(question=question, answer=answer, box=box))
    session.commit()


def delete_card(id_num):
    """equivalent to the following SQL statement:
    DELETE FROM FlashCard
    WHERE FlashCard.id = id_num
    """
    query = session.query(FlashCard)
    query.filter(FlashCard.id == id_num).delete()
    session.commit()


def edit_card(id_num, field, value):
    """equivalent to the following SQL statement:
    UPDATE FlashCard
    SET field=value_new
    WHERE FlashCard.id = id
    """
    query = session.query(FlashCard)
    card_filter = query.filter(FlashCard.id == id_num)
    card_filter.update({f'{field}': value})
    session.commit()


def prepare_session(session_num):
    """equivalent to the following SQL statement:
        SELECT * from FlashCard
        WHERE FlashCard.box <= session_num
        """
    box_filter = FlashCard.box <= session_num
    # style 1
    # statement = select(FlashCard).filter(box_filter)
    # results = session.execute(statement).scalars().all()
    # style 2
    query = session.query(FlashCard)
    results = query.filter(box_filter)
    return results


def change_box(card_id, designated_box):
    if designated_box > 3:
        # it means you've learned them, and you don't need those cards anymore
        delete_card(card_id)
    else:
        edit_card(card_id, 'box', designated_box)


def print_db_info():
    insp = inspect(engine)
    print(f'{db_name} contains folowing tables:')
    print(Inspector.get_table_names(insp))
    for row in get_cards():
        print(str(row.id) + ' | ', row.question + ' | ', row.answer + ' | ', row.box)
    print()


# print(get_card_by_id(2))
# cards = prepare_session(2)
# for card in cards:
#     print(card.id, card.question, card.box)
