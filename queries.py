create_table_students_query = """
CREATE TABLE IF NOT EXISTS Students(
    birthday DATETIME,
    id INT PRIMARY KEY,
    name VARCHAR(100),
    room INT,
    sex VARCHAR(1)
)
"""

create_table_rooms_query = """
CREATE TABLE IF NOT EXISTS Rooms(
    id INT PRIMARY KEY,
    name VARCHAR(100)
)
"""

alter_table_students_foreign_key_query = """
ALTER TABLE Students ADD CONSTRAINT fk_room_id FOREIGN KEY (room) REFERENCES Rooms(id);
"""


def insert_into_students_query(values):
    query = """
    INSERT IGNORE INTO Students(birthday, id, name, room, sex)
    VALUES {};
    """.format(values)
    return query

# insert_into_students_query = """
# INSERT IGNORE INTO Students(birthday, id, name, room, sex)
# VALUES %s;
# """

def insert_into_rooms_query(values):
    query = """
    INSERT IGNORE INTO Rooms(id, name)
    VALUES {};
    """.format(values)
    return query

# insert_into_rooms_query = """
# INSERT IGNORE INTO Rooms(id, name)
# VALUES %s;
# """

create_index_query = """
CREATE INDEX Students_room_index
    ON Students (room);
"""

select_count_of_students_by_room_query = """
SELECT Rooms.id, Rooms.name, COUNT(Students.id) AS StudentCount
FROM Rooms
         LEFT JOIN Students
                   ON Rooms.id = Students.room
GROUP BY Rooms.id
ORDER BY Rooms.id;
"""

select_min_avg_age_by_room_query = """
SELECT Rooms.id,
       Rooms.name,
       AVG((YEAR(CURRENT_DATE) - YEAR(Students.birthday)) -
           (RIGHT(CURRENT_DATE, 5) < RIGHT(Students.birthday, 5))) AS AverageAge
FROM Rooms
         JOIN Students
              ON Rooms.id = Students.room
GROUP BY id
ORDER BY AverageAge, Rooms.id
LIMIT 5;
"""

select_max_age_difference_by_room_query = """
SELECT Rooms.id,
       Rooms.name,
       MAX((YEAR(CURRENT_DATE) - YEAR(Students.birthday)) -
           (RIGHT(CURRENT_DATE, 5) < RIGHT(Students.birthday, 5))) -
       MIN((YEAR(CURRENT_DATE) - YEAR(Students.birthday)) -
           (RIGHT(CURRENT_DATE, 5) < RIGHT(Students.birthday, 5))) AS AgeDifference
FROM Rooms
         LEFT JOIN Students
                   ON Rooms.id = Students.room
GROUP BY Rooms.id
ORDER BY AgeDifference DESC, Rooms.id
LIMIT 5;
"""

select_rooms_by_with_different_sexes_query = """
SELECT Rooms.id, Rooms.name
FROM Rooms
         LEFT JOIN Students
                   ON Rooms.id = Students.room
GROUP BY Rooms.id
HAVING COUNT(DISTINCT Students.sex) = 2;
"""
