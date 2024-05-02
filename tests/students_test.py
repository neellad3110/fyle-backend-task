def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2


def test_post_assignment_null_content(client, h_student_1):
    """
    failure case: content cannot be null
    """

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': None
        })

    assert response.status_code == 400


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_post_invalid_assignment(client,h_student_2):
    """
    failure case: invalid assignment id
    """

    content = 'SOLUTION T1 EDITED'
    response = client.post(
        '/student/assignments',
        headers=h_student_2,
        json={
            'id': 999,
            'content': content
        }
    )

    assert response.status_code == 404
    data = response.json
    assert data['error'] == 'FyleError'
    assert response.json['message'] == 'No assignment with this id was found'


# def test_post_assignment_cross(client, h_student_2):
#     """
#     failure case: assignment of student 1 was posted/edited by student 2 instead of student 1
#     """

#     content = 'SOLUTION T1 EDITED'
#     response = client.post(
#         '/student/assignments',
#         headers=h_student_2,
#         json={
#             'id': 999,
#             'content': content
#         }
#     )

#     assert response.status_code == 400
#     data = response.json
#     assert data['error'] == 'ValidationError'
#     assert response.json['message'] == 'This assignment belongs to some other student'


def test_submit_assignment_cross(client, h_student_2):
    """
    failure case: assignment of student 1 was submitted by student 2 instead of student 1
    """

    content = 'SOLUTION T1'
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_2,
        json={
            'content': content
        }
    )

    assert response.status_code == 400
    data = response.json
    assert data['error'] == 'ValidationError'



def test_submit_assignment_student_invalid_teacher_1(client, h_student_1):
    "failure case : invalid teacher id."
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 9999
        })

    assert response.status_code == 404
    assert response.json['error'] == 'FyleError'


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            # as assignment id 2 is already graded with SQL test .
            'id': 21,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2


def test_assignment_resubmit_error(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })
    error_response = response.json
    assert response.status_code == 400
    assert error_response['error'] == 'FyleError'
    assert error_response["message"] == 'only assignment in draft state can be submitted.'
