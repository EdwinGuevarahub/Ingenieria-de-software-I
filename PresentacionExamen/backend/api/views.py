from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from datetime import datetime
from .models import (
    Asignaturas,
    Corresponde,
    Crea,
    Cursa,
    Estudiantes,
    Evalua,
    Imparte,
    Ingresa,
    Preguntas,
    Profesores,
    Programa,
    Responde,
    Respuestas,
    Salones,
    Selecciona,
    Tipospreguntas,
)

from .serializers import (
    AsignaturaSerializer,
    CorrespondeSerializer,
    CreaSerializer,
    CursaSerializer,
    EstudianteSerializer,
    EvaluaSerializer,
    ImparteSerializer,
    IngresaSerializer,
    PreguntasSerializer,
    ProfesoresSerializer,
    ProgramaSerializer,
    RespondeSerializer,
    RespuestasSerializer,
    SalonesSerializer,
    SeleccionaSerializer,
    TipospreguntasSerializer,
    UserSerializer
)

USER_TYPES = {
    'estudiante': 1,
    'docente': 2
}

QUESTION_TYPES = {
    'multiselect-multichoice': 1,
    'multiselect-singlechoice': 2,
    'true-false': 3,
}

class ApiViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "Base entry point. please specify in the path the resource you want to use."})

class AuthViewSet(ViewSet):
    # POST - Validate user
    def create(self, request, *args, **kwargs):
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

class ExamQuestionaireViewSet(ViewSet):
    # GET - pull questionaire questions based on exam_id provided
    def retrieve(self, request, exam_id=None, *args, **kwargs):
        # Usa question_id para manejar la lógica
        s_exam_id = exam_id

        asignaturas = Estudiantes.objects.all()  # Obtén los registros del modelo
        serializer = EstudianteSerializer(asignaturas, many=True)  # Serializa los datos

        o_data = {
            "exam": {
                "subject": 120,
                "duration": 10,
                "isProgrammed": True,
                "typeExam": 1,
                "questions": [
                        {
                            "idQuestion": 19,
                            "typeQuestion": 1,
                            "questionStatement": "Enunciado 1",
                            "options": [
                            {
                                "idOption": 4,
                                "textOption": "Opción multi 1"
                            },
                            {
                                "idOption": 10,
                                "textOption": "Opción multi 2"
                            },
                            {
                                "idOption": 56,
                                "textOption": "Opción multi 3"
                            },
                            {
                                "idOption": 20,
                                "textOption": "Opción multi 4"
                            }
                            ]
                        },
                        {
                            "idQuestion": 40,
                            "typeQuestion": 2,
                            "questionStatement": "Enunciado 2",
                            "options": [
                            {
                                "idOption": 145,
                                "textOption": "Opción unica 1"
                            },
                            {
                                "idOption": 109,
                                "textOption": "Opción unica 2"
                            },
                            {
                                "idOption": 5,
                                "textOption": "Opción unica 3"
                            },
                            {
                                "idOption": 230,
                                "textOption": "Opción unica 4"
                            }
                            ]
                        },
                        {
                            "idQuestion": 396,
                            "typeQuestion": 3,
                            "questionStatement": "Enunciado 3",
                            "options": [
                            {
                                "idOption": 1,
                                "textOption": "Falso"
                            },
                            {
                                "idOption": 2,
                                "textOption": "Verdadero"
                            }
                            ]
                        }
                    ]
                }
            }
        return Response(serializer.data)

    # GET - pull all questionaire ???
    def list(self, request):
        o_data = {
            }
        return Response(o_data)

