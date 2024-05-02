from flask import json
from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    # as per SQL query of number of graded assignments for each student has made assignment id 2 and 5 as graded 
    # therefore assignment id 5 is not in draft state therefore skipping testcase
    assert response.status_code == 400


def test_grade_assignment_bad_assignment(client, h_principal):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 999,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_principal):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/principal/assignments/grade',
        headers=h_principal,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'

def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B
