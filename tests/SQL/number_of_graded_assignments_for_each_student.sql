-- Write query to get number of graded assignments for each student:
SELECT student_id,count(id) as graded
from assignments 
where state='GRADED'