class ExamScheduledViewSet(ViewSet):
    # GET - Retrieve exam scheduled data
    def list(self, request):
        s_subject_id = request.query_params.get('subject_id', None)
        s_student_id = request.query_params.get('student_id', None)

        #estudiante
        o_data = {
            "examList": [
                {
                "subject": 120,
                "subjectName": "Calculo Integral",
                "typeExam": 1,
                "date": "Mon Nov 20 2024 06:12:45 GMT-0500",
                "salonNum": 202,
                "salonBuilding": "Sabio Caldas",
                "numQuestions": 10,
                "duration": 30,
                "isProgrammed": True
                },
                {
                "subject": 115,
                "subjectName": "Calculo Diferencial",
                "typeExam": 1,
                "date": "Fri Nov 24 2024 12:47:09 GMT-0500",
                "salonNum": 201,
                "salonBuilding": "Sabio Caldas",
                "numQuestions": 25,
                "duration": 60,
                "isProgrammed": True
                },
                {
                "subject": 4,
                "subjectName": "Algebra Lineal",
                "typeExam": 1,
                "date": "Thu Nov 30 2024 17:58:41 GMT-0500",
                "salonNum": 305,
                "salonBuilding": "Sabio Caldas",
                "numQuestions": 40,
                "duration": 100,
                "isProgrammed": True
                }
            ]
        }

        #docente
        o_data = {
            "examList": [
                {
                "subject": 120,
                "subjectName": "Calculo Integral",
                "date": "Mon Nov 20 2024 06:12:45 GMT-0500",
                "salonNum": 202,
                "salonBuilding": "Sabio Caldas",
                "numQuestions": 10,
                "duration": 30,
                "isProgrammed": True
                },
                {
                "subject": 115,
                "subjectName": "Calculo Diferencial",
                "typeExam": 1,
                "date": "Fri Nov 24 2024 12:47:09 GMT-0500",
                "salonNum": 201,
                "salonBuilding": "Sabio Caldas",
                "numQuestions": 25,
                "duration": 60,
                "isProgrammed": True
                },
                {
                "subject": 210,
                "subjectName": "Física 1",
                "typeExam": 1,
                "date": "",
                "salonNum": 0,
                "salonBuilding": "",
                "numQuestions": 40,
                "duration": 100,
                "isProgrammed": false
                },
                {
                "subject": 211,
                "subjectName": "Física 2",
                "typeExam": 1,
                "date": "",
                "salonNum": 0,
                "salonBuilding": "",
                "numQuestions": 4,
                "duration": 10,
                "isProgrammed": false
                }
            ]
        }

        return Response(o_data)

    # POST - scheduled an exam
    def create(self, request):
        s_subject_id = request.query_params.get('subject_id', None)
        s_student_id = request.query_params.get('student_id', None)

        # Instancia clase
        # Llamado metodo para obtener info de examenes
        o_data = {
                "status": 200,
                "message": "Examen programado con exito",
                "isCreate": True
            }
        return Response(o_data)

    # PUT - Update scheduled exam
    def update(self, request):
        s_subject_id = request.query_params.get('subject_id', None)
        s_student_id = request.query_params.get('student_id', None)

        # Instancia clase
        # Llamado metodo para obtener info de examenes
        o_data = {
                "status": 200,
                "message": "Examen reprogramado con exito",
                "isCreate": True
            }
        return Response(o_data)

class ExamViewSet(ViewSet):
    # GET - get exam settings based on id
    def list(self, request):
        o_data = {
                "status": 200,
                "message": "El examen ya se encuentra creado",
                "isCreate": True
            }
        return Response(o_data)

    # POST - create an exam
    def create(self, request):
        o_data = {
                "status": 200,
                "message": "Examen creado con exito",
                "isCreate": True
            }
        return Response(o_data)

    # PUT - edit exam info
    def update(self, request):
        o_data = {
                "status": 200,
                "message": "Examen editado con exito",
                "isCreate": True
            }
        return Response(o_data)

class NotesViewSet(ViewSet):
    # GET - retrieve notes based on role and subject
    def list(self, request):

        #student notes
        o_data = {
            "notesStudent": [
                {
                "group": 230,
                "subject": 120,
                "typeExam": 1,
                "subjectName": "Calculo Diferencial",
                "date": "Mon Nov 20 2024 06:12:45 GMT-0500",
                "note": 43,
                "state": "Aprobado"
                },
                {
                "group": 230,
                "subject": 150,
                "typeExam": 1,
                "subjectName": "Base de datos",
                "date": "Tue Nov 21 2024 18:05:33 GMT-0500",
                "note": 43,
                "state": "Aprobado"
                },
                {
                "group": 230,
                "subject": 230,
                "typeExam": 1,
                "subjectName": "Caculo Integral",
                "date": "Tue Nov 21 2024 18:05:33 GMT-0500",
                "note": 43,
                "state": "Aprobado"
                }
            ]
        }

        #teacher notes
        o_data = {
            "notesTeacher": [
                {
                "group:": 120,
                "subject": 150,
                "subjectName": "Base de datos",
                "notesExam": [
                    {
                    "typeExam": 1,
                    "date": "Mon Nov 20 2024 06:12:45 GMT-0500"
                    },
                    {
                    "typeExam": 2,
                    "date": "Tue Nov 21 2024 18:05:33 GMT-0500"
                    }
                ]
                },
                {
                "group:": 120,
                "subject": 210,
                "subjectName": "Ingeniería de software 1",
                "notesExam": [
                    {
                    "typeExam": 1,
                    "date": "Mon Nov 20 2024 06:12:45 GMT-0500"
                    }
                ]
                }
            ]
        }

        #subject notes
        o_data = {
            "subject": 120,
            "subjectName": "Base de datos",
            "date": "Mon Nov 20 2024 06:12:45 GMT-0500",
            "numQuestions": 5,
            "numStudents": 3,
            "notesSubject": [
                {
                    "idStudent": 20241595005,
                    "nameStudent": "Gabriela Leon",
                    "note": 43,
                    "answerStudent": [
                        {
                        "idQuestion": 1,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 2,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 3,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 4,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 5,
                        "isCorrect": false
                        }
                    ]
                },
                {
                    "idStudent": 20241595004,
                    "nameStudent": "Edwin Guevara",
                    "note": 39,
                    "answerStudent": [
                        {
                        "idQuestion": 1,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 2,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 3,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 4,
                        "isCorrect": True
                        },
                        {
                        "idQuestion": 5,
                        "isCorrect": false
                        }
                    ]
                },
                {
                    "idStudent": 20241595010,
                    "nameStudent": "Rodrigo Perez",
                    "note": 15,
                    "answerStudent": [
                        {
                        "idQuestion": 1,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 2,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 3,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 4,
                        "isCorrect": false
                        },
                        {
                        "idQuestion": 5,
                        "isCorrect": True
                        }
                    ]
                }
            ]
        }
        return Response(o_data)

