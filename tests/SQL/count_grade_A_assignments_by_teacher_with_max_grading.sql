-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
select (select count(grade) from assignments where teacher_id=a.teacher_id and grade='A') as count_a_grade
from assignments a 
where state='GRADED' 
group by a.teacher_id
order by count(state) desc
LIMIT 1;