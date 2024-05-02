import enum
from core import db
from core.apis.decorators import AuthPrincipal
from core.libs import helpers, assertions
from core.models.teachers import Teacher
from core.models.students import Student
from sqlalchemy.types import Enum as BaseEnum


class GradeEnum(str, enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class AssignmentStateEnum(str, enum.Enum):
    DRAFT = 'DRAFT'
    SUBMITTED = 'SUBMITTED'
    GRADED = 'GRADED'


class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, db.Sequence('assignments_id_seq'), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey(Student.id), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id), nullable=True)
    content = db.Column(db.Text)
    grade = db.Column(BaseEnum(GradeEnum))
    state = db.Column(BaseEnum(AssignmentStateEnum), default=AssignmentStateEnum.DRAFT, nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False)
    updated_at = db.Column(db.TIMESTAMP(timezone=True), default=helpers.get_utc_now, nullable=False, onupdate=helpers.get_utc_now)

    def __repr__(self):
        return '<Assignment %r>' % self.id

    @classmethod
    def filter(cls, *criterion):
        db_query = db.session.query(cls)
        return db_query.filter(*criterion)

    @classmethod
    def get_by_id(cls, _id):
        return cls.filter(cls.id == _id).first()

    @classmethod
    def upsert(cls, assignment_new):

        assertions.assert_valid(bool(assignment_new.content),'content cannot be null.')
        
        if assignment_new.id is not None:
            assignment = Assignment.get_by_id(assignment_new.id)
            assertions.assert_found(assignment, 'No assignment with this id was found')
            assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT,
                                    'only assignment in draft state can be edited')

            assignment.content = assignment_new.content
        else:
            assignment = assignment_new
            db.session.add(assignment_new)

        db.session.flush()
        return assignment

    @classmethod
    def submit(cls, _id, teacher_id, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        teacher= Teacher.get_by_id(teacher_id)  # fetch teacher records based on requested teacher id

        # checking requested student existence
        assertions.assert_valid(Student.get_by_id(auth_principal.student_id), 'No student with this id was found')

        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_found(teacher, 'No teacher with this id was found')   # teacher existence validation
        assertions.assert_valid(assignment.student_id == auth_principal.student_id, 'This assignment belongs to some other student')
        assertions.assert_valid(assignment.state == AssignmentStateEnum.DRAFT and assignment.state != AssignmentStateEnum.GRADED, 'only assignment in draft state can be submitted.')   # existing submitted assignment.
        assertions.assert_valid(assignment.content is not None, 'assignment with empty content cannot be submitted')

        assignment.teacher_id = teacher_id
        assignment.state = AssignmentStateEnum.SUBMITTED    # changing assignment state.
        db.session.flush()

        return assignment


    @classmethod
    def mark_grade(cls, _id, grade, auth_principal: AuthPrincipal):
        assignment = Assignment.get_by_id(_id)
        assertions.assert_found(assignment, 'No assignment with this id was found')
        assertions.assert_valid(grade is not None, 'assignment with empty grade cannot be graded')
        assertions.assert_valid(assignment.teacher_id is not None, 'only a submitted assignment can be graded.')
        assertions.assert_valid((assignment.state==AssignmentStateEnum.SUBMITTED or assignment.state==AssignmentStateEnum.GRADED), 'only a submitted assignment can be graded.')

        # one teacher cannot grade the assignment of other teacher.
        assertions.assert_valid((assignment.teacher_id == auth_principal.teacher_id) or auth_principal.principal_id is not None , 'This assignment belongs to some other teacher.')
       
        # validation for teacher cannot regrade assigment but principal can
        assertions.assert_valid((assignment.teacher_id == auth_principal.teacher_id and assignment.state != AssignmentStateEnum.GRADED) or auth_principal.principal_id is not None,"teacher cannot regrade already graded assignment.")

        assignment.grade = grade
        assignment.state = AssignmentStateEnum.GRADED
        db.session.flush()

        return assignment

    @classmethod
    def get_assignments_by_student(cls, student_id):
        # checking requested student existence
        assertions.assert_found(Student.get_by_id(student_id), 'No student with this id was found')
        return cls.filter(cls.student_id == student_id).all()

    @classmethod
    def get_assignments_by_teacher(cls,teacher_id):
        # checking requested teacher existence
        assertions.assert_found(Student.get_by_id(teacher_id), 'No teacher with this id was found')
        return cls.filter(cls.teacher_id == teacher_id).all()

    @classmethod
    def get_submitted_and_graded_assignments(cls):
        return cls.filter(cls.state != AssignmentStateEnum.DRAFT or cls.state==AssignmentStateEnum.GRADED).all()