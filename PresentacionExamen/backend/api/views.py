from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

USER_TYPES = {
    'estudiante': 1,
    'docente': 2
}

QUESTION_TYPES = {
    'multiselect-multichoice': 1,
    'multiselect-singlechoice': 2,
    'true-false': 3,
}

@api_view(['GET', 'POST'])
def hello_world(request):
    if request.method == 'POST':
        return Response({"message": "Post method!"})
    return Response({"message": "Hello, world!"})

class ApiViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Base entry point. please specify in the path the resource you want to use."})

class AuthViewSet(ViewSet):
    def list(self, request):
        s_student_id = request.query_params.get('student_id', None)
        s_password = request.data.get('pw')

        # Instancia clase
        # Llamado metodo de validacion

        o_data = {
            'is_active': True,
            'userType': USER_TYPES['estudiante'],
            'firstname': 'Gabriela',
            'lastName': 'León',
            'id': 20241595005
            }
        return Response(o_data)

class DefaultViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Base entry point. Hello, world!"})

class ExamScheduledViewSet(ViewSet):
    def list(self, request):
        s_subject_id = request.query_params.get('subject_id', None)
        s_student_id = request.query_params.get('student_id', None)

        # Instancia clase
        # Llamado metodo para obtener info de examenes

        o_data = {
            'subject': 120,
            'subject_name': 'Calculo Integral',
            'date': 'Sun Nov 17 2024 21:01:27 GMT-0500',
            'classroom': 12,
            'classroom_number': 202,
            'building': 'Sabio Caldas',
            'number_questions': 10,
            'duration': 2
            }
        return Response(o_data)

class ExamQuestionaireViewSet(ViewSet):
    def list(self, request):
        s_question_id = request.query_params.get('question_id', None)

        # Instancia clase
        # Llamado metodo para obtener info de preguntas

        o_data = {
            'exam':{
                'subject': 120,
                'questions':[
                    {
                    'id': 120,
                    'type': QUESTION_TYPES['multiselect-multichoice'],
                    'question_statement': 'Enunciado dummy',
                    'options': [
                        {
                            'id': 1,
                            'text': 'Opcion 1.'
                        },
                        {
                            'id': 2,
                            'text': 'Opcion 2.'
                        },
                        {
                            'id': 3,
                            'text': 'Opcion 3.'
                        },
                        {
                            'id': 4,
                            'text': 'Opcion 4.'
                        },
                        ]
                    },{
                    'id': 121,
                    'type': QUESTION_TYPES['multiselect-singlechoice'],
                    'question_statement': 'Enunciado dummy 2',
                    'options': [
                        {
                            'id': 5,
                            'text': 'Opcion 1.'
                        },
                        {
                            'id': 6,
                            'text': 'Opcion 2.'
                        },
                        {
                            'id': 7,
                            'text': 'Opcion 3.'
                        },
                        {
                            'id': 8,
                            'text': 'Opcion 4.'
                        },
                        ]
                    }
                ]
            }
        }
        return Response(o_data)