class QuestionViewSet(ViewSet):
    #get questions per subject
    def list():
        o_data = {

            }
        return Response(o_data)

    # GET - retrieve question per question_id
    def retrieve(self, request):
        o_data = {

            }
        return Response(o_data)

    # POST - create question
    def create(self, request):
        o_data = {
                "status": 200,
                "message": "La pregunta fue creada correctamente",
                "isCreate": True
            }
        return Response(o_data)

class SalonViewSet(ViewSet):
    # GET - list available salon info, based on id, or date provided in body
    def list(self, request):
         # Obtener los parámetros de consulta
        date = request.query_params.get('date')
        time = request.query_params.get('time')

        # Validar parámetros
        if not date or not time:
            return Response(
                {"error": "Los parámetros 'date' y 'time' son obligatorios."},
                status=400
            )

        # Convertir los parámetros a tipos datetime
        try:
            query_date = datetime.strptime(date, "%Y-%m-%d").date()
            query_time = datetime.strptime(time, "%H:%M:%S").time()
        except ValueError:
            return Response(
                {"error": "El formato de 'date' debe ser 'YYYY-MM-DD' y 'time' debe ser 'HH:MM'."},
                status=400
            )

        # Obtener los exámenes programados en la fecha y hora dadas
        programas_en_horario = Programa.objects.filter(
            fecha_examen=query_date,
            hora_examen__lte=query_time
        )

        # print("Programas encontrados:")
        # for programa in programas_en_horario:
        #     print(f"ID Examen: {programa.id_examen}, Fecha: {programa.fecha_examen}, Hora: {programa.hora_examen}")

        # Obtener los salones ocupados asociados a esos exámenes
        salones_ocupados = Crea.objects.filter(
            id_examen__in=programas_en_horario.values_list('id_examen', flat=True)
        ).exclude(id_salon__isnull=True).values_list('id_salon', flat=True)

        #print("Salones ocupados encontrados:", list(salones_ocupados))

        # Verificar si hay salones ocupados
        if salones_ocupados.exists():
            # Filtrar los salones disponibles
            salones_disponibles = Salones.objects.exclude(id_salon__in=salones_ocupados)
        else:
            # Si no hay salones ocupados, devolver todos los salones
            salones_disponibles = Salones.objects.all()

        # Construir la respuesta
        response = [
            {"id_salon": salon.id_salon, "capacidad": salon.capacidad}
            for salon in salones_disponibles
        ]

        o_data = {
                "salonList": response
            }

        return Response(o_data)

class SubjectViewSet(ViewSet):
    # GET - subjects info based on teacher_id provided
    def list(self, request):
        # Obtener el teacher_id del header
        teacher_id = request.query_params.get('teacher_id')
        #teacher_id = request.META.get('HTTP_TEACHER_ID')
        #teacher_id = request.headers.get('teacher_id')
        #print('teacher_id',teacher_id)

        if not teacher_id:
            return Response(
                {"error": "El header 'teacher_id' es obligatorio."},
                status=400
            )

        # Filtrar las materias impartidas por el docente
        materias = Imparte.objects.filter(cod_profesor=teacher_id).select_related('cod_asignatura')

        # Verificar si se encontraron resultados
        if not materias.exists():
            return Response(
                {"message": "No se encontraron materias para el docente proporcionado."},
                status=404
            )

        # Serializar los datos
        serialized_materias = AsignaturaSerializer([materia.cod_asignatura for materia in materias], many=True)
        o_data = {
            "subjectList":serialized_materias.data
        }

        return Response(o_data, status=200)